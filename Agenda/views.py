from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from Agenda.models import Task, Note, ImportanteDate, QuoteOfTheDay
from django.contrib.auth.mixins import LoginRequiredMixin
from Agenda.forms import FormularioTask, FormularioNote

class HomeView(ListView):
    model = Task, Note, ImportanteDate, QuoteOfTheDay
    context_object_name = 'home'
    template_name = 'Agenda/home.html'

    def get_queryset(self):
        return Task.objects.filter(type='task').order_by('start_date')

class ListTasks(ListView, LoginRequiredMixin):
    model = Task
    context_object_name = 'tasks'
    template_name = 'Agenda/tasks.html'

class ListNotes(ListView, LoginRequiredMixin):
    model = Note
    context_object_name = 'notes'
    template_name = 'Agenda/notes.html'

class CreateTask(CreateView, LoginRequiredMixin):
    model = Task
    form_class = FormularioTask
    template_name = 'Agenda/newTaskhtml'
    success_url = reverse_lazy('list_tasks')

class CreateNote(CreateView, LoginRequiredMixin):
    model = Note
    form_class = FormularioNote
    template_name = 'Agenda/newNote.html'
    success_url = reverse_lazy('list_notes')

class UpdateTask(UpdateView, LoginRequiredMixin):
    model = Task
    form_class = FormularioTask
    template_name = 'Agenda/editTask.html'
    success_url = reverse_lazy('list_tasks')

class UpdateNote(UpdateView, LoginRequiredMixin):
    model = Note
    form_class = FormularioNote
    template_name = 'Agenda/editNote.html'
    success_url = reverse_lazy('list_notes')

class DeleteTask(DeleteView, LoginRequiredMixin):   
    model = Task
    template_name = 'Agenda/deleteTask.html'
    success_url = reverse_lazy('list_tasks')

class DeleteNote(DeleteView, LoginRequiredMixin):
    model = Note
    template_name = 'Agenda/deleteNote.html'
    success_url = reverse_lazy('list_notes')
