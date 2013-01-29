from django import template
register = template.Library()


@register.filter
def get_option(server, command):
    try:
        option = server.config_options.get(command=command)
        return option.get_value()
    except:
        return ''
