from django.core.management.base import BaseCommand
from mod.models import Server


class Command(BaseCommand):
    help = 'Unlocks all servers.'

    def handle(self, *args, **options):
        for server in Server.objects.all():
            server.locked = False
            server.save()
