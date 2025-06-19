from django.forms import ModelForm
from Agenda.models import Task, Note
from django.forms import ModelForm
from django import forms

class FormularioNote(ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'title', 'content', 'border_color']
        exclude = []
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Anotação importante...'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: História, Matemática...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite suas anotações aqui...', 'rows': 10}),
            'border_color': forms.Select(attrs={'class': 'form-select'}),
        }

class FormularioTask(ModelForm):
    class Meta:
        model = Task
        fields = ['type', 'title', 'order', 'concluded']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Pessoais, Estudantis...'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a tarefa (ex: Fazer compras)'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ordem (1, 2, 3...)', 'min': 0}), # Input numérico
            'concluded': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }