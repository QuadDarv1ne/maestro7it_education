@echo off
echo Запуск шахматного движка...
echo =============================

cd build
if exist "chess_engine.exe" (
    echo Запуск основного движка...
    chess_engine.exe
) else (
    echo Основной исполняемый файл не найден!
    echo Попробуйте пересобрать проект: build_engine_windows.bat
)

pause