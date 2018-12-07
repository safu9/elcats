from math import floor
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

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
    value = value.replace('input type="email" ', 'input type="email" class="input" ')
    value = value.replace('input type="password" ', 'input type="password" class="input" ')
    value = value.replace('textarea ', 'textarea class="textarea" ')
    value = re.sub('<select(.*?)/select>', r'<div class="select"><select\1/select></div>', value, flags=re.DOTALL)

    return mark_safe(value)


@register.inclusion_tag("bulma/pagination.html")
def bulma_pagination(page, pages_to_show=5, url=None, extra=None, parameter_name="page"):
    """ Render pagination for a page
    Parameters:
        page : The page of results to show
        pages_to_show : Number of pages in total
        url : URL to navigate to for pagination forward and pagination back
        extra : Any extra page parameters
        parameter_name : Name of the paging URL parameter
    """

    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        pages_to_show = 1

    num_pages = page.paginator.num_pages
    current_page = page.number
    half_page_num = int(floor(pages_to_show / 2))
    if half_page_num < 0:
        half_page_num = 0

    first_page = current_page - half_page_num
    if first_page <= 1:
        first_page = 1
    if first_page > 1:
        pages_back = first_page - half_page_num
        if pages_back < 1:
            pages_back = 1
    else:
        pages_back = None

    last_page = first_page + pages_to_show - 1
    if pages_back is None:
        last_page += 1
    if last_page > num_pages:
        last_page = num_pages
    if last_page < num_pages:
        pages_forward = last_page + half_page_num
        if pages_forward > num_pages:
            pages_forward = num_pages
    else:
        pages_forward = None
        if first_page > 1:
            first_page -= 1
        if pages_back is not None and pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None

    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)

    # parse the url
    parts = urlparse(url or "")
    params = parse_qs(parts.query)

    # append extra query parameters to the url.
    if extra:
        params.update(extra)

    if params.get(parameter_name):
        del params[parameter_name]

    # build url again.
    url = urlunparse(
        [
            parts.scheme,
            parts.netloc,
            parts.path,
            parts.params,
            urlencode(params, doseq=True),
            parts.fragment,
        ]
    )

    if '?' in url:
        url += '&'
    else:
        url += '?'

    return {
        "pagination_url": url,
        "num_pages": num_pages,
        "current_page": current_page,
        "pages_shown": pages_shown,
        "pages_back": pages_back,
        "pages_forward": pages_forward,
        "parameter_name": parameter_name,
    }
