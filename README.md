# 🏃 HabitTracker - Система отслеживания привычек с Telegram ботом

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.5-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17.1-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 О проекте

**HabitTracker** — это веб-приложение для формирования и отслеживания полезных привычек, вдохновлённое книгой Джеймса Клира «Атомные привычки». Проект включает Telegram бота для ежедневных напоминаний и мотивации.

### 🎯 Основные возможности

- ✅ Регистрация и авторизация пользователей (JWT)
- ✅ Управление привычками (CRUD)
- ✅ Публичные привычки (обмен опытом)
- ✅ Telegram бот с напоминаниями
- ✅ Пагинация (5 привычек на страницу)
- ✅ Статистика выполнения привычек
- ✅ Документация API (Swagger/ReDoc)

---

## 🛠 Технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.13+ | Язык программирования |
| **Django** | 6.0.5 | Веб-фреймворк |
| **Django REST Framework** | 3.17.1 | API фреймворк |
| **PostgreSQL** | 15+ | База данных |
| **JWT** | - | Аутентификация |
| **Celery** | 5.6.3 | Асинхронные задачи |
| **Redis** | 7.4+ | Брокер сообщений |
| **python-telegram-bot** | 22.7 | Telegram бот |
| **drf-yasg** | 1.21.15 | Swagger документация |
| **django-celery-beat** | 2.9.0 | Периодические задачи |

---

## 📁 Структура проекта
```
habit\_tracker/
├── config/ # Конфигурация проекта
│ ├── settings.py # Настройки Django
│ ├── urls.py # Главные маршруты
│ └── celery.py # Настройки Celery
│
├── apps/ # Приложения проекта
│ ├── users/ # Управление пользователями
│ │ ├── models.py # User, Payment
│ │ ├── views.py # Регистрация, авторизация
│ │ └── serializers.py # Сериализаторы
│ │
│ ├── habits/ # Управление привычками
│ │ ├── models.py # Habit, HabitExecution
│ │ ├── views.py # CRUD операции
│ │ ├── serializers.py # Сериализаторы
│ │ ├── permissions.py # Права доступа
│ │ ├── pagination.py # Пагинация
│ │ ├── validators.py # Валидация
│ │ └── tests.py # Тесты
│ │
│ └── bot\_service/ # Telegram бот
│ ├── bot.py # Обработчики команд
│ ├── tasks.py # Celery задачи
│ └── keyboards.py # Клавиатуры
│
├── static/ # Статические файлы
├── media/ # Загруженные файлы
├── logs/ # Логи приложения
│
├── .env # Переменные окружения
├── .env.example # Пример .env файла
├── requirements.txt # Зависимости
├── run\_bot.py # Запуск бота
├── check\_services.py # Проверка сервисов
├── start\_all.bat # Запуск всех сервисов (Windows)
├── stop\_all.bat # Остановка сервисов (Windows)
└── README.md # Документация
```
## 🚀 Быстрый старт

### 1. Клонирование репозитория

```
git clone https://github.com/yourusername/habit\_tracker.git

cd habit\_tracker
```
### 2. Создание виртуального окружения


*Windows*
```
python -m venv .venv

.venv\Scripts\activate
```

*Linux/Mac*
```
python -m venv .venv

source .venv/bin/activate
```
### 3. Установка зависимостей

```
pip install -r requirements.txt
```
### 4. Настройка базы данных PostgreSQL
```
sql

CREATE DATABASE habit\_tracker\_db;

CREATE USER habit\_user WITH PASSWORD 'your\_password';

ALTER ROLE habit\_user SET client\_encoding TO 'utf8';

GRANT ALL PRIVILEGES ON DATABASE habit\_tracker\_db TO habit\_user;
```
### 5. Настройка переменных окружения

```

cp .env.example .env

*# Отредактируйте .env, указав свои данные*
```
**Основные переменные:**

| Переменная | Описание |
| --- | --- |
| SECRET\_KEY | Секретный ключ Django (сгенерируйте свой) |
| DB\_NAME | Имя базы данных |
| DB\_USER | Пользователь PostgreSQL |
| DB\_PASSWORD | Пароль PostgreSQL |
| TELEGRAM\_BOT\_TOKEN | Токен бота от @BotFather |
| TELEGRAM\_BOT\_USERNAME | Username бота |

### 6. Применение миграций

```
python manage.py makemigrations users

python manage.py makemigrations habits

python manage.py migrate
```
### 7. Создание суперпользователя

```
python manage.py createsuperuser
```
## 🤖 Настройка Telegram бота

### Регистрация бота

