import sys
import os


path = os.path.expanduser('~/Desktop/Tienda-PY')
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
