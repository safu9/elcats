from django import template


register = template.Library()


@register.filter
def channel_usernames(channel, user):
    return channel.get_usernames(user)
