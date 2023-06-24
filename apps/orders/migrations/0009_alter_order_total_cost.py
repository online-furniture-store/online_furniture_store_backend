# Generated by Django 4.2.2 on 2023-06-24 13:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('orders', '0008_alter_order_user')]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0.0, max_digits=40, null=True, verbose_name='Общая стоимость'
            ),
        )
    ]