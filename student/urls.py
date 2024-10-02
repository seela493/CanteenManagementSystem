
from django.urls import path
from student import views
from django.conf import settings
from django.conf.urls.static import static
 

urlpatterns = [
    path('login/',views.login_view, name= 'login'),
    path('register/', views.register_view, name = 'register'),
    path('logout/', views.logout_view, name = 'logout'),
    path('home/', views.home, name = 'home'),
    path('rfidform/',views.rfid_form_view, name = 'rfidform'),
    path('menu/',views.menu, name = 'menu'),
    path('order/',views.order, name='order' ),
    path('about/',views.about_view, name='about'),
    path('setting/', views.setting, name='setting'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_in_cart/<int:order_item_id>/', views.decrease_in_cart, name='decrease_in_cart'),
    path('increase_in_cart/<int:order_item_id>/', views.increase_in_cart, name='increase_in_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('place-order/<int:order_id>/', views.place_order, name='place_order'),
    # path('create-order/', views.create_order, name='create_order'),
]