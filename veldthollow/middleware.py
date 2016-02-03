import re

from django.views.generic.base import TemplateView, RedirectView
from mezzanine.conf import register_setting, settings

register_setting(
    name='SITE_MAINTENANCE',
    label='Place site in maintenence mode',
    editable=True,
    choices=(('live', 'Live'), ('splash', 'Splash'), ('maintenance', 'Maintenance')),
    default='live',
)


class MaintenanceMiddleware:
    def process_view(self, request, view, *args, **kwargs):
        if settings.SITE_MAINTENANCE == 'live':
            return None

        for url in settings.SITE_MAINTENANCE_ACCESSIBLE:
            if re.match(url, request.path):
                return None

        if settings.SITE_MAINTENANCE == 'splash':
            if request.path == '/':
                return TemplateView.as_view(template_name='splash/index.html')(request)
            return RedirectView.as_view(url='/')(request)

        elif settings.SITE_MAINTENANCE == 'maintenance':
            return MaintenanceView.as_view(template_name='maintenance/index.html')(request)


class MaintenanceView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=503)
