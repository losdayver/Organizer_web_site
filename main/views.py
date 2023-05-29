from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EventForm
from .models import Event
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def home(request):
    return render(request, 'main/home.html', {})

def testing(request):
    return render(request, 'main/calendar.html', {})

@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        event_id = request.POST.get("event-id")
        event = Event.objects.filter(id=event_id).first()
        event.delete()

    events_list = Event.objects.filter(author=request.user)
    
    return render(request, 'main/profile.html', {'events_list':events_list})

def sing_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

    elif request.method == 'GET':
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})

@login_required(login_url='/login')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        print('asdadasd')
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.deadline = form.cleaned_data['deadlineTime']
            print('asdadasd')
            print(form.cleaned_data)
            event.save()
            return redirect('/profile')
    else:
        form = EventForm()

    return render(request, 'main/create_event.html', {'form': form}) 

    
    
    

