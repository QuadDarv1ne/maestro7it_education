@echo off
echo ========================================
echo Сборка проекта "Система управления библиотекой"
echo ========================================
echo.

echo Компиляция основной программы...
g++ -std=c++17 -Wall -Wextra -O2 library.cpp book.cpp ui.cpp main.cpp -o book_manager_with_log.exe
if %errorlevel% equ 0 (
    echo ✓ Основная программа собрана успешно
) else (
    echo ✗ Ошибка при сборке основной программы
    pause
    exit /b 1
)

echo.
echo Компиляция демонстрации логирования...
g++ -std=c++17 -Wall -Wextra -O2 library.cpp book.cpp demo_logging.cpp -o demo_logging.exe
if %errorlevel% equ 0 (
    echo ✓ Демонстрация логирования собрана успешно
) else (
    echo ✗ Ошибка при сборке демонстрации логирования
    pause
    exit /b 1
)

echo.
echo Компиляция демонстрации сортировки и отмены...
g++ -std=c++17 -Wall -Wextra -O2 library.cpp book.cpp demo_undo_sort.cpp -o demo_undo_sort.exe
if %errorlevel% equ 0 (
    echo ✓ Демонстрация сортировки и отмены собрана успешно
) else (
    echo ✗ Ошибка при сборке демонстрации сортировки и отмены
    pause
    exit /b 1
)

echo.
echo ========================================
echo Все программы успешно собраны!
echo ========================================
echo.
echo Исполняемые файлы:
echo - book_manager_with_log.exe (основная программа)
echo - demo_logging.exe (демонстрация логирования)
echo - demo_undo_sort.exe (демонстрация сортировки и отмены)
echo.
pause