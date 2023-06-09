# Generated by Django 4.2.2 on 2023-06-21 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('product', '0004_remove_product_discount')]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Коллекция')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Идентификатор URL на коллекцию')),
                (
                    'image',
                    models.ImageField(
                        default='products/noimage_detail.png', upload_to='', verbose_name='Изображение коллекции'
                    ),
                ),
            ],
            options={'verbose_name': 'Коллекция', 'verbose_name_plural': 'Коллекции'},
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(
                default='products/noimage_detail.png', upload_to='', verbose_name='Фотография продукта'
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='products',
                to='product.collection',
                verbose_name='Коллекция',
            ),
        ),
    ]
