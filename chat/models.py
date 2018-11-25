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
    def filter_by_users(self, users):
        query = self.annotate(count=Count('userinfo')).filter(count=len(users))
        for user in users:
            query = query.filter(userinfo__user=user)
        return query


class Channel(models.Model):

    name = models.CharField('名前', max_length=50)
    updated_at = models.DateTimeField('更新日時', default=timezone.now)

    objects = ChannelQuerySet.as_manager()

    def add_users(self, users):
        for user in users:
            if not getattr(user, 'chatinfo', None):
                info = ChatUserInfo()
                info.user = user
                info.save()

            userInfo = ChannelUserInfo()
            userInfo.channel = self
            userInfo.user = user
            userInfo.save()

    def get_info(self, user):
        return self.userinfo.get(user=user)

    def get_usernames(self, user):
        return ', '.join([info.user.username for info in self.userinfo.exclude(user=user)])

    def __str__(self):
        return str(self.id) + ': ' + ', '.join([info.user.username for info in self.userinfo.all()])

    class Meta:
        verbose_name = 'チャンネル'
        verbose_name_plural = 'チャンネル'


class ChannelUserInfo(models.Model):

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='userinfo', verbose_name='チャンネル')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channelinfo', verbose_name='ユーザー')
    unread_count = models.PositiveIntegerField('未読数', default=0)

    def __str__(self):
        return str(self.channel.id) + ': ' + self.user.username

    class Meta:
        verbose_name = 'チャンネルユーザー情報'
        verbose_name_plural = 'チャンネルユーザー情報'

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
