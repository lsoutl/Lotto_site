from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my/tickets/', views.my_tickets, name='my_tickets'),
]