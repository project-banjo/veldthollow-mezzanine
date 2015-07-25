# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150725_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='blurb',
            field=models.CharField(max_length=250, verbose_name='Blurb', blank=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='featured',
            field=models.BooleanField(default=False, help_text='Will appear in the Featured Stories section of the homepage.'),
        ),
    ]
