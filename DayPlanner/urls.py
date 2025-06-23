from django.contrib import admin
from django.urls import path, include
from DayPlanner.views import Login, Logout, RegisterUser, LoginAPI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('Agenda/', include('Agenda.urls'), name='agenda'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='api_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)