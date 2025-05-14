from django.db import models
from django.conf import settings
from users.models import *

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='destinations/', blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} -> {self.destination.name}"
