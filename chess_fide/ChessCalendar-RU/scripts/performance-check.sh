#!/bin/bash

# Скрипт для проверки производительности системы
# Использование: ./scripts/performance-check.sh

set -e

echo "🚀 Chess Calendar RU - Performance Check"
echo "========================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для проверки команды
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 установлен"
        return 0
    else
        echo -e "${RED}✗${NC} $1 не найден"
        return 1
    fi
}

# Проверка зависимостей
echo "📦 Проверка зависимостей..."
check_command curl || exit 1
check_command jq || echo -e "${YELLOW}⚠${NC} jq не установлен (опционально для красивого вывода)"
check_command docker || exit 1
check_command docker-compose || exit 1
echo ""

# Проверка что сервисы запущены
echo "🔍 Проверка статуса сервисов..."
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${RED}✗${NC} Сервисы не запущены. Запустите: docker-compose up -d"
    exit 1
fi
echo -e "${GREEN}✓${NC} Сервисы запущены"
echo ""

# Health Check
echo "🏥 Health Check..."
HEALTH_RESPONSE=$(curl -s http://localhost:5000/health)
HEALTH_STATUS=$(echo $HEALTH_RESPONSE | jq -r '.overall_status' 2>/dev/null || echo "unknown")

if [ "$HEALTH_STATUS" = "healthy" ]; then
    echo -e "${GREEN}✓${NC} Система здорова"
    echo "$HEALTH_RESPONSE" | jq '.' 2>/dev/null || echo "$HEALTH_RESPONSE"
elif [ "$HEALTH_STATUS" = "degraded" ]; then
    echo -e "${YELLOW}⚠${NC} Система работает с ограничениями"
    echo "$HEALTH_RESPONSE" | jq '.' 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo -e "${RED}✗${NC} Система нездорова"
    echo "$HEALTH_RESPONSE" | jq '.' 2>/dev/null || echo "$HEALTH_RESPONSE"
fi
echo ""

# Проверка времени отклика API
echo "⚡ Проверка времени отклика API..."

test_endpoint() {
    local endpoint=$1
    local name=$2
    local total_time=0
    local iterations=10
    
    for i in $(seq 1 $iterations); do
        response_time=$(curl -o /dev/null -s -w '%{time_total}' http://localhost:5000$endpoint)
        total_time=$(echo "$total_time + $response_time" | bc)
    done
    
    avg_time=$(echo "scale=3; $total_time / $iterations" | bc)
    avg_ms=$(echo "$avg_time * 1000" | bc)
    
    if (( $(echo "$avg_ms < 100" | bc -l) )); then
        echo -e "${GREEN}✓${NC} $name: ${avg_ms}ms (отлично)"
    elif (( $(echo "$avg_ms < 500" | bc -l) )); then
        echo -e "${YELLOW}⚠${NC} $name: ${avg_ms}ms (приемлемо)"
    else
        echo -e "${RED}✗${NC} $name: ${avg_ms}ms (медленно)"
    fi
}

test_endpoint "/health" "Health endpoint"
test_endpoint "/api/tournaments" "Tournaments API"
test_endpoint "/" "Main page"
echo ""

# Проверка использования ресурсов
echo "💾 Использование ресурсов..."

# CPU и Memory для каждого контейнера
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -n 10

echo ""

# Проверка Redis
echo "🔴 Проверка Redis..."
REDIS_INFO=$(docker-compose exec -T redis redis-cli INFO memory 2>/dev/null || echo "")
if [ -n "$REDIS_INFO" ]; then
    REDIS_MEMORY=$(echo "$REDIS_INFO" | grep "used_memory_human" | cut -d: -f2 | tr -d '\r')
    REDIS_KEYS=$(docker-compose exec -T redis redis-cli DBSIZE 2>/dev/null | cut -d: -f2 | tr -d '\r')
    echo -e "${GREEN}✓${NC} Redis работает"
    echo "  Память: $REDIS_MEMORY"
    echo "  Ключей: $REDIS_KEYS"
else
    echo -e "${RED}✗${NC} Redis недоступен"
fi
echo ""

# Проверка PostgreSQL (если используется)
echo "🐘 Проверка базы данных..."
DB_CHECK=$(docker-compose exec -T postgres psql -U chess_user -d chess_calendar_prod -c "SELECT 1" 2>/dev/null || echo "")
if [ -n "$DB_CHECK" ]; then
    echo -e "${GREEN}✓${NC} PostgreSQL работает"
    
    # Размер БД
    DB_SIZE=$(docker-compose exec -T postgres psql -U chess_user -d chess_calendar_prod -t -c \
        "SELECT pg_size_pretty(pg_database_size('chess_calendar_prod'))" 2>/dev/null | tr -d ' \r')
    echo "  Размер БД: $DB_SIZE"
    
    # Количество подключений
    DB_CONNECTIONS=$(docker-compose exec -T postgres psql -U chess_user -d chess_calendar_prod -t -c \
        "SELECT count(*) FROM pg_stat_activity" 2>/dev/null | tr -d ' \r')
    echo "  Подключений: $DB_CONNECTIONS"
else
    echo -e "${YELLOW}⚠${NC} PostgreSQL недоступен (возможно используется SQLite)"
fi
echo ""

# Проверка Celery
echo "🌿 Проверка Celery..."
CELERY_ACTIVE=$(docker-compose exec -T celery-worker celery -A app.celery_app inspect active 2>/dev/null || echo "")
if [ -n "$CELERY_ACTIVE" ]; then
    echo -e "${GREEN}✓${NC} Celery workers активны"
    
    # Количество активных задач
    ACTIVE_TASKS=$(echo "$CELERY_ACTIVE" | grep -c "id" || echo "0")
    echo "  Активных задач: $ACTIVE_TASKS"
else
    echo -e "${RED}✗${NC} Celery workers недоступны"
fi
echo ""

# Проверка дискового пространства
echo "💿 Проверка дискового пространства..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✓${NC} Диск: ${DISK_USAGE}% использовано"
elif [ "$DISK_USAGE" -lt 90 ]; then
    echo -e "${YELLOW}⚠${NC} Диск: ${DISK_USAGE}% использовано (предупреждение)"
else
    echo -e "${RED}✗${NC} Диск: ${DISK_USAGE}% использовано (критично!)"
fi
echo ""

# Проверка логов на ошибки
echo "📋 Проверка логов на ошибки (последние 100 строк)..."
ERROR_COUNT=$(docker-compose logs --tail=100 2>&1 | grep -i "error" | wc -l)
WARNING_COUNT=$(docker-compose logs --tail=100 2>&1 | grep -i "warning" | wc -l)

if [ "$ERROR_COUNT" -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Ошибок не найдено"
else
    echo -e "${RED}✗${NC} Найдено ошибок: $ERROR_COUNT"
fi

if [ "$WARNING_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}⚠${NC} Найдено предупреждений: $WARNING_COUNT"
fi
echo ""

# Нагрузочное тестирование (опционально)
echo "🔥 Нагрузочное тестирование (опционально)..."
read -p "Запустить нагрузочный тест? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Запуск 100 параллельных запросов..."
    
    START_TIME=$(date +%s)
    for i in $(seq 1 100); do
        curl -s http://localhost:5000/api/tournaments > /dev/null &
    done
    wait
    END_TIME=$(date +%s)
    
    DURATION=$((END_TIME - START_TIME))
    THROUGHPUT=$(echo "scale=2; 100 / $DURATION" | bc)
    
    echo "Завершено за ${DURATION}s"
    echo "Throughput: ${THROUGHPUT} req/s"
    
    if (( $(echo "$THROUGHPUT > 10" | bc -l) )); then
        echo -e "${GREEN}✓${NC} Производительность хорошая"
    else
        echo -e "${YELLOW}⚠${NC} Производительность может быть улучшена"
    fi
fi
echo ""

# Итоговый отчет
echo "========================================"
echo "📊 Итоговый отчет"
echo "========================================"
echo "Время проверки: $(date)"
echo ""
echo "Рекомендации:"
echo "- Регулярно проверяйте логи: docker-compose logs -f"
echo "- Мониторьте метрики: http://localhost:5000/metrics"
echo "- Проверяйте Celery: http://localhost:5555"
echo "- Делайте резервные копии: make backup"
echo ""
echo "Для подробной информации см. docs/DEPLOYMENT_GUIDE.md"
