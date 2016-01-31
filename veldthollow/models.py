from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from mezzanine.blog.models import BlogCategory
from mezzanine.core.fields import RichTextField
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to

from .fields import FileBrowseImageField


class User(AbstractUser):
    contact_email = models.EmailField(blank=True)
    NONAUTHOR = None
    GUEST = 5
    STAFF = 10
    AUTHOR_STATUS_CHOICES = (
        (NONAUTHOR, 'No'),
        (GUEST, 'Guest'),
        (STAFF, 'Staff'),
    )
    author_status = models.IntegerField(
        'Author Status', choices=AUTHOR_STATUS_CHOICES, default=None, null=True)
    short_bio = models.TextField(blank=True)
    full_bio = RichTextField(blank=True)
    profile_image = FileBrowseImageField(
        file_obj_name='profile_image_file',
        upload_to=upload_to("veldthollow.User.profile_image", "profiles"),
        format="Image", max_length=255, null=True, blank=True)
    profile_thumbnail = ImageSpecField(
        source='profile_image_file', processors=[SmartResize(150, 150)],
        format='PNG')

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'auth_user'
        ordering = ('first_name', 'last_name')

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


class Homepage(Page):
    featured_category = models.ForeignKey(
        BlogCategory, blank=True, null=True)
    featured_author = models.ForeignKey(User, blank=True, null=True)
