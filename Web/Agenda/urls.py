from django.contrib import admin
from django.urls import path, include
from Agenda.views import *

urlpatterns = [
    path('', HomeView.as_view() , name='home_agenda'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('listar-anotacoes/', ListNotes.as_view(), name='list_notes'),
    path('anotacao/ver/<int:pk>/', ViewNote.as_view(), name='view_note'),
    path('listar-datas/', ListDates.as_view(), name='list_dates'),
    path('listar-tarefas/', ListTasks.as_view(), name='list_tasks'),
    path('criar-tarefa/', CreateTask.as_view(), name='create_task'),
    path('criar-anotacao/', CreateNote.as_view(), name='create_note'),
    path('criar-data/', CreateDate.as_view(), name='create_date'),
    path('tarefas/<int:pk>/', UpdateTask.as_view(), name='update_task'),
    path('anotacao/<int:pk>/', UpdateNote.as_view(), name='update_note'),
    path('datas/editar/<int:pk>/', UpdateDate.as_view(), name='update_date'),
    path('deletar-tarefa/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
    path('datas/deletar/<int:pk>/', DeleteDate.as_view(), name='delete_date'),
    path('deletar-anotacao/<int:pk>/', DeleteNote.as_view(), name='delete_note'),

    path('api/tasks/', TaskListAPIView.as_view(), name='api_tasks_list'),
    path('api/notes/', NoteListAPIView.as_view(), name='api_notes_list'),
    path('api/dates/', DateListAPIView.as_view(), name='api_dates_list'),
    path('api/tasks/delete/<int:pk>/', DeleteTaskAPI.as_view(), name='api_delete_task'),
    path('api/notes/delete/<int:pk>/', DeleteNoteAPI.as_view(), name='api_delete_note'),
    path('api/dates/delete/<int:pk>/', DeleteDateAPI.as_view(), name='api_delete_date'),
    path('api/notes/ver/<int:pk>/', ViewNoteAPI.as_view(), name='api_view_note'),
]

