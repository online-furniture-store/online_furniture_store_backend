from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = 'online_furniture_store_backend.users'
    verbose_name = _('Users')

    def ready(self):
        try:
            import online_furniture_store_backend.users.signals  # noqa: F401
        except ImportError:
            pass
