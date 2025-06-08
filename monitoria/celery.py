import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoria.settings')

app = Celery('monitoria')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app = Celery('monitoria')
app.conf.broker_url = settings.CELERY_BROKER_URL
