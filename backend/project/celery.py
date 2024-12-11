import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Using Redis as the broker
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'
app.conf.broker_connection_retry_on_startup = True

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()