from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import CharField, DateField, EmailField
from django.utils import timezone

from apps.users.managers import UserManager
from apps.users.validators import validate_email, validate_phone


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользоввателя
    """

    MAN = 'M'
    WOMAN = 'W'
    GENDER = [(MAN, 'мужской'), (WOMAN, 'женский')]

    email = EmailField('Email', validators=(validate_email,), unique=True)
    phone = CharField('Телефон', validators=(validate_phone,), max_length=30)
    first_name = CharField('Имя', max_length=30, blank=True, null=True)
    last_name = CharField('Фамилия', max_length=50, blank=True, null=True)
    gender = CharField('Пол', max_length=30, choices=GENDER,
                       default=GENDER[0][0])
    birthday = DateField('День рождения', blank=True, null=True)
    date_joined = models.DateTimeField('Дата создания', default=timezone.now)
    is_staff = models.BooleanField('Статус пользователя', default=False)
    is_active = models.BooleanField(
        'Активен',
        default=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
