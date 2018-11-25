from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(needs_autoescape=True)
def bulma_input(value, autoescape=True):
    if autoescape:
        value = conditional_escape(value)

    return mark_safe(value.replace('input ', 'input class="input"'))


@register.filter(needs_autoescape=True)
def bulma_textarea(value, autoescape=True):
    if autoescape:
        value = conditional_escape(value)

    return mark_safe(value.replace('textarea ', 'textarea class="textarea"'))
