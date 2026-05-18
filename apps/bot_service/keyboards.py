from telegram import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard(is_registered=False):
    """Главная клавиатура бота"""
    buttons = [
        [KeyboardButton("/start"), KeyboardButton("/help")],
        [KeyboardButton("/my_id"), KeyboardButton("/about")],
    ]

    # Если пользователь зарегистрирован, показываем дополнительные кнопки
    if is_registered:
        buttons.insert(0, [KeyboardButton("/today"), KeyboardButton("/status")])
        buttons.insert(1, [KeyboardButton("/stats")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
