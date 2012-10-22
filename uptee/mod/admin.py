import os, tarfile, zipfile
from django.contrib import admin
from mod.forms import *
from mod.models import *
from settings import MEDIA_ROOT
from lib.twconfig import Config as TwCongig

class ModAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'mod_file', 'mimetype')
    search_fields = ('title', 'mod_file', 'mimetype')
    list_filter = ('upload_date', 'mimetype')
    form = ModAdminForm
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(ModAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
    really_delete_selected.short_description = u"Delete selected mods"

class ServerAdmin(admin.ModelAdmin):
    list_display = ('mod', 'owner', 'is_active')
    search_fields = ('title', 'owner')
    list_filter = ('mod', 'owner', 'is_active')
    form = ServerAdminForm
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(ServerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
    really_delete_selected.short_description = u"Delete selected servers"

    def save_model(self, request, obj, form, change):
        obj.save()
        if not obj.is_active:
            obj.set_offline()
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
                widget = 1 # text
                for widget_type in Option.WIDGET_CHOICES:
                    if widget_type[1] == value[1]:
                        widget = widget_type[0]
                data = Option(server=obj, command=key, value=value[0], widget=widget)
                data.save()
            for tune in config.tunes:
                data = Tune(server=obj, command=tune['command'], value=tune['value'])
                data.save()
            for vote in config.votes:
                data = Vote(server=obj, command=vote['command'], title=vote['title'])
                data.save()

class PortAdmin(admin.ModelAdmin):
    list_display = ('port', 'is_active')
    list_filter = ('is_active',)
    actions = ['set_free']

    def set_free(self, request, queryset):
        for obj in queryset:
            try:
                obj.server.set_offline()
            except:
                obj.is_active = False
                obj.save()
    set_free.short_description = u"Set selected ports free"

    def save_model(self, request, obj, form, change):
        if not obj.is_active:
            try:
                obj.server.set_offline()
            except:
                pass
        obj.save()

admin.site.register(Mod, ModAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Port, PortAdmin)
