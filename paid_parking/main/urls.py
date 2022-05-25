from django.urls import path
from . import views


urlpatterns = [
    path('',views.TicketsList.as_view(),name='ticketslist'),
    path('ticket_create/',views.TicketCreate,name='ticket_create'),
    path('ticket_out/<str:pk>',views.TicketOut,name='ticket_out'),
    path('cars/residents/',views.CarsList.as_view(),name='cars_list'),
    path('bill/<str:license_plate>',views.BillList,name='bill')
    ]