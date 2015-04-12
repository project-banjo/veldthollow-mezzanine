# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from mezzanine.blog.models import BlogCategory
from mezzanine.core.fields import RichTextField
from mezzanine.utils.models import upload_to

from .fields import FileBrowseImageField


@python_2_unicode_compatible
class User(AbstractUser):
    is_author = models.BooleanField('author status', default=False)
    short_bio = models.TextField(blank=True)
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

    def __str__(self):
        return self.get_full_name() or self.username


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


class Homepage(models.Model):
    featured_category = models.ForeignKey(
        BlogCategory, blank=True, null=True)
    featured_author = models.ForeignKey(User, blank=True, null=True)
