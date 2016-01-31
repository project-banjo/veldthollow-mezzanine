from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.http import HttpResponse

from mezzanine.conf import settings
from mezzanine.core.sitemaps import DisplayableSitemap

from .views import (
    AuthorArticleListView,
    AuthorListView,
    BlogRouterView,
    HomepageView,
)


admin.autodiscover()
urlpatterns = i18n_patterns(
    "",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # ADD YOUR OWN URLPATTERNS HERE.
)
# Return a robots.txt that disallows all spiders when DEBUG is True.
if getattr(settings, 'DEBUG', False):
    urlpatterns += patterns(
        '',
        url('^robots.txt$',
            lambda r: HttpResponse('User-agent: *\nDisallow: /',
                                   content_type='text/plain')),
    )

urlpatterns += patterns(
    '',
    url(r'^jsi18n/(?P<packages>\S+?)/$',
        'django.views.i18n.javascript_catalog', {'domain': 'django'}),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'all': DisplayableSitemap}}),
    url(r'^', include('mezzanine.core.urls')),
    url(r'^', include('mezzanine.generic.urls')),
)

# Blog urls
urlpatterns += patterns(
    'mezzanine.blog.views',
    url("^$", "blog_post_list", name="blog_post_list"),
    url('^feed.(?P<format>(rss|atom))$', 'blog_post_feed',
        name='blog_post_feed'),
    url('^(?P<category>.*).(?P<format>(rss|atom))$', 'blog_post_feed',
        name='blog_post_feed_category'),
    url("^authors/$", AuthorListView.as_view(),
        name="blog_post_authors",
        kwargs={'template': 'blog/blog_post_list_authors.html'}),
    url("^authors/(?P<author>.*)/$", AuthorArticleListView.as_view(),
        name="blog_post_list_author",
        kwargs={'template': 'blog/blog_post_list_authors.html'}),
    url(r'^(?P<slug>.*)/$', BlogRouterView.as_view()),
    url('^(?P<category>.*)/$', 'blog_post_list',
        name='blog_post_list_category'),
    url('^(?P<slug>.*)/$', 'blog_post_detail',
        name='blog_post_detail'),
)

urlpatterns += patterns(
    '',
    url(r'^', include('mezzanine.pages.urls')),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
