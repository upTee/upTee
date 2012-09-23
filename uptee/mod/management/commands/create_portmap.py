from django.core.management.base import BaseCommand, CommandError
from mod.models import Port

class Command(BaseCommand):
    args = '<min_port max_port>'
    help = 'Creates a portmap.'

    def handle(self, *args, **options):
        min_port, max_port = int(args[0]), int(args[1])
        if min_port >= max_port:
            CommandError('The minimal port has to be bigger than the maximal port.')

        # delete old range
        for port in Port.objects.all():
            port.delete()

        # create new range
        for port_num in range(min_port, max_port+1):
            port = Port(port=port_num)
            port.save()
