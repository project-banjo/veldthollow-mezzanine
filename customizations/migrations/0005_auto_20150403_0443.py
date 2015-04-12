# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('customizations', '0004_user_is_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured_author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('featured_category', models.ForeignKey(blank=True, to='blog.BlogCategory', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_author',
            field=models.BooleanField(default=False, verbose_name='author status'),
            preserve_default=True,
        ),
    ]
