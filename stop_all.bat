@echo off
title HabitTracker - Остановка всех сервисов

echo ========================================
echo   HabitTracker - Остановка всех сервисов
echo ========================================
echo.

:: Остановка Redis
echo [1/4] Остановка Redis сервера...
taskkill /f /im redis-server.exe >nul 2>&1
echo OK
echo.

:: Остановка Celery процессов
echo [2/4] Остановка Celery процессов...
taskkill /f /im python.exe /fi "windowtitle eq Celery Worker*" >nul 2>&1
taskkill /f /im python.exe /fi "windowtitle eq Celery Beat*" >nul 2>&1
timeout /t 1 /nobreak >nul
echo OK
echo.

:: Остановка Django сервера
echo [3/4] Остановка Django сервера...
taskkill /f /im python.exe /fi "windowtitle eq Django Server*" >nul 2>&1
echo OK
echo.

:: Остановка Telegram бота
echo [4/4] Остановка Telegram бота...
taskkill /f /im python.exe /fi "windowtitle eq Telegram Bot*" >nul 2>&1
echo OK
echo.

echo ========================================
echo   Все сервисы успешно остановлены!
echo ========================================

pause
