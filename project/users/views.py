from django.shortcuts import render

# Create your views here.

from django.shortcuts import render , redirect

from .models import *
from users.models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        user = User.objects.create_user(
            email=email, name=name, password=password, phone=phone)
        user.save()
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('booking_list')  # Redirect to booking list or any other page
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'users/login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

