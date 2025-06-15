from django.contrib import admin
from django.urls import path, include # Certifique-se de importar 'include'
from DayPlanner.views import Login, Logout # Importa as views de autenticação do projeto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('Agenda/', include('Agenda.urls'), name='agenda'),
    # path('autenticacao-api/', LoginApi.as_view()),
]