from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='booking/home.html'), name='home'),
    path('categories/', views.get_categories, name='categories_list'),
    path('categories/<int:category_id>', views.rooms_by_category, name='rooms_by_category'),
    path('categories/rooms/<int:room_id>', views.get_room, name='room_detail'),
    path('about/', TemplateView.as_view(template_name='booking/about.html'), name='about'),
]