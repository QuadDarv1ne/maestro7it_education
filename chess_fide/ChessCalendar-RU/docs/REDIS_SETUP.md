# Настройка Redis для Chess Calendar

## Зачем нужен Redis?

Redis используется в приложении для:
- **Кэширование** - ускорение загрузки данных
- **Rate limiting** - ограничение частоты запросов
- **Celery broker** - очередь фоновых задач
- **Сессии** - хранение пользовательских сессий

## Работа без Redis

Приложение может работать без Redis в режиме разработки:
- ✅ Используется in-memory кэш
- ✅ Rate limiting работает в памяти
- ⚠️ Celery задачи недоступны
- ⚠️ Сессии хранятся в cookies

## Установка Redis

### Windows

#### Вариант 1: Memurai (рекомендуется)
Memurai - это Redis-совместимый сервер для Windows.

1. Скачайте Memurai: https://www.memurai.com/get-memurai
2. Установите и запустите
3. Redis будет доступен на `localhost:6379`

#### Вариант 2: Redis через WSL
```bash
# В WSL терминале
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

#### Вариант 3: Docker
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

### Linux

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### CentOS/RHEL
```bash
sudo yum install redis
sudo systemctl start redis
sudo systemctl enable redis
```

### macOS

#### Homebrew
```bash
brew install redis
brew services start redis
```

## Проверка установки

### Проверка подключения
```bash
# Через redis-cli
redis-cli ping
# Должно вернуть: PONG

# Через Python
python -c "import redis; r = redis.Redis(); print(r.ping())"
# Должно вернуть: True
```

### Проверка в приложении
```bash
python scripts/diagnose.py
```

## Конфигурация

### .env файл
```env
# Redis для кэширования
REDIS_URL=redis://localhost:6379/0

# Redis для Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Redis для rate limiting
RATELIMIT_STORAGE_URL=redis://localhost:6379/1
```

### Разные базы данных Redis
- База 0: Основной кэш
- База 1: Rate limiting
- База 2: Celery (опционально)

## Запуск Celery (требует Redis)

### Worker
```bash
celery -A app.celery_app worker --loglevel=info
```

### Beat (планировщик)
```bash
celery -A app.celery_app beat --loglevel=info
```

### Flower (мониторинг)
```bash
celery -A app.celery_app flower
```
Откройте http://localhost:5555

## Мониторинг Redis

### Redis CLI
```bash
# Подключение
redis-cli

# Информация о сервере
INFO

# Список ключей
KEYS *

# Статистика памяти
INFO memory

# Мониторинг команд в реальном времени
MONITOR
```

### Redis Commander (GUI)
```bash
npm install -g redis-commander
redis-commander
```
Откройте http://localhost:8081

## Оптимизация Redis

### Настройка памяти
```bash
# В redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Персистентность
```bash
# Отключить для development (быстрее)
save ""

# Включить для production
save 900 1
save 300 10
save 60 10000
```

## Troubleshooting

### Redis не запускается

#### Windows
```bash
# Проверить службу
sc query Redis

# Запустить службу
sc start Redis
```

#### Linux
```bash
# Проверить статус
sudo systemctl status redis-server

# Посмотреть логи
sudo journalctl -u redis-server -f

# Перезапустить
sudo systemctl restart redis-server
```

### Ошибка подключения

1. Проверьте, что Redis запущен:
```bash
redis-cli ping
```

2. Проверьте порт:
```bash
netstat -an | grep 6379
```

3. Проверьте firewall:
```bash
# Linux
sudo ufw allow 6379

# Windows
netsh advfirewall firewall add rule name="Redis" dir=in action=allow protocol=TCP localport=6379
```

### Очистка кэша

```bash
# Через CLI
redis-cli FLUSHDB

# Через Python
python -c "import redis; r = redis.Redis(); r.flushdb()"
```

## Production рекомендации

### Безопасность
```bash
# В redis.conf
bind 127.0.0.1
requirepass your_strong_password
```

### Обновите .env
```env
REDIS_URL=redis://:your_strong_password@localhost:6379/0
```

### Мониторинг
- Настройте алерты на использование памяти
- Мониторьте количество подключений
- Отслеживайте hit rate кэша

### Backup
```bash
# Создать snapshot
redis-cli BGSAVE

# Автоматический backup
# В redis.conf
save 900 1
save 300 10
save 60 10000
```

## Альтернативы Redis

Если Redis недоступен, можно использовать:

### Memcached
```env
CACHE_TYPE=memcached
CACHE_MEMCACHED_SERVERS=localhost:11211
```

### In-Memory (по умолчанию)
```env
# Ничего не указывать
# Приложение автоматически использует in-memory кэш
```

## Полезные команды

```bash
# Информация о Redis
redis-cli INFO

# Количество ключей
redis-cli DBSIZE

# Очистить текущую БД
redis-cli FLUSHDB

# Очистить все БД
redis-cli FLUSHALL

# Получить значение ключа
redis-cli GET key_name

# Установить значение
redis-cli SET key_name value

# Удалить ключ
redis-cli DEL key_name

# TTL ключа
redis-cli TTL key_name
```

## Заключение

Redis значительно улучшает производительность приложения, но не является обязательным для разработки. Для production окружения настоятельно рекомендуется использовать Redis.
