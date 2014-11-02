# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mod', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=32, unique=True, null=True)),
                ('user', models.OneToOneField(related_name='activation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('restart_allowed', models.BooleanField(default=False)),
                ('edit_automatic_restart_allowed', models.BooleanField(default=False)),
                ('edit_map_download_allowed', models.BooleanField(default=False)),
                ('edit_votes_allowed', models.BooleanField(default=False)),
                ('map_upload_allowed', models.BooleanField(default=False)),
                ('console_allowed', models.BooleanField(default=False)),
                ('edit_rcon_commands_allowed', models.BooleanField(default=False)),
                ('allowed_options', models.ManyToManyField(related_name='moderators', to='mod.Option')),
                ('allowed_tunings', models.ManyToManyField(related_name='moderators', to='mod.Tune')),
                ('server', models.ForeignKey(related_name='moderators', to='mod.Server')),
                ('user', models.ForeignKey(related_name='moderators', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template', models.CharField(default=b'simpleflat', max_length=100)),
                ('gender', models.IntegerField(default=1, choices=[(1, b'Not saying'), (2, b'Male'), (3, b'Female')])),
                ('publish_gender', models.BooleanField(default=False)),
                ('birthday', models.DateField(help_text=b'only your age will be shown (e.g. 15-20) | (YYYY-MM-DD)', null=True, blank=True)),
                ('publish_birthday', models.BooleanField(default=False)),
                ('ingame_name', models.CharField(default=b'', max_length=20, null=True, blank=True)),
                ('publish_ingame_name', models.BooleanField(default=False)),
                ('fav_map', models.CharField(default=b'', max_length=50, null=True, verbose_name=b'favorite map', blank=True)),
                ('publish_fav_map', models.BooleanField(default=False)),
                ('fav_mod', models.CharField(default=b'', max_length=20, null=True, verbose_name=b'favorite mod', blank=True)),
                ('publish_fav_mod', models.BooleanField(default=False)),
                ('contact', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('publish_contact', models.BooleanField(default=False)),
                ('website', models.URLField(default=b'', null=True, blank=True)),
                ('publish_website', models.BooleanField(default=False)),
                ('publish_name', models.BooleanField(default=False)),
                ('allowed_mods', models.ManyToManyField(related_name='users', to='mod.Mod', blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
