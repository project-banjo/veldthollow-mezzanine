# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('veldthollow', '0002_auto_20150830_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_author',
        ),
        migrations.AddField(
            model_name='user',
            name='author_status',
            field=models.IntegerField(default=False, null=True, verbose_name='Author Status', choices=[(None, 'No'), (5, 'Guest'), (10, 'Staff')]),
        ),
    ]
