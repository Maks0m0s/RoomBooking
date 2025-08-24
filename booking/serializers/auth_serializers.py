from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.models import User


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