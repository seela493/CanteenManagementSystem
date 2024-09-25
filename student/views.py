from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, rfidform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, Order, OrderItem
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse 
from django.core import serializers
from firebase_admin import db
import pyrebase

config = {
    "apiKey": "AIzaSyAkvuzmGmXX0XezhSeOqltGKAVfwHHo5M4",
    "authDomain": "newupdatedcanteen.firebaseapp.com",
    "databaseURL": "https://newupdatedcanteen-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "newupdatedcanteen",
    "storageBucket": "newupdatedcanteen.appspot.com",
    "messagingSenderId": "333329487780",
    "appId": "1:333329487780:web:bd5d1e17021470e8dc9331",
    "measurementId": "G-R6490XPPFG"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


# Home view
@login_required
def home(request):
    user = database.child('users').child('36395E32')
    user_id= user.child('user_id').get().val()
    balance = user.child('balance').get().val()
    
    context = {
        'balance': balance,
        'user_id': user_id,
    }
    
    return render(request, 'student/home.html')


# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "The form is invalid.")
    else:
        form = LoginForm()
    return render(request, 'student/login.html', {'form': form})

# Registration view
def register_view(request):
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
                return redirect('register')

            if len(password1) < 6:
                messages.error(request, 'Password must be at least 6 characters.')
                return redirect('register')

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect('register')

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            # Inform user and redirect to login page
            messages.success(request, "User has been successfully registered! Please log in.")
            return redirect('login')

        else:
            messages.error(request, "The form is invalid.")
            form = RegistrationForm()
    else:
        form = RegistrationForm()
    return render(request, 'student/register.html', {'form': form})

@login_required
def about_view(request):
    return render(request,'student/about.html')

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# RFID form view
@login_required
def rfid_form_view(request):
    if request.method == 'POST':
        form = rfidform(request.POST)
        if form.is_valid():
            form.save()  # Save the form if it's valid
            messages.success(request, "RFID details have been saved.")
            return redirect('home')
    else:
        form = rfidform()  # Initialize the form
    return render(request, 'student/rfid.html', {'form': form})


# Setting view
@login_required
def setting(request):
    return render(request, 'student/setting.html')


@login_required
def order(request):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()  # Fetch the current cart
    order_items = OrderItem.objects.filter(order=order).all() if order else None
    context = { 'order': order, 'order_items': order_items }
    return render(request, 'student/order.html', context)


# Menu view
def menu(request):
    items = Item.objects.all()  # Fetch all items from the database
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    order_items = OrderItem.objects.filter(order=order).all() if order else None

    return render(request, 'student/menu.html', {'items': items, 'order': order, 'order_items': order_items})

# Add to cart view
@login_required
def add_to_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)
        order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        
        if not created:
            order_item.quantity += 1
            order_item.save()

        # Return JSON response with updated order information
        response = {
            'status': 'success',
            'item_name': item.name,
            'item_image': item.image.url if item.image else None,
            'item_price': str(item.price),
            'total_price': str(order.get_total_price())
        }
        return redirect('menu')
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def increase_in_cart(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.quantity += 1
    order_item.save()
    
    return redirect('order')

@login_required
def decrease_in_cart(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    if(order_item.quantity == 1):
        order_item.delete()
    else:
        order_item.quantity -= 1
        order_item.save()

    return redirect('order')


# Place order view
@login_required
def place_order(request):
    order = Order.objects.get(user=request.user, is_ordered=False)
    order.is_ordered = True
    order.date_ordered = timezone.now()
    order.save()

    messages.success(request, 'Your order has been placed successfully.')
    return redirect('order')

# Order history view
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-date_ordered')
    context = {'orders': orders}
    return render(request, 'student/order.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Order, OrderItem

# Existing view for deleting an entire order
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == "POST":
        OrderItem.objects.filter(order=order).delete()
        order.is_ordered = False
        order.order_number = ""
        order.save()
        messages.success(request, "Order has been deleted successfully.")
    
    return redirect(reverse('order'))

def place_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        order.is_ordered = True
        order.save()
        messages.success(request, "Order has been placed successfully.")
    return redirect(reverse('order'))

# New view for deleting a single item from an order
def delete_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)

    if request.method == "POST":
        order_item.delete()
        messages.success(request, f"Item {order_item.item.name} has been deleted from your order.")

    return redirect(reverse('order'))  # Redirect to cart or appropriate page

