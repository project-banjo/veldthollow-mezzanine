# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('blog', '0003_auto_20150725_1609'),
        ('customizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
            ],
            options={
                'ordering': ('_order',),
            },
            bases=('pages.page',),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_author',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_category',
            field=models.ForeignKey(blank=True, to='blog.BlogCategory', null=True),
        ),
    ]
