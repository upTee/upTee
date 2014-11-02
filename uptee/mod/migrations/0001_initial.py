# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableRconCommand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100, blank=True)),
                ('info', models.CharField(max_length=300, blank=True)),
                ('download_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mod_file', models.FileField(help_text=b'Should be .zip or .tar', upload_to=b'uploads')),
                ('upload_date', models.DateTimeField(auto_now=True, verbose_name=b'Upload date')),
                ('title', models.CharField(max_length=100)),
                ('mimetype', models.CharField(max_length=100, editable=False)),
            ],
            options={
                'ordering': ['upload_date', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=500, blank=True)),
                ('widget', models.IntegerField(default=1, choices=[(1, b'text'), (2, b'textarea'), (3, b'password'), (4, b'checkbox'), (5, b'select')])),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port', models.IntegerField(unique=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['port'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RconCommand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=500, blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.IntegerField(unique=True, null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('online', models.BooleanField(default=False)),
                ('set_online_at', models.DateTimeField(auto_now=True)),
                ('locked', models.BooleanField(default=False)),
                ('automatic_restart', models.BooleanField(default=False)),
                ('map_download_allowed', models.BooleanField(default=True)),
                ('description', models.TextField(help_text=b'You may use markdown', blank=True)),
                ('description_html', models.TextField(blank=True)),
                ('server_info', picklefield.fields.PickledObjectField(null=True, editable=False, blank=True)),
                ('random_key', models.CharField(max_length=24, unique=True, null=True)),
                ('mod', models.ForeignKey(related_name='servers', to='mod.Mod')),
                ('owner', models.ForeignKey(related_name='servers', to=settings.AUTH_USER_MODEL)),
                ('port', models.OneToOneField(related_name='server', null=True, blank=True, to='mod.Port')),
            ],
            options={
                'ordering': ['owner', 'mod', 'port'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('task_type', models.IntegerField(default=3, choices=[(1, b'start'), (2, b'stop'), (3, b'restart')])),
                ('date', models.DateTimeField()),
                ('repeat', models.IntegerField(default=0, help_text=b'minutes for repeating the task (0 is no repeat)<br>day=1440, week=10080')),
                ('status', models.IntegerField(default=1, choices=[(1, b'active'), (2, b'done'), (3, b'error')])),
                ('task_id', models.CharField(max_length=100, null=True, blank=True)),
                ('server', models.ForeignKey(related_name='events', to='mod.Server', null=True)),
            ],
            options={
                'ordering': ['date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tune',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('server', models.ForeignKey(related_name='config_tunes', to='mod.Server')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('server', models.ForeignKey(related_name='config_votes', to='mod.Server')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rconcommand',
            name='server',
            field=models.ForeignKey(related_name='config_rconcommands', to='mod.Server'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='option',
            name='server',
            field=models.ForeignKey(related_name='config_options', to='mod.Server'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='map',
            name='server',
            field=models.ForeignKey(related_name='maps', to='mod.Server'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availablerconcommand',
            name='server',
            field=models.ForeignKey(related_name='config_available_rconcommands', to='mod.Server'),
            preserve_default=True,
        ),
    ]
