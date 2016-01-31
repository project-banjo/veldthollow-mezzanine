import os

from django.core.wsgi import get_wsgi_application
from mezzanine.utils.conf import real_project_name

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "%s.settings.local" % real_project_name("veldthollow"))

application = get_wsgi_application()
