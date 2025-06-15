from django.forms import ModelForm
from Agenda.models import Task
from django.forms import ModelForm

class FormularioVeiculo(ModelForm):
    class Meta:
        model = Task
        exclude = []