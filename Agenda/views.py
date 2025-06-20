import os
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from Agenda.models import Task, Note, ImportanteDate, QuoteOfTheDay
from django.contrib.auth.mixins import LoginRequiredMixin
from Agenda.forms import FormularioTask, FormularioNote
from django.core.exceptions import ObjectDoesNotExist

from DayPlanner import settings

class HomeView(ListView):
    model = Task
    context_object_name = 'home_tasks' 
    template_name = 'Agenda/home.html'

    def get_queryset(self):
        return Task.objects.all().order_by('priority', 'name')[:5] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        processed_home_tasks = []
        for task_obj in self.get_queryset():
            items_for_display = []
            for i in range(1, 10): # Loop para 9 itens
                item_text = getattr(task_obj, f'item{i}_text', '')
                if item_text: # Só adiciona se tiver texto
                    items_for_display.append(item_text)
            processed_home_tasks.append({
                'task_obj': task_obj,
                'items_for_display': items_for_display
            })
        context['processed_home_tasks'] = processed_home_tasks # NOVA VARIÁVEL DE CONTEXTO

        context['all_notes'] = Note.objects.all().order_by('-created_at')[:5]
        context['all_important_dates'] = ImportanteDate.objects.all().order_by('date')[:5]
        context['daily_quote'] = QuoteOfTheDay.objects.filter(is_active=True).order_by('?').first()
        return context
    
class ListTasks(ListView, LoginRequiredMixin):
    model = Task
    context_object_name = 'all_tasks_categories' 
    template_name = 'Agenda/Tasks/tasks.html'

    def get_queryset(self):
        # Ordena as categorias de tarefas por prioridade e depois por nome
        return Task.objects.all().order_by('priority', 'name') 

    def get_context_data(self, **kwargs):
        # Prepara a lista de itens para cada tarefa para ser exibida no template
        context = super().get_context_data(**kwargs)
        
        processed_categories = []
        for task_category_obj in self.get_queryset():
            items_for_display = []
            for i in range(1, 10):
                item_text = getattr(task_category_obj, f'item{i}_text', '')
                if item_text: # Apenas adiciona o item se ele não estiver em branco
                    items_for_display.append(item_text)
            
            processed_categories.append({
                'task_obj': task_category_obj, # O objeto Task completo
                'items_for_display': items_for_display # Lista de strings de itens não vazios
            })
        context['processed_task_categories'] = processed_categories # Nova variável de contexto

        return context

    
class ListNotes(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'Agenda/Notes/notes.html'

class ViewNote(DetailView, LoginRequiredMixin): # NOVA VIEW
    model = Note
    context_object_name = 'note' # O objeto Note será acessível como 'note' no template
    template_name = 'Agenda/Notes/detailNote.html'

def upload_imagem(request):
    if request.method == 'POST':
        form = FormularioNote(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_imagem')
    else:
        form = FormularioNote()
    return render(request, 'createNote.html', {'form': form})

class CreateTask(CreateView, LoginRequiredMixin):
    model = Task
    form_class = FormularioTask
    template_name = 'Agenda/Tasks/createTask.html'
    success_url = reverse_lazy('list_tasks')

    def form_valid(self, form):
        return super().form_valid(form)

class CreateNote(LoginRequiredMixin, CreateView):
    model = Note
    form_class = FormularioNote
    template_name = 'Agenda/Notes/createNote.html'
    success_url = reverse_lazy('list_notes')

class UpdateTask(UpdateView, LoginRequiredMixin):
    model = Task
    form_class = FormularioTask
    template_name = 'Agenda/Tasks/editTask.html'
    success_url = reverse_lazy('list_tasks')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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
