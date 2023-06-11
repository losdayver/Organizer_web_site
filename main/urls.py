from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.sing_up, name='sign up'),
    path('profile/', views.profile, name='profile'),
    path('testing/', views.testing, name='testing'),

    path('calendar/', views.calendar, name='calendar'),
    path('create-event/', views.create_event, name='create event'),
    path('edit-event/', views.edit_event, name='edit event'),

    path('notes/', views.notes, name='notes'),
    path('edit-note/', views.edit_note, name='edit note'),
    path('create-note/', views.create_note, name='create note'),
]