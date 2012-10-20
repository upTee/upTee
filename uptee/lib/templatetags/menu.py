import re
from django import template

register = template.Library()

@register.simple_tag
def current(request, pattern):
    if request.path == pattern:
        return ' current'
    else:
        return ''
