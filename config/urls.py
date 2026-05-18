"""
URL configuration for config project.
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

# Django Debug Toolbar (только в режиме DEBUG)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
