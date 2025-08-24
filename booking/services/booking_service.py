from booking.models import Booking
from booking.services import email_service

def list_bookings(request):
    return Booking.objects.filter(user=request.user)

def create_booking(request, serializer):
    booking = serializer.save(user=request.user)
    email_service.send_booking_email(booking.user, serializer.validated_data)