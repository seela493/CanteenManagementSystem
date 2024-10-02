from django.urls import path, include
from Start import  views

urlpatterns = [
    path('', views.start_view, name = 'start'),
]