"""Скрипт для запуска Telegram бота"""

import os
import django


def main():
    # Устанавливаем настройки Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Инициализируем Django
    django.setup()

    # Импортируем и запускаем бота
    from apps.bot_service.bot import run_bot

    print("🤖 Запуск Telegram бота Steven_habbit_bot...")
    print("Бот запущен и готов к работе!")
    run_bot()


if __name__ == '__main__':
    main()
