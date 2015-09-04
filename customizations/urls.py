# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.http import HttpResponse

from customizations.views import (
    AuthorArticleListView,
    AuthorListView,
    BlogRouterView,
)
from mezzanine.conf import settings
from mezzanine.core.sitemaps import DisplayableSitemap

urlpatterns = []

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
