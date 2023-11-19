from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser

from decimal import Decimal

from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField


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
        return f'self.title адрес: self.city self.address'


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
    is_free = models.BooleanField('Статус', default=True)
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


class FAQ(models.Model):
    question = models.TextField('Вопрос')
    answer = HTMLField('Ответ')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return f'{self.question[:50]}...'
