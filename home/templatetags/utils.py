from urllib.parse import urlencode

from django import template


register = template.Library()


@register.simple_tag
def urlparams(param, *args, **kwargs):
    param = param.copy()

    dicts = list(args)
    dicts.append(kwargs)
    for dict in dicts:
        for key, value in dict.items():
            if value is None:
                if key in param:
                    del param[key]
            else:
                param[key] = value

    return '?' + urlencode(param)
