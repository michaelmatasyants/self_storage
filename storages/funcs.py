import os

from main_app.settings import SELF_STORAGE_URL


def get_html_message(order: dict):
    filepath = os.path.join('messages', 'message.html')
    with open(filepath, 'r') as file:
        message = file.read()

    # создать ссылку на оплату

    replacements = {
        '[ссылка на сайт]': SELF_STORAGE_URL,
        '[ссылка на оплату]': '',
        '[ссылка на правила]': '',
    }
    replacements.update(order)

    for key, value in replacements.items():
        message = message.replace(key, value)

    return message




