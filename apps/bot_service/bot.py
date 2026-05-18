import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
from django.conf import settings
from asgiref.sync import sync_to_async
from apps.users.models import User

logger = logging.getLogger(__name__)

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN


def get_main_keyboard(is_registered=False):
    """Главная клавиатура бота"""
    buttons = [
        ["/start", "/help"],
        ["/my_id", "/about"],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    welcome_text = f"""🤖 HabitTracker Bot - Ваш помощник!

Привет, {user.first_name}!

Как начать:
1. Скопируйте ваш Chat ID: {chat_id}
2. В веб-приложении в профиле вставьте этот Chat ID

Команды:
/help - Помощь
/my_id - Ваш Chat ID
/about - О боте"""

    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """Доступные команды:

/start - Начать работу
/help - Помощь
/my_id - Показать Chat ID
/about - О боте

Поддержка: support@habittracker.com"""
    await update.message.reply_text(help_text)


async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать Chat ID"""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Ваш Chat ID: {chat_id}")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """О боте"""
    about_text = """🤖 HabitTracker Bot

Версия: 1.0.0

Веб-приложение: http://127.0.0.1:8000"""
    await update.message.reply_text(about_text)


async def send_reminder(chat_id: str, habit_data: dict):
    """Отправка напоминания (для Celery)"""
    from telegram import Bot

    bot = Bot(token=BOT_TOKEN)

    message = f"""⏰ НАПОМИНАНИЕ О ПРИВЫЧКЕ!

Действие: {habit_data['action']}
Место: {habit_data['place']}
Время выполнения: {habit_data['execution_time']} сек.

💪 Не откладывайте!"""

    try:
        await bot.send_message(chat_id=chat_id, text=message)
        return True
    except Exception as e:
        logger.error(f"Failed: {e}")
        return False


def run_bot():
    """Запуск бота"""
    if not BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не настроен!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("my_id", my_id))
    app.add_handler(CommandHandler("about", about))

    print("🤖 Бот запущен!")
    app.run_polling()
