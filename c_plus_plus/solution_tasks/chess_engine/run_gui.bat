@echo off
echo Запуск графического шахматного движка
echo ====================================

if exist "chess_engine_gui.exe" (
    echo Запуск графического интерфейса...
    chess_engine_gui.exe
) else (
    echo Графический исполняемый файл не найден!
    echo Сначала соберите проект: build_gui_windows.bat
    pause
    exit /b 1
)

echo Программа завершена
pause