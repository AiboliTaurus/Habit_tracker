from celery import shared_task
from datetime import date, timedelta
from .models import Habit, HabitExecution
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

    # Если привычка никогда не выполнялась, нужно выполнить
    if not last_execution:
        return True

    # Вычисляем следующий день выполнения
    next_execution_date = last_execution.execution_date + timedelta(days=days)

    # Если сегодня >= следующей даты выполнения, нужно выполнить
    return today >= next_execution_date


@shared_task
def create_habit_executions():
    """Создание записей о выполнении привычек на сегодня"""
    today = date.today()

    # Получаем все активные привычки пользователей
    habits = Habit.objects.filter(is_pleasant=False)

    created_count = 0
    for habit in habits:
        # Проверяем, нужно ли выполнять привычку сегодня
        if should_execute_today(habit, today):
            execution, created = HabitExecution.objects.get_or_create(
                habit=habit,
                execution_date=today,
                defaults={'status': 'pending'}
            )
            if created:
                created_count += 1
                logger.info(f"Created execution record for habit {habit.id} on {today}")

    logger.info(f"Created {created_count} execution records for {today}")
    return created_count
