@echo off
title Celery Worker - HabitTracker

echo ========================================
echo   Запуск Celery Worker
echo ========================================
echo.

:: Активация виртуального окружения
call venv\Scripts\activate

:: Запуск Celery worker с флагом -P eventlet для Windows
echo Запуск Celery worker с поддержкой eventlet...
celery -A config worker -l INFO -P eventlet --pool=solo

pause
