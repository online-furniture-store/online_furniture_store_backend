from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from apps.product.models import Product

User = get_user_model()


class DeliveryMethod(models.Model):
    """Модель способов доставки"""

    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы  доставки'


class Delivery(models.Model):
    """Модель доставки"""

    adres = models.CharField(max_length=200, verbose_name='Адрес')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    type_delivery = models.ForeignKey(DeliveryMethod, verbose_name='Доставка', on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name='Дата оформления', auto_now_add=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

    def __str__(self):
        return f'{self.adres}'


class Orders(models.Model):
    """Модель заказов"""

    number = models.AutoField(verbose_name='Номер заказа', primary_key=True)
    created = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    products = models.ManyToManyField(Product, through='ProductsOrder', verbose_name='Товар')
    total = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='Стоимость')
    delivery = models.ManyToManyField(
        Delivery, through='Delivery_order', related_name='delivery', verbose_name='Доставка'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.number}'


class ProductsOrder(models.Model):
    """Модель продукты/заказ"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    amount = models.PositiveIntegerField(verbose_name='Колличество')
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class DeliveryOrder(models.Model):
    """Модель заказ/доставка"""

    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ')
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, verbose_name='Доставка')

    class Meta:
        verbose_name = 'Доставка'
        constraints = [UniqueConstraint(fields=['order', 'delivery'], name='unique_delivery')]


class Storehouse(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    amount = models.IntegerField()


# class Meta:
#     verbose_name = 'Склад'
#     constraints = [
#         UniqueConstraint(fields=['product', 'amount'],
#                          name='unique_products')
#     ]


# def __str__(self):
#     return f'{self.product} --> {self.amount}'
