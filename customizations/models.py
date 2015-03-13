# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from mezzanine.core.fields import FileField
from mezzanine.utils.models import upload_to


class User(AbstractUser):
    profile_image = FileField(
        upload_to=upload_to("customizations.User.profile_image", "profiles"),
        format="Image", max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'auth_user'
