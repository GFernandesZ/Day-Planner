from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from Agenda.models import Task, Note, ImportanteDate, QuoteOfTheDay
from django.contrib.auth.mixins import LoginRequiredMixin
from Agenda.forms import FormularioTask, FormularioNote

class HomeView(ListView):
    model = Task
    context_object_name = 'home_tasks'
    template_name = 'Agenda/home.html'

    def get_queryset(self):
        return Task.objects.filter(concluded=False).order_by('order', 'title')[:5] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_notes'] = Note.objects.all().order_by('-created_at')[:5]
        context['all_important_dates'] = ImportanteDate.objects.all().order_by('date')
        context['daily_quote'] = QuoteOfTheDay.objects.filter(is_active=True).order_by('?').first()
        return context

class ListTasks(ListView, LoginRequiredMixin):
    model = Task
    context_object_name = 'all_tasks'
    template_name = 'Agenda/Tasks/tasks.html'

    def get_queryset(self):
        # Ordena por: não concluídas primeiro, depois por ordem, depois por título.
        return Task.objects.all().order_by('concluded', 'order', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        distinct_task_types = list(self.get_queryset().values_list('type', flat=True).distinct())
        default_order_types = ['Pessoais', 'Estudantis', 'Profissionais']
        sorted_task_types = sorted(distinct_task_types, 
                                   key=lambda x: (default_order_types.index(x) if x in default_order_types else len(default_order_types), x))

        context['task_categories'] = []
        for task_type_name in sorted_task_types:
            tasks_by_type = self.get_queryset().filter(type=task_type_name)
            context['task_categories'].append({
                'type_name': task_type_name, 
                'tasks': tasks_by_type,
            })
        return context
    
class ListNotes(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'Agenda/Notes/notes.html'

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = FormularioTask
    template_name = 'Agenda/Tasks/createTask.html'
    success_url = reverse_lazy('list_tasks')

class CreateNote(LoginRequiredMixin, CreateView):
    model = Note
    form_class = FormularioNote
    template_name = 'Agenda/Notes/createNote.html'
    success_url = reverse_lazy('list_notes')

class UpdateTask(LoginRequiredMixin,UpdateView ):
    model = Task
    form_class = FormularioTask
    template_name = 'Agenda/Tasks/editTask.html'
    success_url = reverse_lazy('list_tasks')

class UpdateNote(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = FormularioNote
    template_name = 'Agenda/Notes/editNote.html'
    success_url = reverse_lazy('list_notes')

class DeleteTask(LoginRequiredMixin, DeleteView):   
    model = Task
    template_name = 'Agenda/Tasks/deleteTask.html'
    success_url = reverse_lazy('list_tasks')

class DeleteNote(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'Agenda/Notes/deleteNote.html'
    success_url = reverse_lazy('list_notes')
