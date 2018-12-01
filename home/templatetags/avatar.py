import hashlib
from urllib.parse import urlencode

from django import template
from django.utils.encoding import force_bytes


register = template.Library()


@register.inclusion_tag("avatar/avatar.html")
def avatar_img(user, size=32, img_class=""):
    params = {'s': str(size), 'd': 'identicon', 'r': 'g'}
    hash = hashlib.md5(force_bytes(user.email)).hexdigest()
    url = 'https://www.gravatar.com/avatar/%s?%s' % (hash, urlencode(params))

    img_class = ("avatar " + img_class.strip()).strip()

    return { 'avatar_url': url, 'size': size, 'alt': user.username, 'img_class': img_class }
