@echo off
echo Тестирование производительности шахматного движка
echo =================================================

cd build

echo Проверка наличия исполняемых файлов...
if exist "chess_engine.exe" (
    echo ✓ Основной движок найден
) else (
    echo ✗ Основной движок не найден
)

if exist "encoding_test.exe" (
    echo ✓ Тест кодировки найден
) else (
    echo ✗ Тест кодировки не найден
)

echo.
echo Запуск теста кодировки...
encoding_test.exe

echo.
echo Запуск основного движка в тестовом режиме...
timeout /t 3 >nul
chess_engine.exe

echo.
echo Тестирование завершено!
pause