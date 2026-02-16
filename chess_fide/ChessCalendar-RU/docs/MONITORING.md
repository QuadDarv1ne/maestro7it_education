# Мониторинг Chess Calendar RU

## Обзор

Система мониторинга включает:
- **Prometheus** - сбор метрик
- **Grafana** - визуализация
- **Alertmanager** - управление алертами
- **Redis Exporter** - метрики Redis
- **Node Exporter** - системные метрики
- **cAdvisor** - метрики контейнеров

## Быстрый старт

### Запуск мониторинга

```bash
# Запуск основных сервисов + мониторинг
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Или через Makefile
make start-monitoring
```

### Доступ к интерфейсам

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Alertmanager**: http://localhost:9093
- **cAdvisor**: http://localhost:8080

## Grafana

### Первый вход

1. Откройте http://localhost:3000
2. Войдите с учетными данными: admin/admin
3. Смените пароль при первом входе

### Дашборды

#### Overview Dashboard
Основной дашборд с ключевыми метриками:
- API Request Rate
- Response Time (95th percentile)
- Error Rate
- Cache Hit Rate
- Active Celery Tasks
- Redis Memory Usage
- CPU/Memory Usage

#### Создание собственного дашборда

1. Нажмите "+" → "Dashboard"
2. Добавьте панель
3. Выберите Prometheus как источник данных
4. Введите PromQL запрос

### Полезные PromQL запросы

```promql
# Request rate
rate(http_requests_total[5m])

# Response time (95th percentile)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Cache hit rate
rate(cache_hits_total[5m]) / rate(cache_requests_total[5m])

# Active Celery tasks
celery_active_tasks

# Redis memory usage
redis_memory_used_bytes / redis_memory_max_bytes

# CPU usage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes
```

## Prometheus

### Targets

Проверьте статус всех targets:
http://localhost:9090/targets

Должны быть активны:
- api-gateway
- tournament-service
- user-service
- redis
- celery
- node
- docker

### Alerts

Просмотр активных алертов:
http://localhost:9090/alerts

### Query Browser

Используйте для тестирования PromQL запросов:
http://localhost:9090/graph

## Alertmanager

### Конфигурация алертов

Алерты настроены в `monitoring/alerts/`:
- `api-alerts.yml` - алерты API
- `system-alerts.yml` - системные алерты

### Типы алертов

#### API Alerts
- **HighErrorRate**: Высокий процент ошибок (>5%)
- **SlowResponseTime**: Медленное время ответа (>1s)
- **ServiceDown**: Сервис недоступен
- **HighRequestRate**: Высокая нагрузка (>1000 req/s)
- **LowCacheHitRate**: Низкий hit rate кэша (<50%)

#### System Alerts
- **HighMemoryUsage**: Высокое использование памяти (>90%)
- **HighCPUUsage**: Высокая нагрузка CPU (>80%)
- **LowDiskSpace**: Мало места на диске (<10%)
- **RedisDown**: Redis недоступен
- **CeleryQueueBacklog**: Большая очередь задач (>1000)
- **CeleryWorkerDown**: Нет активных worker'ов

### Настройка уведомлений

Отредактируйте `monitoring/alertmanager.yml`:

```yaml
route:
  receiver: 'email'
  
receivers:
  - name: 'email'
    email_configs:
      - to: 'admin@example.com'
        from: 'alertmanager@example.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'your-email@gmail.com'
        auth_password: 'your-app-password'
```

## Метрики приложения

### Добавление метрик в код

```python
from prometheus_client import Counter, Histogram, Gauge

# Counter для подсчета событий
requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogram для измерения времени
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Gauge для текущих значений
active_users = Gauge(
    'active_users',
    'Number of active users'
)

# Использование
@app.route('/api/tournaments')
def get_tournaments():
    with request_duration.labels('GET', '/api/tournaments').time():
        # Ваш код
        result = ...
        requests_total.labels('GET', '/api/tournaments', '200').inc()
        return result
```

