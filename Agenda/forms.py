from django.forms import ModelForm
from Agenda.models import Task, Note
from django.forms import ModelForm

class FormularioNote(ModelForm):
    class Meta:
        model = Note
        exclude = []

class FormularioTask(ModelForm):
    class Meta:
        model = Task
        exclude = []