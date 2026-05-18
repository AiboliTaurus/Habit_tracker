from celery import shared_task
from datetime import date, timedelta
from django.utils import timezone as django_timezone
from apps.habits.models import Habit, HabitExecution
from .bot import send_reminder
import logging
import pytz

logger = logging.getLogger(__name__)


def should_execute_today(habit, today):
    """
    Определяет, нужно ли выполнять привычку в указанную дату
    с учетом периодичности.
    """
    periodicity_days = {
        'daily': 1,
        'every_2_days': 2,
        'every_3_days': 3,
        'every_4_days': 4,
        'every_5_days': 5,
        'every_6_days': 6,
        'weekly': 7,
    }

    days = periodicity_days.get(habit.periodicity, 1)

    # Получаем последнее выполнение привычки
    last_execution = HabitExecution.objects.filter(
        habit=habit,
        status='completed'
    ).order_by('-execution_date').first()

    # Если привычка никогда не выполнялась, нужно напомнить
    if not last_execution:
        return True

    # Вычисляем следующий день выполнения
    next_execution_date = last_execution.execution_date + timedelta(days=days)

    # Если сегодня >= следующей даты выполнения, нужно напомнить
    return today >= next_execution_date


@shared_task
def process_habit_reminders():
    """
    Обработка и отправка напоминаний о привычках.
    Проверяет периодичность и отправляет только те привычки,
    которые нужно выполнить сегодня.
    Учитывает часовой пояс пользователя.
    """
    now = django_timezone.now()
    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        user__telegram_notifications=True,
        user__is_active=True,
        user__is_blocked=False,
        is_pleasant=False
    ).select_related('user', 'related_habit')

    sent_count = 0
    for habit in habits:
        # Получаем часовой пояс пользователя
        user_tz = pytz.timezone(habit.user.user_timezone) if habit.user.user_timezone else pytz.timezone(
            'Europe/Moscow')
        user_now = now.astimezone(user_tz)
        current_time = user_now.time()
        today = user_now.date()

        # Проверяем, совпадает ли время привычки с текущим временем пользователя
        if habit.time.hour == current_time.hour and habit.time.minute == current_time.minute:
            # Проверяем, нужно ли выполнять привычку сегодня (с учетом периодичности)
            if should_execute_today(habit, today):
                # Проверяем, не выполнена ли уже привычка сегодня
                execution = HabitExecution.objects.filter(
                    habit=habit,
                    execution_date=today
                ).first()

                # Отправляем напоминание, если привычка еще не выполнена
                if not execution or execution.status != 'completed':
                    habit_data = {
                        'action': habit.action,
                        'place': habit.place,
                        'execution_time': habit.execution_time,
                        'reward': habit.reward,
                        'related_habit_action': habit.related_habit.action if habit.related_habit else None,
                        'periodicity': habit.get_periodicity_display(),
                        'local_time': current_time.strftime('%H:%M'),
                    }

                    result = send_reminder(habit.user.telegram_chat_id, habit_data)
                    if result:
                        sent_count += 1
                        logger.info(f"Reminder sent for habit {habit.id} to user {habit.user.email}")

    logger.info(f"Sent {sent_count} reminders")
    return sent_count


@shared_task
def check_missed_habits():
    """
    Проверка пропущенных привычек.
    Отмечает как пропущенные привычки, которые не были выполнены в срок.
    Учитывает часовой пояс пользователя.
    """
    now = django_timezone.now()
    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        user__telegram_notifications=True,
        is_pleasant=False
    ).select_related('user')

    marked_count = 0
    for habit in habits:
        user_tz = pytz.timezone(habit.user.user_timezone) if habit.user.user_timezone else pytz.timezone(
            'Europe/Moscow')
        user_today = now.astimezone(user_tz).date()

        # Проверяем, есть ли запись о выполнении за сегодня
        execution = HabitExecution.objects.filter(
            habit=habit,
            execution_date=user_today
        ).first()

        # Если записи нет, создаём со статусом "пропущено"
        if not execution:
            # Проверяем, нужно ли было выполнять привычку сегодня
            periodicity_days = {
                'daily': 1,
                'every_2_days': 2,
                'every_3_days': 3,
                'every_4_days': 4,
                'every_5_days': 5,
                'every_6_days': 6,
                'weekly': 7,
            }
            days = periodicity_days.get(habit.periodicity, 1)

            # Получаем последнее выполнение
            last_execution = HabitExecution.objects.filter(
                habit=habit,
                status='completed'
            ).order_by('-execution_date').first()

            should_have_executed = False
            if not last_execution:
                should_have_executed = True
            else:
                next_date = last_execution.execution_date + timedelta(days=days)
                if user_today >= next_date:
                    should_have_executed = True

            if should_have_executed:
                HabitExecution.objects.create(
                    habit=habit,
                    execution_date=user_today,
                    status='skipped'
                )
                marked_count += 1
                logger.info(f"Marked habit {habit.id} as skipped for {user_today}")

    return marked_count
