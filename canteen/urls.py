from django.urls import path
from . import views
from .views import delete_item

urlpatterns = [
    path('canteen_login/', views.canteen_login, name='canteen_login'),
    path('canteen_register/', views.canteen_register, name='canteen_register'),
    path('canteen_logout/', views.canteen_logout, name='canteen_logout'),
    path('canteen_home/', views.canteen_home, name='canteen_home'),
    path('canteen_menu/', views.canteen_menu, name='canteen_menu'),
    path('canteen_order/', views.canteen_order, name='canteen_order'),
    path('canteen_order/paid/<str:order_number>', views.canteen_order_paid, name='canteen_order_paid'),
    path('canteen_about/', views.canteen_about, name='canteen_about'),
    path('canteen_settings/', views.canteen_settings, name='canteen_settings'),
    path('canteen_nonveg/', views.canteen_nonveg, name='canteen_nonveg'),
    path('canteen_veg/',views.canteen_veg, name='canteen_veg'),
    path('canteen_drinks/',views.canteen_drinks, name='canteen_drinks'),
    path('edit_nonveg/<int:item_id>/', views.edit_nonveg, name='edit_nonveg'),
    path('edit_veg/<int:item_id>/', views.edit_veg, name='edit_veg'),
    path('edit_colddrinks/',views.edit_colddrinks, name='edit_colddrinks'),
    path('edit_hotdrinks/',views.edit_hotdrinks, name='edit_hotdrinks'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]
