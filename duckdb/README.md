# Полное руководство по DuckDB - Образовательный ресурс

Этот проект демонстрирует использование `DuckDB` для создания и анализа базы данных товаров Ozon, российской торговой платформы.

## Что такое DuckDB?

`DuckDB` - это встроенная система управления OLAP базами данных SQL. Она создана для того, чтобы быть легкой, быстрой и удобной в использовании, что делает её идеальной для науки о данных, аналитики и встроенных приложений баз данных.

### Ключевые особенности DuckDB:

- **Легковесность**: Встраиваемая база данных, не требующая отдельного сервера
- **Высокая производительность**: Оптимизирована для аналитических запросов с колоночным хранением
- **Стандарт SQL**: Поддерживает большинство стандартов SQL с расширениями
- **Соответствие ACID**: Обеспечивает целостность данных
- **Кроссплатформенность**: Работает в Windows, macOS и Linux
- **Поддержка нескольких языков**: Python, R, C++, Java и другие
- **Встроенные функции**: Богатый набор аналитических функций
- **Поддержка форматов файлов**: Прямое чтение/запись файлов CSV, Parquet, JSON

## Обзор

**Проект состоит из:**

- Скрипта настройки базы данных для создания базы данных товаров Ozon
- Примеров данных товаров с реалистичными записями
- Аналитических запросов для извлечения информации из данных
- Правильной обработки ошибок и опций конфигурации

## Почему использовать DuckDB?

### Преимущества:

1. **Производительность**: DuckDB разработан для аналитических нагрузок и может обрабатывать запросы намного быстрее, чем традиционные базы данных для аналитических задач
2. **Простота**: Не требуется настройка или администрирование сервера - просто используйте как библиотеку
3. **Интеграция**: Бесшовно интегрируется с Python, R и другими инструментами для науки о данных
4. **Открытый исходный код**: Полностью бесплатный и с активным сообществом
5. **Поддержка форматов файлов**: Может напрямую запрашивать данные из CSV, Parquet, JSON файлов без импорта
6. **Соответствие стандартам**: Реализует большинство стандартов SQL
7. **Малый объем**: Минимальные требования к памяти и дисковому пространству

### Когда использовать DuckDB:

- Проекты науки о данных и аналитики
- Прототипирование и разработка
- Приложения аналитики для одного пользователя
- ETL процессы и преобразование данных
- Встроенные базы данных в приложениях
- Обработка больших наборов данных локально
- Обучение и изучение SQL

### Когда НЕ использовать DuckDB:

- Многопользовательские транзакционные приложения
- Приложения реального времени, требующие задержки менее миллисекунды
- Приложения, требующие сложных одновременных записей
- Продуктивные веб-приложения с большой нагрузкой
- Системы, требующие продвинутого репликации или кластеризации

## Files

- `main.py` - Главная точка входа проекта с поддержкой различных режимов работы
- `ozon_db_setup.py` - Скрипт для создания базы данных, вставки данных и аналитики
- `analytics.py` - Расширенная аналитика с возможностью экспорта данных
- `config.py` - Конфигурационный файл с настройками проекта
- `utils.py` - Вспомогательные функции для логирования и форматирования
- `setup_project.py` - Скрипт установки и настройки проекта
- `test_duckdb.py` - Простой скрипт для проверки установки DuckDB
- `duckdb_install_guide.txt` - Руководство по установке DuckDB на Windows
- `requirements.txt` - Зависимости Python
- `exports/` - Директория для экспортированных файлов
- `data/` - Директория для данных
- `logs/` - Директория для файлов логов
- `backup_manager.py` - Модуль для резервного копирования и восстановления базы данных
- `data_validator.py` - Модуль для проверки качества данных
- `performance_monitor.py` - Модуль для мониторинга производительности запросов
- `query_optimizer.py` - Модуль оптимизации SQL-запросов с анализом производительности
- `data_visualizer.py` - Модуль визуализации данных с созданием графиков и диаграмм
- `error_recovery.py` - Система восстановления после ошибок с точками восстановления
- `db_migration.py` - Система управления миграциями базы данных
- `run_examples.bat` - Скрипт для удобного запуска различных компонентов проекта

## Руководство по синтаксису SQL в DuckDB

DuckDB поддерживает стандарт SQL с некоторыми дополнительными возможностями. Вот исчерпывающее руководство по общим операциям:

### Основные операции:

