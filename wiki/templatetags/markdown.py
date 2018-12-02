from django import template

import markdown


register = template.Library()


@register.filter
def markdown2html(value):
    return markdown.markdown(value)
