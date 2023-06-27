from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, UniqueConstraint

from apps.product.models import Product
from common.validators import validate_phone

User = get_user_model()


class DeliveryType(models.Model):
    """Модель способов доставки"""

    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы  доставки'

    def __str__(self):
        return f'{self.name}'


class Delivery(models.Model):
    """Модель доставки"""

    address = models.CharField(max_length=200, verbose_name='Адрес')
    phone = models.CharField('Телефон', validators=(validate_phone,), max_length=30)
    type_delivery = models.ForeignKey(
        DeliveryType,
        related_name='delivery',
        null=True,
        blank=True,
        verbose_name='Доставка',
        on_delete=models.SET_NULL,
    )
    created = models.DateTimeField(verbose_name='Дата оформления', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

    def __str__(self):
        return self.address


class Order(models.Model):
    """Модель заказов"""

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders', verbose_name='Клиент')
    created = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления заказа', auto_now=True)
    products = models.ManyToManyField(Product, through='OrderProduct', verbose_name='Товар')
    delivery = models.ForeignKey(
        Delivery, related_name='orders_delivery', verbose_name='Доставка', on_delete=models.SET_NULL, null=True
    )
    paid = models.BooleanField(verbose_name='Оплачено', default=False)
    total_cost = models.DecimalField(
        verbose_name='Общая стоимость', null=True, blank=True, default=0.00, max_digits=40, decimal_places=2
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # def __str__(self):
    #     return f'Order {self.id}, {self.user.email}'


class OrderProduct(models.Model):
    """Модель товаров в заказе"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='order_products')
    quantity = models.PositiveIntegerField(verbose_name='Колличество', default=1)
    price = models.DecimalField(verbose_name='Цена', max_digits=20, decimal_places=2)
    cost = models.DecimalField(verbose_name='Стоимость', default=0, max_digits=40, decimal_places=2)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
        constraints = [UniqueConstraint(fields=['order', 'product'], name='unique_product_order')]

    def __str__(self):
        return f'Product {self.product.id} -->> Order {self.order.id}'

    def save(self, *args, **kwargs):
        self.cost = self.product.price * self.quantity
        self.price = self.product.price
        super().save(*args, **kwargs)
        self.order.total_cost = OrderProduct.objects.filter(order=self.order).aggregate(Sum('cost'))['cost__sum']
        self.order.save(update_fields=['total_cost'])
        return


class Storehouse(models.Model):
    """Модель товаров на складе"""

    product = models.OneToOneField(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='storehouse')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=0, message='Минимальное количество 0!')]
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'

    def __str__(self):
        return f'{self.product} ---> {self.quantity}'
