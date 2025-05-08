from django.contrib import admin

# Register your models here.
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'tour_type']