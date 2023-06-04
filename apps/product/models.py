from django.db import models

from apps.users.models import User


class Categories(models.Model):
    """Модель категорий товаров в магазине."""

    name = models.CharField(verbose_name='Название категории', max_length=20, unique=True)
    slug = models.SlugField(verbose_name='Ссылка на категорию', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Materials(models.Model):
    """Модель материалов товаров в магазине."""

    name = models.CharField(verbose_name='Название материала', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель Продуктов(Товаров) магазина"""

    article = models.IntegerField(verbose_name='Артикул', null=False, unique=True)
    name = models.CharField(verbose_name='Название', max_length=20, unique=True)
    width = models.IntegerField(verbose_name='Ширина, см', null=False)
    height = models.IntegerField(verbose_name='Высота, см', null=False)
    length = models.IntegerField(verbose_name='Длина, см', null=False)
    weight = models.IntegerField(verbose_name='Вес, кг', null=False)
    color = models.CharField(verbose_name='Цвет')
    image = models.ImageField(verbose_name='Фотография продукта', upload_to='')
    material = models.ManyToManyField(Materials)
    country = models.CharField(verbose_name='Страна-производитель')
    brand = models.CharField(verbose_name='Бренд', null=True)
    warranty = models.IntegerField(verbose_name='Гарантия , лет', null=True)
    price = models.DecimalField(verbose_name='Цена', null=False, max_digits=10, decimal_places=2)
    description = models.CharField(verbose_name='Описание', null=False)
    category = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.CASCADE, null=False)

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
