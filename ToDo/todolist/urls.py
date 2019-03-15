from .views import *
from django.urls import path

app_name = 'todolist'

urlpatterns = [
    path('', home, name='homepage'),
    path('api/', api, name='api'),
    path('api/<int:user_id>/', todos_api, name='to-dos-api'),
    path('add-task/', add_task, name='Add Task'),
    path('tasks/', todos, name='tasks'),
    path('check/', check_due_date),
    path('delete-task/<int:task_id>', delete_task, name='Delete Task'),
    path('edit-task/<int:task_id>', edit_task, name='Edit Task')
]