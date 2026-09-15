import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','DIVERSE_MIND_LIBRARY.settings')
application = get_wsgi_application()
