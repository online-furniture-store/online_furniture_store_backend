from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, EmailField
from django.utils.translation import gettext_lazy as _

from apps.users.managers import UserManager
from apps.users.validators import validate_phone


class User(AbstractUser):
    """
    Кастомная модель пользоввателя
    """

    MAN = 'M'
    WOMAN = 'W'
    GENDER = [(MAN, 'мужской'), (WOMAN, 'женский')]

    phone = CharField('Телефон', validators=(validate_phone,), max_length=30, unique=True)
    first_name = CharField('Имя', max_length=30, blank=True, null=True)
    last_name = CharField('Фамилия', max_length=50, blank=True, null=True)
    email = EmailField(_('Email'), unique=True)
    gender = CharField('Пол', max_length=30, choices=GENDER, default=GENDER[0][0])
    birthday = DateField('День рождения', blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()
