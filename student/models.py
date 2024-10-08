from django.db import models
from django.contrib.auth.models import User
import uuid
import random
import string


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('drink', 'Drink'),
    ]
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='veg')
    price = models.DecimalField(max_digits=10, decimal_places=3)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField('Item', through='OrderItem')
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    order_number = models.CharField(max_length=4, unique=True, blank=True)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_unique_order_number()
        super(Order, self).save(*args, **kwargs)

    def generate_unique_order_number(self):
        """
        Generate a unique 4-character order number.
        """
        while True:
            order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def get_total_price(self):
        total = sum(order_item.item.price * order_item.quantity for order_item in self.orderitem_set.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Order {self.order.order_number}"
    
    def total(self):
        return self.item.price * self.quantity
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    rfid = models.CharField(max_length=100, unique=True, blank=True, null=True)  # RFID field
    balance = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    has_applied_for_rfid = models.BooleanField(default=False)  # Track RFID application status
    country = models.CharField(max_length=100, blank=True, null=True)  # Optional field for 'country'
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True) 
    
    def __str__(self):
        return self.user.username
    
class User_RFID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rfid = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f'{self.user} - {self.rfid}'
    

    
