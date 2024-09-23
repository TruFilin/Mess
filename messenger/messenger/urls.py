from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),  # Замените your_app на имя вашего приложения
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Добавь этот путь
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

