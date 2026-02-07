# SQL Query Testing Framework
# Используйте этот фреймворк для проверки и отладки SQL-запросов

## Создание тестовой базы данных
CREATE DATABASE IF NOT EXISTS sql_test;

## Базовая схема тестов
Типы проверки, поддерживаемых тест-фреймворком:

1. **Синтаксическая проверка** - проверяет корректность SQL-синтаксиса
2. **Структурная проверка** - проверяет наличие необходимых таблиц и колонок
3. **Функциональная проверка** - проверяет корректность результатов
4. **Производительная проверка** - проверяет эффективность запросов

## Примеры тестов

### Тест 1: Проверка структуры таблицы
```sql
-- Проверяем, что таблица существует и имеет правильную структуру
SELECT 
    name as column_name,
    type as data_type,
    "notnull" as is_not_null,
    dflt_value as default_value
FROM pragma_table_info('test_customers')
ORDER BY cid;
```

### Тест 2: Проверка наличия данных
```sql
-- Проверяем, что таблица содержит данные
SELECT 
    COUNT(*) as total_rows,
    COUNT(first_name) as non_null_first_names,
    COUNT(DISTINCT country) as unique_countries
FROM test_customers;
```

### Тест 3: Проверка целостности данных
```sql
-- Проверяем ограничения и связи
SELECT 
    'Customers without orders' as test_name,
    COUNT(*) as issue_count
FROM test_customers c
LEFT JOIN test_orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL

UNION ALL

SELECT 
    'Orders without customers' as test_name,
    COUNT(*) as issue_count
FROM test_orders o
LEFT JOIN test_customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

### Тест 4: Проверка бизнес-логики
```sql
-- Проверяем корректность расчетов
SELECT 
    'Average order value calculation' as test_name,
    CASE 
        WHEN ABS(AVG(total_amount) - (SELECT AVG(total_amount) FROM test_orders)) < 0.01 
        THEN 'PASS' 
        ELSE 'FAIL' 
    END as result
FROM test_orders;
```

## Автоматизированные тесты

### Тест-кейс 1: Базовые операции SELECT
```sql
-- Тест: Простой SELECT
SELECT first_name, last_name FROM test_customers LIMIT 3;

-- Ожидаемый результат: 3 строки с именами и фамилиями
-- Expected columns: first_name, last_name
-- Expected row count: 3
```

### Тест-кейс 2: Фильтрация данных
```sql
-- Тест: WHERE clause
SELECT * FROM test_customers WHERE country = 'Россия';

-- Ожидаемый результат: все клиенты из России
-- Expected row count: 10
```

### Тест-кейс 3: Агрегация
```sql
-- Тест: GROUP BY и агрегатные функции
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price
FROM test_products
GROUP BY category;

-- Ожидаемый результат: группировка по категориям с подсчетом
```

### Тест-кейс 4: JOIN операции
```sql
-- Тест: INNER JOIN
SELECT 
    c.first_name,
    c.last_name,
    o.total_amount
FROM test_customers c
INNER JOIN test_orders o ON c.customer_id = o.customer_id;

-- Ожидаемый результат: объединение данных клиентов и заказов
```

## Проверка производительности

### Тест: Индексы
```sql
-- Проверяем наличие индексов
SELECT 
    name as index_name,
    tbl_name as table_name
FROM sqlite_master 
WHERE type = 'index' 
AND tbl_name IN ('test_customers', 'test_orders', 'test_products');
```

### Тест: EXPLAIN для анализа плана выполнения
```sql
-- Анализируем план выполнения запроса
EXPLAIN QUERY PLAN
SELECT 
    c.first_name,
    o.total_amount
FROM test_customers c
JOIN test_orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Россия';
```

## Отчет о тестировании

### Формат отчета
```sql
-- Генерация отчета о тестировании
WITH test_results AS (
    SELECT 'Syntax Check' as test_name, 'PASS' as result
    UNION ALL
    SELECT 'Data Integrity', 'PASS'
    UNION ALL
    SELECT 'Business Logic', 'PASS'
    UNION ALL
    SELECT 'Performance', 'WARNING'
)
SELECT 
    test_name,
    result,
    CASE 
        WHEN result = 'PASS' THEN '✅'
        WHEN result = 'FAIL' THEN '❌'
        WHEN result = 'WARNING' THEN '⚠️'
    END as status_icon
FROM test_results
ORDER BY test_name;
```

## Рекомендации по тестированию

1. **Начинайте с простых запросов** - проверяйте базовый синтаксис
2. **Постепенно усложняйте** - добавляйте JOIN, агрегации, подзапросы
3. **Проверяйте граничные условия** - NULL значения, пустые таблицы
4. **Тестируйте производительность** - большие наборы данных
5. **Используйте EXPLAIN** - для оптимизации запросов

## Пример комплексного теста
```sql
-- Комплексный тест для проверки аналитического запроса
WITH expected_results AS (
    SELECT 
        'Электроника' as category,
        4 as expected_count,
        73750.00 as expected_avg_price
    UNION ALL
    SELECT 
        'Бытовая техника' as category,
        4 as expected_count,
        23625.00 as expected_avg_price
),
actual_results AS (
    SELECT 
        category,
        COUNT(*) as actual_count,
        ROUND(AVG(price), 2) as actual_avg_price
    FROM test_products
    GROUP BY category
)
SELECT 
    e.category,
    e.expected_count,
    a.actual_count,
    CASE WHEN e.expected_count = a.actual_count THEN '✅' ELSE '❌' END as count_check,
    e.expected_avg_price,
    a.actual_avg_price,
    CASE WHEN ABS(e.expected_avg_price - a.actual_avg_price) < 1.00 THEN '✅' ELSE '❌' END as price_check
FROM expected_results e
JOIN actual_results a ON e.category = a.category;
```