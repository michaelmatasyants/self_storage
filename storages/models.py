from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal


class CustomUser(AbstractUser):
    # username = models.CharField('Имя пользователя', max_length=200, unique=True)
    email = models.EmailField('Почта', unique=True)
    phone = PhoneNumberField('Телефон', null=True, blank=True)
    first_name = models.CharField('Имя', max_length=100, null=True, blank=True)
    last_name = models.CharField('Имя', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Storage(models.Model):
    title = models.CharField('Склад', max_length=100)
    city = models.CharField('Город', max_length=100)
    address = models.CharField('Адрес', max_length=200)
    photo = models.ImageField('Фото')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'self.title адрес: self.city self.address'


# class BoxType(models.Model):
#     length = models.FloatField('Длина')
#     width = models.FloatField('Ширина')
#     height = models.FloatField('Высота')
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


class Box(models.Model):
    title = models.CharField('Бокс', max_length=100)
    is_free = models.BooleanField('Статус', default=True)
    # box_type = models.ForeignKey(BoxType,
    #                              on_delete=models.CASCADE,
    #                              related_name='boxes')
    storage = models.ForeignKey(Storage,
                                on_delete=models.CASCADE,
                                related_name='boxes',
                                null=True,
                                )
    length = models.FloatField('Длина')
    width = models.FloatField('Ширина')
    height = models.FloatField('Высота')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return self.title


class Order(models.Model):
    client = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='clients',
                               verbose_name='Клиент',
                               )
    box = models.ForeignKey(Box,
                            on_delete=models.CASCADE,
                            null=True,
                            verbose_name='Бокс',
                            )
    paid_date = models.DateTimeField('Дата оплаты', null=True)
    paid_from = models.DateTimeField('Оплата с', null=True)
    paid_till = models.DateTimeField('Оплата до', null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'self.client бокс: self.box'
