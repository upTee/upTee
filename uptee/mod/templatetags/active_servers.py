from django import template
register = template.Library()


@register.filter
def active_servers(servers):
    return servers.filter(is_active=True)
