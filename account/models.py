import re

from django.core.validators import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


def validate_username(value):
    if not re.match(r'^[-a-z0-9_]+\Z', value):
        raise ValidationError('半角の英数字、アンダースコア、ハイフン以外は使用できません。', code='invalid')


class User(AbstractUser):

    username = models.CharField('ユーザー名', max_length=30, unique=True, validators=[validate_username])
