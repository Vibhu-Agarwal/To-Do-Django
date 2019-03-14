from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget = forms.SelectDateWidget)

    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'due_date', 'category']
