
from django.urls import path
from student import views
from django.conf import settings
from django.conf.urls.static import static
 

urlpatterns = [
    path('', views.login_view, name = 'login'),
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
    path('place_order/', views.place_order, name='place_order'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)