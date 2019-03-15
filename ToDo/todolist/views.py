from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from celery.schedules import crontab
from celery.task import periodic_task
from .mail import Mail


SENDER_EMAIL_ID = ''
SENDER_PASSWORD = ''


@login_required(login_url='/user/login')
def home(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})


#@periodic_task(run_every=crontab(minute=[4, 5, 34, 35]))
def check_due_date(request):
    #users = User.objects.filter(id=1)
    users = User.objects.all()
    task_msg = """
    
    Task: {title}
    Category: {cat}
    {desc}
    Due-Date: {due}
    """
    for user in users:
        mail = Mail(SENDER_EMAIL_ID, SENDER_PASSWORD)
        any_incomplete = False
        mail_content = ""
        tasks = ToDoList.objects.filter(user=user)
        for task in tasks:
            if not task.completed:
                mail_content += task_msg.format(title=task.title,
                                                cat=str(task.category),
                                                desc=task.description,
                                                due=task.due_date)
                any_incomplete = True
        if any_incomplete:
            mail_content = mail_content.strip()
            mail.define_message(user.email, 'To-Do App | TASKS OVERDUE', mail_content)
            print('Sending Mail ...')
            print(user.email, 'Heading', mail_content)
            sent_status, msg = mail.send_email()
            if not sent_status:
                print("Could Not Send Email to", user.username)


def todos_data(request, user_id):
    response = {}
    if request.method != 'POST':
        user = User.objects.get(id=user_id)
        todo_query_set = ToDoList.objects.filter(user=user)
        todo_list = []
        for todo_query in todo_query_set:
            todo = {'title': todo_query.title,
                    'description': todo_query.description,
                    'created_by': str(todo_query.user),
                    'created': todo_query.created,
                    'due_date': todo_query.due_date,
                    'category': str(todo_query.category),
                    'due': 'No' if todo_query.completed else 'Yes'}
            todo_list.append(todo)
        response['to-dos'] = todo_list
    return response


def api(request):
    users = User.objects.all()
    response = {}
    for user in users:
        tasks = todos_data(request, user.id)['to-dos']
        response[user.username] = tasks
    return JsonResponse(response)


def todos_api(request, user_id):
    response = todos_data(request, user_id)
    return JsonResponse(response)


@login_required(login_url='/user/login/')
def todos(request):
    user_id = request.user.id

    user = User.objects.get(id=user_id)
    todo_query_set = ToDoList.objects.filter(user=user)
    todo_data = []
    for todo_query in todo_query_set:
        todo = {'task_id': todo_query.id,
                'title': todo_query.title,
                'description': todo_query.description,
                'created_by': str(todo_query.user),
                'created': todo_query.created,
                'due_date': todo_query.due_date,
                'category': str(todo_query.category),
                'due': 'No' if todo_query.completed else 'Yes'}
        todo_data.append(todo)
    return render(request, 'todos.html', {'tasks': todo_data,
                                          'len_tasks': len(todo_data)})


@login_required(login_url='/user/login/')
def add_task(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            task.refresh_from_db()
            task.user = user
            task.save()
            return redirect('todolist:tasks')
        else:
            return render(request, 'error.html', {'detail': "Invalid Task Entry"})
    else:
        form = TaskForm()
        return render(request, 'addTask.html', {'form': form})


@login_required(login_url='/user/login/')
def delete_task(request, task_id):
    user_id = request.user.id
    selected_task = ToDoList.objects.get(id=task_id)
    if selected_task.user.id == user_id:
        selected_task.delete()
    return redirect('todolist:tasks')
