# Тренировка запросов к базе данных Basketball

**Узнать колличество таблиц в базе данных и их наименования:**

```sql
SELECT name AS TABLE_NAME
FROM sqlite_master
WHERE type = 'table';
```

**Узнать структуру таблицы:**

```sql
PRAGMA table_info(имя_таблицы);
```

**Найти команды, основанные после 2000 года:**

```sql
SELECT full_name, year_founded
FROM Team
WHERE year_founded > 2000;
```

**Преподаватель:** Дуплей Максим Игоревич

**Дата:** 14.03.2025
