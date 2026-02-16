# Архитектура Chess Calendar RU

## Обзор

Chess Calendar RU использует микросервисную архитектуру с API Gateway, асинхронной обработкой задач и многоуровневым кэшированием.

## Компоненты системы

### 1. API Gateway (порт 5000)

**Назначение**: Единая точка входа для всех клиентских запросов

**Функции**:
- JWT аутентификация и авторизация
- Маршрутизация запросов к микросервисам
- Rate limiting (защита от DDoS)
- Кэширование ответов
- Агрегация данных из нескольких сервисов
- Мониторинг и логирование

**Технологии**: Flask, PyJWT, Flask-Limiter, Redis

**Эндпоинты**:
- `POST /auth/login` - Аутентификация
- `POST /auth/refresh` - Обновление токена
- `GET /auth/verify` - Проверка токена
- `GET /api/tournaments` - Список турниров
- `GET /api/users` - Список пользователей (admin)
- `GET /health` - Health check
- `GET /metrics` - Метрики (admin)

### 2. Микросервисы

#### Tournament Service (порт 5001)
- Управление турнирами (CRUD)
- Фильтрация и поиск
- Пагинация

#### User Service (порт 5002)
- Управление пользователями
- Аутентификация (базовая)
- Профили пользователей

#### Parser Service (порт 5003)
- Парсинг турниров с FIDE
- Парсинг турниров с CFR
- Валидация данных

#### Recommendation Service (порт 5008)
- Персонализированные рекомендации
- Коллаборативная фильтрация
- Трендовые турниры

#### Notification Service (порт 5007)
- Отправка уведомлений
- Email рассылки
- Push уведомления

#### Favorites Service (порт 5009)
- Избранные турниры
- Подписки на турниры

#### Calendar Service (порт 5006)
- Генерация календарей
- Экспорт в iCal

#### Image Optimization Service (порт 5005)
- Оптимизация изображений
- Генерация thumbnails

#### CDN Service (порт 5004)
- Кэширование статики
- Интеграция с CDN провайдерами

### 3. Асинхронная обработка (Celery)

**Компоненты**:
- **Celery Worker** - Обработка задач
- **Celery Beat** - Планировщик периодических задач
- **Flower** (порт 5555) - Мониторинг Celery

**Очереди задач**:
- `parser` - Парсинг турниров
- `notifications` - Отправка уведомлений
- `analytics` - Аналитика и отчеты
- `maintenance` - Обслуживание системы

**Периодические задачи**:
- Парсинг FIDE турниров (каждые 6 часов)
- Парсинг CFR турниров (каждые 6 часов)
- Отправка уведомлений (каждый час)
- Проверка предстоящих турниров (ежедневно в 9:00)
- Генерация аналитики (ежедневно в 3:00)
- Резервное копирование (ежедневно в 4:00)
- Очистка старых данных (еженедельно)

### 4. Система кэширования

**Уровни кэширования**:

#### L1 - In-Memory Cache
- Самый быстрый
- Ограниченный размер (1000 элементов)
- LFU (Least Frequently Used) вытеснение
- Локальный для каждого процесса

#### L2 - Redis Cache
- Распределенный кэш
- Поддержка тегов для группировки
- Автоматическая инвалидация по времени
- Shared между всеми сервисами

#### L3 - CDN Cache (опционально)
- Глобальное кэширование статики
- Интеграция с Cloudflare/AWS CloudFront
- Purge API для инвалидации

**Стратегии инвалидации**:
- **Time-based** - По истечении времени
- **Tag-based** - По тегам (например, все турниры)
- **Pattern-based** - По паттерну ключей
- **Event-based** - При изменении данных

**Примеры использования**:
```python
from app.utils.cache_manager import cached, invalidate_cache

@cached(timeout=600, tags=['tournaments'], key_prefix='tournaments')
def get_tournaments():
    return Tournament.query.all()

@invalidate_cache(tags=['tournaments'])
def update_tournament(tournament_id, data):
    # Обновление турнира
    pass
```

### 5. Аутентификация и авторизация

**JWT (JSON Web Tokens)**:
- Stateless аутентификация
- Токены с истечением срока действия (24 часа по умолчанию)
- Refresh токены для обновления
- Роли: user, admin

