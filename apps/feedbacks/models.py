from django.db import models
from apps.users.models import User
from apps.product.models import Product


class Feedback(models.Model):
    """Модель отзывов на товары в магазине."""

    RATE_CHOICES = zip(range(1, 6), range(1, 6))
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар',
                                on_delete=models.CASCADE)
    feedback = models.TextField(verbose_name='', blank=True)
    rating = models.IntegerField(choices=RATE_CHOICES)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'feedbacks'

    def __str__(self):
        return f'{self.user} -> {self.product}'


class Rating(models.Model):
    """Модель рейтинга товара в магазине."""

    product = models.ForeignKey(Product, verbose_name='Товар',
                                on_delete=models.CASCADE)
    count = models.IntegerField()
    score = models.IntegerField()

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return self.product
