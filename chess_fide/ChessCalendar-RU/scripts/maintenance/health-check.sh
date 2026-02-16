#!/bin/bash
# Comprehensive health check script

set -e

echo "🏥 Running health checks..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

FAILED=0

check_service() {
    local name=$1
    local url=$2
    
    if curl -f -s "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $name is healthy"
        return 0
    else
        echo -e "${RED}❌${NC} $name is unhealthy"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

check_docker_service() {
    local service=$1
    
    if docker-compose ps "$service" | grep -q "Up"; then
        echo -e "${GREEN}✅${NC} Docker service $service is running"
        return 0
    else
        echo -e "${RED}❌${NC} Docker service $service is not running"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo ""
echo "=== HTTP Health Checks ==="
check_service "API Gateway" "http://localhost:5000/health"
check_service "Tournament Service" "http://localhost:5001/health"
check_service "User Service" "http://localhost:5002/health"

echo ""
echo "=== Docker Services ==="
check_docker_service "redis"
check_docker_service "celery-worker"
check_docker_service "celery-beat"

echo ""
echo "=== Redis Check ==="
if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo -e "${GREEN}✅${NC} Redis is responding"
else
    echo -e "${RED}❌${NC} Redis is not responding"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "=== Celery Check ==="
ACTIVE_TASKS=$(docker-compose exec -T celery-worker celery -A app.celery_app inspect active 2>/dev/null | grep -c "tasks" || echo "0")
echo -e "${GREEN}ℹ️${NC}  Active Celery tasks: $ACTIVE_TASKS"

echo ""
echo "=== Disk Space ==="
DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✅${NC} Disk usage: ${DISK_USAGE}%"
else
    echo -e "${YELLOW}⚠️${NC}  Disk usage: ${DISK_USAGE}% (Warning: >80%)"
fi

echo ""
echo "=== Memory Usage ==="
if command -v free &> /dev/null; then
    MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    if [ "$MEM_USAGE" -lt 80 ]; then
        echo -e "${GREEN}✅${NC} Memory usage: ${MEM_USAGE}%"
    else
        echo -e "${YELLOW}⚠️${NC}  Memory usage: ${MEM_USAGE}% (Warning: >80%)"
    fi
fi

echo ""
echo "========================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All health checks passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED health check(s) failed${NC}"
    exit 1
fi
