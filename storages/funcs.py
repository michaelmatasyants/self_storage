import os

from main_app.settings import SELF_STORAGE_URL, YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY
import uuid
from yookassa import Configuration, Payment


def get_html_message(order: dict):
    filepath = os.path.join('messages', 'message.html')
    with open(filepath, 'r') as file:
        message = file.read()

    confirmation_url = get_payment_link(
        order['[стоимость]'],
        f'Оплата заказа {order['[номер заказа]']}'
    )

    replacements = {
        '[ссылка на сайт]': SELF_STORAGE_URL,
        '[ссылка на оплату]': confirmation_url,
        '[ссылка на правила]': '',
    }
    replacements.update(order)

    for key, value in replacements.items():
        message = message.replace(key, value)

    return message


def get_payment_link(value, description):
    Configuration.account_id = YOOKASSA_SHOP_ID
    Configuration.secret_key = YOOKASSA_SECRET_KEY
    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{SELF_STORAGE_URL}"
        },
        "capture": True,
        "description": description
    }, uuid.uuid4())

    return payment.confirmation.confirmation_url




