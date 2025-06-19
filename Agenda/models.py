from django.db import models
from django.utils import timezone
from Agenda.consts import NOTE_BORDER_COLOR_CHOICES # Mantenha se NOTE_BORDER_COLOR_CHOICES estiver em consts.py

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tarefa')
    type = models.CharField(max_length=50, verbose_name='Tipo de Tarefa', default='Pessoais')
    order = models.IntegerField(default=0, verbose_name='Ordem') # O CAMPO PROBLEMÁTICO
    concluded = models.BooleanField(default=False, verbose_name='Concluída')

    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    topic = models.CharField(max_length=100, verbose_name='Tópico', blank=True, null=True)
    content = models.TextField(verbose_name='Conteúdo')
    border_color = models.CharField(
        max_length=20,
        choices=NOTE_BORDER_COLOR_CHOICES, # Assumindo que está em consts.py
        default='border-primary',
        verbose_name='Cor da Borda'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return self.title

class ImportanteDate(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    date = models.DateTimeField(verbose_name='Data')
    description = models.TextField(verbose_name='Descrição', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Data Importante'
        verbose_name_plural = 'Datas Importantes'
        ordering = ['date']

class QuoteOfTheDay(models.Model):
    text = models.TextField(verbose_name='Texto da Frase')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='Autor')
    date = models.DateField(blank=True, null=True, verbose_name='Data (opcional)')
    is_active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Frase do Dia'
        verbose_name_plural = 'Frases do Dia'