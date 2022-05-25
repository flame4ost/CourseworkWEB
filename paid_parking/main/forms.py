from django import forms
from django.db.models import fields
from django.forms import widgets
from database.models import *

class TicketForm(forms.ModelForm):    
    class Meta:
        model  = Parking_Ticket
        fields = ('license_plate',)
        

class CarForm(forms.ModelForm):
    class Meta:
        model  = Car
        fields = '__all__'