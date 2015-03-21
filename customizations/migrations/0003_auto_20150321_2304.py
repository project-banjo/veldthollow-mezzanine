# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('customizations', '0002_user_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_type', models.CharField(max_length=25, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('web', 'Web'), ('pinterest', 'Pinterest')])),
                ('url', models.URLField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='full_bio',
            field=mezzanine.core.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='short_bio',
            field=mezzanine.core.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
    ]
