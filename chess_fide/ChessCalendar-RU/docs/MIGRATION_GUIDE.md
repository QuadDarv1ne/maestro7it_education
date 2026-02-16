# Руководство по миграции на v2.1

## Обзор

Это руководство поможет вам мигрировать с предыдущей версии Chess Calendar RU на версию 2.1 с новой архитектурой.

## Что изменилось

### Структура проекта
- Скрипты перемещены в `/scripts`
- Документация перемещена в `/docs`
- Добавлена папка `/monitoring`

### Новые компоненты
- API Gateway (порт 5000)
- Celery для асинхронных задач
- Система мониторинга (Prometheus + Grafana)
- CI/CD pipeline

### Изменения в API
- JWT аутентификация вместо сессий
- Все запросы через API Gateway
- Новые эндпоинты для аутентификации

## Пошаговая миграция

### Шаг 1: Резервное копирование

```bash
# Создайте backup текущей версии
python manage.py --action backup

# Экспортируйте данные
python manage.py --action export --format json

# Сохраните .env файл
cp .env .env.backup
```

### Шаг 2: Обновление кода

```bash
# Сохраните изменения
git stash

# Получите последнюю версию
git pull origin main

# Восстановите изменения (если нужно)
git stash pop
```

### Шаг 3: Обновление зависимостей

```bash
# Обновите зависимости
pip install -r requirements.txt

# Или через Docker
docker-compose build
```

### Шаг 4: Обновление конфигурации

```bash
# Сравните .env с .env.example
diff .env .env.example

# Добавьте новые переменные из .env.example
# Особенно важно:
# - SECRET_KEY (если не было)
# - JWT_EXPIRATION_HOURS
# - CELERY_BROKER_URL
# - CELERY_RESULT_BACKEND
```

### Шаг 5: Миграция базы данных

```bash
# Если используете миграции
python manage.py migrate

# Или через Docker
docker-compose exec api-gateway python manage.py migrate
```

### Шаг 6: Запуск новой версии

```bash
# Остановите старую версию
docker-compose down

# Запустите новую версию
make start
# или
./scripts/start-all.sh
```

### Шаг 7: Проверка

```bash
# Проверьте health checks
make health

# Проверьте логи
make logs

# Проверьте API
curl http://localhost:5000/health
```

### Шаг 8: Создание администратора (если нужно)

```bash
# Если у вас еще нет администратора
make create-admin
```

## Миграция аутентификации

### Для клиентов API

**Старый способ** (сессии):
```bash
# Логин
curl -X POST http://localhost:5000/admin/login \
  -d "username=admin&password=password"
```

**Новый способ** (JWT):
```bash
# Получение токена
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Использование токена
curl -X GET http://localhost:5000/api/tournaments \
  -H "Authorization: Bearer <token>"
```

### Для веб-интерфейса

Веб-интерфейс продолжит работать как раньше, но внутренне будет использовать JWT.

## Миграция скриптов

### Старые пути
```bash
./start-all.sh
./start-all.bat
```

### Новые пути
```bash
./scripts/start-all.sh
scripts\start-all.bat  # Windows
```

### Или используйте Makefile
```bash
make start
```

## Новые возможности

### Makefile команды

```bash
# Вместо длинных команд Docker
docker-compose up -d
docker-compose logs -f
docker-compose exec api-gateway python manage.py --action backup

# Используйте короткие команды
make start
make logs
make backup
```

### Мониторинг

```bash
# Запустите мониторинг
make start-monitoring

# Откройте Grafana
make grafana
# http://localhost:3000 (admin/admin)

# Откройте Prometheus
make prometheus
# http://localhost:9090
```

### Автоматическое развертывание

```bash
# Вместо ручного развертывания
make deploy

# Откат при проблемах
make rollback
```

### Health checks

```bash
# Комплексная проверка
make health

# Real-time мониторинг
make monitor
```

## Troubleshooting

### Проблема: Сервисы не запускаются

```bash
# Проверьте логи
make logs

# Проверьте конфигурацию
docker-compose config

# Пересоберите образы
docker-compose build --no-cache
```

### Проблема: Ошибки аутентификации

```bash
# Проверьте SECRET_KEY в .env
grep SECRET_KEY .env

# Создайте нового администратора
make create-admin
```

### Проблема: Celery не работает

```bash
# Проверьте Redis
docker-compose exec redis redis-cli ping

# Проверьте Celery worker
docker-compose logs celery-worker

# Перезапустите Celery
docker-compose restart celery-worker celery-beat
```

### Проблема: Кэш не работает

```bash
# Очистите Redis
docker-compose exec redis redis-cli FLUSHDB

# Перезапустите сервисы
make restart
```

### Проблема: Старые данные

```bash
# Восстановите из backup
cp backups/pre-deployment/chess_calendar-*.db instance/chess_calendar.db

# Или используйте rollback
make rollback
```

## Откат к предыдущей версии

Если что-то пошло не так:

```bash
# 1. Остановите новую версию
docker-compose down

# 2. Восстановите код
git checkout <previous-version-tag>

# 3. Восстановите базу данных
cp .env.backup .env
cp backups/pre-deployment/chess_calendar-*.db instance/chess_calendar.db

# 4. Запустите старую версию
docker-compose up -d
```

## Проверка успешной миграции

### Чеклист

- [ ] Все сервисы запущены (`make ps`)
- [ ] Health checks проходят (`make health`)
- [ ] API отвечает (`curl http://localhost:5000/health`)
- [ ] JWT аутентификация работает
- [ ] Celery обрабатывает задачи (`make flower`)
- [ ] Данные сохранены
- [ ] Администратор может войти
- [ ] Мониторинг работает (`make grafana`)

### Тестовые запросы

```bash
# Health check
curl http://localhost:5000/health

# Получение токена
TOKEN=$(curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}' \
  | jq -r '.token')

# Запрос с токеном
curl -X GET http://localhost:5000/api/tournaments \
  -H "Authorization: Bearer $TOKEN"
```

## Дополнительная помощь

### Документация
- [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура
- [QUICK_START.md](QUICK_START.md) - Быстрый старт
- [DEPLOYMENT.md](DEPLOYMENT.md) - Развертывание
- [MONITORING.md](MONITORING.md) - Мониторинг

### Команды
```bash
make help  # Список всех команд
```

### Логи
```bash
make logs              # Все логи
make logs-api          # API Gateway
make logs-celery       # Celery
make logs-prometheus   # Prometheus
make logs-grafana      # Grafana
```

## FAQ

### Q: Нужно ли мигрировать данные?
A: Нет, структура базы данных не изменилась. Данные останутся как есть.

### Q: Будет ли работать старый API?
A: Да, но рекомендуется перейти на JWT аутентификацию.

### Q: Можно ли использовать без Docker?
A: Да, но Docker рекомендуется для production.

### Q: Как обновить в production?
A: Используйте `make deploy` или `./scripts/deployment/deploy-production.sh`

### Q: Что делать при ошибках?
A: Используйте `make rollback` для отката к предыдущей версии.

### Q: Нужно ли настраивать мониторинг?
A: Опционально, но рекомендуется для production.

---

**Версия**: 2.1  
**Дата**: 2024  
**Поддержка**: См. документацию в `/docs`
