@echo off
chcp 65001 >nul
title Шахматный движок - Интерфейс с иконками

echo Запуск графического интерфейса с иконками фигур
echo ===============================================

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не найден в PATH
    echo Пожалуйста, установите Python с https://python.org
    pause
    exit /b 1
)

echo Запуск интерфейса с иконками...
python chess_gui_with_icons.py

echo Интерфейс завершен
pause