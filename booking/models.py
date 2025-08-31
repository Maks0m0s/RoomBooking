from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def current_time():
    return timezone.now().time()


class Booking(models.Model):
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    confirmed = models.BooleanField(default=False)
    reservation_time = models.TimeField(default=current_time)

    def __str__(self):
        return f"{self.room.name} was booked by {self.user.first_name} {self.user.last_name}. From {self.start_time} to {self.end_time} | {self.date}"


class Rating(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        related_name="ratings",
        null=True,  # ✅ allow null
        blank=True  # optional, for forms/admin
    )
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1,
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'"{self.comment}". {self.stars}/5'


class Room(models.Model):
    name = models.CharField(max_length=100)
    rating = models.ManyToManyField("Rating", blank=True)   # ✅ use string ref, blank=True only
    capacity = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='room_photos/', blank=True, null=True)
    equipment = models.ManyToManyField(Equipment, related_name='rooms')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return self.name