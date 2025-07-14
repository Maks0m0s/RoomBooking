from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Room, Category

def get_categories(request):
    categories = Category.objects.all()
    return render(request, 'booking/categories_list.html', {'categories':categories})

def rooms_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    rooms = category.rooms.all()
    return render(request, 'booking/rooms_list.html', {'rooms':rooms, 'category':category})

def get_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if room:
        return render(request, 'booking/room_detail.html', {'room':room})
    else:
        return JsonResponse(
            {"error" : f"no room with id {room_id}."}
        )