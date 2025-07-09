from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='booking/home.html'), name='home'),
    path('rooms/', views.get_rooms, name='rooms_list'),
    path('rooms/<int:room_id>', views.get_room, name='room_detail'),
    path('about/', TemplateView.as_view(template_name='booking/about.html'), name='about'),
]