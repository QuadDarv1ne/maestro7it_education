# Управление базой данных

## Автоматическая инициализация

При запуске приложения база данных автоматически проверяется и инициализируется:

```bash
python run.py
```

Система автоматически:
1. ✅ Проверяет существование файла базы данных
2. ✅ Создаёт все необходимые таблицы, если их нет
3. ✅ Добавляет отсутствующие колонки в существующие таблицы
4. ✅ Проверяет целостность базы данных

В логах приложения вы увидите:
```
2026-02-17 14:43:39 - chess_calendar - INFO - DATABASE INITIALIZATION CHECK
2026-02-17 14:43:39 - chess_calendar - INFO - Database file check: ... - EXISTS
2026-02-17 14:43:39 - chess_calendar - INFO - All required tables exist (16 tables)
2026-02-17 14:43:39 - chess_calendar - INFO - DATABASE INITIALIZATION COMPLETE
2026-02-17 14:43:39 - chess_calendar - INFO - Tables: 16
2026-02-17 14:43:39 - chess_calendar - INFO - Tournaments: 10
2026-02-17 14:43:39 - chess_calendar - INFO - Users: 1
```

## Ручное управление базой данных

Для ручного управления используйте утилиту `manage_db.py`:

### Инициализация базы данных

Создать все таблицы и добавить недостающие колонки:

```bash
python manage_db.py init
```

Вывод:
```
============================================================
DATABASE INITIALIZATION
============================================================
Database file check: instance/chess_calendar.db - EXISTS
All required tables exist (16 tables)
All required columns exist in tournament table
============================================================
✓ DATABASE INITIALIZATION COMPLETE
============================================================

✓ Database initialized successfully!

Database Info:
  Engine: sqlite
  Tables: 16
  Tournaments: 0
  Users: 0
```

### Проверка состояния базы данных

Проверить, все ли таблицы и колонки существуют:

```bash
python manage_db.py check
```

Вывод:
```
============================================================
DATABASE CHECK
============================================================

Database file: ✓ EXISTS
Tables: ✓ ALL EXIST (16 tables)
Tournament columns: ✓ ALL EXIST

Database integrity: ✓ OK

Database Info:
  Engine: sqlite
  Total tables: 16
  Tournaments: 0
  Users: 0
```

### Информация о базе данных

Показать детальную информацию:

```bash
python manage_db.py info
```

Вывод:
```
============================================================
DATABASE INFORMATION
============================================================

Database URI: sqlite:///instance/chess_calendar.db
Engine: sqlite
Total tables: 16

Tables:
  - audit_log
  - favorite_tournament
  - forum_post
  - forum_thread
  - login_attempt
  - notification
  - report
  - subscription
  - tournament
  - tournament_rating
  - tournament_reminder
  - tournament_subscription
  - two_factor_secret
  - user
  - user_interaction
  - user_preference

Records:
  Tournaments: 0
  Users: 0
```

### Сброс базы данных (ОПАСНО!)

⚠️ **ВНИМАНИЕ**: Эта команда удалит ВСЕ данные!

```bash
python manage_db.py reset
```

Система попросит подтверждение:
```
============================================================
DATABASE RESET - WARNING!
============================================================

This will DELETE ALL DATA and recreate the database!

Type 'YES' to confirm: YES

Dropping all tables...
✓ All tables dropped

Creating all tables...
✓ All tables created

✓ Database reset successfully!
```

## Структура базы данных

### Основные таблицы

1. **user** - Пользователи системы
2. **tournament** - Турниры
3. **tournament_rating** - Рейтинги турниров
4. **favorite_tournament** - Избранные турниры пользователей
5. **subscription** - Подписки на уведомления
6. **notification** - Уведомления
7. **user_preference** - Настройки пользователей
8. **user_interaction** - Взаимодействия пользователей с турнирами

### Дополнительные таблицы

9. **audit_log** - Журнал аудита
10. **login_attempt** - Попытки входа
11. **two_factor_secret** - Секреты для 2FA
12. **forum_thread** - Темы форума
13. **forum_post** - Сообщения форума
14. **report** - Отчёты о проблемах
15. **tournament_reminder** - Напоминания о турнирах
16. **tournament_subscription** - Подписки на турниры

