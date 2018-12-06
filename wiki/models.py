from django.db import models

from home.models import Project


class Page(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='プロジェクト')
    name = models.CharField('名前', max_length=50)
    slug = models.SlugField('スラッグ', max_length=50)
    content = models.TextField('内容', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'ページ'
        verbose_name_plural = 'ページ'
