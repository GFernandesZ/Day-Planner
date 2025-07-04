from django.urls import reverse
from rest_framework import serializers
from Agenda.models import Task, Note, Date
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    items_list_display = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'owner', 'name', 'priority', 'items_list_display']
        read_only_fields = ['owner']

    def get_items_list_display(self, obj):
        return [getattr(obj, f'item{i}_text') for i in range(1, 10) if getattr(obj, f'item{i}_text')]

class NoteSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'owner', 'title', 'topic', 'content', 'border_color', 'foto_url', 'created_at']
        read_only_fields = ['owner', 'created_at']

    def get_foto_url(self, obj):
        if obj.foto and hasattr(obj.foto, 'name'):
            return reverse('foto_anotacao', kwargs={'filename': obj.foto.name.split('/')[-1]})
        return None

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ['id', 'owner', 'title', 'date', 'description', 'type', 'category', 'color', 'is_fixed', 'created_at']
        read_only_fields = ['owner', 'is_fixed', 'created_at']
