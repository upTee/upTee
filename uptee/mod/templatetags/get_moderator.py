from django import template
register = template.Library()


@register.filter
def get_moderator(server, userid):
    try:
        return server.moderators.get(user__id=userid)
    except:
        return ''
