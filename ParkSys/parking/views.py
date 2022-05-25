from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ParkingInfo,ParkingSpot
from datetime import datetime,timedelta
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import make_aware
from django.core.mail import send_mail
import threading
import time
from django.conf import settings
# Create your views here.
def index(request):
    total=ParkingSpot.objects.all().count()
    vacant= ParkingSpot.objects.filter(isoccupied=False).count()
    return render(request,'index.html',{'total':total,'vacant':vacant,'booked':(total-vacant)})

def home(request):
    uid=request.user
    hasbooking=ParkingInfo.objects.filter(userid=uid.id,isactive=True)
    if hasbooking.exists():
        return render(request,'parkinginfo.html',{'vehicleid':hasbooking[0].vehicleid,'slotid':hasbooking[0].slotid.id,'stime':hasbooking[0].stime,'etime':hasbooking[0].etime})
    else:
        freespots= ParkingSpot.objects.filter(isoccupied=False)
        occupiedspots=ParkingInfo.objects.filter(isactive=True)
        return render(request,'home.html',{'freespots':freespots,'occupiedspots':occupiedspots})
def book(request):
    if request.method=='POST':
        slotid=request.POST['slotid']
        slot=ParkingSpot.objects.get(id=slotid)
        slot.isoccupied=True
        slot.save()
        uid= request.POST['userid']
        userid=User.objects.get(id=uid)

        hourss=int(request.POST['hours'])
        dateobj=make_aware(datetime.now()) + timedelta(minutes=5) #parking overhead
        etimeobj=dateobj+timedelta(hours=hourss)
        print(dateobj)
        print(etimeobj)

        #finaltime=dateobj.strftime("%d/%m/%Y %H:%M:%S")
        vehicleid= request.POST['vehicleid']
        details=ParkingInfo(userid=userid,slotid=slot,stime=dateobj,etime=etimeobj,vehicleid=vehicleid,isactive=True,notifid=0)
        details.save()
        return redirect('home')
    else:
        return redirect('home')

def vacate(request):
    if request.method=='POST':
        uid =request.user
        slotid=request.POST['slotid']
        print(slotid)
        undoslot=ParkingSpot.objects.get(id=slotid)
        undoslot.isoccupied=False
        undoslot.save()
        undoinfo=ParkingInfo.objects.get(slotid=undoslot,isactive=True)
        undoinfo.isactive=False
        undoinfo.etime=make_aware(datetime.now())+timedelta(minutes=5)
        undoinfo.save()
        return redirect('home')
    else:
        return redirect('home')
    
def parkhistory(request):
    uid=request.user
    histry=ParkingInfo.objects.filter(userid=uid).order_by('-id')
    return render(request,'uhistory.html',{'histry':histry})

def update(request):
    
    if request.method == 'POST':
        uid =request.user
        email=request.POST['email1']
        if email is None:
            messages.info(request,'email field cannot be empty...')
            return redirect('update')
        match=User.objects.filter(email=email)
        print(match)
        print(email)
        if uid.email==email:
            messages.info(request,'email is same')
            return redirect('update')
        elif match.exists():
            messages.info(request,'email taken')
            return redirect('update')
        else:
            updating=User.objects.get(id=uid.id)
            updating.email=email
            updating.save()
            messages.info(request,'contact details were updated successfully...')
            return redirect('home')
    else:
        return render(request,'conupdt.html')


def extendtime(request):
    if request.method=='POST':
        uid =request.user
        slotid=request.POST['slotid']
        hourss=int(request.POST['hours'])
        print(slotid)
        extndslot=ParkingSpot.objects.get(id=slotid)
        exinfo=ParkingInfo.objects.get(slotid=extndslot,isactive=True,notifid=0)
        exinfo.etime+=timedelta(hours=hourss)
        exinfo.save()
        messages.info(request,'Time extension accepted.')
        return redirect('home')
    else:
        return redirect('home')  

def notifyadmin(sid):
    subject ='Regarding Parking spot vacation'
    msg= f'User did not vacate spot : {sid} even though duration ended and user was notified. Kindly take appropriate decision.'
    to ='iit2019176@iiita.ac.in'
    res =send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
    if(res==1):
        print('eMail success')
        return 0
    else:
        print('eMail failure')
        return 1

def notifyuser(emailid):
    subject ='Vacate Parking Spot'
    msg= 'Times up! Kindly vacate the parking Spot or Request extension'
    to =emailid
    res =send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
    if(res==1):
        print('eMail success')
        return 0
    else:
        print('eMail failure')
        return 1

def checkin():
    infolists=ParkingInfo.objects.filter(isactive=True)
    for i in infolists:
        ltime=i.etime
        print('working') #all printfs are for testing purposes.
        print(ltime)
        print(make_aware(datetime.now()))
        nowtime=make_aware(datetime.now())
        tdiff=(ltime-nowtime).total_seconds()/60.0
        print(nowtime+timedelta(minutes=tdiff)) # just to check time converts from utc to ist correctly
        print(tdiff)        
        if tdiff > 0 and tdiff < 10 and i.notifid == 0:
            #user has less than 10 minutes left
            print("under 10 minutes")
            stat=notifyuser(i.userid.email)
            if stat == 0:
                obj=ParkingInfo.objects.get(userid=i.userid.id)
                obj.notifid=1
                obj.save()    
        elif tdiff < 0 and tdiff < -5 and i.notifid == 1:
            #user hasn't vacated yet. inform admin.
            print("complain to admin")
            stat=notifyadmin(i.slotid.id)
            if stat == 0:
                obj=ParkingInfo.objects.get(userid=i.userid.id,isactive=True)
                obj.notifid=2
                obj.save()
        
def checker():
    while True:
        checkin()
        time.sleep(300)
    #obj=ParkingInfo.objects.filter(isactive=True)
    #print(obj)

threading.Thread(target=checker,daemon=True).start() #just one extra thread to handle scheduled checkup of expiry timings