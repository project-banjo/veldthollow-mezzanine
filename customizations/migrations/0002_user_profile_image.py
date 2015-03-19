# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import customizations.fields


class Migration(migrations.Migration):

    dependencies = [
        ('customizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=customizations.fields.FileBrowseImageField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
