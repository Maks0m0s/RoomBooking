from django.utils import timezone
from booking.models import Booking

def bookings_for_today(request):
    today = timezone.now().date()
    bookings = Booking.objects.filter(user=request.user, date=today)
    return bookings, today