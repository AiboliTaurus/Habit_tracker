@echo off
title Celery Beat - HabitTracker

echo ========================================
echo   Запуск Celery Beat
echo ========================================
echo.

:: Активация виртуального окружения
call venv\Scripts\activate

:: Запуск Celery beat
echo Запуск Celery beat...
celery -A config beat -l INFO

pause
