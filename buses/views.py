from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView,DetailView, DeleteView, CreateView,UpdateView
from django.shortcuts import redirect, render
from .models import Bus,BusBooking,BookedSeats
from django.contrib.auth.models import User,Group
from .forms import BookBusForm
# Create your views here.
def home(request):
    return render(request,'buses/home.html')
def is_traveller(user):
    return user.groups.filter(name='TRAVELLER').exists()
    
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def after_login(request):
    if is_traveller(request.user):
        return redirect('buses-home')
    elif is_admin(request.user):
        return redirect('buses')
    else:
        return redirect('login')


def available_buses(request): 
    context={} 
    if request.method=='POST':
        source=request.POST.get('source')
        destination=request.POST.get('destination')
        date=request.POST.get('date')
        bus_list=Bus.objects.filter(source=source,destination=destination,date=date)
        if bus_list:
            return render(request,'buses/available_buses.html',{'buses':bus_list})
        else:
            error={
            'error':f"No buses available for that route/date!"
                }
            return render(request,'buses/available_buses.html',error)
    else:
        return render(request,'buses/available_buses.html')

@login_required
def book_bus(request,*args,**kwargs):
    if request.method =='POST':
        # getting form input names
        busId=request.POST["bus_id"]
        bus_creation=BookBusForm()
        
        bus_name_id=Bus.objects.get(id=busId)
        bus_seats=bus_name_id.no_of_seats
        busSeats=int(bus_seats)
        new_dict={val:0 for val in range(busSeats)}

        # if any seats were booked 
        if Bus.objects.filter(id=busId).exists():
            bus=Bus.objects.filter(id=busId).first()
            temp =  bus.bookedseats.seats
            seats=temp.split(',')
            seats.pop()
            i=0
            for i in range(len(seats)):
                    seat=seats[i]
                    temp=int(seat)
                    new_dict[temp]=1
            return render(request,'buses/book_bus.html',{'bus':bus_creation, 'busId':busId, 'seats':new_dict})
        else:
            return render(request,'buses/book_bus.html',{'bus':bus_creation, 'busId':busId, 'seats':new_dict})
   



            
            
    
              
    

@login_required
def booking_details(request,*args, **kwargs):
    if request.method == 'POST':
        bus_id=request.POST.get('bus_id')
        seat_nos=request.POST.get('seat_nos')
        seat_nos=seat_nos[:-1]
        no_of_seats=int(request.POST.get('count'))
        phone_no=request.POST.get('phone_number')
        picking_station=request.POST.get('pick_up_station')
        
        bus=Bus.objects.get(id=bus_id)
        if bus:
            if bus.remaining_seats > no_of_seats or bus.remaining_seats == int(no_of_seats) :
                username=request.user.username
                user_id=request.user.id
                email=request.user.email
                name=bus.name
                price=bus.price
                total_price=int(no_of_seats) * bus.price
                source=bus.source
                destination=bus.destination
                date=bus.date
                seats= seat_nos
                time=bus.departure_time
                bus_remaining_seats=bus.remaining_seats - int(no_of_seats)
               
                booked_seats=bus.bookedseats.seats
                booked_seats += ',' + seats
                BookedSeats.objects.update(seats=booked_seats, bus=bus)



                # try:
                #     booked_seats, created=BookedSeats.objects.get_or_create(id=bus_id)
                    
                #     if created:
                #         booked_seats.seats += seats
                #         booked_seats.save()
                #         print(booked_seats)
                # except:
                #         bus=Bus.objects.filter(id=bus_id).first()
                #         booked_seats=BookedSeats(seats=seat_nos, bus=bus)
                #         booked_seats.save()
                
             
                Bus.objects.filter(id=bus_id).update(remaining_seats=bus_remaining_seats)
                booking_details=BusBooking.objects.create(
                   user_name=username,
                    user_email=email,
                    user_id=user_id,
                    source=source,
                    destination=destination,
                    bus_name=name,
                    date=date,
                    price=total_price,
                    bus_id=bus_id,
                    time=time,
                    no_of_seats=no_of_seats,
                    seat_numbers=seat_nos,
                    phone_no=phone_no,
                    pick_up_station=picking_station
                )
                context={
                    'booking_details':booking_details,
                    'seat_price':price,
                    'bus':bus
                }
                print('============Booking ID==========', booking_details.id)     
                return render(request,'buses/booking_details.html',locals())
            else:
                context={
                    'error':f'Input {bus.remaining_seats} seat/s or less.'
                }    
                return render(request,'buses/book_bus.html', context)
        else:
            context={
              'error':'Please input a valid Bus ID'
            }    
            return render(request,'buses/book_bus.html', context)        
    else:
        return render(request,'buses/book_bus.html')

        

@staff_member_required
def bus_report(request):
    #  bus_report=BusBooking.objects.all()

    if request.method == 'POST':
        bus_name=request.POST.get('bus_name')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        search_results=Bus.objects.raw('select * from buses_bus where name="'+ bus_name+'" and  date between  "'+ start_date+'" and "'+ end_date+'" order by date asc')

        if search_results:
            buses=Bus.objects.all()
            context={
                    'buses':buses,
                    'bus_name':bus_name,
                    'end_date':end_date,
                    'start_date':start_date,
                    "search_results":search_results
                    }
            return render(request,'buses/bus_report.html',context)
        else:
            buses=Bus.objects.all()
            return render(request,'buses/bus_report.html',{"error":"Sorry! No reports to display",'buses':buses})
    else:
        buses=Bus.objects.all()
        return render(request,'buses/bus_report.html', {'buses':buses})

@method_decorator(staff_member_required, name='dispatch')
class BusListView(ListView):
    model = Bus
    context_object_name="bus_list"
    ordering=['name']

@method_decorator(staff_member_required, name='dispatch')
class BusDetailView(DetailView):
    model = Bus
  
@method_decorator(staff_member_required, name='dispatch')
class BusCreateView(CreateView):
    model = Bus  
    fields=['name','image','source','destination','no_of_seats',
    'remaining_seats','price','date','departure_time']
    
@method_decorator(staff_member_required, name='dispatch')
class BusUpdateView(UpdateView):
    model = Bus  
    fields=['name','image','source','destination','no_of_seats',
    'remaining_seats','price','date','departure_time']

@method_decorator(staff_member_required, name='dispatch')
class BusDeleteView(DeleteView):
    model = Bus
    success_url='/buses'


class UserListView(ListView):
    model=User
    template_name='buses/users_list.html'
    context_object_name='users_list'
    ordering='username'

class UserCreateView(CreateView):
    model=User
    fields=['username','email','first_name','last_name','password',]
    template_name='buses/user_form.html'

class UserUpdateView(UpdateView):
    model=User
    fields=['username','email','first_name','last_name','password',]
    template_name='buses/user_update.html'

class UserDetailView(DetailView):
    model=User
    template_name='buses/user_detail.html'


class UserDeleteView(DeleteView):
     model=User
     template_name='buses/user_confirm_delete.html'
     success_url='/users'