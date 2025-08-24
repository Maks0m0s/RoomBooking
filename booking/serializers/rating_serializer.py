from rest_framework import serializers
from booking.models import Booking, Rating


class RatingSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(),
        source='booking',
        write_only=True
    )
    booking = serializers.StringRelatedField(read_only=True)  # to show booking info in responses

    class Meta:
        model = Rating
        fields = ['id', 'booking_id', 'booking', 'stars', 'comment']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None
        booking = data.get('booking')

        if not booking:
            raise serializers.ValidationError("Booking is required.")

        if booking.user != user:
            raise serializers.ValidationError("You can only rate your own bookings.")

        return data