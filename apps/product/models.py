from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.users.models import User


class Category(models.Model):
    """Модель категорий товаров в магазине."""

    name = models.CharField(verbose_name='Название категории', max_length=20, unique=True)
    slug = models.SlugField(verbose_name='Ссылка на категорию', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Material(models.Model):
    """Модель материалов товаров в магазине."""

    name = models.CharField(verbose_name='Название материала', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.name


class Color(models.Model):
    """Модель цветов товаров в магазине."""

    name = models.CharField(verbose_name='Название цвета', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class FurnitureDetails(models.Model):
    purpose = models.CharField(verbose_name='Назначение', max_length=50, blank=True, null=True)
    furniture_type = models.CharField(verbose_name='Тип', max_length=50, blank=True, null=True)
    construction = models.CharField(verbose_name='Конструкция', max_length=50, blank=True, null=True)
    swing_mechanism = models.CharField(verbose_name='Механизм качания', max_length=50, blank=True, null=True)
    armrest_adjustment = models.CharField(
        verbose_name='Регулирование подлокотников', max_length=50, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Особенности конструкции'
        verbose_name_plural = 'Особенности конструкций'

    def __str__(self):
        fields = [
            str(field)
            for field in [
                self.purpose,
                self.furniture_type,
                self.construction,
                self.swing_mechanism,
                self.armrest_adjustment,
            ]
            if field
        ]
        return ', '.join(fields) if fields else 'FurnitureDetails object'


class Product(models.Model):
    """Модель Продуктов(Товаров) магазина"""

    article = models.PositiveIntegerField(verbose_name='Артикул', unique=True)
    name = models.CharField(verbose_name='Название', max_length=20)
    width = models.PositiveSmallIntegerField(verbose_name='Ширина, см', validators=[MaxValueValidator(15000)])
    height = models.PositiveSmallIntegerField(verbose_name='Высота, см', validators=[MaxValueValidator(15000)])
    length = models.PositiveSmallIntegerField(verbose_name='Длина, см', validators=[MaxValueValidator(15000)])
    weight = models.DecimalField(
        verbose_name='Вес, кг', validators=[MaxValueValidator(500)], decimal_places=2, max_digits=5
    )
    color = models.ForeignKey(Color, verbose_name='Цвет', on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(
        verbose_name='Фотография продукта', upload_to='products/', default='products/noimage_detail.png'
    )
    material = models.ManyToManyField(Material, related_name='products')
    furniture_details = models.ForeignKey(
        FurnitureDetails, verbose_name='Особенности конструкции', null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.ForeignKey(
        'Discount', related_name='products', verbose_name='Скидки', null=True, blank=True, on_delete=models.SET_NULL
    )
    fast_delivery = models.BooleanField(verbose_name='Быстрая доставка', default=False)
    country = models.CharField(verbose_name='Страна-производитель', max_length=40)
    brand = models.CharField(verbose_name='Бренд', null=True, max_length=100)
    warranty = models.PositiveSmallIntegerField(
        verbose_name='Гарантия , лет', null=True, validators=[MaxValueValidator(100)]
    )
    price = models.DecimalField(verbose_name='Цена', null=False, max_digits=10, decimal_places=2)
    description = models.CharField(verbose_name='Описание')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Discount(models.Model):
    """Модель скидок для  товаров в магазине."""

    applied_products = models.ManyToManyField(Product, verbose_name='Применяемые товары', related_name='discounts')
    discount = models.SmallIntegerField(verbose_name='Размер скидки, %', validators=[MaxValueValidator(99)], default=0)
    discount_created_at = models.DateTimeField(verbose_name='Начало скидки', default=timezone.now)
    discount_end_at = models.DateTimeField(verbose_name='Окончание скидки')

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Favorite(models.Model):
    """Модель для добавления товаров в избранное."""

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'
        constraints = (models.UniqueConstraint(fields=('product', 'user'), name='product_user_unique'),)

    def __str__(self) -> str:
        return f'{self.user} -> {self.product}'


class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'


class CartItem(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Корзина с товарами'
        verbose_name_plural = 'Корзины с товарами'
