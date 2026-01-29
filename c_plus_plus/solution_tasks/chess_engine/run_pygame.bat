@echo off
chcp 65001 >nul
title Шахматы на Pygame

echo Запуск шахматного интерфейса на Pygame
echo ======================================

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не найден в PATH
    echo Пожалуйста, установите Python с https://python.org
    pause
    exit /b 1
)

:: Проверка наличия Pygame
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка Pygame...
    pip install pygame
    if %errorlevel% neq 0 (
        echo Ошибка установки Pygame
        pause
        exit /b 1
    )
)

echo Запуск Pygame шахмат...
echo ========================
echo Управление:
echo - Клик по фигуре для выбора
echo - Клик по клетке для хода
echo - Клавиша N - новая игра
echo - ESC - выход
echo ========================

python pygame_chess.py

echo Игра завершена
pause