import re


def validate_telegram_chat_id(chat_id):
    """Валидация Telegram Chat ID"""
    if not chat_id:
        return False
    # Chat ID может быть положительным или отрицательным числом
    pattern = r'^-?\d+$'
    return bool(re.match(pattern, str(chat_id)))
