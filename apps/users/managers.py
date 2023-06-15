from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    """Индивидуальная модель пользователя."""

    def _create_user(self, email: str, password: str | None, **extra_fields):
        """
        Создание пользователя с помощью email.
        """
        if not email:
            raise ValueError('Необходим email.')
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.username = None
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
