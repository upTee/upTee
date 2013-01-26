# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Moderator'
        db.create_table('accounts_moderator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(related_name='moderators', to=orm['mod.Server'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='moderators', to=orm['auth.User'])),
            ('restart_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('edit_votes_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('map_upload_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('accounts', ['Moderator'])

        # Adding M2M table for field allowed_options on 'Moderator'
        db.create_table('accounts_moderator_allowed_options', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('moderator', models.ForeignKey(orm['accounts.moderator'], null=False)),
            ('option', models.ForeignKey(orm['mod.option'], null=False))
        ))
        db.create_unique('accounts_moderator_allowed_options', ['moderator_id', 'option_id'])

        # Adding M2M table for field allowed_tunings on 'Moderator'
        db.create_table('accounts_moderator_allowed_tunings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('moderator', models.ForeignKey(orm['accounts.moderator'], null=False)),
            ('tune', models.ForeignKey(orm['mod.tune'], null=False))
        ))
        db.create_unique('accounts_moderator_allowed_tunings', ['moderator_id', 'tune_id'])


    def backwards(self, orm):
        # Deleting model 'Moderator'
        db.delete_table('accounts_moderator')

        # Removing M2M table for field allowed_options on 'Moderator'
        db.delete_table('accounts_moderator_allowed_options')

        # Removing M2M table for field allowed_tunings on 'Moderator'
        db.delete_table('accounts_moderator_allowed_tunings')


    models = {
        'accounts.moderator': {
            'Meta': {'object_name': 'Moderator'},
            'allowed_options': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderators'", 'symmetrical': 'False', 'to': "orm['mod.Option']"}),
            'allowed_tunings': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderators'", 'symmetrical': 'False', 'to': "orm['mod.Tune']"}),
            'edit_votes_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_upload_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restart_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderators'", 'to': "orm['mod.Server']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderators'", 'to': "orm['auth.User']"})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'simpleblue'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mod.mod': {
            'Meta': {'ordering': "['upload_date', 'title']", 'object_name': 'Mod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mod_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'mod.option': {
            'Meta': {'ordering': "['id']", 'object_name': 'Option'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_options'", 'to': "orm['mod.Server']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'widget': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'mod.port': {
            'Meta': {'ordering': "['port']", 'object_name': 'Port'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'port': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'mod.server': {
            'Meta': {'ordering': "['owner', 'mod', 'port']", 'object_name': 'Server'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'servers'", 'to': "orm['mod.Mod']"}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'servers'", 'to': "orm['auth.User']"}),
            'pid': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'server'", 'unique': 'True', 'null': 'True', 'to': "orm['mod.Port']"})
        },
        'mod.tune': {
            'Meta': {'ordering': "['id']", 'object_name': 'Tune'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_tunes'", 'to': "orm['mod.Server']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['accounts']