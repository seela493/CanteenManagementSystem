from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from student.models import Order
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import MenuItem
from .forms import MenuItemForm

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
    order_status = request.GET.get('order_satus', 'ORDER_IN')
    order_number = request.GET.get('order_number')
    print(order_number)
    if(order_status == 'PAID'):
        orders = Order.objects.filter(is_paid=True).all()
    else:
        orders = Order.objects.filter(is_ordered=True, is_paid=False).all()
    
    order_details = None
    if order_number:
        try:
            order_details = Order.objects.select_related('user').prefetch_related('items').get(order_number=order_number)
        except Order.DoesNotExist:
            order_details = None
            messages.error(request,'Invalid order number. Please try again. ')
            return redirect('canteen_order')
            
    return render(request, 'canteen/order.html', {'order_status': order_status, 'orders':orders, 'order_details':order_details})

def canteen_order_paid(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.is_paid = True
    order.save()
    return redirect('canteen_order')

def canteen_about(request):
    return render(request, 'canteen/about.html')

def canteen_settings(request):
    return render(request, 'canteen/settings.html')

def canteen_nonveg(request):
    nonveg_items = MenuItem.objects.filter(category='non-veg')
    return render(request, 'canteen/nonveg-menu.html',{'products':  nonveg_items})

def canteen_veg(request):
    products = MenuItem.objects.filter(category='veg')
    return render(request, 'canteen/veg-menu.html', {'products': products})
    

def canteen_drinks(request):
    return render(request, 'canteen/drink-menu.html')

def edit_nonveg(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    # Ensure the category is 'non-veg' when editing this item
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            nonveg_item = form.save(commit=False)  # Do not save to DB yet
            nonveg_item.category = 'non-veg'  # Set category to non-veg
            nonveg_item.save()  # Now save to DB
            return redirect('canteen_nonveg')
    else:
        form = MenuItemForm(instance=item)
    
    return render(request, 'canteen/edit-nv-item.html', {'form': form, 'product': item})

def edit_veg(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    # Ensure the category is 'veg' when editing this item
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            veg_item = form.save(commit=False)  # Do not save to DB yet
            veg_item.category = 'veg'  # Set category to veg
            veg_item.save()  # Now save to DB
            return redirect('canteen_veg')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'canteen/edit-v-item.html', {'form': form, 'product': item})

def delete_item(request, item_id):
    product = get_object_or_404(MenuItem,id=item_id)
    product.delete()
    return redirect('canteen_veg')


def edit_colddrinks(request):
    return render(request, 'canteen/edit-colddrink.html')

def edit_hotdrinks(request):
    return render(request, 'canteen/edit-hotdrink.html')