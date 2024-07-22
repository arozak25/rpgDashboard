from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpgDashboard.settings')

app = Celery('celery_app_dashboard',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0'
             )

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
