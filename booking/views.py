from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone


ROOMS = [
    {"id": 1, "name": "Big Meeting Room", "capacity": 20, "photo": "booking/img/meeting-room1.jpg", "price":80},
    {"id": 2, "name": "Personal Meeting Room", "capacity": 3, "photo": "booking/img/meeting-room2.jpeg", "price":30},
    {"id": 3, "name": "Team Meeting Room", "capacity": 6, "photo": "booking/img/meeting-room3.jpg", "price":50},
    {"id": 4, "name": "Relax-Play Room", "capacity": 8, "photo": "booking/img/meeting-room4.jpg", "price":60},
]

def get_rooms(request):
    return render(request, 'booking/rooms_list.html', {'rooms':ROOMS, 'now': timezone.now})

def get_room(request, room_id):
    room = next((room for room in ROOMS if room["id"] == room_id), None)
    if room:
        return render(request, 'booking/room_detail.html', {'room':room})
    else:
        return JsonResponse(
            {"error" : f"no room with id {room_id}."}
        )