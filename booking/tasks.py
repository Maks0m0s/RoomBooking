from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Booking

@shared_task
def check_bookings():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    expired_bookings = Booking.objects.filter(
        confirmed=False,
        reservation_time__lte=one_hour_ago
    )
    for booking in expired_bookings:
        booking.delete()