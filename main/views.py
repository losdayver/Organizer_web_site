from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EventForm
from .models import Event
from django.contrib.auth import login, logout, authenticate

from django.db.models import Q
from datetime import datetime
from calendar import monthrange, weekday
from django.forms.models import model_to_dict

# Create your views here
def home(request):
    return render(request, 'main/home.html', {})

def calendar(request):
    if request.method == 'GET':
        # TODO сделать лучше

        year = 2023
        month = 6

        num_days = monthrange(year, month)[1]

        # 0 = monday
        start_day = weekday(year, month, 1)

        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=30)

        # data index = calendar row index
        data = [None]*start_day

        for i in range(num_days):
            data.append({ 'date_num': i + 1, 'events': [] })

        objects = Event.objects.filter(Q(startTime__gte=start_date) & Q(startTime__lte=end_date))

        for o in objects:
            event_dict = model_to_dict(o)

            event_day = event_dict['startTime'].day

            event_name = event_dict['name']

            event_dict = {'name':event_name}

            data[event_day + start_day - 1]['events'].append(event_dict)

        print(data) 

    return render (request, 'main/calendar_isolated.html', {'data': data})

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