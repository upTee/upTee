import os
from datetime import timedelta
from subprocess import Popen
from celery import task
from django.contrib.auth.models import User
from django.utils import timezone
from mod.models import TaskEvent
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


@task()
def start_server(event_id):
    event = TaskEvent.objects.filter(pk=event_id)
    if event:
        event = event[0]
    else:
        return
    event.server.set_online()
    if not event.repeat:
        event.status = 2  # done
        event.save(update_fields=['status'])
    else:
        next_run = event.date + timedelta(minutes=event.repeat)
        if timezone.now() >= next_run:
            event.status = 2  # done
            event.save(update_fields=['status'])
            return
        task = start_server.apply_async((event_id,), eta=next_run)
        event.date = next_run
        event.task_id = task.task_id
        event.save(update_fields=['date', 'task_id'])


@task()
def stop_server(event_id):
    event = TaskEvent.objects.filter(pk=event_id)
    if event:
        event = event[0]
    else:
        return
    event.server.set_offline()
    if not event.repeat:
        event.status = 2  # done
        event.save(update_fields=['status'])
    else:
        next_run = event.date + timedelta(minutes=event.repeat)
        if timezone.now() >= next_run:
            event.status = 2  # done
            event.save(update_fields=['status'])
            return
        task = stop_server.apply_async((event_id,), eta=next_run)
        event.date = next_run
        event.task_id = task.task_id
        event.save(update_fields=['date', 'task_id'])


@task()
def restart_server(event_id):
    event = TaskEvent.objects.filter(pk=event_id)
    if event:
        event = event[0]
    else:
        return
    if event.server.is_online:
        event.server.set_offline()
    event.server.set_online()
    if not event.repeat:
        event.status = 2  # done
        event.save(update_fields=['status'])
    else:
        next_run = event.date + timedelta(minutes=event.repeat)
        if timezone.now() >= next_run:
            event.status = 2  # done
            event.save(update_fields=['status'])
            return
        task = restart_server.apply_async((event_id,), eta=next_run)
        event.date = next_run
        event.task_id = task.task_id
        event.save(update_fields=['date', 'task_id'])
