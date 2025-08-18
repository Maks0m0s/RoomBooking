from crypt import methods
from http.client import responses

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Room, Booking, Category
from .serializers import RoomSerializer, BookingSerializer, CategorySerializer, JWTLoginSerializer, JWTRefreshSerializer, JWTRegistrationSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], url_path='category/(?P<category_id>[^/.]+)')
    def list_by_category(self, request, category_id=None):
        category = get_object_or_404(Category, id=category_id)
        rooms = category.rooms.all()
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class HomeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        today = timezone.now().date()
        bookings = Booking.objects.filter(user=request.user, date=today)
        serializer = BookingSerializer(bookings, many=True)
        return Response({"today": today, "bookings": serializer.data})

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
        return Response(serializer.save(), status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path='refresh_token')
    def refresh(self, request):
        serializer = JWTRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)