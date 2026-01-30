@echo off
chcp 65001 >nul
title Шахматы - Сборка проекта

echo Сборка шахматного движка
echo =========================

:: Проверка наличия CMake
cmake --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: CMake не найден
    echo Пожалуйста, установите CMake с https://cmake.org
    pause
    exit /b 1
)

:: Проверка наличия компилятора
g++ --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Компилятор g++ не найден
    echo Пожалуйста, установите MinGW-w64
    pause
    exit /b 1
)

:: Создание директории сборки
if exist build rmdir /s /q build
mkdir build
cd build

:: Генерация файлов сборки
echo Генерация файлов сборки...
cmake .. -G "MinGW Makefiles"
if %errorlevel% neq 0 (
    echo Ошибка генерации CMake файлов
    cd ..
    pause
    exit /b 1
)

:: Сборка проекта
echo Сборка проекта...
mingw32-make
if %errorlevel% neq 0 (
    echo Ошибка компиляции
    cd ..
    pause
    exit /b 1
)

echo.
echo Сборка успешна!
echo Исполняемый файл: build\chess_engine.exe
echo.
echo Для запуска:
echo   cd build
echo   chess_engine.exe
echo.

cd ..
pause