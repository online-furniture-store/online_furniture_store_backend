# Generated by Django 4.2.2 on 2023-06-21 18:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('orders', '0001_initial')]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=40, verbose_name='Общая стоимость'),
        )
    ]