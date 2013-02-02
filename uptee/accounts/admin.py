from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from accounts.models import Activation, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    fields = ('allowed_mods',)
    filter_horizontal = ('allowed_mods',)


class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')

    def add_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline]
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()
        # delete activation key if there is any
        if obj.is_active:
            activation = Activation.objects.filter(user=obj)
            if activation:
                activation[0].delete()

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)
