from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Home view
def canteen_home(request):
    return render(request, 'canteen/home.html')

# Login view
def canteen_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('canteen_home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "The form is invalid.")
    else:
        form = LoginForm()
    return render(request, 'canteen/login.html', {'form': form})

# Registration view
def canteen_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            # Check if passwords match
            if password1 != password2:
                messages.error(request, "The passwords do not match.")
                return redirect('canteen_register')

            if len(password1) < 6:
                messages.error(request, 'Password must be at least 6 characters.')
                return redirect('canteen_register')

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('canteen_register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect('canteen_register')

            # Create the user
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "User has been successfully registered! Please log in.")
            return redirect('canteen_login')

        else:
            messages.error(request, "The form is invalid.")
    else:
        form = RegistrationForm()
    return render(request, 'canteen/register.html', {'form': form})

# Logout view
def canteen_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('canteen_login')


def canteen_menu(request):
    return render(request, 'canteen/menu.html')

def canteen_order(request):
    return render(request, 'canteen/order.html')

def canteen_about(request):
    return render(request, 'canteen/about.html')

def canteen_settings(request):
    return render(request, 'canteen/settings.html')