from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'})
    )
    
class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder':'Enter your full name'})
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name']
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data

def save(self):
        # Get the cleaned data
        full_name = self.cleaned_data.get('full_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')

        # Split the full name into first and last name
        name_parts = full_name.split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        # Create a new User object
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Set the user's password
        user.set_password(password)
        
        # Save the user to the database
        user.save()
        return user


class rfidform(forms.Form):
    full_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    email_address = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    
    phone_number = forms.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    
    student_id = forms.CharField(
        max_length=10,  # You can adjust max_length based on the format of your IDs
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Student ID'})
    )
    
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your address'})
    )
    
    issuance_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    

    