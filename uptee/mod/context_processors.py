from mod.models import Server


def mod(request):
    user = request.user if request.user.is_authenticated() else None
    servers = None
    moderated_servers = []
    moderated_servers_restart = []
    try:  # try invalidating cache for server model (have no idea if this is right)
        from johnny.cache import invalidate
        invalidate(Server)
    except:
        pass
    if user:
        servers = Server.objects.filter(is_active=True, owner=user)
        moderated_servers = Server.objects.filter(moderators__user=user)
        moderated_servers_restart = Server.objects.filter(moderators__user=user, moderators__restart_allowed=True)
    return {
        'user_server_list': servers,
        'user_moderated_servers': moderated_servers,
        'user_moderated_servers_restart': moderated_servers_restart
    }
