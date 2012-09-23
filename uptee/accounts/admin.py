import os, tarfile, zipfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from mod.models import Mod
from settings import MEDIA_ROOT

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class UserAdmin(AuthUserAdmin):
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            path = os.path.join(MEDIA_ROOT, 'users', obj.username)
            if not os.path.exists(path):
                os.makedirs(path)
            mods = Mod.objects.all()
            zips = mods.filter(mimetype='application/zip')
            tars = mods.filter(mimetype='application/x-tar')
            for mod in zips:
                mod_path = os.path.join(MEDIA_ROOT, 'users', obj.username, mod.title)
                if not os.path.exists(mod_path):
                    os.makedirs(mod_path)
                    with zipfile.ZipFile(mod.mod_file.path) as z:
                        z.extractall(mod_path)
            for mod in tars:
                mod_path = os.path.join(MEDIA_ROOT, 'users', obj.username, mod.title)
                if not os.path.exists(mod_path):
                    os.makedirs(mod_path)
                    with tarfile.TarFile(mod.mod_file.path) as t:
                        t.extractall(mod_path)
        obj.save()

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
