from django.conf import settings
from django.db import models


class Task(models.Model):

    TODO = 0
    DOING = 1
    DONE = 2

    STATES = (
        (TODO, '未対応'),
        (DOING, '対応中'),
        (DONE, '完了'),
    )

    name = models.CharField('名前', max_length=50)
    description = models.TextField('説明', blank=True)
    date_from = models.DateField('開始日', blank=True, null=True)
    date_to = models.DateField('終了日', blank=True, null=True)
    state = models.IntegerField('状態', choices=STATES, default=TODO, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_tasks', verbose_name='作成者')
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='assigned_tasks', verbose_name='担当者')

    class Meta:
        verbose_name = 'タスク'
        verbose_name_plural = 'タスク'
