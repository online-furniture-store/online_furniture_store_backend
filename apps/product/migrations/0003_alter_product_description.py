# Generated by Django 4.2.2 on 2023-06-20 20:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('product', '0002_alter_product_name')]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, null=True, verbose_name='Описание'),
        )
    ]
