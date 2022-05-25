from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('home/book',views.book,name='book'),
    path('home/vacate',views.vacate, name='vacate'),
    path('home/extendtime',views.extendtime, name='extendtime'),
    path('parkhistory',views.parkhistory,name='parkhistory'),
    path('update/',views.update,name='update'),

]
