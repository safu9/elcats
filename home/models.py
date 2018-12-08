from django.conf import settings
from django.core.validators import ValidationError
from django.db import models


class Project(models.Model):

    name = models.CharField('名前', max_length=50)
    slug = models.SlugField('スラッグ', max_length=50, unique=True)
    description = models.CharField('説明', max_length=50, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='メンバー')
    is_private = models.BooleanField('非公開', default=False)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    def clean(self):
        if self.slug in ('login','logout','password','user','create','admin','api'):
            raise ValidationError({'slug': 'このスラッグは利用できません。'})

    class Meta:
        verbose_name = 'プロジェクト'
        verbose_name_plural = 'プロジェクト'
