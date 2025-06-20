import os
from django.http import FileResponse, Http404
from django.shortcuts import render
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
        # Vai pegar as 5 tarefas mais prioritárias/recentes
        # Se 'order' não está mais em Task, remova-o daqui.
        # As últimas instruções removeram 'order' do modelo Task.
        # então deve ser: return Task.objects.all().order_by('priority', 'name')[:5] 
        return Task.objects.all().order_by('priority', 'name')[:5] 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # O problema 'getattribute' não deve mais ocorrer na home.html
        # Se usar `task_obj|getattribute:"item"|add:i|add:"_text"` diretamente
        # será `AttributeError` no template.
        # Solução para isso: ou usar um filtro customizado `attribute`,
        # ou passar os dados já processados da view.

        # PARA EVITAR GETATTRIBUTE NO TEMPLATE, PRE-PROCESSAR AQUI:
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

class FotoAnotacoes(LoginRequiredMixin, View):
    def get(self, request, arquivo): 
        try:
            note = note.objects.filter(foto='Agenda/fotos/{}'.format(arquivo)).first()

            print(note)
            
            return FileResponse(note.foto)
        except ObjectDoesNotExist:
            raise Http404('Fotos não encontradas ou acesso não autorizado')
        except Exception as exception:
            raise exception

class ViewNote(DetailView, LoginRequiredMixin): # NOVA VIEW
    model = Note
    context_object_name = 'note' # O objeto Note será acessível como 'note' no template
    template_name = 'Agenda/Notes/detailNote.html'

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
