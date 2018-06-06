import os
import sys

from celery import Celery
from django.conf import settings

sys.path.append('..')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('auth_core')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
