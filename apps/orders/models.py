from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from apps.product.models import Product

User = get_user_model()


class DeliveryMethod(models.Model):
    """Модель способов доставки"""

    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы  доставки'

    def __str__(self):
        return f'{self.name}'


class Delivery(models.Model):
    """Модель доставки"""

    # TODO поле user
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery',verbose_name='Клиент')
    adres = models.CharField(max_length=200, verbose_name='Адрес')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    type_delivery = models.ForeignKey(
        DeliveryMethod, related_name='delivery', verbose_name='Доставка', on_delete=models.PROTECT
    )
    created = models.DateTimeField(verbose_name='Дата оформления', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

    def __str__(self):
        return f'{self.adres}'


class Orders(models.Model):
    """Модель заказов"""

    # TODO поле user
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',verbose_name='Клиент')
    created = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления заказа', auto_now=True)
    products = models.ManyToManyField(Product, through='OrderProduct', verbose_name='Товар')
    delivery = models.ForeignKey(
        Delivery, related_name='order_delivery', verbose_name='Доставка', on_delete=models.PROTECT
    )
    paid = models.BooleanField(default=False)
    total_cost = models.DecimalField(max_digits=40, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id}'


class OrderProduct(models.Model):
    """Модель продукты/заказ"""

    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='order_item')
    quantity = models.PositiveIntegerField(verbose_name='Колличество', default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    cost = models.DecimalField(max_digits=40, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        self.cost = self.order_item.price * self.quantity
        return super().save(*args, **kwargs)


class Storehouse(models.Model):
    product = models.OneToOneField(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='storehouse')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=0, message='Минимальное количество 1!')]
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'

    def __str__(self):
        return f'{self.product} ---> {self.quantity}'
