from django.urls import path
from . import views

urlpatterns = [
    path('traveller_bookings/',views.traveller_bookings, name='traveller-bookings'),   
]