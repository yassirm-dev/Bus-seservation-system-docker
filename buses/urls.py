from django.urls import path
from . import views
from .views import BusListView,BusDetailView,BusCreateView,BusUpdateView,UserDeleteView,BusDeleteView,UserListView,UserDetailView,UserUpdateView,UserCreateView

urlpatterns = [
    path('',views.home, name='buses-home'),
    path('available_buses/',views.available_buses, name='available-buses'),
    path('book_bus/',views.book_bus, name='book-bus'),
    path('booking-details/',views.booking_details, name='booking-details'),
    path('bus-report/',views.bus_report, name='bus-report'),
    path('buses',BusListView.as_view(), name='buses'),
    path('bus-detail/<int:pk>',BusDetailView.as_view(), name='bus-detail'),
    path('bus-update/<int:pk>',BusUpdateView.as_view(), name='bus-update'),
    path('bus-new',BusCreateView.as_view(), name='bus-new'),
    path('bus-detail/<int:pk>/delete',BusDeleteView.as_view(), name='bus-delete'),
    path('users',UserListView.as_view(), name='users'),
    path('after_login',views.after_login, name='after_login'),
    path('user-new',UserCreateView.as_view(), name='user-new'),
    path('user-detail/<int:pk>',UserDetailView.as_view(), name='user-detail'),
    path('user-detail/<int:pk>/delete',UserDeleteView.as_view(), name='user-delete'),
    path('user-update/<int:pk>',UserUpdateView.as_view(), name='user-update'),



    
]