# Примеры использования улучшений

## HTTP Кэширование

### Использование декоратора @etag_cache

```python
from app.utils.http_cache import etag_cache
from flask import Blueprint

api_bp = Blueprint('api', __name__)

@api_bp.route('/tournaments')
@etag_cache(timeout=300, vary_on=['Accept-Language'])
def get_tournaments():
    """Турниры с ETag кэшированием на 5 минут"""
    tournaments = Tournament.query.all()
    return jsonify([t.to_dict() for t in tournaments])
```

### Использование @cache_control

```python
from app.utils.http_cache import cache_control

@api_bp.route('/tournaments/<int:id>')
@cache_control(max_age=600, public=True, must_revalidate=True)
def get_tournament(id):
    """Турнир с Cache-Control заголовками"""
    tournament = Tournament.query.get_or_404(id)
    return jsonify(tournament.to_dict())
```

### Использование @cached_view

```python
from app.utils.http_cache import cached_view

@main_bp.route('/calendar')
@cached_view(timeout=300, key_prefix='calendar')
def calendar():
    """View с кэшированием результата"""
    tournaments = Tournament.query.filter(
        Tournament.start_date >= datetime.now()
    ).all()
    return render_template('calendar.html', tournaments=tournaments)
```

### Инвалидация кэша view

```python
from app.utils.http_cache import invalidate_view_cache

@api_bp.route('/tournaments', methods=['POST'])
def create_tournament():
    # Создаем турнир
    tournament = Tournament(**request.json)
    db.session.add(tournament)
    db.session.commit()
    
    # Инвалидируем кэш
    invalidate_view_cache('/api/tournaments*')
    invalidate_view_cache('/calendar')
    
    return jsonify(tournament.to_dict()), 201
```

---

## Многоуровневое кэширование

### Использование cache_manager

```python
from app.utils.cache_manager import cache_manager

# Установка значения
cache_manager.set('user:123', user_data, timeout=600, tags=['users'])

# Получение значения
user_data = cache_manager.get('user:123')

# Удаление
cache_manager.delete('user:123')

# Инвалидация по тегу
cache_manager.invalidate_by_tag('users')

# Инвалидация по паттерну
cache_manager.invalidate_by_pattern('user:*')

# Статистика
stats = cache_manager.get_stats()
print(f"L1 utilization: {stats['l1']['utilization']:.2f}%")
```

### Использование декоратора @cached

```python
from app.utils.cache_manager import cached

@cached(timeout=600, tags=['tournaments', 'list'], key_prefix='tournaments')
def get_upcoming_tournaments(days=30):
    """Функция с автоматическим кэшированием"""
    end_date = datetime.now() + timedelta(days=days)
    return Tournament.query.filter(
        Tournament.start_date <= end_date,
        Tournament.status == 'Scheduled'
    ).all()

# Вызов функции - результат будет закэширован
tournaments = get_upcoming_tournaments(days=7)
```

### Использование специализированных менеджеров

```python
from app.utils.cache_manager import TournamentCacheManager, UserCacheManager

# Получить турниры с кэшированием
tournaments = TournamentCacheManager.get_all(filters={'category': 'FIDE'})

# Получить турнир по ID
tournament = TournamentCacheManager.get_by_id(123)

# Инвалидировать кэш турнира
TournamentCacheManager.invalidate_tournament(123)

# Инвалидировать весь кэш турниров
TournamentCacheManager.invalidate_all()

# Работа с пользователями
user = UserCacheManager.get_by_id(456)
UserCacheManager.invalidate_user(456)
```

---

## Оптимизация запросов к БД

### Eager Loading

```python
from app.utils.db_optimization import EagerLoadingMixin
from app.models.tournament import Tournament

# Добавляем mixin к модели
class Tournament(db.Model, EagerLoadingMixin):
    # ... поля модели ...
    pass

# Использование
tournaments = Tournament.with_relationships('ratings', 'favorites').all()

# Или с SELECT IN (лучше для one-to-many)
tournaments = Tournament.with_selectin('ratings', 'subscriptions').all()
```

### Пагинация

