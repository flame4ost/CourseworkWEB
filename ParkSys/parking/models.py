from django.db import models
from django.conf import settings

# Create your models here.
class ParkingSpot(models.Model):
    isoccupied = models.BooleanField()
    directions = models.TextField(max_length=150)
    destination=models.CharField(max_length=30,null=True,blank=True)
    def __str__(self):
        return self.directions


class ParkingInfo(models.Model):
    userid= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slotid= models.ForeignKey(ParkingSpot,on_delete=models.CASCADE)
    stime= models.DateTimeField()
    etime = models.DateTimeField(null=True,blank=True)
    vehicleid=models.CharField(max_length=50)
    isactive=models.BooleanField()
    notifid=models.IntegerField()
    def __str__(self):
        return f'Vehicle with id:{self.vehicleid} was parked from {self.stime} to {self.etime} at Parking spot: {self.slotid.id}'


