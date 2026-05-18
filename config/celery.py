from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('habit_tracker')

# Загрузка настроек из файла Django с префиксом CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    """Отладочная задача для проверки работы Celery"""
    print(f'Request: {self.request!r}')


@app.task(bind=True)
def ping(self):
    """Проверка связи с Celery"""
    return 'pong'


# Дополнительные настройки для Windows
if os.name == 'nt':  # Если система Windows
    app.conf.update(
        worker_pool='solo',
        task_always_eager=False,
        task_eager_propagates=True,
    )
