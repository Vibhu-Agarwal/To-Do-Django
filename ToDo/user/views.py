from django.shortcuts import render, redirect
from .forms import *
from .models import *


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todolist:homepage')
        else:
            return render(request, 'error.html', {'detail': 'Invalid Form!'})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
