from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EventForm
from .models import Event, Note, Task
from django.contrib.auth import login, logout, authenticate

from django.db.models import Q
from datetime import datetime
from calendar import monthrange, weekday
from django.forms.models import model_to_dict

import random

month_names = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}

# Create your views here
def home(request):
    return render(request, 'main/home.html', {})

@login_required(login_url='/login')
def calendar(request):
    if request.method == 'GET':
        try:
            tag_search = request.GET.get('search_bar_contents')
            tag_search += f'&tag={request.GET.get("search-box")}'

            return redirect(tag_search)
        except:
            pass

        try:
            year = int(request.GET.get('year'))
            month = int(request.GET.get('month'))

            if (year < 1000 or year > 3000 or month < 1 or month > 12):
                raise Exception()
        except:
            now = datetime.now()
            
            year = now.year
            month = now.month

            redirect_url = f'/calendar?year={year}&month={month}'

            return redirect(redirect_url)

        num_days = monthrange(year, month)[1]

        # 0 = monday
        start_day = weekday(year, month, 1)

        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=num_days)

        # data index = calendar row index
        data = [None]*start_day

        for i in range(num_days):
            data.append({ 'date_num': i + 1, 'events': [] })

        objects = Event.objects.filter(author=request.user)
        objects = objects.filter(Q(startTime__gte=start_date) & Q(startTime__lte=end_date))

        try:
            tag = request.GET.get('tag')

            if tag == None or tag == '':
                raise Exception()
            
            objects = objects.filter(tag=tag)
        except: pass

        for o in objects:
            event_dict = model_to_dict(o)

            event_day = event_dict['startTime'].day
            event_name = event_dict['name']
            event_id = event_dict['id']
            color = generate_color(event_dict['tag'])

            event_dict = {'name':event_name, 'color':f'{color}', 'event_id':event_id}

            data[event_day + start_day - 1]['events'].append(event_dict)

    return render (request, 'main/calendar.html', {'data': data, 
                                                            'year_month': f'{year} {month}', 
                                                            'month_name': month_names[month],
                                                            'year': year,
                                                            'search_bar_contents':f'/calendar?year={year}&month={month}'})

def generate_color(word):
    random.seed(word)
    color = '#{:06x}'.format(random.randint(0x555555, 0xbbbbbb))
    return color

def testing(request):
    return render(request, 'main/notes.html', {})

@login_required(login_url='/login')
def profile(request):
    return render(request, 'main/profile.html')

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
        name = request.POST.get('name')
        text = request.POST.get('text')
        startTime = request.POST.get('startTime')
        tag = request.POST.get('tag')

        e = Event()

        e.name = name
        e.text = text
        e.startTime = startTime
        e.tag = tag
        e.author = request.user

        e.save()

        return redirect('/calendar')

    return render(request, 'main/create_event.html') 

@login_required(login_url='/login')
def edit_event(request):
    id = request.GET.get('id')

    if request.method == 'POST':
        form_id = request.POST.get('form_id')

        if form_id == 'edit':
            name = request.POST.get('name')
            text = request.POST.get('text')
            startTime = request.POST.get('startTime')
            tag = request.POST.get('tag')

            e = Event()

            e.id = id
            e.name = name
            e.text = text
            e.startTime = startTime
            e.tag = tag
            e.author = request.user

            e.save()

            return redirect('/calendar')
        elif form_id == 'delete':
            event = Event.objects.filter(id=id)[0]
            event.delete()
            return redirect('/calendar')

    event = Event.objects.filter(id=id)[0]

    return render(request, 'main/edit_event.html', {'event':event})

@login_required(login_url='/login')
def notes(request):
    notes = Note.objects.filter(author=request.user).order_by('-lastModifiedTime')

    try:
        name = request.GET.get('search')
        if name == '': raise Exception()
        notes = notes.filter(name=name)
    except: pass

    return render(request, 'main/notes.html', {'notes':notes})

@login_required(login_url='/login')
def create_note(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')
        color = request.POST.get('color')

        n = Note()

        n.name = name
        n.text = text
        n.author = request.user
        n.color = color

        n.save()

        return redirect('/notes')

    return render(request, 'main/create_note.html') 

@login_required(login_url='/login')
def edit_note(request):

    
    id = request.GET.get('id')

    if request.method == 'POST':
        form_id = request.POST.get('form_id')

        if form_id == 'edit':
            name = request.POST.get('name')
            text = request.POST.get('text')
            color = request.POST.get('color')

            n = Note()

            n.id = id
            n.name = name
            n.text = text
            n.author = request.user
            n.color = color
            n.lastModifiedTime = datetime.now()

            n.save()

            return redirect('/notes')
        if form_id == 'delete':
            note = Note.objects.filter(id=id)[0]
            note.delete()
            return redirect('/notes')

    note = Note.objects.filter(id=id)[0]
    return render(request, 'main/edit_note.html', {'note':note}) 

@login_required(login_url='/login')
def tasks(request):
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        
        if form_id == 'move_task':
            task_id = request.POST.get('task_id')
            action = request.POST.get('action')

            task = Task.objects.filter(id=task_id)[0]

            if action == 'move_right': task.status += 1
            elif action == 'move_left': task.status -= 1

            task.save()
        elif form_id == 'delete_done':
            tasks_done = Task.objects.filter(author=request.user, status=3)

            print(tasks_done)

            for task in tasks_done:
                task.delete()

            

    tasks_1 = Task.objects.filter(author=request.user, status=1)
    tasks_2 = Task.objects.filter(author=request.user, status=2)
    tasks_3 = Task.objects.filter(author=request.user, status=3)

    max_query_length = max(len(tasks_1), len(tasks_2), len(tasks_3))

    task_dict_list = []

    for i in range(max_query_length):
        try: task_1 = tasks_1[i]
        except: task_1 = None

        try: task_2 = tasks_2[i]
        except: task_2 = None

        try: task_3 = tasks_3[i]
        except: task_3 = None

        task_dict_list.append({'task_1':task_1, 'task_2':task_2, 'task_3':task_3})

    return render(request, 'main/tasks.html', {'task_dict_list':task_dict_list})

@login_required(login_url='/login')
def create_task(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        status = request.POST.get('status-task')
        
        status_id = 1
        if status == 'Запланировано':
            status_id = 1
        elif status == 'В процессе':
            status_id = 2
        elif status == 'Сделано':
            status_id = 3

        t = Task()

        t.name = name
        t.author = request.user
        t.status = status_id

        t.save()

        return redirect('/tasks')

    return render(request, 'main/create_task.html')
