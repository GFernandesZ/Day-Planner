from django.contrib import admin
from django.urls import path, include
from DayPlanner.views import Login, Logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('Agenda/', include('Agenda.urls'), name='agenda'),
    # path('autenticacao-api/', LoginApi.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)