### Новые колонки в таблице tournament

- **view_count** (INTEGER) - Счётчик просмотров
- **participants_count** (INTEGER) - Количество участников
- **rating_type** (VARCHAR(50)) - Тип рейтинга

## Программный доступ

### Использование в коде

```python
from app import create_app, db
from app.utils.db_init import DatabaseInitializer

app = create_app()

with app.app_context():
    # Создать инициализатор
    initializer = DatabaseInitializer(app, db)
    
    # Полная инициализация
    success = initializer.initialize_database()
    
    # Проверка таблиц
    tables_exist, missing = initializer.check_tables_exist()
    
    # Проверка колонок
    columns_exist, missing = initializer.check_tournament_columns()
    
    # Проверка целостности
    is_ok = initializer.verify_database_integrity()
    
    # Получить информацию
    info = initializer.get_database_info()
```

### Быстрая проверка

```python
from app import create_app, db
from app.utils.db_init import verify_database

app = create_app()
is_ok = verify_database(app, db)
```

## Миграции

Для создания миграций используйте Alembic:

```bash
# Создать новую миграцию
alembic revision -m "Description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

## Резервное копирование

### SQLite

```bash
# Создать резервную копию
cp instance/chess_calendar.db instance/chess_calendar.db.backup

# Восстановить из резервной копии
cp instance/chess_calendar.db.backup instance/chess_calendar.db
```

### Автоматическое резервное копирование

Используйте скрипт `scripts/backup-manager.py`:

```bash
python scripts/backup-manager.py
```

## Устранение проблем

### Проблема: "no such column"

Если при запуске возникает ошибка `no such column: tournament.view_count`:

```bash
# Решение 1: Автоматическое исправление
python manage_db.py init

# Решение 2: Ручное добавление колонок
python -c "from app import create_app, db; from sqlalchemy import text; app = create_app(); ctx = app.app_context(); ctx.push(); db.session.execute(text('ALTER TABLE tournament ADD COLUMN view_count INTEGER DEFAULT 0')); db.session.commit()"
```

### Проблема: "no such table"

Если таблицы не существуют:

```bash
# Создать все таблицы
python manage_db.py init
```

### Проблема: База данных повреждена

```bash
# Проверить целостность
python manage_db.py check

# Если повреждена - пересоздать (потеря данных!)
python manage_db.py reset
```

## Логирование

Все операции с базой данных логируются в:
- `logs/chess_calendar.log` - общий лог
- `logs/chess_calendar_error.log` - ошибки

Пример лога инициализации:
```
2026-02-17 14:30:00 - chess_calendar - INFO - ============================================================
2026-02-17 14:30:00 - chess_calendar - INFO - DATABASE INITIALIZATION CHECK
2026-02-17 14:30:00 - chess_calendar - INFO - ============================================================
2026-02-17 14:30:00 - chess_calendar - INFO - Database file check: instance/chess_calendar.db - EXISTS
2026-02-17 14:30:00 - chess_calendar - INFO - All required tables exist (16 tables)
2026-02-17 14:30:00 - chess_calendar - INFO - All required columns exist in tournament table
2026-02-17 14:30:00 - chess_calendar - INFO - ============================================================
2026-02-17 14:30:00 - chess_calendar - INFO - ✓ DATABASE INITIALIZATION COMPLETE
2026-02-17 14:30:00 - chess_calendar - INFO - ============================================================
```

## Best Practices

1. ✅ Всегда делайте резервную копию перед изменениями
2. ✅ Используйте `manage_db.py check` для проверки состояния
3. ✅ Проверяйте логи после инициализации
4. ✅ Тестируйте миграции на копии БД
5. ⚠️ Никогда не используйте `reset` на продакшене без бэкапа

## Поддержка

При возникновении проблем:
1. Проверьте логи в `logs/`
2. Запустите `python manage_db.py check`
3. Проверьте права доступа к файлу БД
4. Убедитесь, что SQLite установлен корректно
