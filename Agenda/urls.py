from django.contrib import admin
from django.urls import path, include
from Agenda.views import *

urlpatterns = [
    path('', HomeView.as_view() , name='home_agenda'),
    path('listar-anotacoes/', ListNotes.as_view(), name='list_notes'),
    path('listar-tarefas/', ListTasks.as_view(), name='list_tasks'),
    path('criar-tarefa/', CreateTask.as_view(), name='create_task'),
    path('criar-anotacao/', CreateNote.as_view(), name='create_note'),
    path('tarefas/<int:pk>/', UpdateTask.as_view(), name='update_task'),
    path('anotacao/<int:pk>/', UpdateNote.as_view(), name='update_note'),
    path('deletar-tarefa/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
    path('deletar-anotacao/<int:pk>/', DeleteNote.as_view(), name='delete_note'),
]
