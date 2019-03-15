from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='Sign-Up')
]