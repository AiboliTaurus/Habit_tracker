from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.users.models import User


class Habit(models.Model):
    """Модель привычки"""

    class Periodicity(models.TextChoices):
        DAILY = 'daily', 'Ежедневно'
        EVERY_2_DAYS = 'every_2_days', 'Каждые 2 дня'
        EVERY_3_DAYS = 'every_3_days', 'Каждые 3 дня'
        EVERY_4_DAYS = 'every_4_days', 'Каждые 4 дня'
        EVERY_5_DAYS = 'every_5_days', 'Каждые 5 дней'
        EVERY_6_DAYS = 'every_6_days', 'Каждые 6 дней'
        WEEKLY = 'weekly', 'Еженедельно'

    # Основные поля (обязательные)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=200, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=200, verbose_name='Действие')

    # Связи и вознаграждение
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='related_to', verbose_name='Связанная привычка',
        limit_choices_to={'is_pleasant': True}
    )
    reward = models.CharField(max_length=200, blank=True, null=True, verbose_name='Вознаграждение')

    # Временные параметры
    periodicity = models.CharField(
        max_length=20, choices=Periodicity.choices,
        default=Periodicity.DAILY, verbose_name='Периодичность'
    )
    execution_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        default=60, verbose_name='Время на выполнение (секунды)'
    )

    # Дополнительные поля
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'habits'
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['time']
        indexes = [
            models.Index(fields=['user', 'is_public']),
            models.Index(fields=['periodicity', 'time']),
        ]

    def __str__(self):
        return f"{self.action} в {self.time} - {self.user.email}"

    def clean(self):
        """Валидация модели согласно заданию"""
        errors = {}

        # 1. Нельзя одновременно выбрать связанную привычку и вознаграждение
        if self.related_habit and self.reward:
            errors['non_field_errors'] = ['Нельзя одновременно указать связанную привычку и вознаграждение']

        # 2. Связанная привычка должна быть приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            errors['related_habit'] = ['Связанная привычка должна быть приятной']

        # 3. У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            errors['is_pleasant'] = ['У приятной привычки не может быть вознаграждения или связанной привычки']

        # 4. Время выполнения не более 120 секунд (проверяется валидатором)
        if self.execution_time > 120:
            errors['execution_time'] = ['Время выполнения не должно превышать 120 секунд']

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class HabitExecution(models.Model):
    """Модель для отслеживания выполнения привычек"""

    class Status(models.TextChoices):
        COMPLETED = 'completed', 'Выполнено'
        SKIPPED = 'skipped', 'Пропущено'
        PENDING = 'pending', 'Ожидает'

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='executions')
    execution_date = models.DateField(verbose_name='Дата выполнения')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        db_table = 'habit_executions'
        verbose_name = 'Выполнение привычки'
        verbose_name_plural = 'Выполнения привычек'
        unique_together = ['habit', 'execution_date']
        ordering = ['-execution_date']
        indexes = [
            models.Index(fields=['habit', 'execution_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.habit.action} - {self.execution_date}"
