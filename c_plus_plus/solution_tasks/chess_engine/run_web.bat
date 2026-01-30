@echo off
echo === ЗАПУСК ВЕБ-ИНТЕРФЕЙСА ШАХМАТ ===
echo.

REM Проверяем наличие Python
py -3.13 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python 3.13 не найден!
    echo Пожалуйста, установите Python 3.13.11
    pause
    exit /b 1
)

REM Проверяем наличие Flask
py -3.13 -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo Устанавливаем Flask...
    py -3.13 -m pip install flask
    if %errorlevel% neq 0 (
        echo Ошибка установки Flask!
        pause
        exit /b 1
    )
)

echo Запуск веб-сервера...
echo Откройте в браузере: http://localhost:5000
echo Для остановки нажмите Ctrl+C
echo.

REM Запускаем сервер
py -3.13 web/chess_server.py

pause