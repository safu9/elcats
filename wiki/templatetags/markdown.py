from django import template

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension


register = template.Library()


@register.filter
def markdown2html(value):
    return markdown.markdown(value, extensions=[
        'gfm',
        WikiLinkExtension(base_url='../'),
    ], output_format='html5')
