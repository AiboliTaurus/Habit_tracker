from celery import shared_task
from datetime import date, timedelta
from apps.habits.models import Habit, HabitExecution
from apps.users.models import User
from .bot import send_reminder
import logging

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
    """
    from django.utils import timezone

    current_time = timezone.localtime(timezone.now()).time()
    today = date.today()

    # Получаем привычки, у которых время совпадает с текущим
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__telegram_chat_id__isnull=False,
        user__telegram_notifications=True,
        user__is_active=True,
        user__is_blocked=False,
        is_pleasant=False
    ).select_related('user', 'related_habit')

    sent_count = 0
    for habit in habits:
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
    """
    yesterday = date.today() - timedelta(days=1)

    # Находим все невыполненные привычки за вчерашний день
    missed_executions = HabitExecution.objects.filter(
        execution_date=yesterday,
        status='pending'
    )

    # Отмечаем их как пропущенные
    count = missed_executions.update(status='skipped')

    if count > 0:
        logger.info(f"Marked {count} habits as skipped for {yesterday}")

    return count
