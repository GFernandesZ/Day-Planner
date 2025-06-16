from django.forms import ModelForm
from Agenda.models import Task
from django.forms import ModelForm

class FormularioNote(ModelForm):
    class Meta:
        model = Task
        exclude = []

class FormularioTask(ModelForm):
    class Meta:
        model = Task
        exclude = []