import os
import tarfile
import zipfile
from shutil import move, rmtree
from django.contrib import admin
from django.contrib.auth.models import User
from mod.forms import *
from mod.models import *
from settings import MEDIA_ROOT


class ModAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'mod_file', 'mimetype')
    search_fields = ('title', 'mod_file', 'mimetype')
    list_filter = ('upload_date', 'mimetype')
    form = ModAdminForm
    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(ModAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
    really_delete_selected.short_description = u"Delete selected mods"

    def save_model(self, request, obj, form, change):
        obj.save()
        mod_path = os.path.join(MEDIA_ROOT, 'mods', obj.title)
        if not change:
            self.extract_mod(obj, mod_path)
        else:
            tmp_dir = os.path.join(MEDIA_ROOT, 'tmp')
            servers_path = os.path.join(MEDIA_ROOT, 'mods', obj.title, 'servers')
            if os.path.exists(servers_path):
                move(servers_path, os.path.join(tmp_dir, obj.title, 'servers'))
            if os.path.exists(mod_path):
                rmtree(mod_path)
            self.extract_mod(obj, mod_path)
            if os.path.exists(os.path.join(tmp_dir, obj.title, 'servers')):
                move(os.path.join(tmp_dir, obj.title, 'servers'), os.path.join(mod_path))

    def extract_mod(self, obj, mod_path):
        if not os.path.exists(mod_path):
            os.makedirs(mod_path)
            if obj.mimetype == 'application/zip':
                with zipfile.ZipFile(obj.mod_file.path) as z:
                    z.extractall(mod_path)
            elif obj.mimetype == 'application/x-tar':
                with tarfile.TarFile(obj.mod_file.path) as t:
                    t.extractall(mod_path)


class ServerAdmin(admin.ModelAdmin):
    list_display = ('mod', 'owner', 'is_active')
    search_fields = ('title', 'owner')
    list_filter = ('mod', 'owner', 'is_active')
    form = ServerAdminForm
    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(ServerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
    really_delete_selected.short_description = u"Delete selected servers"

    def save_model(self, request, obj, form, change):
        old_obj = Server.objects.get(pk=obj.id) if change else None
        if not obj.is_active:
            obj.set_offline()
        default_settings = False
        if not change:
            obj.random_key = User.objects.make_random_password()
            default_settings = True
        else:
            # check if server mod changed and reset config
            if old_obj and old_obj.mod != obj.mod:
                default_settings = True
        if obj.mod not in obj.owner.profile.allowed_mods.all():
            obj.owner.profile.allowed_mods.add(obj.mod)
            obj.owner.profile.save()
        obj.save()
        if default_settings:
            obj.reset_settings(old_obj)


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


class MapAdmin(admin.ModelAdmin):
    list_display = ('owner', 'server', 'name', 'author')
    list_filter = ('server', 'server__owner')
    actions = ['really_delete_selected']

    def get_actions(self, request):
        actions = super(MapAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
    really_delete_selected.short_description = u"Delete selected maps"

    def owner(self, obj):
        return obj.server.owner

admin.site.register(Mod, ModAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Port, PortAdmin)
admin.site.register(Map, MapAdmin)
