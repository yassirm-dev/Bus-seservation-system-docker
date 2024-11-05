from django.contrib import admin
from .models import Bus,BusBooking,BookedSeats
# Register your models here.
admin.site.register(Bus)
admin.site.register(BusBooking)
admin.site.register(BookedSeats)
