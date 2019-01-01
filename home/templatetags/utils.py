from urllib.parse import urlencode

from django import template


register = template.Library()


@register.simple_tag
def urlparams(param, *args, **kwargs):
    param = param.copy()
    for arg in args:
        param.update(arg)
    param.update(kwargs)

    return '?' + urlencode(param)
