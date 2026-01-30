@echo off
chcp 65001 >nul
title Запуск стабильной версии шахмат

echo Запуск стабильной версии шахмат
echo ================================

:: Проверка Python 3.13
py -3.13 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python 3.13 не найден
    pause
    exit /b 1
)

:: Проверка Pygame
py -3.13 -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка Pygame...
    py -3.13 -m pip install pygame
    if %errorlevel% neq 0 (
        echo Ошибка установки Pygame
        pause
        exit /b 1
    )
)

echo Запуск стабильной версии...
py -3.13 stable_chess.py

pause