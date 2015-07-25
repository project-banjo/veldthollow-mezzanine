# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='user',
            field=models.ForeignKey(related_name='blogposts', verbose_name='Author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
    ]
