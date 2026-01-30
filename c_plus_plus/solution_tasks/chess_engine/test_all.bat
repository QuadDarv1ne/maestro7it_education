@echo off
chcp 65001 >nul
title Тестирование шахматного движка

echo Тестирование шахматного движка
echo ===============================

:: Проверка Python 3.13
py -3.13 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python 3.13 не найден
    pause
    exit /b 1
)

echo Запуск тестов...

:: Тест базового движка
echo 1. Тест базового движка...
py -3.13 test_chess.py
if %errorlevel% neq 0 (
    echo Ошибка в test_chess.py
    pause
    exit /b 1
)

:: Тест UTF-8
echo 2. Тест UTF-8 поддержки...
py -3.13 test_utf8.bat
if %errorlevel% neq 0 (
    echo Ошибка в UTF-8 тесте
)

:: Тест производительности
echo 3. Тест производительности...
py -3.13 test_performance.bat
if %errorlevel% neq 0 (
    echo Ошибка в тесте производительности
)

echo.
echo Все тесты завершены успешно!
pause