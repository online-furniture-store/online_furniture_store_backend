from django.core.validators import MaxValueValidator
from django.db import models

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


class Product(models.Model):
    """Модель Продуктов(Товаров) магазина"""

    article = models.PositiveIntegerField(verbose_name='Артикул', unique=True)
    name = models.CharField(verbose_name='Название', max_length=20, unique=True)
    width = models.PositiveSmallIntegerField(verbose_name='Ширина, см', validators=[MaxValueValidator(15000)])
    height = models.PositiveSmallIntegerField(verbose_name='Высота, см', validators=[MaxValueValidator(15000)])
    length = models.PositiveSmallIntegerField(verbose_name='Длина, см', validators=[MaxValueValidator(15000)])
    weight = models.PositiveSmallIntegerField(verbose_name='Вес, кг', validators=[MaxValueValidator(500)])
    color = models.ForeignKey(Color, verbose_name='Цвет', on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(
        verbose_name='Фотография продукта', upload_to='products/', default='products/noimage_detail.png'
    )
    material = models.ManyToManyField(Material, related_name='products')
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


class Favorite(models.Model):
    """Модель для добавления товаров в избранное."""

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='fav_user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='fav_product', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'
        constraints = (models.UniqueConstraint(fields=('product', 'user'), name='product_user_unique'),)

    def __str__(self) -> str:
        return f'{self.user} -> {self.product}'
