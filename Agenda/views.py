from datetime import date
import os
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from Agenda.consts import DAILY_QUOTES
from Agenda.models import Task, Note, Date, QuoteOfTheDay
from django.contrib.auth.mixins import LoginRequiredMixin
from Agenda.forms import FormularioTask, FormularioNote, FormularioDate
from django.core.exceptions import ObjectDoesNotExist

from DayPlanner import settings

class HomeView(ListView):
    model = Task
    context_object_name = 'home_tasks' 
    template_name = 'Agenda/home.html'
    def get_queryset(self):
            # Ex: 5 tarefas não concluídas mais recentes ou as de maior ordem.
            # Mantemos esta query para as "home_tasks"
        return Task.objects.all().order_by('priority', 'name')[:5] 

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Pré-processar as tarefas para evitar 'getattribute' no template
            processed_home_tasks = []
            for task_obj in self.get_queryset():
                items_for_display = []
                for i in range(1, 10): 
                    item_text = getattr(task_obj, f'item{i}_text', '')
                    if item_text:
                        items_for_display.append(item_text)
                processed_home_tasks.append({
                    'task_obj': task_obj,
                    'items_for_display': items_for_display
                })
            context['processed_home_tasks'] = processed_home_tasks 

            context['all_notes'] = Note.objects.all().order_by('-created_at')[:5]
            
            today = date.today()
            day_of_month = today.day
        
            quote_index = (day_of_month - 1) % len(DAILY_QUOTES) 
            context['daily_quote_text'] = DAILY_QUOTES[quote_index]

            current_month = today.month
            current_year = today.year

            comemorativas_home_raw = Date.objects.filter(
                type='comemorativa',
                date__month=current_month,
                date__year=current_year
            ).order_by('date')
            
            comemorativas_home_processed = []
            for d in comemorativas_home_raw:
                date_data = {
                    'obj': d, 
                    'month_color_class': d.get_month_color_class(), 
                }
                comemorativas_home_processed.append(date_data)
            context['comemorativas_home'] = comemorativas_home_processed
            
            context['importantes_geral_home'] = Date.objects.filter(type='importante').order_by('date')[:6]
                
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

class ListDates(LoginRequiredMixin, ListView):
    model = Date
    context_object_name = 'dates'
    template_name = 'Agenda/Dates/dates.html'

    def get_queryset(self):
        return Date.objects.all() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_dates = self.get_queryset()
        
        # --- LÓGICA PARA FILTRAR POR MÊS ATUAL ---
        today = date.today()
        current_month = today.month
        current_year = today.year

        # Filtrar Datas Comemorativas APENAS DO MÊS ATUAL E ORDENAR POR DATA
        comemorativas_raw = all_dates.filter(
            type='comemorativa',
            date__month=current_month, # Filtra pelo mês atual
            date__year=current_year    # Filtra pelo ano atual
        ).order_by('date')
        
        # Processa as datas para adicionar a classe de cor do mês
        comemorativas_processed = []
        for d in comemorativas_raw:
            date_data = {
                'obj': d, 
                'month_color_class': d.get_month_color_class(), 
            }
            comemorativas_processed.append(date_data)
        
        context['comemorativas'] = comemorativas_processed
        
        context['importantes_geral'] = all_dates.filter(type='importante').order_by('date')
        
        return context

class ViewNote(DetailView, LoginRequiredMixin):
    model = Note
    context_object_name = 'note'
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

class CreateDate(LoginRequiredMixin, CreateView):
    model = Date
    form_class = FormularioDate
    template_name = 'Agenda/Dates/createDate.html'
    success_url = reverse_lazy('list_dates')


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

class UpdateDate(LoginRequiredMixin, UpdateView):
    model = Date
    form_class = FormularioDate
    template_name = 'Agenda/Dates/editDate.html'
    success_url = reverse_lazy('list_dates')

class DeleteTask(LoginRequiredMixin, DeleteView):   
    model = Task
    template_name = 'Agenda/Tasks/deleteTask.html'
    success_url = reverse_lazy('list_tasks')

class DeleteNote(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'Agenda/Notes/deleteNote.html'
    success_url = reverse_lazy('list_notes')

class DeleteDate(LoginRequiredMixin, DeleteView):
    model = Date
    template_name = 'Agenda/Dates/deleteDate.html'
    success_url = reverse_lazy('list_dates')
