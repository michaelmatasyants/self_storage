import schedule
import time
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.core.mail import mail_managers
from django.utils import timezone

from storages.models import Order


def delete_unpaid_orders():
    due_date = timezone.now() - timezone.timedelta(days=2) 
    orders = Order.objects.filter(paid_date=None, created_date__lt=due_date)
    orders.delete()


def send_reminder(order: Order, days_left: int):
    if days_left:
        noun_declension = ('дней' if days_left >= 5 else 
                           'дня' if days_left != 1 else 'день')
        when = f'через {days_left} {noun_declension}'
    else:
        when = 'сегодня'
    subject = 'Заканчивается оплаченный период'
    message = f'Оплаченный вами период подходит к концу {when}.' \
              'Продлите срок хранения или заберите вещи.'
    send_mail(subject, message, [order.client.email])


def send_period_has_expired(order: Order, max_months: int):
    day_x = order.paid_till + timezone.timedelta(days=max_months*30)

    subject = 'Оплаченный период закончился. Штрафная наценка'
    message = f'Оплаченный вами период по заказу №{order.id}, бокс ' \
              f'№{order.box.id} закончился. С этого дня и в течении ' \
              f'{max_months} месяцев ваш тариф увеличится на 20%.\n' \
              'Если по истечению этого срока (до ' \
              f'{day_x.strftime("%d.%m.%Y")}) вы не внесете оплату или' \
              'не освободите бокс, ваши вещи будут утилизированны.'
    send_mail(subject, message, [order.client.email])


def send_next_debt_months(order: Order, month: int, max_months: int):
    debt = order.box.box_type.price * 1.2 * month
    day_x = order.paid_till + timezone.timedelta(days=max_months*30)

    subject = f'Не оплачен очередной месяц задолженности'
    message = f'Ваша задолженность по заказу №{order.id}, бокс ' \
              f'№{order.box.id} длится уже {month} месяц(ев) и составила ' \
              f'{debt} руб.\nЕсли не погасите задолженность до ' \
              f'{day_x.strftime("%d.%m.%Y")}, ваши вещи будут утилизированны.'
    send_mail(subject, message, [order.client.email])


def send_last_day_before_withdrawal(order: Order, month: int):
    debt = order.box.box_type.price * 1.2 * month

    subject = 'Утилизация ващих вещей из бокса'
    message = 'Сегодня последний день, когда вы можете оплатить ' \
              f'задолженность по заказу №{order.id}, бокс №{order.box.id} ' \
              f'в размере {debt} руб.\n' \
              'В случае неуплаты завтра ваши вещи будут утилизированны.'
    send_mail(subject, message, [order.client.email])


def send_mail(subject: str, message: str, recipient_list: list,):
    mail = EmailMessage(
        subject,
        message,
        to=recipient_list,
    )
    mail.send(fail_silently=True, timeout=5)


def send_mail_to_managers(order: Order):
    subject = 'Очистить бокс'
    message = f'Клиент {order.client} не оплатил заказ №{order.id},' \
              f'необходимо освободить бокс №{order.box.id}.'
    mail_managers(subject, message, fail_silently=True, timeout=15)


def check_terms():
    delete_unpaid_orders()
    orders = Order.objects.filter(is_open=True).select_related('box')

    for order in orders:
        days_left = order.paid_till.date() - timezone.now().date()
        max_months = 3

        if days_left.days >= 0:
            if days_left.days == 7:
                send_reminder(order, days_left.days)
            if days_left.days == 3:
                send_reminder(order, days_left.days)
            if days_left.days == 0:
                send_reminder(order, days_left.days)

        elif days_left.days == -1:
            send_period_has_expired(order, max_months)

        elif abs(days_left.days) % 30 == 0 and abs(days_left.days) <= 90:
            months_of_debt = abs(days_left.days + 1) // 30
            if max_months - months_of_debt:
                send_next_debt_months(order, months_of_debt, max_months)
            else:
                send_last_day_before_withdrawal(order, max_months)

        else:
            order.box.is_free = True
            order.box.save()
            order.is_open = False
            order.save()
            send_mail_to_managers(order)


class Command(BaseCommand):
    help = 'проверка сроков оплаты и рассылка уведомлений'

    def handle(self, *args, **options):
        schedule.every().day.at('00:00', 'Europe/Moscow').do(check_terms)
        while True:
            schedule.run_pending()
            time.sleep(1)
