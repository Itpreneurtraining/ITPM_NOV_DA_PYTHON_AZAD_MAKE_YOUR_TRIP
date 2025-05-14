from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User

# ---------------------------
# User Registration View
# ---------------------------
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# ---------------------------
# User Login View
# ---------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # Change to your homepage URL name
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')

# ---------------------------
# User Logout View
# ---------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# ---------------------------
# Profile View (Optional)
# ---------------------------
@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})
