from rest_framework import serializers
from booking.models import Room

from booking.serializers import (
    category_serializer,
    equipment_serializer
)


class RoomSerializer(serializers.ModelSerializer):
    category = category_serializer.CategorySerializer(read_only=True)
    equipment = equipment_serializer.EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            'id', 'name', 'rating', 'capacity', 'description',
            'photo', 'equipment', 'category'
        ]
