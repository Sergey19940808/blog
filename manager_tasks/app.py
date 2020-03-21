import os
import django

from celery import Celery
from core.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

app = Celery('blog', broker=CELERY_BROKER_URL)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(['manager_tasks.tasks'])