from datetime import date
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from Agenda.consts import DAILY_QUOTES
from Agenda.models import Task, Note, Date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from Agenda.forms import FormularioTask, FormularioNote, FormularioDate
from Agenda.serializers import DateSerializer, NoteSerializer, TaskSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, DestroyAPIView

class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user
    
class HomeView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'home_tasks' 
    template_name = 'Agenda/home.html'
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('priority', 'name')[:5] 

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
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

            context['all_notes'] = Note.objects.filter(owner=self.request.user).order_by('-created_at')[:5]
            
            today = date.today()
            day_of_month = today.day
        
            quote_index = (day_of_month - 1) % len(DAILY_QUOTES) 
            context['daily_quote_text'] = DAILY_QUOTES[quote_index]

            current_month = today.month
            current_year = today.year

            comemorativas_home_raw = Date.objects.filter(
                is_fixed=True,
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
            
            context['importantes_geral_home'] = Date.objects.filter(owner=self.request.user, type='importante').order_by('date')[:5]
                
            return context
    
class ListTasks(ListView, LoginRequiredMixin):
    model = Task
    context_object_name = 'all_tasks_categories' 
    template_name = 'Agenda/Tasks/tasks.html'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('priority', 'name')

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        processed_categories = []
        for task_category_obj in self.get_queryset():
            items_for_display = []
            for i in range(1, 10):
                item_text = getattr(task_category_obj, f'item{i}_text', '')
                if item_text: 
                    items_for_display.append(item_text)
            
            processed_categories.append({
                'task_obj': task_category_obj, 
                'items_for_display': items_for_display 
            })
        context['processed_task_categories'] = processed_categories 

        return context

    
class ListNotes(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'Agenda/Notes/notes.html'
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-created_at')

class ListDates(LoginRequiredMixin, ListView):
    model = Date
    context_object_name = 'dates'
    template_name = 'Agenda/Dates/dates.html'

    def get_queryset(self):
        return Date.objects.filter(owner=self.request.user).order_by('date') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_dates_queryset = self.get_queryset() 
        
        today = date.today()
        current_month = today.month
        current_year = today.year

        comemorativas_raw = Date.objects.filter(
            type='comemorativa',
            is_fixed=True,
            date__month=current_month,
            date__year=current_year
        ).order_by('date')
        
        comemorativas_processed = []
        for d in comemorativas_raw:
            date_data = {
                'obj': d, 
                'month_color_class': d.get_month_color_class(), 
            }
            comemorativas_processed.append(date_data)
        context['comemorativas_home'] = comemorativas_processed 

        importantes_geral_home = all_dates_queryset.filter(
            type='importante',
            owner=self.request.user
        ).order_by('date')
        
        context['importantes_geral_home'] = importantes_geral_home

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
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CreateNote(LoginRequiredMixin, CreateView):
    model = Note
    form_class = FormularioNote
    template_name = 'Agenda/Notes/createNote.html'
    success_url = reverse_lazy('list_notes')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CreateDate(LoginRequiredMixin, CreateView):
    model = Date
    form_class = FormularioDate
    template_name = 'Agenda/Dates/createDate.html'
    success_url = reverse_lazy('list_dates')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateTask(UpdateView, OwnerRequiredMixin):
    model = Task
    form_class = FormularioTask
    template_name = 'Agenda/Tasks/editTask.html'
    success_url = reverse_lazy('list_tasks')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UpdateNote(OwnerRequiredMixin, UpdateView):
    model = Note
    form_class = FormularioNote
    template_name = 'Agenda/Notes/editNote.html'
    success_url = reverse_lazy('list_notes')

class UpdateDate(OwnerRequiredMixin, UpdateView):
    model = Date
    form_class = FormularioDate
    template_name = 'Agenda/Dates/editDate.html'
    success_url = reverse_lazy('list_dates')

class DeleteTask(OwnerRequiredMixin, DeleteView):   
    model = Task
    template_name = 'Agenda/Tasks/deleteTask.html'
    success_url = reverse_lazy('list_tasks')

class DeleteNote(OwnerRequiredMixin, DeleteView):
    model = Note
    template_name = 'Agenda/Notes/deleteNote.html'
    success_url = reverse_lazy('list_notes')

class DeleteDate(OwnerRequiredMixin, DeleteView):
    model = Date
    template_name = 'Agenda/Dates/deleteDate.html'
    success_url = reverse_lazy('list_dates')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_fixed:
            raise Http404("Não é possível excluir uma data fixa.")
        return obj


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'Agenda/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['user_profile'] = user
        context['user_name'] = user.get_full_name() or user.username
        context['user_email'] = user.email or 'Não informado'
        context['user_initials'] = ''.join([name[0] for name in user.get_full_name().split()]).upper() if user.get_full_name() else user.username[0].upper()
        
        context['completed_tasks_count'] = Task.objects.filter(owner=user).count()
        context['created_notes_count'] = Note.objects.filter(owner=user).count()
        context['important_dates_count'] = Date.objects.filter(owner=user).count()
        
        if user.date_joined:
            days_since_joined = (date.today() - user.date_joined.date()).days
            context['days_of_use'] = days_since_joined
        else:
            context['days_of_use'] = 0

        return context

class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication] 

    def get_queryset(self):
        
        return Task.objects.filter(owner=self.request.user).order_by('name')


class NoteListAPIView(ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-created_at')


class DateListAPIView(ListAPIView):
    serializer_class = DateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):

        fixed_dates = Date.objects.filter(is_fixed=True, type='comemorativa').order_by('date')
        user_dates = Date.objects.filter(owner=self.request.user, type='importante').order_by('date')
        return fixed_dates.union(user_dates).order_by('date')
    
class DeleteTaskAPI(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class DeleteNoteAPI(DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class DeleteDateAPI(DestroyAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, is_fixed=False)


class ViewNoteAPI(ListAPIView):
    serializer_class = NoteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-created_at')
