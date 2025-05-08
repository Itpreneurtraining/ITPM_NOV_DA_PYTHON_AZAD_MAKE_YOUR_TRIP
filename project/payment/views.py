from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PaymentForm
from .models import Payment


from django.core.mail import EmailMessage
from django.conf import settings


def payment_view(request):
    selected_method = request.POST.get('payment_method') if request.method == 'POST' else None

    # If the form is submitted via POST
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        # If the form is valid, save the payment data
        if form.is_valid():
            payment = form.save(commit=False)  
            payment.status = 'Success' 
            
            # Redirect to a success page or display a success message
            return redirect('payment_success')  # You can replace 'payment_success' with your own URL name

        else:
            # If form is not valid, render the form again with validation errors
            return render(request, 'payment/payment_view.html', {'form': form, 'selected_method': selected_method})

    else:
        # If the request is a GET, show the payment form
        form = PaymentForm()

    # Render the payment form on the page
    return render(request, 'payment/payment_view.html', {'form': form, 'selected_method': selected_method})


def payment_success(request):
    # Simple success page after successful payment submission
    return render(request, 'payment/payment_success.html')

    
    
    
