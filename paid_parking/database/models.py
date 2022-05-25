from django.db import models
from datetime import datetime

# Create your models here.

class Parking_Ticket(models.Model):
    
        
    license_plate = models.CharField(verbose_name='License Plate',max_length=50)
    checkin_time  = models.DateTimeField(verbose_name='Check In Time',)
    checkout_time = models.DateTimeField(verbose_name='Check Out Time',null=True,blank=True)
    time_spent    = models.CharField(verbose_name='Time Spent',null=True,blank=True,max_length=50)
    total_due     = models.DecimalField(verbose_name='Total Due',decimal_places=2,max_digits=6,null=True,blank=True, )
    def __str__(self) :
        return self.license_plate


class Car(models.Model):
    license_plate = models.CharField(verbose_name='License Plate',max_length=50)
    resident      = models.CharField(verbose_name='Resident',max_length=100)  

    def __str__(self) :
        return self.license_plate 
    
class Total_Amount(models.Model):
    car       = models.ForeignKey(Car,on_delete=models.CASCADE,verbose_name='Cars')
    month     = models.CharField(max_length=2)
    year      = models.CharField(max_length=4)
    total_due = models.DecimalField(verbose_name='Total Due',decimal_places=2,max_digits=6,null=True,blank=True)

