from __future__ import (
    absolute_import,
    unicode_literals,
)

import os

from celery import Celery
from celery.schedules import crontab
from decouple import config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("SETTINGS_FILE"))

app = Celery(
    "crm",
    broker_url=config("BROKER_URL"),
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.update(
    CELERY_IMPORTS=["app.tasks"],
)
app.conf.beat_schedule = {
    "send-show-reminders": {
        "task": "app.tasks.send_reminders",
        "schedule": crontab(hour=17, minute=15),
    },
    "send-movie-digital-notifications": {
        "task": "app.tasks.check_for_digital_task_via_api",
        "schedule": crontab(hour=13, minute=30),
    },
}
