from re import match

from django.core.exceptions import ValidationError


def validate_phone(value):
    if match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7}$', value):
        return value
    raise ValidationError('Некорректный номер телефона.')
