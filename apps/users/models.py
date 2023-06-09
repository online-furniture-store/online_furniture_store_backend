from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, DateTimeField, EmailField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.users.managers import UserManager

GENDER = ['мужской', 'женский']


class User(AbstractUser):
    """
    Кастомная модель пользоввателя
    """

    first_name = CharField('Имя', max_length=20, blank=True)
    last_name = CharField('Фамилия', max_length=50, blank=True)
    email = EmailField(_('Email'), unique=True)
    phone = CharField('Телефон', max_length=50, unique=True)
    gender = CharField('Пол', max_length=10, default=GENDER[0])
    birthday = DateField('День рождения', blank=True, null=True)
    date_joined = DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """
        Профиль пользователя
        """
        return reverse('users:detail', kwargs={'pk': self.id})
