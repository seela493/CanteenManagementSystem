
from django.urls import path
from student import views

urlpatterns = [
    
    path('', views.login_view, name = 'login'),
    path('login/',views.login_view, name= 'login'),
    path('register/', views.register_view, name = 'register'),
    path('logout/', views.logout_view, name = 'logout'),
    path('home/', views.home, name = 'home'),
    path('rfidform/',views.rfid_form_view, name = 'rfidform'),
    path('menu/',views.menu, name = 'menu'),
    path('order/',views.order, name='order' ),
    path('setting/', views.setting, name='setting'),
    
]