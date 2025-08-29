from os.path import basename

from rest_framework.routers import DefaultRouter
from django.urls import path, include

from booking.api import (
    auth_views,
    bookings_views,
    categories_views,
    home_views,
    rooms_views,
    rating_views,
    openai_views
)

from booking.views import LangChainViewSet

router = DefaultRouter()
router.register(r'rooms', rooms_views.RoomViewSet, basename='rooms')
router.register(r'bookings', bookings_views.BookingViewSet, basename='bookings')
router.register(r'categories', categories_views.CategoryViewSet, basename='categories')
router.register(r'home', home_views.HomeViewSet, basename='home')
router.register(r'auth', auth_views.AuthViewSet, basename='auth')
router.register(r'rating', rating_views.RatingViewSet, basename='rating')
router.register(r'openai', openai_views.OpenAIViewSet, basename='openai')
router.register(r'langchain', LangChainViewSet, basename='langchain')

urlpatterns = [
    path('', include(router.urls)),
]