from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from booking.models import Rating, Room
from booking.serializers.rating_serializer import RatingSerializer
from booking.services import rating_service


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]  # default for all actions

    @action(detail=False, methods=['post'], url_path='rate-room', permission_classes=[permissions.IsAuthenticated])
    def rate_room(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = rating_service.rate_room(serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='room/(?P<room_id>[^/.]+)',
            permission_classes=[permissions.AllowAny])
    def get_room_ratings(self, request, room_id=None):
        room = get_object_or_404(Room, id=room_id)
        ratings = Rating.objects.filter(booking__room=room)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)