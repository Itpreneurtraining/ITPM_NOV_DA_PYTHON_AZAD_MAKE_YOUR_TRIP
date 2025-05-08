from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.payment_view, name='payment_page'),  # Change payment_page to payment_view
    path('payment/success/', views.payment_success, name='payment_success'),
]
