from django import template
register = template.Library()

@register.filter
def gametype(server):
    try:
        gametype = server.config_options.get(command='sv_gametype')
        return gametype.value
    except:
        return ''
