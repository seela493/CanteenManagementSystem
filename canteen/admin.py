from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'updated_at')  # Added 'category' to display
    search_fields = ('name',)
    list_filter = ('category', 'updated_at')  # Added 'category' for filtering
    ordering = ('-updated_at',)  # Optional: Order items by 'updated_at' descending
