from os import write

from rest_framework import serializers
from .models import Room, Booking, Category, Equipment
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name']

class RoomSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            'id', 'name', 'rating', 'capacity', 'description',
            'photo', 'equipment', 'category', 'reserved'
        ]

class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
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

class JWTLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Username or password is invalid.")

        refresh_token = RefreshToken.for_user(user)
        return {
            "user":
                {
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                },
            "tokens":{
                "refresh":str(refresh_token),
                "access":str(refresh_token.access_token),
            }
        }

class JWTRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

    def validate_email(self, email):
        if not email or "@" not in email:
            raise serializers.ValidationError("Invalid email.")
        return email

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        refresh_token = RefreshToken.for_user(user)

        return {
            "user":
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            "tokens": {
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
            }
        }

class JWTRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh = data.get('refresh')
        if not refresh:
            raise serializers.ValidationError("Refresh token is required.")

        try:
            refresh = RefreshToken(refresh)
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token.")

        return {
            'tokens':{
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            }
        }