from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Message


@receiver(post_save, sender=Message)
def update_channel(sender, instance, created, update_fields, **kwargs):
    if not created:
        return

    channel = instance.channel
    channel.updated_at = timezone.now()
    channel.save()

    for channelInfo in channel.userinfo.exclude(user=instance.user).all():
        channelInfo.unread_count = F('unread_count') + 1
        channelInfo.save()
        
        userInfo = getattr(channelInfo.user, 'chatinfo', None)
        userInfo.unread_count = F('unread_count') + 1
        userInfo.save()
