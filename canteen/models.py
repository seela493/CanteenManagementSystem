from django.db import models

# Create your models here.
class MenuItem(models.Model):
    CATEGORY_CHOICES = (
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('colddrinks', 'Cold-Drinks'),
        ('hotdrinks', 'Hot-Drinks'),
    )
    name = models.CharField(max_length=100)  # Name of the menu item
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='veg')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
