import os
from celery import task
from settings import SERVER_EXEC
from subprocess import Popen

@task()
def run_server(path, server):
    with open(os.path.join(path, 'log.txt'), 'w') as f:
        p = Popen((os.path.join(path, SERVER_EXEC), '-f', 'generated.cfg'), cwd=path, stdout=f, stderr=f)
        server.pid = p.pid
        server.save()
        p.wait()
