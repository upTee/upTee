from django import template
register = template.Library()

@register.filter
def servername(server):
    try:
        servername = server.config_options.get(command='sv_name')
        return servername.value
    except:
        return ''
