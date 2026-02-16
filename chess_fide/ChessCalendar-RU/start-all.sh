#!/bin/bash

# Скрипт для быстрого запуска всей инфраструктуры Chess Calendar RU

set -e

echo "🚀 Запуск Chess Calendar RU..."

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Создаю из .env.example..."
    cp .env.example .env
    echo "✅ Файл .env создан. Пожалуйста, отредактируйте его перед запуском."
    echo "   Минимум измените SECRET_KEY!"
    exit 1
fi

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p logs backups data/tournaments data/users

# Остановка существующих контейнеров
echo "🛑 Остановка существующих контейнеров..."
docker-compose down

# Сборка образов
echo "🔨 Сборка Docker образов..."
docker-compose build

# Запуск сервисов
echo "▶️  Запуск сервисов..."
docker-compose up -d

# Ожидание запуска Redis
echo "⏳ Ожидание запуска Redis..."
sleep 5

# Проверка статуса
echo "📊 Проверка статуса сервисов..."
docker-compose ps

# Health checks
echo ""
echo "🏥 Проверка health checks..."
sleep 10

services=("api-gateway:5000" "tournament-service:5001" "user-service:5002")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -f -s "http://localhost:$port/health" > /dev/null; then
        echo "✅ $name: OK"
    else
        echo "❌ $name: FAILED"
    fi
done

echo ""
echo "🎉 Запуск завершен!"
echo ""
echo "📍 Доступные сервисы:"
echo "   - API Gateway: http://localhost:5000"
echo "   - Flower (Celery): http://localhost:5555"
echo "   - Tournament Service: http://localhost:5001"
echo "   - User Service: http://localhost:5002"
echo ""
echo "📚 Документация:"
echo "   - Архитектура: ARCHITECTURE.md"
echo "   - Быстрый старт: QUICK_START.md"
echo ""
echo "🔧 Полезные команды:"
echo "   - Просмотр логов: docker-compose logs -f"
echo "   - Остановка: docker-compose down"
echo "   - Перезапуск: docker-compose restart"
echo ""
echo "👤 Создание администратора:"
echo "   docker-compose exec api-gateway python manage.py --action create-admin \\"
echo "     --username admin --email admin@example.com --password YourPassword"
