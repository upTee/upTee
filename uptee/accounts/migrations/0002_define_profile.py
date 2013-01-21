# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Migration(SchemaMigration):

    def forwards(self, orm):
        for user in User.objects.all():
            user.profile = UserProfile()
            user.profile.save()
            user.save()

    def backwards(self, orm):
        pass


    complete_apps = ['accounts']
