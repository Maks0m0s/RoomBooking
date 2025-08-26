from booking.models import Booking
from booking.services import email_service

from rest_framework.response import Response
from rest_framework import status


def list_bookings(request):
    return Booking.objects.filter(user=request.user)

def create_booking(request, serializer):
    booking = serializer.save(user=request.user)
    email_service.send_booking_email(booking.user, serializer.validated_data)

def pay_booking(self, pk):
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response(
            {"detail": "Booking not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    booking.confirmed = True
    booking.save()

    serializer = self.get_serializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


