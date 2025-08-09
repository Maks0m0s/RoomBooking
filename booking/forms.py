from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        room = self.initial.get('room')
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Start time has to be less then the time of end.")
        if date and start_time and end_time and room:
            conflicts = Booking.objects.filter(
                room=room,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time)

            if conflicts.exists():
                raise forms.ValidationError("This room was already reserved for this time.")

        return cleaned_data