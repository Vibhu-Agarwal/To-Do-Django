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
                    'created': todo_query.created,
                    'due date': todo_query.due_date,
                    'category': str(todo_query.category),
                    'due': 'No' if todo_query.completed else 'Yes'}
            todo_list.append(todo)
        response['to-dos'] = todo_list
    return response


def todos_api(request, user_id):
    response = todos_data(request, user_id)
    return JsonResponse(response)


@login_required(login_url='/user/login/')
def todos(request):
    user_id = request.user.id
    todo_data = todos_data(request, user_id)
    return render(request, 'todos.html', {})


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
            return redirect('')
        else:
            return render(request, 'error.html', {'detail': "Invalid Task Entry"})
    else:
        form = TaskForm()
        return render(request, 'addTask.html', {'form': form})
