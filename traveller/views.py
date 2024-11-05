from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm
from buses.models import BusBooking
# Create your views here.
def register(request):
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            new_traveller=form.save()
            traveller=Group.objects.get(name='TRAVELLER')
            new_traveller.groups.add(traveller)
            # username=form.cleaned_data.get('username')
            # messages.error(request,f'Dear {username}, your account has been created! Please Log in.')
            return redirect('login')

    else:
        form=UserRegistrationForm()
    return render(request, 'traveller/register.html', {'form':form})

@login_required
def profile(request):
    return render(request,'traveller/profile.html')           



@login_required
def traveller_bookings(request):
    userId=request.user.id
    traveller_bookings_info=BusBooking.objects.filter(user_id=userId)
    if traveller_bookings_info:
        context={
            'traveller_bookings_info':traveller_bookings_info
        }
        return render(request, 'traveller/traveller_bookings.html',context)
    
    else:
        
        return render(request, 'traveller/traveller_bookings.html',{
                   'error' :f'You have no booking records'
        })
