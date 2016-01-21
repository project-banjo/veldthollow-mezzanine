from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.conf import settings
from mezzanine.core.views import direct_to_template

from customizations.views import HomepageView


admin.autodiscover()
urlpatterns = i18n_patterns(
    "",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    url(r"^$", direct_to_template, {"template": "splash.html"}, name="home"),
    # url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^ckeditor/', include('ckeditor.urls')),

    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    (r"^", include("customizations.urls")),

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
