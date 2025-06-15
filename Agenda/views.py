from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from Agenda.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin

class ListTasks(ListView, LoginRequiredMixin):
    model = Task
    context_object_name = 'tasks'
    template_name = 'Agenda/home.html'