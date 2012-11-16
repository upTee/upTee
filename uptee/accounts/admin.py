from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User


class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