```python
from app.utils.db_optimization import PaginationHelper

# Offset-based пагинация
query = Tournament.query.filter(Tournament.status == 'Scheduled')
result = PaginationHelper.paginate(query, page=1, per_page=20)

print(f"Total: {result['total']}")
print(f"Pages: {result['pages']}")
for tournament in result['items']:
    print(tournament.name)

# Cursor-based пагинация (для больших датасетов)
query = Tournament.query.order_by(Tournament.id)
result = PaginationHelper.cursor_paginate(query, cursor=None, per_page=20)

print(f"Next cursor: {result['next_cursor']}")
for tournament in result['items']:
    print(tournament.name)
```

### Массовые операции

```python
from app.utils.db_optimization import BulkOperations

# Массовая вставка
tournaments_data = [
    {'name': 'Tournament 1', 'location': 'Moscow', ...},
    {'name': 'Tournament 2', 'location': 'SPb', ...},
    # ... еще 1000 записей
]
BulkOperations.bulk_insert(db, Tournament, tournaments_data, batch_size=1000)

# Массовое обновление
updates = [
    {'id': 1, 'status': 'Completed'},
    {'id': 2, 'status': 'Completed'},
    # ...
]
BulkOperations.bulk_update(db, Tournament, updates, batch_size=500)

# Массовое удаление
ids_to_delete = [1, 2, 3, 4, 5, ...]
BulkOperations.bulk_delete(db, Tournament, ids_to_delete, batch_size=1000)
```

### Кэширование запросов

```python
from app.utils.db_optimization import QueryCache
from app.utils.cache_manager import cache_manager

query_cache = QueryCache(cache_manager)

# Выполнить запрос с кэшированием
query = Tournament.query.filter(Tournament.category == 'FIDE')
tournaments = query_cache.cached_query(
    query, 
    cache_key='tournaments:fide', 
    timeout=600
)

# Инвалидировать кэш запроса
query_cache.invalidate_query('tournaments:fide')
```

### Логирование медленных запросов

```python
from app.utils.db_optimization import QueryOptimizer

# В app/__init__.py
def create_app():
    app = Flask(__name__)
    
    # Включаем логирование медленных запросов
    QueryOptimizer.enable_query_logging(app)
    
    # Настраиваем connection pooling
    QueryOptimizer.enable_connection_pooling(app, pool_size=10, max_overflow=20)
    
    return app
```

### Анализ производительности БД

```python
from app.utils.db_optimization import DatabaseAnalyzer

# Анализ таблицы (обновление статистики)
DatabaseAnalyzer.analyze_table(db, 'tournament')

# Получить статистику таблицы
stats = DatabaseAnalyzer.get_table_stats(db, 'tournament')
print(f"Total size: {stats['total_size']}")
print(f"Table size: {stats['table_size']}")
print(f"Indexes size: {stats['indexes_size']}")

# Получить медленные запросы
slow_queries = DatabaseAnalyzer.get_slow_queries(db, limit=10)
for query in slow_queries:
    print(f"Mean time: {query['mean_time']}ms")
    print(f"Query: {query['query'][:100]}")

# VACUUM ANALYZE
DatabaseAnalyzer.vacuum_analyze(db, 'tournament')
```

---

## Тестирование

### Запуск тестов

```bash
# Все тесты
make test

# Только unit тесты
make test-unit

# Только integration тесты
make test-integration

# С покрытием
pytest tests/ --cov=app --cov-report=html

# Конкретный файл
pytest tests/unit/test_models.py -v

# Конкретный тест
pytest tests/unit/test_models.py::TestUserModel::test_create_user -v
```

### Использование фикстур

```python
def test_create_tournament(client, admin_user, auth_headers):
    """Тест с использованием фикстур"""
    tournament_data = {
        'name': 'Test Tournament',
        'start_date': (datetime.now() + timedelta(days=30)).isoformat(),
        'end_date': (datetime.now() + timedelta(days=32)).isoformat(),
        'location': 'Moscow',
        'category': 'Regional'
    }
    
    response = client.post('/api/tournaments',
                         json=tournament_data,
                         headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == tournament_data['name']
```

### Создание собственных фикстур

```python
import pytest

@pytest.fixture
def tournament_with_ratings(db_session, sample_tournament, regular_user):
    """Турнир с рейтингами"""
    from app.models.rating import Rating
    
    for rating_value in [5, 4, 5, 3, 4]:
        rating = Rating(
            user_id=regular_user.id,
            tournament_id=sample_tournament.id,
            rating=rating_value
        )
        db_session.add(rating)
    
    db_session.commit()
    return sample_tournament

def test_average_rating(tournament_with_ratings):
    """Использование кастомной фикстуры"""
    avg = calculate_average_rating(tournament_with_ratings.id)
    assert avg == 4.2
```

