from django import template
register = template.Library()


@register.filter
def get_option(server, command):
    try:
        servername = server.config_options.get(command=command)
        return servername.value
    except:
        return ''
