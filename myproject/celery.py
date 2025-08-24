from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-bookings-every-5-minutes": {
        "task": "booking.tasks.check_bookings",
        "schedule": crontab(minute="*/5"),  # every 5 minutes
    },
}