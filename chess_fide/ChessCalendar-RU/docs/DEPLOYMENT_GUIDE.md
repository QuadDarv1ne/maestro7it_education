# Руководство по развертыванию Chess Calendar RU

## Содержание

1. [Подготовка к развертыванию](#подготовка)
2. [Development окружение](#development)
3. [Staging окружение](#staging)
4. [Production окружение](#production)
5. [Мониторинг и обслуживание](#мониторинг)
6. [Troubleshooting](#troubleshooting)

## Подготовка

### Системные требования

#### Минимальные (Development)
- CPU: 2 cores
- RAM: 4 GB
- Disk: 20 GB
- OS: Linux/macOS/Windows с Docker

#### Рекомендуемые (Production)
- CPU: 4+ cores
- RAM: 8+ GB
- Disk: 50+ GB SSD
- OS: Ubuntu 22.04 LTS / Debian 11+

### Необходимое ПО

```bash
# Docker и Docker Compose
docker --version  # >= 24.0
docker-compose --version  # >= 2.20

# Python (для локальной разработки)
python --version  # >= 3.11

# Node.js (для фронтенда)
node --version  # >= 18.0
npm --version  # >= 9.0
```

## Development

### Быстрый старт

```bash
# 1. Клонирование репозитория
git clone https://github.com/your-org/chess-calendar-ru.git
cd chess-calendar-ru

# 2. Создание .env файла
cp config/.env.example .env

# 3. Редактирование .env
nano .env
# Установите минимум SECRET_KEY

# 4. Запуск всех сервисов
make start
# или
docker-compose up -d

# 5. Проверка статуса
make health
docker-compose ps

# 6. Создание администратора
make create-admin
```

### Доступ к сервисам

- Приложение: http://localhost:5000
- API Gateway: http://localhost:5000/api
- Flower (Celery): http://localhost:5555
- Redis: localhost:6379

### Остановка

```bash
make stop
# или
docker-compose down
```

## Staging

### Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузка для применения изменений
sudo reboot
```

### Развертывание

```bash
# 1. Клонирование на сервер
git clone https://github.com/your-org/chess-calendar-ru.git
cd chess-calendar-ru

# 2. Создание .env для staging
cp config/.env.example .env
nano .env

# Важные настройки для staging:
# SECRET_KEY=<сгенерированный ключ>
# FLASK_ENV=staging
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://redis:6379/0

# 3. Запуск с staging конфигурацией
docker-compose -f infrastructure/docker-compose.yml up -d

# 4. Проверка логов
docker-compose logs -f

# 5. Миграция БД
docker-compose exec api-gateway python manage.py migrate

# 6. Создание администратора
docker-compose exec api-gateway python manage.py create-admin
```

### Настройка Nginx

```bash
# Установка Nginx
sudo apt install nginx -y

# Создание конфигурации
sudo nano /etc/nginx/sites-available/chess-calendar

# Содержимое:
server {
    listen 80;
    server_name staging.chesscalendar.ru;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/chess-calendar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL сертификат (Let's Encrypt)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получение сертификата
sudo certbot --nginx -d staging.chesscalendar.ru

# Автообновление
sudo certbot renew --dry-run
```

## Production

### Подготовка

```bash
# 1. Клонирование
git clone https://github.com/your-org/chess-calendar-ru.git
cd chess-calendar-ru

# 2. Создание production .env
cp config/.env.production .env
nano .env
```

### Критичные настройки .env

```bash
# Безопасность
SECRET_KEY=<сгенерируйте криптостойкий ключ>
FLASK_ENV=production
FLASK_DEBUG=False
SESSION_COOKIE_SECURE=True

# База данных
DATABASE_URL=postgresql://user:password@postgres:5432/chess_calendar_prod
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_MAX_OVERFLOW=40

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_MAX_CONNECTIONS=50

# Email
EMAIL_NOTIFICATIONS_ENABLED=True
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=<app-password>

# Мониторинг
SENTRY_DSN=https://...@sentry.io/...
SENTRY_ENVIRONMENT=production

# Flower
FLOWER_USER=admin
FLOWER_PASSWORD=<сильный пароль>
```

### Развертывание

```bash
# 1. Использование оптимизированной конфигурации
docker-compose -f infrastructure/docker-compose.prod.optimized.yml up -d

# 2. Проверка статуса
docker-compose -f infrastructure/docker-compose.prod.optimized.yml ps

# 3. Миграция БД
docker-compose -f infrastructure/docker-compose.prod.optimized.yml exec api-gateway \
  python manage.py migrate

# 4. Создание администратора
docker-compose -f infrastructure/docker-compose.prod.optimized.yml exec api-gateway \
  python manage.py create-admin \
  --username admin \
  --email admin@chesscalendar.ru \
  --password <сильный пароль>

# 5. Проверка health checks
curl http://localhost:5000/health
```

### Настройка мониторинга

```bash
# Запуск мониторинга (Prometheus + Grafana)
docker-compose -f infrastructure/docker-compose.monitoring.yml up -d

# Доступ:
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

### Резервное копирование

```bash
# Автоматическое резервное копирование
# Настроено в docker-compose через Celery Beat

# Ручное резервное копирование
docker-compose exec api-gateway python manage.py backup

# Восстановление из резервной копии
docker-compose exec api-gateway python manage.py restore \
  --backup-file /app/backups/backup_2024-01-01.sql
```

## Мониторинг

### Health Checks

```bash
# Проверка всех сервисов
curl http://localhost:5000/health | jq

# Ожидаемый ответ:
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "checks": {
    "database": {"status": "healthy", "latency_ms": 5.2},
    "redis": {"status": "healthy", "latency_ms": 1.1},
    "celery": {"status": "healthy", "workers": 2}
  }
}
```

### Логи

```bash
# Все логи
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f api-gateway

# Последние 100 строк
docker-compose logs --tail=100 celery-worker

# Поиск ошибок
docker-compose logs | grep ERROR
```

### Метрики

```bash
# Prometheus метрики
curl http://localhost:5000/metrics

# Celery метрики (Flower)
open http://localhost:5555
```

### Алерты

Настройте алерты в `monitoring/alerts/`:
- `api-alerts.yml` - алерты для API
- `system-alerts.yml` - системные алерты

## Обновление

### Rolling Update (без даунтайма)

```bash
# 1. Получение обновлений
git pull origin main

# 2. Пересборка образов
docker-compose build

# 3. Обновление по одному сервису
docker-compose up -d --no-deps --build api-gateway

# 4. Проверка
curl http://localhost:5000/health

# 5. Обновление остальных сервисов
docker-compose up -d --no-deps --build tournament-service
docker-compose up -d --no-deps --build user-service
```

### Blue-Green Deployment

```bash
# 1. Запуск новой версии на другом порту
docker-compose -f docker-compose.blue.yml up -d

# 2. Проверка новой версии
curl http://localhost:5001/health

# 3. Переключение Nginx на новую версию
sudo nano /etc/nginx/sites-available/chess-calendar
# Изменить proxy_pass на http://localhost:5001

# 4. Перезагрузка Nginx
sudo nginx -t && sudo systemctl reload nginx

# 5. Остановка старой версии
docker-compose -f docker-compose.green.yml down
```

## Troubleshooting

### Проблема: Сервис не запускается

```bash
# Проверка логов
docker-compose logs <service-name>

# Проверка статуса
docker-compose ps

# Перезапуск сервиса
docker-compose restart <service-name>

# Полная пересборка
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Проблема: База данных недоступна

```bash
# Проверка подключения
docker-compose exec postgres psql -U chess_user -d chess_calendar_prod -c "SELECT 1"

# Проверка логов PostgreSQL
docker-compose logs postgres

# Восстановление из резервной копии
docker-compose exec api-gateway python manage.py restore --backup-file <file>
```

### Проблема: Redis недоступен

```bash
# Проверка Redis
docker-compose exec redis redis-cli ping

# Очистка Redis
docker-compose exec redis redis-cli FLUSHALL

# Перезапуск Redis
docker-compose restart redis
```

### Проблема: Celery не обрабатывает задачи

```bash
# Проверка workers
docker-compose exec celery-worker celery -A app.celery_app inspect active

# Проверка очереди
docker-compose exec celery-worker celery -A app.celery_app inspect reserved

# Очистка очереди
docker-compose exec celery-worker celery -A app.celery_app purge

# Перезапуск workers
docker-compose restart celery-worker celery-beat
```

### Проблема: Высокое использование памяти

```bash
# Проверка использования ресурсов
docker stats

# Ограничение памяти для сервиса
# В docker-compose.yml:
services:
  api-gateway:
    deploy:
      resources:
        limits:
          memory: 1G
```

### Проблема: Медленные запросы

```bash
# Проверка метрик
curl http://localhost:5000/metrics | grep response_time

# Анализ медленных запросов в PostgreSQL
docker-compose exec postgres psql -U chess_user -d chess_calendar_prod -c \
  "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10"

# Очистка кэша
docker-compose exec redis redis-cli FLUSHDB
```

## Безопасность

### Checklist перед production

- [ ] Изменен SECRET_KEY
- [ ] Отключен DEBUG режим
- [ ] Настроен HTTPS
- [ ] Настроены security headers
- [ ] Включен CSRF protection
- [ ] Настроен rate limiting
- [ ] Изменены пароли по умолчанию (Flower, admin)
- [ ] Настроен firewall
- [ ] Включено логирование
- [ ] Настроен мониторинг
- [ ] Настроено резервное копирование
- [ ] Обновлены все зависимости

### Регулярное обслуживание

```bash
# Еженедельно
- Проверка логов на ошибки
- Проверка использования ресурсов
- Проверка резервных копий

# Ежемесячно
- Обновление зависимостей
- Проверка безопасности (bandit, safety)
- Анализ производительности

# Ежеквартально
- Аудит безопасности
- Оптимизация базы данных
- Обновление документации
```

## Дополнительные ресурсы

- [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура системы
- [MONITORING.md](MONITORING.md) - Мониторинг и метрики
- [TESTING.md](TESTING.md) - Тестирование
- [API Documentation](http://localhost:5000/api/docs) - API документация
