from re import match

from django.core.exceptions import ValidationError


def validate_phone(value):
    if match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7}$', value):
        return ''.join([i for i in value if i.isdigit()][-10:])
    raise ValidationError('Некорректный номер телефона.')
