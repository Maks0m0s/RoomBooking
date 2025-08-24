from rest_framework import viewsets, permissions
from rest_framework.response import Response

from booking.serializers import booking_serializer
from booking.services import home_service


class HomeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        bookings, today = home_service.bookings_for_today(request)
        serializer = booking_serializer.BookingSerializer(bookings, many=True)
        return Response({"today": today, "bookings": serializer.data})