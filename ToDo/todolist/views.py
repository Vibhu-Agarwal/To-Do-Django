from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required


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
                    'category': str(todo_query.category)}
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
