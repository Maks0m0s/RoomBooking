from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def send_registration_email(user):
    subject = "Welcome to RoomBooking!"
    message = f"""
    Hi {user.first_name or user.username},

    Your account has been successfully created!

    Username: {user.username}
    Email: {user.email}

    Thank you for registering.
    """
    recipient = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=False,
    )

def send_booking_email(user, validated_data):
    subject = f"Booking of : {validated_data['room']}"
    message = f"""
        Hi {user.first_name or user.username},

        Your booking has been successfully created!

        Room: {validated_data['room']}
        Date: {validated_data['date']}
        Start time: {validated_data['start_time']}
        End time: {validated_data['end_time']}

        Thank you for booking.
        """
    recipient = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=False,
    )