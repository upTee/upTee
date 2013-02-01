import os
from datetime import timedelta
from subprocess import Popen
from celery import task
from django.contrib.auth.models import User
from django.utils import timezone
from settings import MEDIA_ROOT, SERVER_EXEC


@task()
def run_server(path, server):
    log_path = os.path.join(MEDIA_ROOT, 'logs', server.owner.username, server.mod.title)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    with open(os.path.join(log_path, '{0}_{1}_{2}.txt'.format(server.id, timezone.now().strftime("%y%m%d%H%M%S"), User.objects.make_random_password())), 'w') as f:
        p = Popen((os.path.join(path, SERVER_EXEC), '-f', os.path.join(path, 'servers', server.owner.username, '{0}'.format(server.id), server.random_key, 'generated.cfg')), cwd=path, stdout=f, stderr=f)
        server.pid = p.pid
        server.online = True
        server.locked = False
        server.save()
        p.wait()


@task()
def check_server_state():
    from mod.models import Server
    servers = Server.active.filter(is_active=True)
    for server in servers:
        old_is_online = server.is_online
        if not server.is_online and server.set_online_at >= timezone.now() - timedelta(seconds=10):
            server.locked = False
            server.save()
        server.check_online()
        server.get_server_info()
        if server.automatic_restart and old_is_online and not server.is_online:
            server.set_online()
