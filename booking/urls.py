from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.get_categories, name='categories_list'),
    path('categories/<int:category_id>', views.rooms_by_category, name='rooms_by_category'),
    path('categories/rooms/<int:room_id>', views.get_room, name='room_detail'),
    path('about/', TemplateView.as_view(template_name='booking/about.html'), name='about'),

    path('categories/rooms/booking/<int:room_id>', views.make_booking, name='make_booking'),
    path('categories/rooms/booking/done/', TemplateView.as_view(template_name='booking/success_booking.html'), name='booking_success'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('my_booking/delete/<int:booking_id>', views.delete_booking, name='delete_booking'),

    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
]