from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from booking.services import auth_service

from booking.serializers.auth_serializers import (
    JWTLoginSerializer,
    JWTRegistrationSerializer,
    JWTRefreshSerializer
)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path='login')
    def login(self, request):
        serializer = JWTLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path='register')
    def register(self, request):
        serializer = JWTRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = auth_service.register(serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path='refresh_token')
    def refresh(self, request):
        serializer = JWTRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)