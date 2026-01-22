@echo off
echo ========================================
echo Система управления библиотекой книг
echo ========================================
echo.
echo Выберите программу для запуска:
echo 1. Основная программа (book_manager_with_log.exe)
echo 2. Демонстрация логирования (demo_logging.exe)
echo 3. Демонстрация сортировки и отмены (demo_undo_sort.exe)
echo 0. Выход
echo.
set /p choice=Введите номер программы: 

if "%choice%"=="1" (
    echo Запуск основной программы...
    book_manager_with_log.exe
) else if "%choice%"=="2" (
    echo Запуск демонстрации логирования...
    demo_logging.exe
) else if "%choice%"=="3" (
    echo Запуск демонстрации сортировки и отмены...
    demo_undo_sort.exe
) else if "%choice%"=="0" (
    echo До свидания!
    exit /b 0
) else (
    echo Неверный выбор. Попробуйте снова.
    pause
    goto :start
)

:start
pause