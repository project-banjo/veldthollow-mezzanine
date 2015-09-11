from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _
from mezzanine.blog.admin import BlogCategoryAdmin, BlogPostAdmin
from mezzanine.core.admin import SitePermissionUserAdmin
from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.pages.admin import PageAdmin

from .models import User, AuthorLink, Homepage


class CustomBlogPostAdmin(BlogPostAdmin):
    fieldsets = (
        ('Login Details', {
            "fields": ["title", "user", "categories", "status",
                       ("publish_date", "expiry_date"), "featured_image",
                       "content", "blurb", "featured", "allow_comments"],
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

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.base_fields['user'].choices = (
            [(u'', u'---------')] +
            [(u.pk, u) for u in User.objects.filter(
                is_author=True).iterator()])
        return form


admin.site.unregister(BlogPost)
admin.site.register(BlogPost, CustomBlogPostAdmin)


class CustomBlogCategoryAdmin(BlogCategoryAdmin):
    fieldsets = ((None, {"fields": ("slug", "title")}),)


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
            'fields': ('first_name', 'last_name', 'email', 'profile_image',
                       'contact_email'),
        }),
        ('Author Details', {
            'fields': ('author_status', 'short_bio', 'full_bio'),
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
    list_filter = SitePermissionUserAdmin.list_filter + ('author_status',)
    inlines = (AuthorLinkAdmin,)


class HomepageAdmin(PageAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'featured_category', 'featured_author')}),
        (_('Meta data'), {
            'fields': ('_meta_title', 'slug'),
            'classes': ('collapse-closed',)})
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        return [u for u in urls
                if not u.name.endswith('_add') and
                not u.name.endswith('_delete')]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Homepage, HomepageAdmin)
