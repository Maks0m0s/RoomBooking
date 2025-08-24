from rest_framework import serializers
from booking.models import Room, Booking
from datetime import date

from booking.serializers import room_serializer

class BookingSerializer(serializers.ModelSerializer):
    room = room_serializer.RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'room', 'room_id', 'date', 'start_time', 'end_time']

    def validate(self, data):
        booking_date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        room = data.get('room')

        if booking_date and booking_date < date.today():
            raise serializers.ValidationError("Date cannot be in the past.")
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        if booking_date and start_time and end_time and room:
            conflicts = Booking.objects.filter(
                room=room,
                date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if conflicts.exists():
                raise serializers.ValidationError("This time slot is already booked.")

        return data
