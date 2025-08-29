import os
from dotenv import load_dotenv

load_dotenv()  # <-- load environment variables first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

from celery import Celery
from celery.schedules import crontab

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-bookings-every-5-minutes": {
        "task": "booking.tasks.check_bookings",
        "schedule": crontab(minute="*/5"),
    },
}