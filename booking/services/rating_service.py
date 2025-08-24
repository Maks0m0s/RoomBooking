from booking.models import Room, Booking, Rating


def rate_room(validated_data):
    booking = validated_data['booking']   # Now we pass booking object from serializer
    stars = validated_data['stars']
    comment = validated_data.get('comment', 'Nothing')

    # Create rating linked to booking
    rating = Rating.objects.create(
        stars=stars,
        comment=comment,
        booking=booking
    )

    # Link rating to the room (ManyToMany)
    room = booking.room
    room.rating.add(rating)
    room.save()

    return {
        'booking_data': {
            'room_id': room.id,
            'room': room.name,
            'booking_id': booking.id,
        },
        'rating': {
            'id': rating.id,
            'stars': stars,
            'comment': comment,
        }
    }