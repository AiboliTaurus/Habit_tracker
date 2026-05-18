from django.contrib import admin
from .models import Habit, HabitExecution


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'time', 'place', 'is_pleasant', 'is_public', 'periodicity')
    list_filter = ('is_pleasant', 'is_public', 'periodicity', 'created_at')
    search_fields = ('action', 'place', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'place', 'time', 'action')
        }),
        ('Настройки', {
            'fields': ('is_pleasant', 'periodicity', 'execution_time', 'is_public')
        }),
        ('Вознаграждение и связи', {
            'fields': ('related_habit', 'reward')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(HabitExecution)
class HabitExecutionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'execution_date', 'status', 'completed_at')
    list_filter = ('status', 'execution_date')
    search_fields = ('habit__action', 'habit__user__email')
    readonly_fields = ('completed_at',)
