@echo off
chcp 65001 >nul
title Шахматы - Главное меню

:menu
cls
echo ========================================
echo        ШАХМАТНЫЙ ДВИЖОК v2.0
echo ========================================
echo.
echo Выберите действие:
echo.
echo 1. Запустить Pygame версию (основная)
echo 2. Запустить стабильную версию
echo 3. Собрать C++ движок
echo 4. Запустить тесты
echo 5. Очистить проект
echo 6. Выход
echo.
echo ========================================

set /p choice="Введите номер действия: "

if "%choice%"=="1" goto run_pygame
if "%choice%"=="2" goto run_stable
if "%choice%"=="3" goto build_cpp
if "%choice%"=="4" goto run_tests
if "%choice%"=="5" goto cleanup
if "%choice%"=="6" goto exit

echo Неверный выбор. Попробуйте снова.
pause
goto menu

:run_pygame
cls
echo Запуск Pygame версии...
call run_pygame.bat
goto menu

:run_stable
cls
echo Запуск стабильной версии...
call run_stable.bat
goto menu

:build_cpp
cls
echo Сборка C++ движка...
call build.bat
goto menu

:run_tests
cls
echo Запуск тестов...
call test_all.bat
goto menu

:cleanup
cls
echo Очистка проекта...
call cleanup_project.bat
goto menu

:exit
echo До свидания!
exit /b 0