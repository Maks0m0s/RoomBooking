from rest_framework import viewsets, permissions, status

from booking.serializers import booking_serializer
from booking.services import booking_service

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = booking_serializer.BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return booking_service.list_bookings(self.request)

    def perform_create(self, serializer):
        booking_service.create_booking(self.request, serializer)
