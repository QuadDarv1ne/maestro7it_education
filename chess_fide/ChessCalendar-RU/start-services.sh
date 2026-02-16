#!/bin/bash

# Скрипт для запуска микросервисов ChessCalendar-RU

echo "Запуск микросервисов ChessCalendar-RU..."

# Создание директорий для данных
mkdir -p data/tournaments data/users data/redis

# Запуск Docker Compose
docker-compose up -d

echo "Сервисы запущены:"
echo "- Tournament Service: http://localhost:5001"
echo "- User Service: http://localhost:5002" 
echo "- Parser Service: http://localhost:5003"
echo "- Web Interface: http://localhost"

echo "Проверка состояния сервисов..."
sleep 10

# Проверка состояния сервисов
docker-compose ps

echo "Готово! Приложение доступно по адресу http://localhost"