@echo off
chcp 65001 >nul
title Шахматы на Pygame

echo Запуск шахматного интерфейса на Pygame
echo ======================================

:: Проверка наличия Python 3.13
py -3.13 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python 3.13 не найден
    echo Пожалуйста, установите Python 3.13 с https://python.org
    pause
    exit /b 1
)

:: Проверка наличия Pygame
py -3.13 -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка Pygame для Python 3.13...
    py -3.13 -m pip install pygame
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
echo - Клавиша R - новая игра
echo - Клавиша M - сменить режим
echo - Пробел - вызов ИИ
echo - ESC - выход
echo ========================

py -3.13 pygame_chess.py

echo Игра завершена
pause