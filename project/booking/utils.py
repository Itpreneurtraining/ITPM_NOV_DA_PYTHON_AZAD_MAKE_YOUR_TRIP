from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os
from django.core.files.base import ContentFile



def create_invoice_pdf(booking):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "MakeUrTrip - Invoice")

    y = height - 100

    # Access user data from related user model
    user = booking.user
    user_name = getattr(user, 'name', 'N/A')
    user_email = getattr(user, 'email', 'N/A')
    user_phone = getattr(user, 'phone', 'N/A')  # Only if your custom User model has this field

    details = [
        ("Booking ID", booking.id),
        ("Customer Name", user_name),
        ("Customer Email", user_email),
        ("Customer Phone", user_phone),
        ("Destination", booking.destination.name),
        ("Tour Type", booking.tour_type),
        ("Transport", booking.transport_mode),
        ("Hotel", booking.hotel_category),
        ("People", booking.num_people),
        ("Travel Date", booking.travel_date.strftime('%Y-%m-%d')),
        ("Total Cost", f"₹ {booking.total_cost:.2f}"),
    ]

    p.setFont("Helvetica", 12)
    for label, value in details:
        p.drawString(80, y, f"{label}: {value}")
        y -= 25

    p.drawString(80, y - 10, "Thank you for booking with us!")
    p.showPage()
    p.save()

    buffer.seek(0)
    return ContentFile(buffer.getvalue())




def save(self, *args, **kwargs):
    self.total_cost = self.calculate_total_cost()

    # Generate PDF and assign
    from .utils import create_invoice_pdf
    pdf_content = create_invoice_pdf(self.booking)
    filename = f"invoice_{self.booking.id}.pdf"
    self.pdf_file.save(filename, pdf_content, save=False)

    super().save(*args, **kwargs)

    self.pdf_file.save(f'invoices/invoice_{self.booking.id}.pdf', pdf_content, save=False)