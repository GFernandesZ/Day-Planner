from django.db import models
from datetime import datetime
from Agenda.consts import *
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='personal', verbose_name='Tipo')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Data de Início')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Data de Término')
    concluded = models.BooleanField(default=False, verbose_name='Concluído')

class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    topic = models.CharField(max_length=100, verbose_name='Tópico', blank=True, null=True)
    content = models.TextField(verbose_name='Conteúdo')
    border_color = models.CharField(
        max_length=20,
        choices=NOTE_BORDER_COLOR_CHOICES,
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
    date = models.DateField(blank=True, null=True, verbose_name='Data (opcional)') # Se a frase for para uma data específica
    is_active = models.BooleanField(default=True, verbose_name='Ativa') # Para controlar qual frase exibir

    class Meta:
        verbose_name = 'Frase do Dia'
        verbose_name_plural = 'Frases do Dia'
        