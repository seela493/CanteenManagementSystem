from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, rfidform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MenuItem, Cart, CartItem



# Create your views here.
@login_required
def home(request):
    return render(request, 'student/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # user = authenticate(request, username = username, password = password)
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')  # Redirect to your homepage
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "The form is invalid.")
    else:
        form = LoginForm()

    return render(request, 'student/login.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "The passwords do not match.")
            return render(request, 'student/register.html', {'form': RegistrationForm()})
        
        if len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'student/register.html', {'form': RegistrationForm()})
            

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'student/register.html', {'form': RegistrationForm()})

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'student/register.html', {'form': RegistrationForm()})
        
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Create the user since all conditions are met
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.full_name = full_name  # Assign full_name to the first_name field
        
        user.save()

        # Inform user and redirect to login page
        messages.success(request, "User has been successfully registered! Please log in.")
        return redirect('login')

    # If not POST, display the registration form
    form = RegistrationForm()
    return render(request, 'student/register.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)

    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def rfid_form_view(request):  # Changed the view name for clarity
    if request.method == 'POST':
        form = rfidform(request.POST)
        if form.is_valid():
            full_name = request.POST.get('full_name')
            email_address = request.POST.get('email_address')
            phone_number = request.POST.get('phone_number')
            student_id = request.POST.get('student_id')
            address = request.POST.get('address')
            issuance_date = request.POST.get('issuance_date')
            expiry_date = request.POST.get('expiry_date')
            
            # Save the data or perform any action
            return redirect('home')  # Assuming 'home' is a valid URL name
    else:
        form = rfidform(request.POST)  # Initialize the form
    
    return render(request, 'student/rfid.html', {'form': form})

@login_required
def menu(request):
    return render(request, 'student/menu.html')

@login_required
def order(request):
    return render(request, 'student/order.html')

@login_required
def setting(request):
    return render(request, 'student/setting.html')



@login_required
def add_to_cart(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})