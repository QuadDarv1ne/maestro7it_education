@echo off
chcp 65001 >nul
title Шахматный движок - Синхронизированный интерфейс

echo Запуск синхронизированного графического интерфейса
echo ================================================

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не найден в PATH
    echo Пожалуйста, установите Python с https://python.org
    pause
    exit /b 1
)

:: Проверка наличия движка
if not exist "build\chess_engine.exe" (
    echo Ошибка: Шахматный движок не найден
    echo Пожалуйста, сначала соберите проект командой build.bat
    pause
    exit /b 1
)

echo Запуск синхронизированного интерфейса...
python synchronized_chess_gui.py

echo Интерфейс завершен
pause