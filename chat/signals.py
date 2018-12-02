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

    for membership in channel.channelmembership_set.exclude(user=instance.user):
        membership.unread_count = F('unread_count') + 1
        membership.save()

        userInfo = getattr(membership.user, 'chatinfo', None)
        userInfo.unread_count = F('unread_count') + 1
        userInfo.save()
