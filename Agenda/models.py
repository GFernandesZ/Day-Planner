from django.db import models
from django.utils import timezone
from Agenda.consts import IMPORTANT_DATE_CATEGORY_CHOICES, IMPORTANT_DATE_COLOR_CHOICES, IMPORTANT_DATE_TYPE_CHOICES, MONTH_COLORS, NOTE_BORDER_COLOR_CHOICES, TASK_BOX_COLOR_MAP, TASK_BOX_PRIORITY_CHOICES

class Task(models.Model):
    name = models.CharField(max_length=20, verbose_name='Nome da Categoria')
    priority = models.CharField(
        max_length=20,
        choices=TASK_BOX_PRIORITY_CHOICES,
        default='medium',
        verbose_name='Prioridade da Categoria'
    )
    item1_text = models.CharField(max_length=30, blank=True, verbose_name='Item 1')
    item2_text = models.CharField(max_length=30, blank=True, verbose_name='Item 2')
    item3_text = models.CharField(max_length=30, blank=True, verbose_name='Item 3')
    item4_text = models.CharField(max_length=30, blank=True, verbose_name='Item 4')
    item5_text = models.CharField(max_length=30, blank=True, verbose_name='Item 5')
    item6_text = models.CharField(max_length=30, blank=True, verbose_name='Item 6')
    item7_text = models.CharField(max_length=30, blank=True, verbose_name='Item 7')
    item8_text = models.CharField(max_length=30, blank=True, verbose_name='Item 8')
    item9_text = models.CharField(max_length=30, blank=True, verbose_name='Item 9')

    def get_box_color_class(self):
        return TASK_BOX_COLOR_MAP.get(self.priority, 'task-box-color-medium')

    def __str__(self):
        return self.name

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
    foto = models.ImageField(upload_to='Agenda/fotos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return self.title

class Date(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título')
    date = models.DateTimeField(verbose_name='Data', blank=True, null=True)
    description = models.TextField(verbose_name='Descrição', blank=True, null=True)

    type = models.CharField(max_length=20, choices=IMPORTANT_DATE_TYPE_CHOICES, default='comemorativa', verbose_name='Tipo')
    category = models.CharField(max_length=20, choices=IMPORTANT_DATE_CATEGORY_CHOICES, blank=True, null=True, verbose_name='Categoria')
    color = models.CharField(max_length=20, choices=IMPORTANT_DATE_COLOR_CHOICES, default='success', verbose_name='Cor')

    # NOVO CAMPO: Para marcar datas que não podem ser excluídas pelo usuário
    is_fixed = models.BooleanField(default=False, verbose_name='Data Fixa (Não Excluível)')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Data Importante'
        verbose_name_plural = 'Datas Importantes'
        ordering = ['date']

    def get_month_color_class(self):
        if self.date:
            return MONTH_COLORS.get(self.date.month, 'bg-secondary')  # Padrão cinza
        return 'bg-secondary'

    def __str__(self):
        return self.title


class QuoteOfTheDay(models.Model):
    text = models.TextField(verbose_name='Texto da Frase')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='Autor')
    date = models.DateField(blank=True, null=True, verbose_name='Data (opcional)')
    is_active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Frase do Dia'
        verbose_name_plural = 'Frases do Dia'