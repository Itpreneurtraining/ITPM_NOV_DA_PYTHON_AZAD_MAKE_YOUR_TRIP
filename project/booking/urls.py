from django.urls import path
from . import views

urlpatterns = [
    path('booking_list', views.booking_list, name='booking_list'),
    path('book/<int:destination_id>/', views.create_booking, name='create_booking'),  
    path('bookingcreate/', views.create_booking, name='create_booking'), 
    path('booking_update/<int:booking_id>/', views.booking_update, name='booking_update'),
    path('booking_delete/<int:booking_id>/', views.booking_delete, name='booking_delete'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('booking/booking_confirm_delete.html', views.booking_delete, name='booking_delete'),
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
]

