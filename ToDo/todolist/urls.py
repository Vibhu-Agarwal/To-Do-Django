from .views import *
from django.urls import path

urlpatterns = [
    path('api/', api, name='api'),
    path('api/<int:user_id>', todos_api, name='to-dos-api'),
    path('add-task/', add_task, name='Add Task'),
    path('', todos, name='to-dos'),
    path('check/', check_due_date),
    path('delete-task/<int:task_id>', delete_task)
]