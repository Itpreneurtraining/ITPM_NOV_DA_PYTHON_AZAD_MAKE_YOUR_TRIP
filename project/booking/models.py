from django.db import models
from datetime import date
from django.conf import settings
from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()



class Destination(models.Model):
    TOUR_TYPE_CHOICES = [
        ('domestic', 'Domestic'),
        ('international', 'International'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(default='No description available')
    country = models.CharField(max_length=100, default='Unknown')
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPE_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=10000)
    duration = models.CharField(max_length=50, default='4')
    places = models.TextField(default='Unknown')

    def __str__(self):
        return f"{self.name} ({self.tour_type})"


class TravelBooking(models.Model):
    TRANSPORT_CHOICES_DOMESTIC = [
        ('flight', 'Flight'),
        ('train', 'Train'),
    ]
    TRANSPORT_CHOICES_INTERNATIONAL = [
        ('flight', 'Flight'),
    ]

    HOTEL_CATEGORY_CHOICES = [
        ('5star', '5 Star'),
        ('4star', '4 Star'),
        ('3star', '3 Star'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    tour_type = models.CharField(max_length=20, choices=Destination.TOUR_TYPE_CHOICES)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    transport_mode = models.CharField(max_length=10)
    hotel_category = models.CharField(max_length=10, choices=HOTEL_CATEGORY_CHOICES)
    num_people = models.PositiveIntegerField()
    travel_date = models.DateField(default=date.today)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if self.tour_type == 'domestic' and self.transport_mode not in dict(self.TRANSPORT_CHOICES_DOMESTIC):
            raise ValueError("Invalid transport mode for domestic tour")
        if self.tour_type == 'international' and self.transport_mode not in dict(self.TRANSPORT_CHOICES_INTERNATIONAL):
            raise ValueError("Invalid transport mode for international tour")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tour_type.title()} tour to {self.destination.name} for {self.num_people} person(s)"




from django.core.files.base import ContentFile
from .utils import create_invoice_pdf  # ensure utils.py has this function

class Invoice(models.Model):
    booking = models.OneToOneField(TravelBooking, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)

    

    