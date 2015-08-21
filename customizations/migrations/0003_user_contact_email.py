# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customizations', '0002_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
