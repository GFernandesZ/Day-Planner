from django.forms import ModelForm
from Agenda.models import Task, Note
from django.forms import ModelForm
from django import forms

class FormularioNote(ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'title', 'content', 'border_color', 'foto']
        exclude = []
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Anotação importante...'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: História, Matemática...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite suas anotações aqui...', 'rows': 10}),
            'border_color': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

class FormularioTask(ModelForm):
    class Meta:
        model = Task
        fields = [
            'name', 'priority', 
            'item1_text','item2_text','item3_text',
            'item4_text','item5_text','item6_text',
            'item7_text','item8_text','item9_text',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tarefas Pessoais...'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),

            'item1_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 1'}),
            'item2_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 2'}),
            'item3_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 3'}),
            'item4_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 4'}),
            'item5_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 5'}),
            'item6_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 6'}),
            'item7_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 7'}),
            'item8_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 8'}),
            'item9_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item 9'}),
        }