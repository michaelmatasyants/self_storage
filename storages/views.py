from datetime import date, datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db.models import Count, Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from storages.backends import EmailBackend
from storages.forms import LoginForm, RegistrationForm
from storages.funcs import get_html_message, get_payment_link
from storages.models import FAQ, Box, BoxType, CustomUser, Order, Storage


def serialize_storage(storage: Storage):
    return {
        'id': storage.id,
        'city': storage.city,
        'address': storage.address,
        'temp': str(storage.temp),
        'photo': storage.photo.url,
        'boxes': storage.boxes.all(),
    }


def serialize_user(user: CustomUser):
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
    }


def serialize_faq(question: FAQ):
    return {
        'question': question.question,
        'answer': question.answer,
    }


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    form.add_error(None, ValidationError("Этот аккаунт отключен"))
            else:
                form.add_error(None, ValidationError("Неверный email или пароль."))
    else:
        form = LoginForm()
    return render(request, "reg_log_forms/login.html", {"form": form})


def register_user(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'),
            )
            if user:
                login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, 'reg_log_forms/register.html', {'form': form})


def index(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    nearest_storage = Storage.objects.first()
    context['nearest_storage'] = (serialize_storage(nearest_storage)
                                 if nearest_storage else None)
    return render(request, 'index.html', context=context)


def choose_boxes(request):
    storages = Storage.objects.prefetch_related(
        Prefetch('boxes', queryset=Box.objects.filter(is_free=True))
    )
    serialize_storages = []
    for storage in storages:
        boxes_count = storage.boxes.count()
        free_boxes = storage.boxes.filter(is_free=True)
        if not free_boxes:
            continue

        box_type_ids = free_boxes.values('box_type').distinct()
        storage_box_types = BoxType.objects.filter(id__in=box_type_ids)
        min_price = int(min(storage_box_types, key=lambda x: x.price).price)
        serialize_storages.append({
            'storage': serialize_storage(storage),
            'free_boxes_count': free_boxes.count(),
            'boxes_count': boxes_count,
            'min_price': min_price,
            'storage_box_types': storage_box_types
        })

    context = {
        'storages': serialize_storages,
        'login_form': LoginForm(),
        'registration_form': RegistrationForm()
    }

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'rent_box':
                new_order = Order(
                    client=request.user,
                    box=Box.objects.get(pk=1),
                    paid_date=timezone.now(),
                    paid_from=timezone.now(),
                    paid_till=timezone.now(),
                )
                new_order.save()

    return render(request, 'boxes.html', context=context)


@login_required(login_url="login")
def show_personal_account(request):
    user = request.user
    orders = user.orders.all()
    serialized_orders = []
    for order in orders:
        time_to_pay = False
        if order.paid_till.date() - datetime.now().date() < timedelta(days=7):
            time_to_pay = True
        serialized_orders.append({
            'order': order,
            'box_id': order.box.id,
            'storage_id': order.box.storage.id,
            'storage_address': order.box.storage.address,
            'paid_for_period': f'С {order.paid_from.date()} по {order.paid_till.date()}',
            'time_to_pay': time_to_pay,
        })
    context = {
        'user': serialize_user(user),
        'orders': serialized_orders,
    }
    return render(request, 'my-rent.html', context=context)


def show_faq(request):
    context = {
        'questions': [
            serialize_faq(question) for question in FAQ.objects.all()
        ]
    }
    return render(request, 'faq.html', context=context)


def send_payment_link(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        box_type = get_object_or_404(
            BoxType,
            id=int(request.POST.get('box_type'))
        )
        storage = get_object_or_404(
            Storage,
            id=int(request.POST.get('storage'))
        )

        box = Box.objects.filter(box_type=box_type,
                                 storage=storage,
                                 is_free=True).first()
        box.is_free = False
        box.save()
        
        order = Order.objects.create(client=request.user, box=box)
        serialize_order = {
            '[номер заказа]': order.id,
            '[адрес склада]': f'г. {storage.city}, {storage.address}',
            '[номер бокса]': box.id,
            '[размер бокса]': box_type,
            '[стоимость]': box_type.price,
            '[ссылка на оплату]': get_payment_link(box_type.price, f'оплата заказа {{order.id}}'),
        }

        email = request.user.email
        mail = EmailMessage(
            'Оплата аренды бокса',
            'обычный текст',
            recipient_list=[email],
            html_message=get_html_message(serialize_order),
            fail_silently=False
        )
        mail.send()
    return redirect('index')
