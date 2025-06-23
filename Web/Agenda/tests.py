from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from Agenda.models import Task, Note, Date, QuoteOfTheDay 
from Agenda.models import IMPORTANT_DATE_TYPE_CHOICES, IMPORTANT_DATE_CATEGORY_CHOICES, IMPORTANT_DATE_COLOR_CHOICES, MONTH_COLORS
from Agenda.consts import NOTE_BORDER_COLOR_CHOICES, TASK_BOX_COLOR_MAP, TASK_BOX_PRIORITY_CHOICES 
from Agenda.forms import FormularioTask, FormularioNote, FormularioDate 

User = get_user_model()

class ModelTests(TestCase):
    """
    Testes para os modelos (Task, Note, Date, QuoteOfTheDay).
    """

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword') 

    def test_task_model_creation(self):
        """Testa a criação de um objeto Task."""
        task = Task.objects.create(
            owner=self.user,
            name="Tarefa P Criada ",
            priority="medium",
            item1_text="Comprar pão",
            item2_text="Estudar Django",
        )
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.name, "Tarefa P Criada ")
        self.assertEqual(task.priority, "medium")
        self.assertEqual(task.item1_text, "Comprar pão")
        self.assertEqual(task.item9_text, "")
        self.assertEqual(task.owner, self.user)
        self.assertEqual(str(task), "Tarefa P Criada ")
        self.assertEqual(task.get_box_color_class(), "task-box-color-medium") # Testa método

    def test_note_model_creation(self):
        """Testa a criação de um objeto Note."""
        note = Note.objects.create(
            owner=self.user,
            title="Revisão de Biologia",
            topic="Genética",
            content="Alelos dominantes e recessivos.",
            border_color="border-primary",
            
        )
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(note.title, "Revisão de Biologia")
        self.assertEqual(note.owner, self.user)
        self.assertEqual(str(note), "Revisão de Biologia")

    def test_date_model_creation(self): 
        """Testa a criação de um objeto Date."""
        today = timezone.now()
        date_obj = Date.objects.create( 
            owner=self.user,
            title="Aniversário do Chefe",
            date=today,
            description="Lembrar de comprar bolo.",
            type="importante",
            category="pessoal",
            color="warning",
            is_fixed=False
        )
        self.assertEqual(Date.objects.count(), 1)
        self.assertEqual(date_obj.title, "Aniversário do Chefe")
        self.assertEqual(date_obj.type, "importante")
        self.assertEqual(date_obj.owner, self.user)
        self.assertEqual(str(date_obj), "Aniversário do Chefe")
        self.assertEqual(date_obj.get_month_color_class(), MONTH_COLORS.get(today.month))


class ViewTests(TestCase):
    """
    Testes para as views (URLs, templates, formulários).
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='otheruser', password='otherpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword') 


        Task.objects.create(owner=self.user, name="Pessoal", priority="high", item1_text="Item 1")
        Task.objects.create(owner=self.user, name="Estudantil", priority="medium", item1_text="Item A")
        Task.objects.create(owner=self.user2, name="Outro User Task", priority="low", item1_text="Item Z") 


        Note.objects.create(owner=self.user, title="Minha Anotação", topic="Geral", content="Conteúdo da anotação.")
        Note.objects.create(owner=self.user2, title="Anotação de Outro", topic="Estudo", content="Outro conteúdo.")


        self.current_month_fixed_date = Date.objects.create( 
            owner=self.admin_user,
            title="Natal Fixo",
            date=timezone.now().replace(day=25, hour=0, minute=0, second=0, microsecond=0),
            type="comemorativa",
            category="religiosa",
            color="danger",
            is_fixed=True
        )
        self.user_date_obj = Date.objects.create( 
            owner=self.user,
            title="Meu Aniversário",
            date=timezone.now() + timedelta(days=5),
            type="importante",
            category="pessoal",
            color="warning",
            is_fixed=False
        )
        
        Date.objects.create(
            owner=self.admin_user,
            title="Dia do Trabalho Fixo",
            date=timezone.now().replace(month=5, day=1, hour=0, minute=0, second=0, microsecond=0), 
            type="comemorativa",
            category="nacional",
            color="primary",
            is_fixed=True
        )

    
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_page_renders(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_user_registration(self):
        
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home_agenda'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Olá, testuser") 

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(self.client.session.get('_auth_user_id')) 

    def test_list_dates_filters_correctly(self): 
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('list_dates')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Agenda/Dates/dates.html')

        
        self.assertEqual(len(response.context['comemorativas_home']), 1) 
        self.assertEqual(response.context['comemorativas_home'][0]['obj'], self.current_month_fixed_date)
        self.assertContains(response, self.current_month_fixed_date.title)
        self.assertNotContains(response, "Dia do Trabalho Fixo") 

        
        self.assertEqual(len(response.context['importantes_geral_home']), 1) 
        self.assertEqual(response.context['importantes_geral_home'][0], self.user_date_obj) 
        self.assertContains(response, self.user_date_obj.title) 



    def test_create_task_assigns_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_task'), {
            'name': 'Tarefa do TestUser',
            'priority': 'low',
            'item1_text': 'Novo item',
            'item2_text': '',
            'item3_text': '',
            'item4_text': '',
            'item5_text': '',
            'item6_text': '',
            'item7_text': '',
            'item8_text': '',
            'item9_text': '',
        })
        self.assertEqual(response.status_code, 302) 
        new_task = Task.objects.get(name='Tarefa do TestUser')
        self.assertEqual(new_task.owner, self.user)

    def test_update_note_only_by_owner(self):
        note_to_update = Note.objects.create(owner=self.user, title="Nota para Editar", content="Conteúdo")
        
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(reverse('update_note', kwargs={'pk': note_to_update.pk}), {
            'title': 'Nota Editada por Outro',
            'topic': 'Tópico Novo',
            'content': 'Conteúdo Editado',
            'border_color': 'border-danger'
        })
        self.assertEqual(response.status_code, 403) 
        self.assertEqual(Note.objects.get(pk=note_to_update.pk).title, "Nota para Editar")

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('update_note', kwargs={'pk': note_to_update.pk}), {
            'title': 'Nota Editada por TestUser',
            'topic': 'Tópico Novo',
            'content': 'Conteúdo Editado',
            'border_color': 'border-danger'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Note.objects.get(pk=note_to_update.pk).title, "Nota Editada por TestUser")

    def test_delete_date_fixed_cannot_be_deleted(self):
        """
        Testa que datas comemorativas fixas não podem ser excluídas por nenhum usuário.
        """

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_date', kwargs={'pk': self.current_month_fixed_date.pk})) 

        self.assertEqual(response.status_code, 404) 
        self.assertTrue(Date.objects.filter(pk=self.current_month_fixed_date.pk).exists()) 


        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('delete_date', kwargs={'pk': self.current_month_fixed_date.pk})) 

        self.assertEqual(response.status_code, 404) 
        self.assertTrue(Date.objects.filter(pk=self.current_month_fixed_date.pk).exists())


    def test_delete_user_owned_date(self):
        date_to_delete = Date.objects.create( 
            owner=self.user, title="Data para Deletar", date=timezone.now(), type="importante"
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_date', kwargs={'pk': date_to_delete.pk})) # CORRIGIDO
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(Date.objects.filter(pk=date_to_delete.pk).exists())