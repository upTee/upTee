# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskEvent'
        db.create_table(u'mod_taskevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', null=True, to=orm['mod.Server'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('task_type', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('repeat', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'mod', ['TaskEvent'])


    def backwards(self, orm):
        # Deleting model 'TaskEvent'
        db.delete_table(u'mod_taskevent')


    models = {
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
        u'mod.availablerconcommand': {
            'Meta': {'ordering': "['id']", 'object_name': 'AvailableRconCommand'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_available_rconcommands'", 'to': u"orm['mod.Server']"})
        },
        u'mod.map': {
            'Meta': {'ordering': "['name']", 'object_name': 'Map'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maps'", 'to': u"orm['mod.Server']"})
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
        u'mod.rconcommand': {
            'Meta': {'ordering': "['id']", 'object_name': 'RconCommand'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_rconcommands'", 'to': u"orm['mod.Server']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
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
        u'mod.taskevent': {
            'Meta': {'object_name': 'TaskEvent'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repeat': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'null': 'True', 'to': u"orm['mod.Server']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'task_type': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        },
        u'mod.tune': {
            'Meta': {'ordering': "['id']", 'object_name': 'Tune'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_tunes'", 'to': u"orm['mod.Server']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'mod.vote': {
            'Meta': {'ordering': "['id']", 'object_name': 'Vote'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_votes'", 'to': u"orm['mod.Server']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mod']