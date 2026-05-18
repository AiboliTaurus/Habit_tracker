from rest_framework import serializers
from .models import Habit, HabitExecution


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""

    related_habit_details = serializers.SerializerMethodField()
    periodicity_display = serializers.CharField(source='get_periodicity_display', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'related_habit', 'related_habit_details', 'reward', 'periodicity',
            'periodicity_display', 'execution_time', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_related_habit_details(self, obj):
        if obj.related_habit:
            return {
                'id': obj.related_habit.id,
                'action': obj.related_habit.action,
                'place': obj.related_habit.place,
                'time': obj.related_habit.time,
                'is_pleasant': obj.related_habit.is_pleasant
            }
        return None

    def validate(self, data):
        errors = {}

        # 1. Нельзя одновременно выбрать связанную привычку и вознаграждение
        if data.get('reward') and data.get('related_habit'):
            errors['non_field_errors'] = ['Нельзя одновременно указать связанную привычку и вознаграждение']

        # 2. Проверка для приятной привычки
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            errors['is_pleasant'] = ['У приятной привычки не может быть вознаграждения или связанной привычки']

        # 3. Проверка, что связанная привычка существует и является приятной
        if data.get('related_habit'):
            related = data['related_habit']
            if not related.is_pleasant:
                errors['related_habit'] = ['Связанная привычка должна быть приятной']

        # 4. Проверка времени выполнения
        if data.get('execution_time', 0) > 120:
            errors['execution_time'] = ['Время выполнения не должно превышать 120 секунд']

        if errors:
            raise serializers.ValidationError(errors)

        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек (только чтение)"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    periodicity_display = serializers.CharField(source='get_periodicity_display', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'user_name', 'place', 'time', 'action',
            'periodicity', 'periodicity_display', 'execution_time',
            'created_at'
        ]
        # Все поля только для чтения
        read_only_fields = fields  # ← Это правильно! fields - это список


class HabitExecutionSerializer(serializers.ModelSerializer):
    """Сериализатор для выполнения привычек"""
    habit_details = HabitSerializer(source='habit', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = HabitExecution
        fields = ['id', 'habit', 'habit_details', 'execution_date', 'status',
                  'status_display', 'completed_at', 'notes']
        read_only_fields = ['completed_at']
