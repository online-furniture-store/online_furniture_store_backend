from re import match

from django.core.exceptions import ValidationError


def validate_phone(value):
    if match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7}$', value):
        correct_value = []
        for i in value:
            if i.isdigit():
                correct_value.append(i)
        return str(''.join(correct_value))[-10:]
    raise ValidationError('Некорректный номер телефона.')
