from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.sing_up, name='sign up'),
    path('profile/', views.profile, name='profile'),
    path('create-event/', views.create_event, name='create event'),
    path('testing/', views.testing, name='testing'),
    path('calendar/', views.calendar, name='calendar'),
]