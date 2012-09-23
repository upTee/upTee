import os, tarfile, zipfile
from django.contrib import admin
from mod.forms import *
from mod.models import *
from settings import MEDIA_ROOT
from twconfig import Config as TwCongig

class ModAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'mod_file', 'mimetype')
    search_fields = ('title', 'mod_file', 'mimetype')
    list_filter = ('upload_date', 'mimetype')
    form = ModAdminForm 

class ServerAdmin(admin.ModelAdmin):
    list_display = ('mod', 'owner', 'is_active')
    search_fields = ('title', 'owner')
    list_filter = ('mod', 'owner', 'is_active')
    form = ServerAdminForm

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            mod_path = os.path.join(MEDIA_ROOT, 'users', obj.owner.username, obj.mod.title)
            if not os.path.exists(mod_path):
                os.makedirs(mod_path)
            if obj.mod.mimetype == 'application/zip':
                with zipfile.ZipFile(obj.mod.mod_file.path) as z:
                    z.extractall(mod_path)
            elif obj.mod.mimetype == 'application/x-tar':
                with tarfile.TarFile(obj.mod.mod_file.path) as t:
                    t.extractall(mod_path)

            config_path = os.path.join(mod_path, 'config.cfg')
            config = TwCongig(config_path)
            config.read()
            for key, value in config.options.iteritems():
                data = Option(server=obj, command=key, value=value)
                data.save()
            for tune in config.tunes:
                data = Tune(server=obj, command=tune['command'], value=tune['value'])
                data.save()
            for vote in config.votes:
                data = Vote(server=obj, command=vote['command'], title=vote['title'])
                data.save()

admin.site.register(Mod, ModAdmin)
admin.site.register(Server, ServerAdmin)
