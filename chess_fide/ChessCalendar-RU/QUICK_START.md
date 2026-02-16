# Быстрый старт - Архитектурные улучшения

## Что нового?

### 1. API Gateway с JWT аутентификацией
Теперь все запросы проходят через единую точку входа с JWT токенами.

### 2. Многоуровневое кэширование
L1 (In-Memory) + L2 (Redis) + L3 (CDN) для максимальной производительности.

### 3. Асинхронная обработка с Celery
Парсинг турниров, отправка уведомлений и другие задачи выполняются в фоне.

## Запуск с Docker Compose

```bash
# 1. Клонируйте репозиторий
git clone <repository-url>
cd chess-calendar-ru

# 2. Создайте .env файл
cp .env.example .env

# 3. Отредактируйте .env (минимум SECRET_KEY)
nano .env

# 4. Запустите все сервисы
docker-compose up -d

# 5. Проверьте статус
docker-compose ps

# 6. Создайте администратора
docker-compose exec api-gateway python manage.py --action create-admin \
  --username admin \
  --email admin@example.com \
  --password SecurePassword123
```

## Доступ к сервисам

- **API Gateway**: http://localhost:5000
- **Flower (Celery мониторинг)**: http://localhost:5555
- **Tournament Service**: http://localhost:5001
- **User Service**: http://localhost:5002

## Использование API с JWT

### 1. Получение токена

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SecurePassword123"
  }'
```

Ответ:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "expires_in": 86400
}
```

### 2. Использование токена

```bash
# Сохраните токен
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Запрос с токеном
curl -X GET http://localhost:5000/api/tournaments \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Обновление токена

```bash
curl -X POST http://localhost:5000/auth/refresh \
  -H "Authorization: Bearer $TOKEN"
```

## Работа с кэшем

### Использование в коде

```python
from app.utils.cache_manager import cached, invalidate_cache, TournamentCacheManager

# Кэширование функции
@cached(timeout=600, tags=['tournaments'], key_prefix='my_func')
def get_tournaments():
    return Tournament.query.all()

# Автоматическая инвалидация
@invalidate_cache(tags=['tournaments'])
def update_tournament(tournament_id, data):
    tournament = Tournament.query.get(tournament_id)
    # Обновление...
    db.session.commit()

# Использование менеджера кэша
tournaments = TournamentCacheManager.get_all()
TournamentCacheManager.invalidate_all()
```

### Мониторинг кэша

```python
from app.utils.cache_manager import cache_manager

# Получить статистику
stats = cache_manager.get_stats()
print(stats)

# Очистить весь кэш
cache_manager.clear()

# Инвалидировать по тегу
cache_manager.invalidate_by_tag('tournaments')

# Инвалидировать по паттерну
cache_manager.invalidate_by_pattern('tournament:*')
```

## Работа с Celery задачами

### Запуск задачи вручную

```python
from app.tasks.parser_tasks import parse_fide_tournaments

# Асинхронный запуск
result = parse_fide_tournaments.delay()

# Получение результата
print(result.get(timeout=300))
```

### Мониторинг задач через Flower

1. Откройте http://localhost:5555
2. Просмотрите активные задачи
3. Проверьте статистику выполнения
4. Управляйте worker'ами

### Полезные команды Celery

```bash
# Просмотр активных задач
docker-compose exec celery-worker celery -A app.celery_app inspect active

# Просмотр зарегистрированных задач
docker-compose exec celery-worker celery -A app.celery_app inspect registered

# Статистика
docker-compose exec celery-worker celery -A app.celery_app inspect stats

# Очистка очереди
docker-compose exec celery-worker celery -A app.celery_app purge
```

## Примеры использования

### 1. Создание турнира через API Gateway

```bash
curl -X POST http://localhost:5000/api/tournaments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Чемпионат России 2024",
    "start_date": "2024-06-01",
    "end_date": "2024-06-15",
    "location": "Москва",
    "category": "National",
    "status": "Scheduled"
  }'
```

### 2. Получение рекомендаций

```bash
curl -X GET http://localhost:5000/api/recommendations \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Запуск парсинга турниров

```python
from app.tasks.parser_tasks import parse_fide_tournaments, parse_cfr_tournaments

# Запуск парсинга FIDE
fide_task = parse_fide_tournaments.delay()

# Запуск парсинга CFR
cfr_task = parse_cfr_tournaments.delay()

# Проверка статуса
print(f"FIDE task: {fide_task.status}")
print(f"CFR task: {cfr_task.status}")
```

### 4. Отправка уведомлений

```python
from app.tasks.notification_tasks import send_notification, send_bulk_notifications

# Одно уведомление
send_notification.delay(
    user_id=1,
    title="Новый турнир",
    message="Добавлен новый турнир в вашем городе",
    notification_type="tournament_new"
)

# Массовая рассылка
user_ids = [1, 2, 3, 4, 5]
send_bulk_notifications.delay(
    user_ids=user_ids,
    title="Важное объявление",
    message="Обновление системы",
    notification_type="system"
)
```

## Health Checks

### Проверка всех сервисов

```bash
# API Gateway
curl http://localhost:5000/health

# Tournament Service
curl http://localhost:5001/health

# User Service
curl http://localhost:5002/health
```

### Метрики (только для администраторов)

```bash
curl -X GET http://localhost:5000/metrics \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Troubleshooting

### Проблема: Сервисы не запускаются

```bash
# Проверьте логи
docker-compose logs

# Проверьте конкретный сервис
docker-compose logs api-gateway

# Перезапустите сервисы
docker-compose restart
```

### Проблема: Redis недоступен

```bash
# Проверьте Redis
docker-compose exec redis redis-cli ping

# Перезапустите Redis
docker-compose restart redis
```

### Проблема: Celery задачи не выполняются

```bash
# Проверьте worker
docker-compose logs celery-worker

# Проверьте beat
docker-compose logs celery-beat

# Перезапустите Celery
docker-compose restart celery-worker celery-beat
```

### Проблема: Кэш не работает

```python
from app.utils.cache_manager import cache_manager

# Проверьте статистику
stats = cache_manager.get_stats()
print(stats)

# Очистите кэш
cache_manager.clear()
```

## Миграция с старой версии

### 1. Резервное копирование

```bash
# Создайте бэкап базы данных
python manage.py --action backup

# Экспортируйте данные
python manage.py --action export --format json
```

### 2. Обновление кода

```bash
git pull origin main
```

### 3. Обновление зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск миграций

```bash
# Если используете Alembic
alembic upgrade head
```

### 5. Запуск новой версии

```bash
docker-compose up -d
```

## Полезные ссылки

- [Полная документация по архитектуре](ARCHITECTURE.md)
- [API документация](http://localhost:5000/api/docs)
- [Flower мониторинг](http://localhost:5555)
- [Celery документация](https://docs.celeryproject.org/)
- [Redis документация](https://redis.io/documentation)

## Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Проверьте health checks
3. Обратитесь к документации
4. Создайте issue в репозитории
