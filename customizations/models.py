# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from mezzanine.core.fields import RichTextField
from mezzanine.utils.models import upload_to

from .fields import FileBrowseImageField


class User(AbstractUser):
    short_bio = RichTextField(blank=True)
    full_bio = RichTextField(blank=True)
    profile_image = FileBrowseImageField(
        file_obj_name='profile_image_file',
        upload_to=upload_to("customizations.User.profile_image", "profiles"),
        format="Image", max_length=255, null=True, blank=True)
    profile_thumbnail = ImageSpecField(
        source='profile_image_file', processors=[SmartResize(150, 150)],
        format='PNG')

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'auth_user'


class AuthorLink(models.Model):
    user = models.ForeignKey(User)
    LINK_TYPE_CHOICES = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('web', 'Web'),
        ('pinterest', 'Pinterest'),
    )
    link_type = models.CharField(max_length=25, choices=LINK_TYPE_CHOICES)
    url = models.URLField()
