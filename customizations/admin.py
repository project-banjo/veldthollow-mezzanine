# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from mezzanine.blog.admin import BlogCategoryAdmin, BlogPostAdmin
from mezzanine.core.admin import SitePermissionUserAdmin
from mezzanine.blog.models import BlogCategory, BlogPost

from .models import User, AuthorLink


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost

    def __init__(self, *args, **kwargs):
        super(BlogPostAdminForm, self).__init__(*args, **kwargs)
        self.fields['user'].choices = (
            [(u'', u'---------')] +
            [(u.pk, u) for u in User.objects.filter(
                is_author=True).iterator()])


class CustomBlogPostAdmin(BlogPostAdmin):
    form = BlogPostAdminForm
    fieldsets = (
        ('Login Details', {
            "fields": ["title", "user", "categories", "status",
                       ("publish_date", "expiry_date"), "featured_image",
                       "content", "allow_comments"],
        }),
        ("Other posts", {
            "fields": ("related_posts",),
        }),
        ("Meta data", {
            "fields": ["_meta_title", "slug",
                       ("description", "gen_description"),
                       "keywords", "in_sitemap"],
            "classes": ("collapse-closed",)
        }),
    )


admin.site.unregister(BlogPost)
admin.site.register(BlogPost, CustomBlogPostAdmin)


class CustomBlogCategoryAdmin(BlogCategoryAdmin):
    fieldsets = ((None, {"fields": ("title",)}),)


admin.site.unregister(BlogCategory)
admin.site.register(BlogCategory, CustomBlogCategoryAdmin)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class AuthorLinkAdmin(admin.TabularInline):
    model = AuthorLink


class CustomUserAdmin(SitePermissionUserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'profile_image'),
        }),
        ('Author Details', {
            'fields': ('is_author', 'short_bio', 'full_bio'),
        }),
        ('Login Info', {
            'fields': ('username', 'password'),
            "classes": ("collapse-closed",),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
            "classes": ("collapse-closed",),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            "classes": ("collapse-closed",),
        }))
    list_filter = SitePermissionUserAdmin.list_filter + ('is_author',)
    inlines = (AuthorLinkAdmin,)


admin.site.register(User, CustomUserAdmin)
