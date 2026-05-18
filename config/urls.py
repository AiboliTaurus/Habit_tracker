"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Схема для Swagger документации
schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version='v1',
        description="""API для отслеживания привычек с Telegram интеграцией

## Возможности:
- Регистрация и авторизация пользователей
- Управление привычками (CRUD)
- Публичные привычки
- Telegram бот для напоминаний
- Пагинация (5 привычек на страницу)
- JWT аутентификация

## Правила валидации:
1. Нельзя одновременно указать связанную привычку и вознаграждение
2. Время выполнения не более 120 секунд
3. Связанная привычка должна быть приятной
4. У приятной привычки не может быть вознаграждения или связанной привычки
5. Привычка должна выполняться не реже 1 раза в 7 дней
""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@habittracker.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Swagger документация
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API эндпоинты
    path('api/users/', include('apps.users.urls')),
    path('api/habits/', include('apps.habits.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
