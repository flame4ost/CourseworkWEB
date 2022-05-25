from django.views.generic import list,detail,edit,CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from database.models import * 
from datetime import datetime

from .forms import *
import calendar

# Create your views here.
def Last_Day_Month(today):
    
    today = datetime.now().date().day
    last_day_month = calendar.monthcalendar(datetime.now().year ,datetime.now().month)
    last_day_month = last_day_month[-1][-1]

    if today == last_day_month:
        obj = Car.objects.all() 

        for o in range(0,len(obj)): 

            month = datetime.now().month 
            year = datetime.now().year                
            tickets =  Parking_Ticket.objects.filter(license_plate=obj[o]).filter(checkin_time__month=month).all()            
            total = 0
            for t in tickets:                        
                total  += t.total_due 

            message = 'Created successufully' 
    else:
        message = 'Today is not the last day of the month'  

class TicketsList(list.ListView):
    model         = Parking_Ticket    
    template_name = 'tickets.html'
    today = datetime.now().date().day
    Last_Day_Month(today)

             
def TicketCreate(request):    
    if request.method == 'POST':
        license_plate = request.POST['license_plate'] 
        checkin_time = datetime.now() 
        Parking_Ticket.objects.create(license_plate = license_plate,checkin_time = checkin_time)   
        return redirect('ticketslist') 
    return render(request,'form.html') 

def TicketOut(request,pk):
    obj           = Parking_Ticket.objects.filter(id=pk).update(checkout_time = datetime.now()) 
    ticket        = Parking_Ticket.objects.get(id=pk)

    # time_spent
    checkin_time  = f"{ticket.checkin_time.time()}"       
    checkout_time = f"{ticket.checkout_time.time()}"
   
    format = '%H:%M:%S.%f'
    time_spent = datetime.strptime(checkout_time, format) - datetime.strptime(checkin_time, format)
    time_spent = str(time_spent).split(".")[0]
    ticket.time_spent = time_spent

    # total_due 

    time_spent = datetime.strptime(checkout_time, format) - datetime.strptime(checkin_time, format)
    time_minutes = time_spent.total_seconds()  / 60
    total_due = time_minutes * 0.5
    total_due = round(total_due,2)
    ticket.total_due = total_due    
    ticket.save()
    return redirect('ticketslist')

class CarsList(list.ListView):
    model         = Car
    template_name = 'cars_list.html'


def BillList(request,license_plate):
    car = Car.objects.get(license_plate=license_plate)
    object_list = Total_Amount.objects.filter(car=car).order_by('-id').all()
    return render(request,'bill_list.html',{'object_list':object_list})


  
    
   
 