from django.contrib import admin
from django.urls import path, include

from .views import users

app_name = 'users'

urlpatterns = [
    path('', users, name='users'),
]
