# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.gender'
        db.add_column(u'accounts_userprofile', 'gender',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'UserProfile.publish_gender'
        db.add_column(u'accounts_userprofile', 'publish_gender',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.birthday'
        db.add_column(u'accounts_userprofile', 'birthday',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.publish_birthday'
        db.add_column(u'accounts_userprofile', 'publish_birthday',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.ingame_name'
        db.add_column(u'accounts_userprofile', 'ingame_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.publish_ingame_name'
        db.add_column(u'accounts_userprofile', 'publish_ingame_name',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.fav_map'
        db.add_column(u'accounts_userprofile', 'fav_map',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.publish_fav_map'
        db.add_column(u'accounts_userprofile', 'publish_fav_map',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.fav_mod'
        db.add_column(u'accounts_userprofile', 'fav_mod',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.publish_fav_mod'
        db.add_column(u'accounts_userprofile', 'publish_fav_mod',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.contact'
        db.add_column(u'accounts_userprofile', 'contact',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.publish_contact'
        db.add_column(u'accounts_userprofile', 'publish_contact',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.website'
        db.add_column(u'accounts_userprofile', 'website',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.publish_website'
        db.add_column(u'accounts_userprofile', 'publish_website',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.publish_name'
        db.add_column(u'accounts_userprofile', 'publish_name',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.gender'
        db.delete_column(u'accounts_userprofile', 'gender')

        # Deleting field 'UserProfile.publish_gender'
        db.delete_column(u'accounts_userprofile', 'publish_gender')

        # Deleting field 'UserProfile.birthday'
        db.delete_column(u'accounts_userprofile', 'birthday')

        # Deleting field 'UserProfile.publish_birthday'
        db.delete_column(u'accounts_userprofile', 'publish_birthday')

        # Deleting field 'UserProfile.ingame_name'
        db.delete_column(u'accounts_userprofile', 'ingame_name')

        # Deleting field 'UserProfile.publish_ingame_name'
        db.delete_column(u'accounts_userprofile', 'publish_ingame_name')

        # Deleting field 'UserProfile.fav_map'
        db.delete_column(u'accounts_userprofile', 'fav_map')

        # Deleting field 'UserProfile.publish_fav_map'
        db.delete_column(u'accounts_userprofile', 'publish_fav_map')

        # Deleting field 'UserProfile.fav_mod'
        db.delete_column(u'accounts_userprofile', 'fav_mod')

        # Deleting field 'UserProfile.publish_fav_mod'
        db.delete_column(u'accounts_userprofile', 'publish_fav_mod')

        # Deleting field 'UserProfile.contact'
        db.delete_column(u'accounts_userprofile', 'contact')

        # Deleting field 'UserProfile.publish_contact'
        db.delete_column(u'accounts_userprofile', 'publish_contact')

        # Deleting field 'UserProfile.website'
        db.delete_column(u'accounts_userprofile', 'website')

        # Deleting field 'UserProfile.publish_website'
        db.delete_column(u'accounts_userprofile', 'publish_website')

        # Deleting field 'UserProfile.publish_name'
        db.delete_column(u'accounts_userprofile', 'publish_name')


    models = {
        u'accounts.activation': {
            'Meta': {'object_name': 'Activation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'activation'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'accounts.moderator': {
            'Meta': {'object_name': 'Moderator'},
            'allowed_options': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderators'", 'symmetrical': 'False', 'to': u"orm['mod.Option']"}),
            'allowed_tunings': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderators'", 'symmetrical': 'False', 'to': u"orm['mod.Tune']"}),
            'console_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edit_automatic_restart_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edit_map_download_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edit_rcon_commands_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edit_votes_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_upload_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restart_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderators'", 'to': u"orm['mod.Server']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderators'", 'to': u"orm['auth.User']"})
        },
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'allowed_mods': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users'", 'blank': 'True', 'to': u"orm['mod.Mod']"}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'fav_map': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fav_mod': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingame_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'publish_birthday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_fav_map': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_fav_mod': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_gender': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_ingame_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_website': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'simpleblue'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mod.mod': {
            'Meta': {'ordering': "['upload_date', 'title']", 'object_name': 'Mod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mod_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'mod.option': {
            'Meta': {'ordering': "['id']", 'object_name': 'Option'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_options'", 'to': u"orm['mod.Server']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'widget': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'mod.port': {
            'Meta': {'ordering': "['port']", 'object_name': 'Port'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'port': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        u'mod.server': {
            'Meta': {'ordering': "['owner', 'mod', 'port']", 'object_name': 'Server'},
            'automatic_restart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map_download_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mod': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'servers'", 'to': u"orm['mod.Mod']"}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'servers'", 'to': u"orm['auth.User']"}),
            'pid': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'server'", 'unique': 'True', 'null': 'True', 'to': u"orm['mod.Port']"}),
            'random_key': ('django.db.models.fields.CharField', [], {'max_length': '24', 'unique': 'True', 'null': 'True'}),
            'server_info': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'set_online_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'mod.tune': {
            'Meta': {'ordering': "['id']", 'object_name': 'Tune'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_tunes'", 'to': u"orm['mod.Server']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['accounts']