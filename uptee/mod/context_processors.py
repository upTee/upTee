from mod.models import Server


def mod(request):
    user = request.user if request.user.is_authenticated() else None
    servers = None
    if user:
        servers = Server.objects.filter(is_active=True, owner=user)
        for server in servers:
            server.check_online()
    return {
        'user_server_list': servers,
    }
