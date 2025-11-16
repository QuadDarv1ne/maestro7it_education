# Docker для Simple HR

## Быстрый старт

### 1. Создайте .env файл
```bash
cp .env.example .env
```

Отредактируйте `.env` файл с вашими настройками.

### 2. Запуск с Docker Compose

```bash
# Запуск в фоновом режиме
docker-compose up -d

# Просмотр логов
docker-compose logs -f web

# Остановка контейнеров
docker-compose down

# Остановка с удалением volumes (БД будет удалена!)
docker-compose down -v
```

### 3. Инициализация базы данных

После первого запуска выполните миграции:

```bash
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "Initial migration"
docker-compose exec web flask db upgrade
```

### 4. Заполнение тестовыми данными

```bash
docker-compose exec web python seed_data.py
```

## Управление

### Просмотр логов
```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs web
docker-compose logs db

# Следить за логами в реальном времени
docker-compose logs -f
```

### Перезапуск сервисов
```bash
# Перезапустить все
docker-compose restart

# Перезапустить конкретный сервис
docker-compose restart web
```

### Доступ к контейнеру
```bash
# Bash в web контейнере
docker-compose exec web bash

# MySQL клиент
docker-compose exec db mysql -u hr_user -p simple_hr_db
```

### Резервное копирование базы данных
```bash
docker-compose exec db mysqldump -u hr_user -p simple_hr_db > backup.sql
```

### Восстановление из резервной копии
```bash
docker-compose exec -T db mysql -u hr_user -p simple_hr_db < backup.sql
```

## Production рекомендации

1. **Измените секретные ключи** в `.env`
2. **Используйте внешний том** для MySQL данных
3. **Настройте nginx** как reverse proxy
4. **Включите SSL/TLS** сертификаты
5. **Настройте логирование** в centralized систему
6. **Используйте Docker secrets** для паролей

## Структура volumes

- `mysql_data` - данные MySQL
- `./logs` - логи приложения
- `./backups` - резервные копии

## Переменные окружения

См. `.env.example` для списка всех доступных переменных.

## Troubleshooting

### Контейнер web не запускается
```bash
docker-compose logs web
```

### База данных не подключается
Проверьте healthcheck:
```bash
docker-compose ps
```

### Порты заняты
Измените порты в `docker-compose.yml` или освободите порты 3306 и 5000.

## Масштабирование

Для запуска нескольких инстансов web:
```bash
docker-compose up -d --scale web=3
```

Затем настройте load balancer (nginx/HAProxy).
