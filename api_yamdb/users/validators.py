import re

from django.core.exceptions import ValidationError
from users.models import User


def validate_username(value):
    regex = re.compile(r'^[\w.@+-]+')
    print(value)
    if value == 'me':
        raise ValidationError('Username "me" is not valid')
    if not regex.match(value):
        raise ValidationError(
            'Username contains invalid characters'
        )
    if User.objects.filter(username=value):
        raise ValidationError(
            'User with this name exists'
        )
    return value


def validate_email(value):
    if User.objects.filter(email=value):
        raise ValidationError(
            'User with this email exists'
        )
    return value
