from django.contrib import admin
from .models import Room, Booking, Category, Equipment, Rating

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(Rating)