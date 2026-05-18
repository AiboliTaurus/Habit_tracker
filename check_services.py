#!/usr/bin/env python
"""Скрипт для проверки работоспособности всех сервисов"""

import os
import django
import redis
import asyncio
from telegram import Bot


def check_redis():
    """Проверка подключения к Redis"""
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Redis: подключен")
        return True
    except Exception as e:
        print(f"❌ Redis: ошибка - {e}")
        return False


def check_celery():
    """Проверка Celery"""
    try:
        from config.celery import app
        app.send_task('ping')
        print("✅ Celery: работает")
        return True
    except Exception as e:
        print(f"❌ Celery: ошибка - {e}")
        return False


def check_database():
    """Проверка подключения к БД"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        django.setup()
        from django.db import connection
        connection.ensure_connection()
        print("✅ PostgreSQL: подключена")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL: ошибка - {e}")
        return False


async def check_telegram_bot_async():
    """Асинхронная проверка Telegram бота"""
    try:
        from django.conf import settings
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Telegram Bot: работает (@{me.username})")
        return True
    except Exception as e:
        print(f"❌ Telegram Bot: ошибка - {e}")
        return False


def check_telegram_bot():
    """Синхронная обёртка для проверки Telegram бота"""
    return asyncio.run(check_telegram_bot_async())


def main():
    print("=" * 50)
    print("Проверка работоспособности сервисов HabitTracker")
    print("=" * 50)
    print()

    results = []

    # Проверка Redis
    results.append(check_redis())

    # Проверка PostgreSQL
    results.append(check_database())

    # Проверка Celery
    results.append(check_celery())

    # Проверка Telegram бота
    results.append(check_telegram_bot())

    print()
    print("=" * 50)
    total = len(results)
    success = sum(results)
    print(f"Результат: {success}/{total} сервисов работают")

    if success == total:
        print("✅ Все сервисы работают корректно!")
    else:
        print("⚠️ Некоторые сервисы не работают. Проверьте конфигурацию.")

    print("=" * 50)


if __name__ == '__main__':
    main()
