# Рекомендации по оптимизации производительности базы данных зоопарка

## 1. Оптимизация структуры базы данных

### 1.1. Индексы
Убедитесь, что у вас есть подходящие индексы для часто используемых запросов:

```sql
-- Индексы для основных таблиц
CREATE INDEX idx_animals_species ON animals(species_id);
CREATE INDEX idx_animals_enclosure ON animals(enclosure_id);
CREATE INDEX idx_animals_health ON animals(health_status);
CREATE INDEX idx_feedings_animal_date ON feedings(animal_id, feeding_date);
CREATE INDEX idx_medical_records_animal_date ON medical_records(animal_id, record_date);
CREATE INDEX idx_vaccinations_animal_date ON vaccinations(animal_id, vaccination_date);
CREATE INDEX idx_animals_birth_date ON animals(birth_date);
CREATE INDEX idx_animals_arrival_date ON animals(arrival_date);
```

### 1.2. Составные индексы
Для часто используемых JOIN'ов и фильтров создайте составные индексы:

```sql
-- Составные индексы для сложных запросов
CREATE INDEX idx_animals_species_health ON animals(species_id, health_status);
CREATE INDEX idx_feedings_date_employee ON feedings(feeding_date, employee_id);
CREATE INDEX idx_medical_records_date_vet ON medical_records(record_date, vet_id);
```

## 2. Оптимизация запросов

### 2.1. Использование JOIN вместо подзапросов
Предпочтительно использовать JOIN вместо подзапросов для повышения производительности:

```sql
-- Неэффективно
SELECT * FROM animals 
WHERE species_id IN (SELECT id FROM species WHERE class = 'Mammal');

-- Эффективно
SELECT a.* FROM animals a
JOIN species s ON a.species_id = s.id
WHERE s.class = 'Mammal';
```

### 2.2. Использование LIMIT
Для больших таблиц всегда используйте LIMIT, если вам не нужны все результаты:

```sql
-- Получение последних 10 кормлений
SELECT * FROM feedings 
ORDER BY feeding_date DESC, feeding_time DESC 
LIMIT 10;
```

### 2.3. Оптимизация сложных запросов
Используйте временные таблицы или представления для сложных запросов:

```sql
-- Создание временной таблицы для сложного аналитического запроса
CREATE TEMPORARY TABLE temp_animal_stats AS
SELECT 
    s.name AS species,
    COUNT(a.id) AS animal_count,
    AVG(TIMESTAMPDIFF(YEAR, a.birth_date, CURDATE())) AS avg_age
FROM species s
LEFT JOIN animals a ON s.id = a.species_id
GROUP BY s.id, s.name;
```

## 3. Параметры MySQL

### 3.1. Оптимизация конфигурации
Обновите конфигурационный файл my.cnf:

```ini
# Размер буфера InnoDB
innodb_buffer_pool_size = 70% от доступной RAM

# Размер кэша запросов
query_cache_size = 256M
query_cache_type = 1

# Размер буфера сортировки
sort_buffer_size = 8M

# Размер буфера соединений
read_buffer_size = 2M
read_rnd_buffer_size = 8M

# Размер временных таблиц
tmp_table_size = 256M
max_heap_table_size = 256M
```

### 3.2. Использование партицирования
Для больших таблиц, таких как feedings и medical_records, рассмотрите использование партицирования:

```sql
-- Партицирование по дате для таблицы feedings
ALTER TABLE feedings 
PARTITION BY RANGE (YEAR(feeding_date)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 4. Использование представлений

### 4.1. Материализованные представления
Для часто используемых аналитических запросов создайте представления:

```sql
-- Представление для часто используемого запроса
CREATE VIEW animal_health_summary AS
SELECT 
    s.name AS species,
    COUNT(a.id) AS total_animals,
    SUM(CASE WHEN a.health_status = 'healthy' THEN 1 ELSE 0 END) AS healthy_count,
    SUM(CASE WHEN a.health_status != 'healthy' THEN 1 ELSE 0 END) AS unhealthy_count
FROM species s
LEFT JOIN animals a ON s.id = a.species_id
GROUP BY s.id, s.name;
```

## 5. Мониторинг производительности

### 5.1. Использование Performance Schema
Включите Performance Schema для мониторинга производительности:

```sql
-- Проверка медленных запросов
SELECT * FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST_TEXT LIKE '%animals%'
ORDER BY TIMER_WAIT DESC
LIMIT 10;
```

### 5.2. Использование Slow Query Log
Включите лог медленных запросов для выявления проблемных запросов:

```ini
slow_query_log = 1
long_query_time = 2
slow_query_log_file = /var/log/mysql/slow.log
```

## 6. Регулярное обслуживание

### 6.1. Анализ и оптимизация таблиц
Регулярно выполняйте ANALYZE и OPTIMIZE TABLE:

```sql
-- Анализ таблицы для обновления статистики
ANALYZE TABLE animals;

-- Оптимизация таблицы
OPTIMIZE TABLE feedings;
```

### 6.2. Обновление статистики
Для InnoDB таблиц обновляйте статистику регулярно:

```sql
-- Обновление статистики для оптимизатора запросов
ALTER TABLE animals DROP INDEX idx_animals_health, ADD INDEX idx_animals_health (health_status);
```

## 7. Архитектурные решения

### 7.1. Разделение нагрузки
Рассмотрите возможность разделения чтения и записи между несколькими серверами MySQL (мастер-слейв репликация).

### 7.2. Кэширование
Используйте внешние решения для кэширования частых запросов (Redis, Memcached).

## 8. Мониторинг и профилирование

### 8.1. Профилирование запросов
Используйте EXPLAIN для анализа плана выполнения запросов:

```sql
EXPLAIN FORMAT=JSON
SELECT a.name, s.name, e.name 
FROM animals a
JOIN species s ON a.species_id = s.id
JOIN enclosures e ON a.enclosure_id = e.id
WHERE a.health_status = 'healthy';
```

### 8.2. Идентификация узких мест
Создайте мониторинг для отслеживания часто выполняемых и медленных запросов:

```sql
-- Запрос для выявления самых медленных запросов
SELECT 
    DIGEST_TEXT,
    COUNT_STAR AS execution_count,
    AVG_TIMER_WAIT / 1000000000 AS avg_time_sec,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY AVG_TIMER_WAIT DESC
LIMIT 10;
```

> Следуя этим рекомендациям, вы сможете значительно повысить производительность вашей базы данных зоопарка и обеспечить быструю работу всех функций системы.
