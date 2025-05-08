from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TravelBooking, Destination, Invoice
from .forms import TravelBookingForm

from django.shortcuts import render, redirect
from .forms import TravelBookingForm
from .models import Destination, Invoice
from django.core.mail import EmailMessage
from django.conf import settings  # To get DEFAULT_FROM_EMAIL


# Homepage
def home(request):
    return render(request, 'home.html')

# About Page
def about(request):
    return render(request, 'about.html')

# Destination List
def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'booking/destination_list.html', {'destinations': destinations})

# Destination List with Filtering
def destination_list_view(request):
    category = request.GET.get('category')
    if category in ['domestic', 'international']:
        destination = Destination.objects.filter(tour_type=category)
    else:
        destination = Destination.objects.all()

    return render(request, 'booking/destination_list.html', {
        'destination': destination,
        'selected_category': category,
    })

# Booking Amount Calculation
def calculate_amount(booking):
    base_price = 5000  # example base price
    multiplier = 1

    if booking.hotel_category == '5star':
        multiplier += 1.0
    elif booking.hotel_category == '4star':
        multiplier += 0.7
    elif booking.hotel_category == '3star':
        multiplier += 0.4

    if booking.transport_mode == 'flight':
        multiplier += 0.8
    elif booking.transport_mode == 'train':
        multiplier += 0.3

    return base_price * multiplier * booking.num_people




# Booking List
@login_required
def booking_list(request):
    bookings = TravelBooking.objects.filter(user=request.user)
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

# Booking Detail
@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(TravelBooking, id=booking_id)
    return render(request, 'booking/booking_detail.html', {'booking': booking})

# Update Booking
@login_required
def booking_update(request, booking_id):
    booking = get_object_or_404(TravelBooking, id=booking_id)

    if request.method == 'POST':
        form = TravelBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = TravelBookingForm(instance=booking)

    return render(request, 'booking/create_booking.html', {'form': form})

# Delete Booking
@login_required
def booking_delete(request, booking_id):
    booking = get_object_or_404(TravelBooking, id=booking_id)

    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')

    return render(request, 'booking/booking_confirm_delete.html', {'booking': booking})

# Invoice Detail

from .utils import create_invoice_pdf  # Make sure this is imported

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Generate PDF if it doesn't already exist
    if not invoice.pdf_file:
        pdf_content = create_invoice_pdf(invoice.booking)
        filename = f"invoice_{invoice.id}.pdf"
        invoice.pdf_file.save(filename, pdf_content, save=True)
        invoice.booking.user.name
        invoice.booking.user.email
        invoice.booking.user.phone
        


    return render(request, 'booking/invoice_detail.html', {'invoice': invoice})


@login_required
def create_booking(request, destination_id=None):
    tour_type = None
    destinations = Destination.objects.none()
    transport_modes = []

    if request.method == 'POST':
        tour_type = request.POST.get('tour_type')

        if tour_type:
            destinations = Destination.objects.filter(tour_type=tour_type)
            if destination_id:
                destinations = destinations.filter(id=destination_id)

            if tour_type.lower() == 'domestic':
                transport_modes = ['Flight', 'Train']
            elif tour_type.lower() == 'international':
                transport_modes = ['Flight']

        form = TravelBookingForm(request.POST)

        if 'submit_booking' in request.POST and form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            amount = calculate_amount(booking)
            booking.total_cost = amount
            booking.save()

            # Create invoice and generate PDF
            invoice = Invoice.objects.create(booking=booking, total_cost=amount)

            # Send confirmation email with invoice PDF
            subject = 'Booking Confirmation - MakeUrTrip'
            message = f"""
Dear {request.user.name},

Thank you for booking your trip with MakeUrTrip!

Here are your booking details:
- Destination: {booking.destination.name}
- Tour Type: {booking.tour_type}
- Transport: {booking.transport_mode}
- Hotel: {booking.hotel_category}
- Number of People: {booking.num_people}
- Travel Date: {booking.travel_date}
- Total Cost: ₹ {booking.total_cost:.2f}

Your invoice is attached to this email.

Regards,
MakeUrTrip Team
"""
            recipient = request.user.email

            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
            if invoice.pdf_file:
                with invoice.pdf_file.open('rb') as pdf:
                  email.attach(invoice.pdf_file.name, invoice.pdf_file.read(), 'application/pdf')
            email.send()

            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = TravelBookingForm()

    return render(request, 'booking/create_booking.html', {
        'form': form,
        'tour_type': tour_type,
        'destinations': destinations,
        'transport_modes': transport_modes,
    })