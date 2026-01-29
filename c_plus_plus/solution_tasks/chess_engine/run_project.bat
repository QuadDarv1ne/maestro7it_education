@echo off
chcp 65001 >nul
title Шахматный движок - Запуск
echo ========================================
echo           ШАХМАТНЫЙ ДВИЖОК           
echo ========================================
echo.
echo Доступные режимы:
echo 1. Консольный интерфейс (по умолчанию)
echo 2. Тест производительности
echo 3. Кодировка тест
echo.
echo Выберите режим (1-3) или нажмите Enter для режима 1:

set /p mode=

if "%mode%"=="2" goto performance
if "%mode%"=="3" goto encoding

:main
echo Запуск консольного интерфейса...
echo =================================
cd build
if exist "chess_engine.exe" (
    chess_engine.exe
) else (
    echo Ошибка: исполняемый файл не найден!
    echo Сначала выполните сборку проекта.
)
goto end

:performance
echo Запуск теста производительности...
echo ===================================
cd build
if exist "comprehensive_benchmark.exe" (
    comprehensive_benchmark.exe
) else (
    echo Ошибка: тестовый файл не найден!
)
goto end

:encoding
echo Запуск теста кодировки...
echo ==========================
cd build
if exist "encoding_test.exe" (
    encoding_test.exe
) else (
    echo Ошибка: тест кодировки не найден!
)
goto end

:end
echo.
echo Программа завершена.
pause