```sql
-- Создание таблицы
CREATE TABLE example_table (
  id INTEGER PRIMARY KEY,
  name VARCHAR,
  price DECIMAL(10,2),
  created_date DATE
);

-- Вставка данных
INSERT INTO example_table VALUES (1, 'Товар A', 99.99, '2023-01-01');
INSERT INTO example_table (id, name, price) VALUES (2, 'Товар B', 149.99);

-- Запрос данных
SELECT * FROM example_table;
SELECT name, price FROM example_table WHERE price > 50;

-- Обновление данных
UPDATE example_table SET price = 89.99 WHERE id = 1;

-- Удаление данных
DELETE FROM example_table WHERE id = 2;
```

### Специфические особенности DuckDB:

#### 1. Прямой доступ к файлам
```sql
-- Чтение из CSV напрямую
SELECT * FROM read_csv_auto('data.csv');

-- Чтение из Parquet
SELECT * FROM parquet_scan('data.parquet');

-- Чтение из JSON
SELECT * FROM read_json_auto('data.json');
```

#### 2. Типы массивов и карт
```sql
-- Работа с массивами
SELECT [1, 2, 3] AS my_array;
SELECT LIST_VALUE(1, 2, 3) AS my_list;

-- Работа с картами
SELECT MAP(['key1', 'key2'], ['value1', 'value2']) AS my_map;
```

#### 3. Функции даты и времени
```sql
-- Текущая метка времени
SELECT now(), current_timestamp();

-- Арифметика дат
SELECT date '2023-01-01' + interval 1 month;

-- Извлечение частей
SELECT EXTRACT(YEAR FROM date '2023-05-15');
```

#### 4. Функции агрегирования
```sql
-- Стандартные агрегации
SELECT 
  COUNT(*) as total_rows,
  AVG(price) as avg_price,
  MIN(price) as min_price,
  MAX(price) as max_price,
  SUM(quantity) as total_quantity
FROM products;

-- Группированные агрегации
SELECT 
  category,
  COUNT(*) as product_count,
  AVG(price) as avg_price
FROM products
GROUP BY category;
```

#### 5. Оконные функции
```sql
-- Функции ранжирования
SELECT 
  name,
  price,
  ROW_NUMBER() OVER (ORDER BY price DESC) as rank_by_price,
  RANK() OVER (PARTITION BY category ORDER BY price DESC) as rank_in_category
FROM products;

-- Скользящие суммы
SELECT 
  date,
  sales,
  SUM(sales) OVER (ORDER BY date) as running_total
FROM daily_sales;
```

### Советы по производительности:

1. **Используйте подходящие типы данных**: Выбирайте наиболее конкретные типы данных для оптимального хранения и производительности
2. **Используйте колоночное хранилище**: DuckDB оптимизирован для аналитических запросов к столбцам
3. **Используйте векторизованные операции**: Используйте встроенные векторизованные функции
4. **Рассмотрите разделение**: Для больших наборов данных разделяйте по часто фильтруемым столбцам
5. **Использование индексов**: Хотя DuckDB не имеет традиционных индексов, он использует автоматическую статистику
6. **Пакетные операции**: Обрабатывайте данные более крупными частями, когда это возможно

## Features

- Robust error handling throughout the script
- Configurable database name via environment variables
- Debug mode for verbose output
- Comprehensive analytical queries
- Sample dataset with 15 realistic product entries
- Support for product characteristics stored as JSON
- Advanced configuration management with centralized settings
- Comprehensive data validation utilities
- Performance monitoring and benchmarking tools
- Database backup and recovery mechanisms
- Multi-module architecture with separation of concerns
- Extensive logging and diagnostics
- Cross-platform compatibility
- Automated setup and deployment scripts
- Rich export capabilities with multiple formats
- Interactive batch script for easy access to all features
- Advanced query optimization with performance analysis
- Data visualization with charts and graphs
- Error recovery system with restoration points
- Database migration management with versioning
- Comprehensive monitoring and diagnostic tools

## DuckDB с Python - Полное руководство

DuckDB бесшовно интегрируется с Python, делая его мощным инструментом для науки о данных и аналитики.

### Установка:

```bash
pip install duckdb
```

### Основное использование:

```python
import duckdb

# Создать базу данных в памяти
conn = duckdb.connect()

# Или подключиться к постоянному файлу базы данных
conn = duckdb.connect('my_database.db')

# Выполнить запросы
cursor = conn.cursor()
result = cursor.execute("SELECT 42 AS answer;").fetchall()
print(result)  # [(42,)]

# Использование с pandas
import pandas as pd
df = conn.execute("SELECT 42 AS answer;").fetchdf()
print(df)
```

### Работа с DataFrames:

```python
import duckdb
import pandas as pd

# Создать пример DataFrame
sample_df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Алиса', 'Боб', 'Чарли'],
    'age': [25, 30, 35]
})

# Зарегистрировать DataFrame в DuckDB
conn = duckdb.connect()
conn.register('users', sample_df)

# Запросить DataFrame
result = conn.execute("SELECT * FROM users WHERE age > 27;").fetchdf()
print(result)
```

