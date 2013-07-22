from django.contrib import admin
from testingstate.models import TestingKey


class TestingAdmin(admin.ModelAdmin):
    list_display = ('key', 'is_used')


admin.site.register(TestingKey, TestingAdmin)
