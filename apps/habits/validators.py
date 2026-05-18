from django.core.exceptions import ValidationError


def validate_execution_time(value):
    """Валидатор времени выполнения (не более 120 секунд)"""
    if value > 120:
        raise ValidationError(f'Время выполнения не должно превышать 120 секунд. Текущее: {value} секунд')
    if value < 1:
        raise ValidationError('Время выполнения должно быть положительным числом')
    return value


def validate_periodicity(periodicity_value):
    """Валидатор периодичности (не реже 1 раза в 7 дней)"""
    periodicity_days = {
        'daily': 1,
        'every_2_days': 2,
        'every_3_days': 3,
        'every_4_days': 4,
        'every_5_days': 5,
        'every_6_days': 6,
        'weekly': 7,
    }

    days = periodicity_days.get(periodicity_value, 7)
    if days > 7:
        raise ValidationError('Привычку нельзя выполнять реже, чем 1 раз в 7 дней')
    if days < 1:
        raise ValidationError('Периодичность должна быть положительной')
    return periodicity_value
