from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(needs_autoescape=True)
def bulma_form(value, autoescape=True):
    if autoescape:
        value = conditional_escape(value)

    value = value.replace('input type="text" ', 'input type="text" class="input" ')
    value = value.replace('input type="date" ', 'input type="date" class="input" ')
    value = value.replace('input type="password" ', 'input type="password" class="input" ')
    value = value.replace('textarea ', 'textarea class="textarea" ')

    return mark_safe(value)
