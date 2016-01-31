# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('veldthollow', '0004_populate_initial_pages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('first_name', 'last_name')},
        ),
        migrations.AlterField(
            model_name='user',
            name='author_status',
            field=models.IntegerField(default=None, verbose_name='Author Status', null=True, choices=[(None, 'No'), (5, 'Guest'), (10, 'Staff')]),
        ),
    ]