---

## Docker и развертывание

### Запуск в development

```bash
# Запустить все сервисы
make start

# Проверить статус
make ps

# Посмотреть логи
make logs

# Остановить
make stop
```

### Запуск в production

```bash
# Запустить с PostgreSQL
make start-prod

# Применить миграции
make db-upgrade

# Создать администратора
make create-admin

# Проверить здоровье
make health
```

### Работа с БД

```bash
# Создать миграцию
make db-migrate message="Add new field"

# Применить миграции
make db-upgrade

# Откатить миграцию
make db-downgrade

# Заполнить тестовыми данными
make db-seed

# Создать резервную копию
make backup
```

### Мониторинг

```bash
# Проверить здоровье сервисов
make health

# Показать метрики
make metrics

# Запустить Prometheus и Grafana
make monitor

# Статус Celery
make celery-status
```

---

## Celery задачи

### Запуск Celery

```bash
# Worker
make celery-worker

# Beat (планировщик)
make celery-beat

# Flower (мониторинг)
make celery-flower

# Статус
make celery-status
```

### Создание задачи

```python
from app.celery_app import celery_app
from app.utils.cache_manager import cache_manager

@celery_app.task(bind=True, max_retries=3)
def parse_tournaments(self):
    """Парсинг турниров"""
    try:
        # Парсим турниры
        tournaments = parse_fide_tournaments()
        
        # Сохраняем в БД
        for tournament_data in tournaments:
            tournament = Tournament(**tournament_data)
            db.session.add(tournament)
        
        db.session.commit()
        
        # Инвалидируем кэш
        cache_manager.invalidate_by_tag('tournaments')
        
        return {'success': True, 'count': len(tournaments)}
    
    except Exception as exc:
        # Retry через 5 минут
        raise self.retry(exc=exc, countdown=300)
```

### Вызов задачи

```python
# Асинхронный вызов
result = parse_tournaments.delay()

# Получить результат
result.get(timeout=10)

# Вызов с параметрами
result = send_notification.apply_async(
    args=[user_id, message],
    countdown=60  # Через 60 секунд
)

# Периодическая задача (в celery_app.py)
celery_app.conf.beat_schedule = {
    'parse-tournaments-every-6-hours': {
        'task': 'app.tasks.parser_tasks.parse_tournaments',
        'schedule': crontab(minute=0, hour='*/6'),
    },
}
```

---

## Качество кода

### Линтинг

```bash
# Проверить код
make lint

# Форматировать код
make format

# Проверить форматирование
make format-check

# Проверка безопасности
make security
```

### Pre-commit hooks

```bash
# Установить hooks
pre-commit install

# Запустить вручную
pre-commit run --all-files
```

---

## Полезные команды

```bash
# Показать все команды
make help

# Информация о проекте
make info

# Статистика
make stats

# Валидация данных
make validate

# Обновить турниры
make update-tournaments

# Открыть shell
make shell

# Очистить временные файлы
make clean
```

---

## Примеры API запросов

### С ETag

```bash
# Первый запрос
curl -i http://localhost:5000/api/tournaments

# HTTP/1.1 200 OK
# ETag: "abc123"
# Cache-Control: public, max-age=300

# Повторный запрос с ETag
curl -i -H "If-None-Match: abc123" http://localhost:5000/api/tournaments

# HTTP/1.1 304 Not Modified
# ETag: "abc123"
```

### С аутентификацией

```bash
# Получить токен
TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

# Использовать токен
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/tournaments
```

### Создание турнира

```bash
curl -X POST http://localhost:5000/api/tournaments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новый турнир",
    "start_date": "2024-03-01T10:00:00",
    "end_date": "2024-03-03T18:00:00",
    "location": "Москва",
    "category": "National",
    "status": "Scheduled"
  }'
```

---

## Заключение

Эти примеры демонстрируют основные возможности улучшенной системы. Для более подробной информации см.:

- `docs/IMPROVEMENTS_COMPLETED.md` - список всех улучшений
- `docs/ARCHITECTURE.md` - архитектура системы
- `README.md` - общая документация
- `Makefile` - все доступные команды
