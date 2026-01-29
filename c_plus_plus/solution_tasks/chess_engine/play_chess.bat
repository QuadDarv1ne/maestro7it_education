@echo off
title Шахматный движок - Игровой режим
echo Запуск шахматного движка в игровом режиме...
echo ==============================================

cd build
if exist "chess_engine.exe" (
    echo Запуск игры...
    chess_engine.exe
) else (
    echo Ошибка: исполняемый файл не найден!
    echo Сначала выполните сборку проекта: build_engine_windows.bat
    pause
    exit /b 1
)

echo.
echo Игра завершена.
pause