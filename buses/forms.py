from django import forms
from .models import BookBus


class BookBusForm(forms.ModelForm):
    class Meta:
        model=BookBus
        fields=[
            'phone_number',
            'pick_up_station',
            ]





# class BookedSeatsForm(forms.Form):
#     booked_seats = forms.CharField()
