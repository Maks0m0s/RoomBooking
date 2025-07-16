from email.policy import default
from tabnanny import check

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        blank = True,
        null = True
    )
    capacity = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to='room_photos/', blank=True, null=True)
    equipment = models.ManyToManyField(Equipment, related_name='rooms')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rooms')
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.room.name} was booked by {self.user.first_name} {self.user.last_name}. From {self.start_time} to {self.end_time} | {self.date}"