from django.contrib import admin
from django.urls import path, include
from Agenda.views import ListTasks

urlpatterns = [
    path('', ListTasks.as_view() , name='home'),
]
