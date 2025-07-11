# Generated by Django 5.2.3 on 2025-06-22 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agenda', '0006_alter_note_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('date', models.DateTimeField(verbose_name='Data')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('type', models.CharField(choices=[('comemorativa', 'Comemorativa'), ('importante', 'Importante')], default='comemorativa', max_length=20, verbose_name='Tipo')),
                ('category', models.CharField(blank=True, choices=[('nacional', 'Nacional'), ('internacional', 'Internacional'), ('religiosa', 'Religiosa'), ('especial', 'Especial'), ('pessoal', 'Pessoal'), ('academica', 'Acadêmica'), ('profissional', 'Profissional'), ('historica', 'Histórica')], max_length=20, null=True, verbose_name='Categoria')),
                ('color', models.CharField(choices=[('success', 'Verde (Padrão Comemorativa)'), ('primary', 'Azul'), ('danger', 'Vermelho'), ('warning', 'Amarelo'), ('info', 'Azul Claro'), ('secondary', 'Cinza')], default='success', max_length=20, verbose_name='Cor')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
            ],
            options={
                'verbose_name': 'Data Importante',
                'verbose_name_plural': 'Datas Importantes',
                'ordering': ['date'],
            },
        ),
        migrations.DeleteModel(
            name='ImportanteDate',
        ),
    ]
