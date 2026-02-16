@echo off
REM Скрипт для запуска микросервисов ChessCalendar-RU на Windows

echo Запуск микросервисов ChessCalendar-RU...

REM Создание директорий для данных
mkdir data\tournaments 2>nul
mkdir data\users 2>nul
mkdir data\redis 2>nul

REM Запуск Docker Compose
docker-compose up -d

echo Сервисы запущены:
echo - Tournament Service: http://localhost:5001
echo - User Service: http://localhost:5002
echo - Parser Service: http://localhost:5003
echo - Web Interface: http://localhost

echo Проверка состояния сервисов...
timeout /t 10 /nobreak >nul

REM Проверка состояния сервисов
docker-compose ps

echo Готово! Приложение доступно по адресу http://localhost

pause