### Практический пример - Контекст нашего проекта:

В нашем проекте товаров Ozon мы используем DuckDB для:

1. **Создания схемы базы данных**:
```python
conn.execute("""
CREATE TABLE ozon_products (
    product_id      BIGINT PRIMARY KEY,
    name            VARCHAR,
    brand           VARCHAR,
    category        VARCHAR,
    price           DOUBLE,
    old_price       DOUBLE,
    rating          DOUBLE,
    review_count    INTEGER,
    is_in_stock     BOOLEAN,
    url             VARCHAR,
    description     VARCHAR,
    characteristics VARCHAR,
    scraped_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
```

2. **Вставки данных с обработкой конфликта**:
```python
conn.execute("""
INSERT INTO ozon_products (
    product_id, name, brand, category, price, old_price,
    rating, review_count, is_in_stock, url, description, characteristics
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT (product_id) DO UPDATE SET
    price = EXCLUDED.price,
    old_price = EXCLUDED.old_price,
    rating = EXCLUDED.rating,
    review_count = EXCLUDED.review_count,
    is_in_stock = EXCLUDED.is_in_stock,
    scraped_at = NOW();
""", values)
```

3. **Выполнения аналитических запросов**:
```python
# Средняя цена по категории
result = conn.execute("""
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price
FROM ozon_products
GROUP BY category
ORDER BY avg_price DESC;
""").fetchdf()
```

### Лучшие практики для интеграции Python:

1. **Всегда закрывайте соединения**:
```python
conn.close()
# Или используйте контекстные менеджеры
with duckdb.connect() as conn:
    # Ваш код здесь
    pass
```

2. **Правильно обрабатывайте исключения**:
```python
try:
    conn = duckdb.connect('database.db')
    result = conn.execute("SELECT * FROM table").fetchdf()
except Exception as e:
    print(f"Ошибка базы данных: {e}")
finally:
    if 'conn' in locals():
        conn.close()
```

3. **Используйте параметризованные запросы** для предотвращения SQL-инъекций:
```python
# Хорошо - Параметризованный запрос
conn.execute("SELECT * FROM table WHERE id = ?", [some_id])

# Избегайте - Конкатенация строк
conn.execute(f"SELECT * FROM table WHERE id = {some_id}")
```

4. **Учитывайте использование памяти** для больших наборов данных:
```python
# Для больших наборов результатов используйте fetchmany() вместо fetchall()
while True:
    chunk = cursor.fetchmany(size=1000)
    if not chunk:
        break
    # Обработать часть
```

## Usage

### Prerequisites
- Python 3.7+
- Pip package manager

### Installation

1. Quick setup with setup script:
   ```
   python setup_project.py
   ```

2. Or install all dependencies manually:
   ```
   pip install -r requirements.txt
   ```

### Running the Scripts

1. To run the main database setup:
   ```
   python ozon_db_setup.py
   ```

2. To run full project workflow (init + analytics + export):
   ```
   python main.py --full-analysis
   ```

3. To run specific components:
   ```
   python main.py --init-db          # Initialize database
   python main.py --run-analytics    # Run analytics
   python main.py --export-data      # Export data
   ```

4. To run advanced analytics and data export:
   ```
   python analytics.py
   ```

5. To test DuckDB installation:
   ```
   python test_duckdb.py
   ```

6. To run the interactive examples script (Windows):
   ```
   run_examples.bat
   ```

7. To run data validation checks:
   ```
   python data_validator.py
   ```

8. To run performance monitoring:
   ```
   python performance_monitor.py
   ```

9. To run backup management:
   ```
   python backup_manager.py
   ```

10. To run query optimization:
   ```
   python query_optimizer.py
   ```

11. To run data visualization:
   ```
   python data_visualizer.py
   ```

12. To run error recovery system:
   ```
   python error_recovery.py
   ```

13. To run database migration system:
   ```
   python db_migration.py
   ```

3. To run in debug mode:
   ```
   DEBUG_MODE=True python ozon_db_setup.py
   ```

4. To specify a custom database name:
   ```
   DUCKDB_DATABASE_NAME=my_custom_db.duckdb python ozon_db_setup.py
   ```

## Data Schema

