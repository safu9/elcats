from math import floor
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from django import forms, template
from django.template.loader import get_template


register = template.Library()


INPUT_WIDGETS = (
    forms.TextInput,
    forms.NumberInput,
    forms.EmailInput,
    forms.URLInput,
    forms.PasswordInput,
    forms.DateInput,
    forms.TimeInput,
    forms.DateTimeInput
)


@register.simple_tag
def bulma_field(field, extra_class=''):
    widget = field.field.widget
    html_class = extra_class.split()

    if isinstance(widget, INPUT_WIDGETS):
        html_class.insert(0, "input")
    elif isinstance(widget, forms.Textarea):
        html_class.insert(0, "textarea")
    elif isinstance(widget, forms.Select):
        html_class.insert(0, "select")
        template = get_template("bulma/select.html")
        return template.render({'field': field, 'html_class': html_class})

    widget.attrs["class"] = ' '.join(html_class)
    return field


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
