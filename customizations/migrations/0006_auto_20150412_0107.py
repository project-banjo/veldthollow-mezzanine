# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customizations', '0005_auto_20150403_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='short_bio',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
