# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mod'
        db.create_table('mod_mod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mod_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mimetype', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('mod', ['Mod'])

        # Adding model 'Port'
        db.create_table('mod_port', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('port', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mod', ['Port'])

        # Adding model 'Server'
        db.create_table('mod_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.OneToOneField')(related_name='server', unique=True, to=orm['auth.User'])),
            ('mod', self.gf('django.db.models.fields.related.ForeignKey')(related_name='servers', to=orm['mod.Mod'])),
            ('pid', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('port', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='server', null=True, to=orm['mod.Port'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mod', ['Server'])

        # Adding model 'Option'
        db.create_table('mod_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_options', to=orm['mod.Server'])),
            ('command', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('mod', ['Option'])

        # Adding model 'Tune'
        db.create_table('mod_tune', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_tunes', to=orm['mod.Server'])),
            ('command', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('mod', ['Tune'])

        # Adding model 'Vote'
        db.create_table('mod_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(related_name='config_votes', to=orm['mod.Server'])),
            ('command', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('mod', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'Mod'
        db.delete_table('mod_mod')

        # Deleting model 'Port'
        db.delete_table('mod_port')

        # Deleting model 'Server'
        db.delete_table('mod_server')

        # Deleting model 'Option'
        db.delete_table('mod_option')

        # Deleting model 'Tune'
        db.delete_table('mod_tune')

        # Deleting model 'Vote'
        db.delete_table('mod_vote')


    models = {
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
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'mod.port': {
            'Meta': {'ordering': "['port']", 'object_name': 'Port'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'port': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'mod.server': {
            'Meta': {'object_name': 'Server'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mod': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'servers'", 'to': "orm['mod.Mod']"}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'server'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'pid': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'server'", 'null': 'True', 'to': "orm['mod.Port']"})
        },
        'mod.tune': {
            'Meta': {'ordering': "['id']", 'object_name': 'Tune'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_tunes'", 'to': "orm['mod.Server']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'mod.vote': {
            'Meta': {'ordering': "['id']", 'object_name': 'Vote'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'config_votes'", 'to': "orm['mod.Server']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mod']