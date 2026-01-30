@echo off
chcp 65001 >nul
cls
echo ========================================
echo    ЗАПУСК УЛУЧШЕННОГО ВЕБ-СЕРВЕРА ШАХМАТ
echo ========================================
echo.

echo Проверяю наличие необходимых библиотек...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Устанавливаю Flask...
    pip install flask
)

python -c "import flask_socketio" 2>nul
if errorlevel 1 (
    echo Устанавливаю Flask-SocketIO...
    pip install flask-socketio
)

echo.
echo 🚀 Запуск веб-сервера...
echo.
echo Сервер будет доступен по адресу:
echo http://localhost:8000
echo.
echo Нажмите Ctrl+C для остановки сервера
echo.

python interfaces/fastapi_chess.py

pause