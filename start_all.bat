@echo off
title HabitTracker - Запуск всех сервисов

echo ========================================
echo   HabitTracker - Запуск всех сервисов
echo ========================================
echo.

:: Активация виртуального окружения
echo [1/6] Активация виртуального окружения...
call venv\Scripts\activate
if errorlevel 1 (
    echo Ошибка: Не удалось активировать виртуальное окружение
    pause
    exit /b 1
)
echo OK
echo.

:: Запуск Redis
echo [2/6] Запуск Redis сервера...
start "Redis Server" /min redis-server
timeout /t 2 /nobreak >nul
echo OK
echo.

:: Запуск Celery Worker (с флагом -P eventlet для Windows)
echo [3/6] Запуск Celery Worker...
start "Celery Worker" /min cmd /c "celery -A config worker -l INFO -P eventlet --pool=solo"
timeout /t 3 /nobreak >nul
echo OK
echo.

:: Запуск Celery Beat
echo [4/6] Запуск Celery Beat...
start "Celery Beat" /min cmd /c "celery -A config beat -l INFO"
timeout /t 2 /nobreak >nul
echo OK
echo.

:: Запуск Django сервера
echo [5/6] Запуск Django сервера...
start "Django Server" cmd /k "python manage.py runserver"
timeout /t 3 /nobreak >nul
echo OK
echo.

:: Запуск Telegram бота
echo [6/6] Запуск Telegram бота...
start "Telegram Bot" cmd /k "python run_bot.py"
timeout /t 2 /nobreak >nul
echo OK
echo.

echo ========================================
echo   Все сервисы успешно запущены!
echo ========================================
echo.
echo Сервисы:
echo   - Redis Server: запущен (фоновый процесс)
echo   - Celery Worker: запущен
echo   - Celery Beat: запущен
echo   - Django Server: http://localhost:8000
echo   - Telegram Bot: запущен
echo.
echo Для остановки закройте все окна командной строки
echo.

pause
