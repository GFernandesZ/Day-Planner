from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from Agenda.forms import CustomUserCreationForm
from django.views.generic import CreateView
from django.contrib import messages
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class Login(View):
    def get(self, request):
        contexto = {'mensagem': ''}
        if request.user.is_authenticated:
            return redirect('/Agenda')
        else:
            return render(request, 'login.html', contexto)
    
    def post(self, request):
        usuario = request.POST.get('nome', None)
        senha = request.POST.get('senha', None)

        print(usuario, senha)

        user = authenticate(request, username=usuario, password=senha)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/Agenda/')
            else:
                return render(request, 'login.html', {'mensagem': 'Usuário inativo'})
        else:
            return render(request, 'login.html', {'mensagem': 'Usuário ou senha inválidos'})
        
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)

class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signin.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        messages.success(self.request, 'Sua conta foi criada com sucesso! Faça login para continuar.')
        return response

class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email, # Acessa o campo email do User.
            'first_name': user.first_name,
            'last_name': user.last_name,
        })