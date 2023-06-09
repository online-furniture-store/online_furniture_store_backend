# Generated by Django 4.2.2 on 2023-07-02 21:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('orders', '0001_initial')]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.PositiveIntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество: 1 шт.')],
                verbose_name='Колличество',
            ),
        )
    ]
