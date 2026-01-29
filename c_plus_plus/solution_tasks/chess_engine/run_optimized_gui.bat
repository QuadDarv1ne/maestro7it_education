@echo off
chcp 65001 >nul
title Оптимизированный шахматный движок

echo Запуск оптимизированного шахматного интерфейса
echo =============================================

:: Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не найден в PATH
    echo Пожалуйста, установите Python с https://python.org
    pause
    exit /b 1
)

echo Запуск оптимизированного интерфейса...
echo Размер окна: 520x450 (адаптивный)
echo Настройки: глубина 6, время 3 сек
echo ====================================

python optimized_chess_gui.py

echo Интерфейс завершен
pause