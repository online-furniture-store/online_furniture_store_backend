from re import match

from django.core.exceptions import ValidationError


def validate_phone(value):
    if match(r'^((8|' r'\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7}$', value):
        return ''.join([i for i in value if i.isdigit()][-10:])
    raise ValidationError('Некорректный номер телефона.')


def validate_email(value):
    if match(r'^[^@]+@[^@]+\.[^@]{2,3}$', value):
        return value
    raise ValidationError('Некорректная форма записи email.')
