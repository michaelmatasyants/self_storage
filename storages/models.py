from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from storages.bitlink import (is_bitlink, shorten_link,
                              count_clicks, delete_link)
from main_app.settings import SELF_STORAGE_URL


class CustomUser(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=200, unique=True)
    email = models.EmailField('Почта', unique=True)
    phone = PhoneNumberField('Телефон', null=True, blank=True)
    first_name = models.CharField('Имя', max_length=100, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=100, null=True, blank=True)

    # USERNAME_FIELD = "email"
    # EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.id}. {self.username}'


class Storage(models.Model):
    title = models.CharField('Склад', max_length=100)
    city = models.CharField('Город', max_length=100)
    address = models.CharField('Адрес', max_length=200)
    photo = models.ImageField('Фото')
    temp = models.IntegerField('Температура', default=0)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'г. {self.city}, {self.address}'


class BoxType(models.Model):
    length = models.FloatField('Длина')
    width = models.FloatField('Ширина')
    height = models.FloatField('Высота')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Тип боксов'
        verbose_name_plural = 'Типы боксов'

    def __str__(self):
        return f'Бокс {self.length}м х {self.width}м х {self.height}м'


class Box(models.Model):
    title = models.CharField('Бокс', max_length=100)
    is_free = models.BooleanField('Свободен', default=True)
    box_type = models.ForeignKey(BoxType,
                                 on_delete=models.CASCADE,
                                 related_name='boxes',
                                 default=None,
                                 )
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE,
                                related_name='boxes',
                                null=True,
                                )

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return self.title


class Order(models.Model):

    client = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='orders',
                               verbose_name='Клиент',
                               null=True
                               )
    box = models.ForeignKey(Box,
                            on_delete=models.CASCADE,
                            null=True,
                            verbose_name='Бокс',
                            )
    is_open = models.BooleanField('Открыт', default=True)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    paid_date = models.DateTimeField('Дата оплаты', null=True, blank=True)
    paid_from = models.DateTimeField('Оплата с', null=True, blank=True)
    paid_till = models.DateTimeField('Оплата до', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Клиент {self.client}, бокс: {self.box}'


class FAQ(models.Model):
    question = models.TextField('Вопрос')
    answer = HTMLField('Ответ')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return f'{self.question[:50]}...'


def create_new_bitlink():
    max_id = Link.objects.aggregate(Max('id'))['id__max']
    if not max_id:
        max_id = 0
    next_bitlink_id = max_id + 1
    while True:
        if not is_bitlink(SELF_STORAGE_URL, next_bitlink_id):
            return shorten_link(SELF_STORAGE_URL, next_bitlink_id)
        next_bitlink_id += 1


class Link(models.Model):
    shorten_link = models.CharField(
        'Сокращенная ссылка',
        max_length=20,
        null=True, blank=True,
        default=create_new_bitlink)
    place_of_use = models.CharField(
        'Место использования ссылки',
        max_length=50,
        null=True, blank=True)

    def delete(self, *args, **kwargs):
        delete_link(self.shorten_link)
        super().delete(*args, **kwargs)

    @property
    def clicks(self):
        return count_clicks(self.shorten_link)

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
