# Generated by Django 4.2.1 on 2023-06-11 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('users', '0002_alter_user_first_name_alter_user_gender_and_more')]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default=1, max_length=30, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, default=1, max_length=50, verbose_name='Фамилия'),
            preserve_default=False,
        ),
    ]