from django import template
register = template.Library()


@register.filter
def possessive(input):
    possessive = '' if input.endswith('s') else 's'
    return "{0}'{1}".format(input, possessive)