### Экспорт метрик

Добавьте эндпоинт `/metrics` в ваш сервис:

```python
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
```

## Мониторинг производительности

### Ключевые метрики

#### API Performance
- **Request Rate**: Количество запросов в секунду
- **Response Time**: Время ответа (p50, p95, p99)
- **Error Rate**: Процент ошибок
- **Throughput**: Пропускная способность

#### Cache Performance
- **Hit Rate**: Процент попаданий в кэш
- **Miss Rate**: Процент промахов
- **Eviction Rate**: Скорость вытеснения
- **Memory Usage**: Использование памяти

#### Celery Performance
- **Task Rate**: Скорость обработки задач
- **Queue Length**: Длина очереди
- **Task Duration**: Время выполнения задач
- **Failed Tasks**: Количество неудачных задач

#### System Performance
- **CPU Usage**: Использование CPU
- **Memory Usage**: Использование памяти
- **Disk I/O**: Операции ввода/вывода
- **Network I/O**: Сетевой трафик

### Анализ производительности

#### Медленные запросы

```promql
# Топ 10 медленных эндпоинтов
topk(10, histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])))
```

#### Высокая нагрузка

```promql
# Эндпоинты с высокой нагрузкой
topk(10, rate(http_requests_total[5m]))
```

#### Ошибки

```promql
# Эндпоинты с ошибками
rate(http_requests_total{status=~"5.."}[5m]) > 0
```

## Troubleshooting

### Prometheus не собирает метрики

1. Проверьте targets: http://localhost:9090/targets
2. Убедитесь, что сервисы доступны
3. Проверьте логи Prometheus:
   ```bash
   docker-compose logs prometheus
   ```

### Grafana не показывает данные

1. Проверьте подключение к Prometheus:
   - Configuration → Data Sources → Prometheus
   - URL должен быть: http://prometheus:9090
2. Проверьте, что Prometheus собирает метрики
3. Проверьте PromQL запросы в дашборде

### Алерты не срабатывают

1. Проверьте правила в Prometheus: http://localhost:9090/rules
2. Проверьте Alertmanager: http://localhost:9093
3. Проверьте конфигурацию уведомлений

### Высокое использование ресурсов

1. Уменьшите `scrape_interval` в prometheus.yml
2. Уменьшите `retention.time` для Prometheus
3. Ограничьте количество метрик

## Best Practices

### Метрики

1. **Используйте правильные типы**:
   - Counter для счетчиков (requests, errors)
   - Gauge для текущих значений (memory, connections)
   - Histogram для распределений (response time)
   - Summary для квантилей

2. **Именование метрик**:
   - Используйте snake_case
   - Добавляйте единицы измерения (seconds, bytes)
   - Используйте префиксы (http_, db_, cache_)

3. **Labels**:
   - Не используйте слишком много labels
   - Избегайте high-cardinality labels (user_id, request_id)
   - Используйте осмысленные имена

### Алерты

1. **Пороговые значения**:
   - Настройте реалистичные пороги
   - Используйте `for` для избежания ложных срабатываний
   - Группируйте похожие алерты

2. **Severity levels**:
   - critical: Требует немедленного вмешательства
   - warning: Требует внимания
   - info: Информационные

3. **Документация**:
   - Добавляйте описания к алертам
   - Указывайте шаги по устранению
   - Ссылки на runbooks

### Дашборды

1. **Организация**:
   - Группируйте связанные метрики
   - Используйте переменные для фильтрации
   - Добавляйте описания к панелям

2. **Производительность**:
   - Ограничивайте временной диапазон
   - Используйте агрегацию для больших данных
   - Кэшируйте запросы

3. **Визуализация**:
   - Выбирайте подходящие типы графиков
   - Используйте цвета осмысленно
   - Добавляйте пороговые значения

## Дополнительные ресурсы

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
