from django import template
register = template.Library()


@register.filter
def le(str):
    return str.replace(r'\n', '\r\n')