The `ozon_products` table includes the following columns:
- `product_id`: BIGINT (Primary Key)
- `name`: VARCHAR - Product name
- `brand`: VARCHAR - Brand name
- `category`: VARCHAR - Product category
- `price`: DOUBLE - Current price
- `old_price`: DOUBLE - Previous price (for discounts)
- `rating`: DOUBLE - Average customer rating
- `review_count`: INTEGER - Number of customer reviews
- `is_in_stock`: BOOLEAN - Availability status
- `url`: VARCHAR - Product URL
- `description`: VARCHAR - Product description
- `characteristics`: VARCHAR - Product specs in JSON format
- `scraped_at`: TIMESTAMP - When the data was added/updated

## Analytics Queries

The main script runs several analytical queries:
1. Top 3 most expensive products
2. Average rating by brand
3. Top 5 most expensive products
4. Products with rating above 4.7

## Распространенные случаи использования DuckDB

DuckDB универсален и может использоваться в различных сценариях:

1. **Наука о данных и аналитика**: Отлично подходит для разведочного анализа данных, статистических вычислений и подготовки данных для машинного обучения
2. **ETL процессы**: Преобразование и загрузка данных между различными форматами и источниками
3. **Прототипирование**: Быстрая разработка и тестирование конвейеров данных
4. **Встроенные базы данных**: Включение функциональности базы данных непосредственно в приложения
5. **Обучение**: Идеально подходит для изучения SQL благодаря своей простоте и скорости
6. **Бизнес-аналитика**: Создание отчетов и дашбордов
7. **IoT и граничные вычисления**: Легковесная база данных для устройств с ограниченными ресурсами

## Устранение распространенных проблем

### Проблемы с установкой:

- **Проблема**: `pip install duckdb` завершается ошибкой
  **Решение**: **Сначала обновите pip:** `python -m pip install --upgrade pip`, затем повторите установку

- **Проблема**: Ошибки импорта в Python
  **Решение**: Убедитесь, что вы используете поддерживаемую версию Python (3.7+)

### Проблемы с производительностью:

- **Проблема**: Медленная работа запросов
  **Решение**: Проверьте типы данных, рассмотрите возможность добавления фильтров для уменьшения объема сканируемых данных

- **Проблема**: Высокое потребление памяти
  **Решение**: Обрабатывайте данные частями, используйте соответствующие типы данных

### Проблемы с подключением:

- **Проблема**: Невозможно подключиться к файлу базы данных
  **Решение**: Проверьте права доступа к файлу и действительность пути

- **Проблема**: Ошибка блокировки базы данных
  **Решение**: Убедитесь, что соединения правильно закрыты

### Проблемы с типами данных:

- **Проблема**: Неожиданные преобразования типов данных
  **Решение**: Явно преобразуйте типы данных в запросах при необходимости

## Ресурсы для дальнейшего изучения

- [Официальная документация DuckDB](https://duckdb.org/docs/)
- [Репозиторий DuckDB на GitHub](https://github.com/duckdb/duckdb)
- [Документация по Python API DuckDB](https://duckdb.org/docs/api/python/overview.html)
- [Форум сообщества](https://github.com/duckdb/duckdb/discussions)
- [Расширения DuckDB](https://github.com/duckdb/extension-gallery)

## Особенности продвинутой аналитики

**Скрипт `advanced_analytics.py` обеспечивает дополнительные аналитические возможности:**

1. Анализ цен по категориям
2. Анализ скидок с показом процентных сбережений
3. Анализ доступности товаров по брендам
4. Корреляция цены и рейтинга
5. Анализ товаров с высоким количеством отзывов
6. Экспорт данных в форматы `CSV` и `JSON`

## Дополнительные модули проекта

**Проект также включает следующие специализированные модули:**

1. **`config.py`** - Централизованное управление конфигурацией проекта, включая настройки базы данных, параметры экспорта и аналитические настройки
2. **`utils.py`** - Вспомогательные функции для логирования, форматирования валюты, расчета скидок и других служебных операций
3. **`analytics.py`** - Расширенный модуль аналитики с поддержкой экспорта данных и комплексных отчетов
4. **`data_validator.py`** - Инструмент для проверки качества данных, выявления пропущенных значений, выбросов и логических несоответствий
5. **`performance_monitor.py`** - Система мониторинга производительности запросов, с измерением времени выполнения и использования ресурсов
6. **`backup_manager.py`** - Механизмы резервного копирования и восстановления базы данных
7. **`demo_complete.py`** - Комплексная демонстрация всех возможностей проекта в одном скрипте
8. **`query_optimizer.py`** - Инструмент для анализа и оптимизации SQL-запросов с рекомендациями по производительности
9. **`data_visualizer.py`** - Модуль визуализации данных с созданием графиков и диаграмм
10. **`error_recovery.py`** - Система восстановления после ошибок с точками восстановления и автоматическим восстановлением
11. **`db_migration.py`** - Система управления миграциями базы данных с поддержкой версионирования схемы
