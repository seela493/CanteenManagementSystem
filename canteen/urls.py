from django.urls import path
from . import views

urlpatterns = [
    path('canteen_login/', views.canteen_login, name='canteen_login'),
    path('canteen_register/', views.canteen_register, name='canteen_register'),
    path('canteen_logout/', views.canteen_logout, name='canteen_logout'),
    path('canteen_home/', views.canteen_home, name='canteen_home'),
    path('canteen_menu/', views.canteen_menu, name='canteen_menu'),
    path('canteen_order/', views.canteen_order, name='canteen_order'),
    path('canteen_about/', views.canteen_about, name='canteen_about'),
    path('canteen_settings/', views.canteen_settings, name='canteen_settings'),
]
