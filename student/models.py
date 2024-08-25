from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')])
    address = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.user.username
    
    
