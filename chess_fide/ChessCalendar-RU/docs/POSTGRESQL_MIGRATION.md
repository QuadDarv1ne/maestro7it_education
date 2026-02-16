# Миграция на PostgreSQL

## Обзор

Этот документ описывает процесс миграции ChessCalendar-RU с SQLite на PostgreSQL для production использования.

## Содержание

1. [Подготовка](#подготовка)
2. [Установка PostgreSQL](#установка-postgresql)
3. [Настройка базы данных](#настройка-базы-данных)
4. [Миграция данных](#миграция-данных)
5. [Проверка](#проверка)
6. [Переключение приложения](#переключение-приложения)
7. [Откат](#откат)

## Подготовка

### 1. Резервное копирование

Перед миграцией создайте резервную копию текущей базы данных:

```bash
# Копирование SQLite базы
cp chess_calendar.db chess_calendar.db.backup

# Экспорт данных в JSON (опционально)
python scripts/export_data.py --format json --output backup.json
```

### 2. Проверка зависимостей

Убедитесь, что установлены необходимые пакеты:

```bash
pip install psycopg2-binary alembic sqlalchemy
```

## Установка PostgreSQL

### Windows

1. Скачайте установщик с https://www.postgresql.org/download/windows/
2. Запустите установщик и следуйте инструкциям
3. Запомните пароль для пользователя `postgres`

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS

```bash
brew install postgresql
brew services start postgresql
```

### Docker

```bash
docker run --name chess-postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=chess_calendar \
  -p 5432:5432 \
  -d postgres:15
```

## Настройка базы данных

### 1. Создание пользователя и базы данных

```sql
-- Подключитесь к PostgreSQL
psql -U postgres

-- Создайте пользователя
CREATE USER chess_user WITH PASSWORD 'secure_password_here';

-- Создайте базу данных
CREATE DATABASE chess_calendar OWNER chess_user;

-- Предоставьте права
GRANT ALL PRIVILEGES ON DATABASE chess_calendar TO chess_user;

-- Выход
\q
```

### 2. Настройка подключения

Создайте или обновите файл `.env`:

```bash
# PostgreSQL Configuration
POSTGRESQL_URL=postgresql://chess_user:secure_password_here@localhost:5432/chess_calendar

# Или используйте отдельные параметры
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chess_calendar
DB_USER=chess_user
DB_PASSWORD=secure_password_here
```

### 3. Оптимизация PostgreSQL

Отредактируйте `postgresql.conf` для оптимальной производительности:

```conf
# Память
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
work_mem = 16MB

# Контрольные точки
checkpoint_completion_target = 0.9
wal_buffers = 16MB

# Планировщик
random_page_cost = 1.1
effective_io_concurrency = 200

# Логирование
log_min_duration_statement = 1000
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
```

## Миграция данных

### Автоматическая миграция

Используйте скрипт миграции:

```bash
# Базовая миграция
python scripts/migrate_to_postgresql.py \
  --source sqlite:///chess_calendar.db \
  --target postgresql://chess_user:password@localhost:5432/chess_calendar

# С переменной окружения
export POSTGRESQL_URL=postgresql://chess_user:password@localhost:5432/chess_calendar
python scripts/migrate_to_postgresql.py
```

### Ручная миграция

#### 1. Создание схемы

```bash
# Применить миграции Alembic
export DATABASE_URL=$POSTGRESQL_URL
alembic upgrade head
```

#### 2. Экспорт данных из SQLite

```python
from sqlalchemy import create_engine
import pandas as pd

# Подключение к SQLite
sqlite_engine = create_engine('sqlite:///chess_calendar.db')

# Экспорт каждой таблицы
tables = ['user', 'tournament', 'tournament_rating', 'favorite_tournament']

for table in tables:
    df = pd.read_sql_table(table, sqlite_engine)
    df.to_csv(f'{table}.csv', index=False)
```

#### 3. Импорт данных в PostgreSQL

```python
from sqlalchemy import create_engine
import pandas as pd

# Подключение к PostgreSQL
pg_engine = create_engine('postgresql://chess_user:password@localhost:5432/chess_calendar')

# Импорт каждой таблицы
for table in tables:
    df = pd.read_csv(f'{table}.csv')
    df.to_sql(table, pg_engine, if_exists='append', index=False)
```

## Проверка

### 1. Проверка количества записей

```bash
# Автоматическая проверка
python scripts/migrate_to_postgresql.py --verify-only
```

### 2. Ручная проверка

```sql
-- Подключитесь к PostgreSQL
psql -U chess_user -d chess_calendar

-- Проверьте количество записей
SELECT 'user' as table_name, COUNT(*) FROM "user"
UNION ALL
SELECT 'tournament', COUNT(*) FROM tournament
UNION ALL
SELECT 'tournament_rating', COUNT(*) FROM tournament_rating;

-- Проверьте индексы
\di

-- Проверьте внешние ключи
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```

### 3. Тестирование приложения

```bash
# Запустите приложение с PostgreSQL
export DATABASE_URL=$POSTGRESQL_URL
python run.py

# Проверьте основные функции
curl http://localhost:5000/
curl http://localhost:5000/api/tournaments
```

## Переключение приложения

### 1. Обновите конфигурацию

В `config/config.py`:

```python
class Config:
    # PostgreSQL вместо SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://chess_user:password@localhost:5432/chess_calendar'
    
    # Оптимизация для PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 40,
        'pool_timeout': 30,
        'echo': False,
        'connect_args': {
            'connect_timeout': 10,
            'options': '-c timezone=utc'
        }
    }
```

### 2. Обновите .env

```bash
# Замените SQLite на PostgreSQL
DATABASE_URL=postgresql://chess_user:password@localhost:5432/chess_calendar
```

### 3. Перезапустите приложение

```bash
# Остановите текущий процесс
pkill -f "python run.py"

# Запустите с новой конфигурацией
python run.py
```

## Откат

Если что-то пошло не так, вы можете откатиться к SQLite:

### 1. Восстановите резервную копию

```bash
cp chess_calendar.db.backup chess_calendar.db
```

### 2. Обновите конфигурацию

```bash
# В .env
DATABASE_URL=sqlite:///chess_calendar.db
```

### 3. Перезапустите приложение

```bash
python run.py
```

## Производительность

### Индексы

PostgreSQL автоматически создаст индексы из моделей SQLAlchemy. Дополнительные индексы:

```sql
-- Индексы для поиска
CREATE INDEX idx_tournament_search ON tournament USING gin(to_tsvector('russian', name || ' ' || COALESCE(description, '')));

-- Индексы для дат
CREATE INDEX idx_tournament_dates ON tournament (start_date, end_date);

-- Индексы для статистики
CREATE INDEX idx_tournament_rating_stats ON tournament_rating (tournament_id, rating);
```

### Vacuum и Analyze

Регулярно выполняйте обслуживание:

```sql
-- Анализ таблиц
ANALYZE;

-- Очистка
VACUUM ANALYZE;

-- Автоматическая настройка
ALTER TABLE tournament SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE tournament SET (autovacuum_analyze_scale_factor = 0.05);
```

## Мониторинг

### 1. Проверка активных соединений

```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'chess_calendar';
```

### 2. Медленные запросы

```sql
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### 3. Размер базы данных

```sql
SELECT pg_size_pretty(pg_database_size('chess_calendar'));
```

## Резервное копирование

### Автоматическое резервное копирование

```bash
#!/bin/bash
# backup_postgres.sh

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/chess_calendar_$DATE.sql"

# Создание резервной копии
pg_dump -U chess_user -d chess_calendar -F c -f "$BACKUP_FILE"

# Сжатие
gzip "$BACKUP_FILE"

# Удаление старых копий (старше 30 дней)
find "$BACKUP_DIR" -name "chess_calendar_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

### Восстановление из резервной копии

```bash
# Восстановление
gunzip chess_calendar_20260216_120000.sql.gz
pg_restore -U chess_user -d chess_calendar -c chess_calendar_20260216_120000.sql
```

## Troubleshooting

### Проблема: Ошибка подключения

```
psycopg2.OperationalError: could not connect to server
```

**Решение:**
1. Проверьте, запущен ли PostgreSQL: `sudo systemctl status postgresql`
2. Проверьте настройки в `pg_hba.conf`
3. Проверьте firewall

### Проблема: Медленные запросы

**Решение:**
1. Проверьте индексы: `\di`
2. Выполните `ANALYZE`
3. Проверьте план запроса: `EXPLAIN ANALYZE SELECT ...`

### Проблема: Нехватка памяти

**Решение:**
1. Уменьшите `shared_buffers`
2. Уменьшите `work_mem`
3. Настройте `max_connections`

## Дополнительные ресурсы

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy PostgreSQL Dialect](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## Поддержка

По вопросам миграции обращайтесь к команде разработки.
