from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from booking.models import Room, Category
from booking.serializers import room_serializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = room_serializer.RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], url_path='category/(?P<category_id>[^/.]+)')
    def list_by_category(self, request, category_id=None):
        category = get_object_or_404(Category, id=category_id)
        rooms = category.rooms.all()
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)