1. Найдите в Telegram [@BotFather](https://t.me/BotFather)
2. Отправьте команду /newbot
3. Укажите имя бота (например: HabitTrackerBot)
4. Укажите username (должен заканчиваться на \_bot)
5. Скопируйте полученный токен в .env файл

### Получение Chat ID

После запуска бота отправьте команду /start — бот покажет ваш Chat ID.

## 🚀 Запуск проекта

### Windows (один клик)



*Запуск всех сервисов*
```
start\_all.bat
```
*Остановка всех сервисов*
```
stop\_all.bat
```
### Ручной запуск (Windows/Linux)



*Терминал 1: Redis*
```
redis-server
```
*Терминал 2: Celery Worker*
```
celery -A config worker -l INFO -P eventlet --pool=solo
```
*Терминал 3: Celery Beat*
```
celery -A config beat -l INFO
```
*Терминал 4: Django сервер*
```
python manage.py runserver
```
*Терминал 5: Telegram бот*
```
python run\_bot.py
```
### Проверка работоспособности

```
python check\_services.py
```
**Ожидаемый вывод:**

text

✅ Redis: подключен

✅ PostgreSQL: подключена

✅ Celery: работает

✅ Telegram Bot: работает (@your\_bot\_username)

Результат: 4/4 сервисов работают

✅ Все сервисы работают корректно!

## 📡 API Эндпоинты

### Пользователи

| Method | Endpoint | Описание |
| --- | --- | --- |
| POST | /api/users/register/ | Регистрация |
| POST | /api/users/login/ | Авторизация (JWT) |
| POST | /api/users/refresh/ | Обновление токена |
| GET | /api/users/profile/ | Профиль пользователя |
| PATCH | /api/users/set-telegram-id/ | Привязка Telegram |
| PATCH | /api/users/set-telegram-notifications/ | Настройка уведомлений |

### Привычки

| Method | Endpoint | Описание |
| --- | --- | --- |
| GET | /api/habits/habits/ | Список привычек (пагинация) |
| POST | /api/habits/habits/ | Создание привычки |
| GET | /api/habits/habits/{id}/ | Детали привычки |
| PUT/PATCH | /api/habits/habits/{id}/ | Обновление привычки |
| DELETE | /api/habits/habits/{id}/ | Удаление привычки |
| GET | /api/habits/habits/public/ | Публичные привычки |
| POST | /api/habits/habits/{id}/toggle-public/ | Сделать публичной |
| GET | /api/habits/habits/{id}/executions/ | История выполнения |
| POST | /api/habits/habits/{id}/complete/ | Отметить выполнение |

### Документация

| Method | Endpoint | Описание |
| --- | --- | --- |
| GET | /swagger/ | Swagger UI |
| GET | /redoc/ | ReDoc документация |

## ✅ Правила валидации привычек

| № | Правило | Описание |
| --- | --- | --- |
| 1 | ❌ | Нельзя одновременно указать связанную привычку и вознаграждение |
| 2 | ⏱ | Время выполнения не должно превышать **120 секунд** |
| 3 | 🔗 | Связанная привычка должна быть **приятной** |
| 4 | 🎁 | У приятной привычки не может быть вознаграждения или связанной привычки |
| 5 | 📅 | Привычка должна выполняться **не реже 1 раза в 7 дней** |

## 📱 Команды Telegram бота

| Команда | Описание |
| --- | --- |
| /start | Начать работу с ботом |
| /help | Показать список команд |
| /my\_id | Показать ваш Chat ID |
| /about | Информация о боте |

## 🧪 Тестирование

### Запуск тестов



*Запуск всех тестов*
```
python manage.py test
```
*Запуск тестов с покрытием*
```
coverage run manage.py test

coverage report

coverage html
```
### Результат тестов

text

Ran 21 tests in 10.358s

OK

## 📊 Модели данных

### Habit (Привычка)

| Поле | Тип | Описание |
| --- | --- | --- |
| user | ForeignKey | Владелец привычки |
| place | CharField | Место выполнения |
| time | TimeField | Время выполнения |
| action | CharField | Действие |
| is\_pleasant | BooleanField | Признак приятной привычки |
| related\_habit | ForeignKey | Связанная привычка |
| reward | CharField | Вознаграждение |
| periodicity | CharField | Периодичность |
| execution\_time | PositiveIntegerField | Время выполнения (сек) |
| is\_public | BooleanField | Публичная привычка |

### HabitExecution (Выполнение)

| Поле | Тип | Описание |
| --- | --- | --- |
| habit | ForeignKey | Связанная привычка |
| execution\_date | DateField | Дата выполнения |
| status | CharField | Статус (выполнено/пропущено) |
| notes | TextField | Заметки |

## 🔧 Устранение неполадок

### Redis не запускается

bash

*Проверка порта*
```
netstat -ano | findstr :6379
```
*Завершение процесса*
```
taskkill /PID <PID> /F
```
### Celery не работает на Windows



*Убедитесь, что установлен eventlet*
```
pip install eventlet
```
*Запуск с правильными параметрами*
```
celery -A config worker -l INFO -P eventlet --pool=solo
```
### Бот не отвечает

1. Проверьте токен в .env
2. Убедитесь, что бот зарегистрирован в @BotFather
3. Проверьте что запущен python run\_bot.py

## 📝 Лицензия

MIT License

## 👨‍💻 Контакты

* **Разработчик:** Степан Прокопьев
* **Telegram:** @Steven\_habbit\_bot
* **Email:** support@habittracker.com

## ⭐ Благодарности

* Джеймс Клир за книгу «Атомные привычки»
* Команда Django и DRF за отличные инструменты
* Сообщество python-telegram-bot за помощь

**© 2026 HabitTracker. Все права защищены.**