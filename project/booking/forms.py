from django import forms
from .models import TravelBooking, Destination

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'country', 'image']


class TravelBookingForm(forms.ModelForm):
    class Meta:
        model = TravelBooking
        fields = ['tour_type', 'destination', 'transport_mode', 'hotel_category', 'num_people']
        widgets = {
            'travel_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(TravelBookingForm, self).__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.all()

    def clean_transport_mode(self):
        tour_type = self.cleaned_data.get('tour_type')
        transport_mode = self.cleaned_data.get('transport_mode')

        # Validate transport mode based on tour type
        if tour_type == 'international' and transport_mode != 'flight':
            raise forms.ValidationError("For international tours, only flight transport is allowed.")

        if tour_type == 'domestic' and transport_mode not in ['flight', 'train']:
            raise forms.ValidationError("For domestic tours, you must select either flight or train.")
        
        return transport_mode

