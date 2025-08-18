from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RoomViewSet, BookingViewSet, CategoryViewSet, HomeViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'home', HomeViewSet, basename='home')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]