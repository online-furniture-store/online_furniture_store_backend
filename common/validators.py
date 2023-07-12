import re

from django.core.exceptions import ValidationError


def validate_phone(value):
    pattern = r'\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$'
    if re.match(pattern, value):
        return value
    raise ValidationError('Некорректный номер телефона.')
