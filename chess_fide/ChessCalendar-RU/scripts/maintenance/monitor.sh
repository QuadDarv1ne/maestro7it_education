#!/bin/bash
# Real-time monitoring script

echo "📊 Chess Calendar RU - Real-time Monitor"
echo "Press Ctrl+C to exit"
echo ""

while true; do
    clear
    echo "=== Chess Calendar RU Monitor ==="
    echo "Updated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    echo "=== Docker Services ==="
    docker-compose ps
    echo ""
    
    echo "=== Resource Usage ==="
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | head -10
    echo ""
    
    echo "=== Redis Info ==="
    docker-compose exec -T redis redis-cli INFO stats 2>/dev/null | grep -E "total_commands_processed|keyspace_hits|keyspace_misses" || echo "Redis not available"
    echo ""
    
    echo "=== Celery Workers ==="
    docker-compose exec -T celery-worker celery -A app.celery_app inspect active 2>/dev/null | head -20 || echo "Celery not available"
    echo ""
    
    echo "=== Recent Logs (last 5 lines) ==="
    docker-compose logs --tail=5 api-gateway 2>/dev/null || echo "No logs available"
    
    sleep 5
done
