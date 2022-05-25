from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Parking_Ticket)
admin.site.register(Total_Amount)
admin.site.register(Car)
