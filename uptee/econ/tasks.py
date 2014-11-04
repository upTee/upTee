import os
import signal
import psutil
from celery import task
from billiard import Process
from django.core.cache import cache
from econ import TelnetClient


@task()
def telnet_client(server_id, port):
    key = 'server-{0}-pid'.format(server_id)
    pid = cache.get(key)
    if pid and pid in psutil.get_pid_list():
        os.kill(pid, signal.SIGTERM)
    p = Process(target=TelnetClient, args=(port, 'uptee', server_id))
    p.start()
    cache.set(key, p.pid)
    p.join()
