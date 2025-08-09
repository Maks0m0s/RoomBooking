from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Room, Category, Booking
from .forms import BookingForm


@login_required
def make_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, initial={'room': room})
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            messages.success(request, "Booking completed successfully!")
            return redirect('booking_success')
    else:
        form = BookingForm(initial={'room': room})

    return render(request, 'booking/make_booking.html', {'room': room, 'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration was successful. Now log in into the system.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'booking/register.html', {'form':form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Booking deleted successfully.")

    # Redirect to the page the request came from
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('my_bookings')  # fallback


def get_categories(request):
    categories = Category.objects.all()
    return render(request, 'booking/categories_list.html', {'categories': categories})


def rooms_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    rooms = category.rooms.all()
    return render(request, 'booking/rooms_list.html', {'rooms': rooms, 'category': category})


def get_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'booking/room_detail.html', {'room': room})

def home(request):
    today = timezone.now().date()
    bookings = []

    if request.user.is_authenticated:
        bookings = Booking.objects.filter(
            user=request.user,
            date=today
        )

    return render(request, 'booking/home.html', {'today': today, 'bookings': bookings})