import os
import sys

sys.path.append('/var/www')
sys.path.append('/var/www/misindicadores/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "misindicadores.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
