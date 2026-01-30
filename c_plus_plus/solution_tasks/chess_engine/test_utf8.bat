@echo off
chcp 65001 >nul
title Тестирование UTF-8 поддержки

echo Тестирование поддержки UTF-8 и русских символов
echo ================================================

:: Проверка Python 3.13
py -3.13 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python 3.13 не найден
    pause
    exit /b 1
)

echo Запуск Python теста UTF-8...
py -3.13 utf8_test.py

echo.
echo Тест завершен!
pause