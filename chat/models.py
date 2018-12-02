from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils import timezone


class ChatUserInfo(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chatinfo', verbose_name='ユーザー')
    unread_count = models.PositiveIntegerField('未読数', default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'ユーザー情報'
        verbose_name_plural = 'ユーザー情報'


class ChannelQuerySet(models.QuerySet):
    def filter_by_members(self, users):
        query = self.annotate(count=Count('members')).filter(count=len(users))
        for user in users:
            query = query.filter(members=user)
        return query


class Channel(models.Model):

    name = models.CharField('名前', max_length=50)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ChannelMembership', verbose_name='メンバー')
    updated_at = models.DateTimeField('更新日時', default=timezone.now)

    objects = ChannelQuerySet.as_manager()

    def get_usernames(self, user):
        return ', '.join([member.username for member in self.members.exclude(pk=user.pk)])

    def __str__(self):
        return str(self.id) + ': ' + ', '.join([member.username for member in self.members.all()])

    class Meta:
        verbose_name = 'チャンネル'
        verbose_name_plural = 'チャンネル'


class ChannelMembership(models.Model):

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='チャンネル')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザー')
    unread_count = models.PositiveIntegerField('未読数', default=0)

    def __str__(self):
        return str(self.channel.id) + ': ' + self.user.username

    class Meta:
        verbose_name = 'チャンネルメンバーシップ'
        verbose_name_plural = 'チャンネルメンバーシップ'

        unique_together = ('channel', 'user')


class Message(models.Model):

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='チャンネル')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ユーザー')
    content = models.TextField('内容')
    posted_at = models.DateTimeField('投稿日時', auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.content

    class Meta:
        verbose_name = 'メッセージ'
        verbose_name_plural = 'メッセージ'
