# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='blurb',
            field=models.CharField(default='Feed me.', max_length=250, verbose_name='Blurb'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='featured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
