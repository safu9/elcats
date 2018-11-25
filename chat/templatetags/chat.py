from django import template


register = template.Library()


@register.filter
def attr(value, arg):
    return getattr(value, arg)


@register.filter
def channel_userinfo(channel, user):
    return channel.get_info(user)


@register.filter
def channel_usernames(channel, user):
    return channel.get_usernames(user)
