from django.conf import settings
from django.db import models

from home.models import Project


class Task(models.Model):

    TODO = 0
    DOING = 1
    DONE = 2

    STATES = (
        (TODO, '未対応'),
        (DOING, '対応中'),
        (DONE, '完了'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='プロジェクト')
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


class TaskComment(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='タスク')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザー')
    content = models.TextField('内容')
    posted_at = models.DateTimeField('投稿日時', auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.content

    class Meta:
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'