**Структура токена**:
```json
{
  "user_id": 123,
  "username": "john_doe",
  "is_admin": false,
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Защита эндпоинтов**:
- `@token_required` - Требует валидный токен
- `@admin_required` - Требует права администратора

### 6. База данных

**Текущая**: SQLite (для разработки)

**Рекомендуется для production**: PostgreSQL

**Миграция на PostgreSQL**:
```bash
# Установка PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Создание базы данных
sudo -u postgres createdb chess_calendar

# Обновление .env
DATABASE_URL=postgresql://user:password@localhost:5432/chess_calendar

# Миграция данных
python manage.py migrate
```

**Модели**:
- Tournament - Турниры
- User - Пользователи
- Notification - Уведомления
- Subscription - Подписки
- Favorite - Избранное
- Rating - Рейтинги
- Report - Отчеты

### 7. Мониторинг и логирование

**Компоненты**:
- Health checks для всех сервисов
- Метрики производительности
- Централизованное логирование
- Flower для мониторинга Celery

**Health Check эндпоинты**:
- `/health` - Статус сервиса
- `/metrics` - Метрики (admin only)

**Логирование**:
- Уровни: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Ротация логов (30 дней)
- Структурированные логи

### 8. Безопасность

**Реализованные меры**:
- JWT аутентификация
- Rate limiting (защита от DDoS)
- CSRF защита
- Security headers (CSP, HSTS, X-Frame-Options)
- Валидация входных данных
- Хэширование паролей (SHA-256, рекомендуется bcrypt)

**Рекомендации**:
- Использовать HTTPS в production
- Регулярно обновлять зависимости
- Мониторинг безопасности
- Аудит логов

## Развертывание

### Docker Compose (рекомендуется)

```bash
# Создание .env файла
cp .env.example .env
# Отредактируйте .env

# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Ручной запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск Redis
redis-server

# Запуск Celery Worker
celery -A app.celery_app worker --loglevel=info

# Запуск Celery Beat
celery -A app.celery_app beat --loglevel=info

# Запуск Flask приложения
python run.py
```

## Масштабирование

### Горизонтальное масштабирование

**API Gateway**:
- Запуск нескольких инстансов за load balancer
- Nginx/HAProxy для балансировки нагрузки

**Микросервисы**:
- Независимое масштабирование каждого сервиса
- Docker Swarm или Kubernetes для оркестрации

**Celery Workers**:
- Добавление worker'ов для обработки большего количества задач
- Разделение по очередям (parser, notifications, analytics)

### Вертикальное масштабирование

- Увеличение ресурсов (CPU, RAM) для контейнеров
- Оптимизация запросов к БД
- Настройка пулов соединений

## Мониторинг производительности

**Метрики**:
- Время ответа API
- Количество запросов в секунду
- Hit rate кэша
- Длина очередей Celery
- Использование памяти Redis
- Нагрузка на БД

**Инструменты**:
- Flower - Мониторинг Celery
- Redis CLI - Статистика Redis
- Docker stats - Использование ресурсов контейнерами

## Troubleshooting

### Проблемы с Redis
```bash
# Проверка подключения
redis-cli ping

# Просмотр ключей
redis-cli keys '*'

# Очистка кэша
redis-cli flushdb
```

### Проблемы с Celery
```bash
# Просмотр активных задач
celery -A app.celery_app inspect active

# Просмотр зарегистрированных задач
celery -A app.celery_app inspect registered

# Очистка очереди
celery -A app.celery_app purge
```

### Проблемы с микросервисами
```bash
# Проверка health check
curl http://localhost:5001/health

# Просмотр логов
docker-compose logs tournament-service
```

## Roadmap

### Ближайшие улучшения
- [ ] Миграция на PostgreSQL
- [ ] Интеграция с Prometheus/Grafana
- [ ] Централизованное логирование (ELK Stack)
- [ ] OAuth2/OpenID Connect
- [ ] GraphQL API
- [ ] WebSocket для real-time уведомлений

### Долгосрочные планы
- [ ] Kubernetes deployment
- [ ] Service Mesh (Istio)
- [ ] Distributed tracing (Jaeger)
- [ ] A/B тестирование
- [ ] Machine Learning рекомендации
