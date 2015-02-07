# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='value',
            field=models.CharField(max_length=1000, blank=True),
            preserve_default=True,
        ),
    ]
