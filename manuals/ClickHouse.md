# 📊 Полный мануал по ClickHouse: Установка, Настройка и Использование

## 📋 Содержание

1. [Введение в ClickHouse](#введение-в-clickhouse)
2. [Системные требования](#системные-требования)
3. [Установка ClickHouse](#установка-clickhouse)
4. [Базовая настройка](#базовая-настройка)
5. [Архитектура и движки таблиц](#архитектура-и-движки-таблиц)
6. [Конфигурация ClickHouse](#конфигурация-clickhouse)
7. [Управление пользователями](#управление-пользователями)
8. [Основные SQL команды](#основные-sql-команды)
9. [Работа с таблицами](#работа-с-таблицами)
10. [Аналитические функции](#аналитические-функции)
11. [Практические примеры](#практические-примеры)
12. [Лучшие практики](#лучшие-практики)

## Введение в ClickHouse

**ClickHouse** — это столбцовая аналитическая система управления базами данных (`ADBMS`), разработанная `Yandex`

Она предназначена для онлайн-аналитической обработки (`OLAP`) и позволяет выполнять сложные аналитические запросы к большим объемам данных с высокой скоростью.

**Основные особенности ClickHouse:**

- Высокая производительность аналитических запросов
- Столбцовое хранение данных
- Векторизованная обработка
- Поддержка SQL
- Масштабируемость и отказоустойчивость
- Поддержка репликации и шардинга
- Встроенные функции машинного обучения
- Поддержка различных форматов данных

## Системные требования

### Минимальные требования:

- **Операционная система:** Linux (CentOS 7+, Ubuntu 16.04+, Debian 9+), также работает в Docker
- **Процессор:** x86_64 (AMD64) с SSE 4.2 (рекомендуется также AVX2)
- **Память:** 4 ГБ RAM (рекомендуется 16 ГБ+)
- **Место на диске:** 10 ГБ свободного места
- **Свободная память:** 2 ГБ для выполнения запросов

### Рекомендуемые требования:

- **Операционная система:** Ubuntu 20.04+, CentOS 8+, Debian 11+
- **Процессор:** Multi-core с поддержкой AVX2
- **Память:** 32 ГБ+ RAM
- **Место на диске:** 100 ГБ+ свободного места
- **Свободная память:** 8 ГБ+ для выполнения запросов
- **SSD диск** для лучшей производительности

### Поддерживаемые версии ClickHouse:

- **23.8** (актуальная стабильная)
- **22.3** (поддерживается)
- **21.8** (EOL: 2024)

## Установка ClickHouse

### Метод №1: Установка на Ubuntu/Debian (рекомендуется)

#### Установка из официального репозитория:

```bash
# Добавьте ключ GPG
wget -O - https://clickhouse.com/altinity_clickhouse_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/clickhouse-keyring.gpg

# Добавьте репозиторий
echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg] https://packages.clickhouse.com/deb stable main" | sudo tee /etc/apt/sources.list.d/clickhouse.list

# Обновите список пакетов
sudo apt update

# Установите ClickHouse
sudo apt install -y clickhouse-server clickhouse-client

# Запустите сервис
sudo systemctl start clickhouse-server
sudo systemctl enable clickhouse-server
```

### Метод №2: Установка на CentOS/RHEL

#### Установка из официального репозитория:

```bash
# Добавьте репозиторий
sudo yum install yum-utils
sudo yum-config-manager --add-repo https://packages.clickhouse.com/rpm/clickhouse.repo

# Установите ClickHouse
sudo yum install -y clickhouse-server clickhouse-client

# Запустите сервис
sudo systemctl start clickhouse-server
sudo systemctl enable clickhouse-server
```

### Метод №3: Установка с помощью Docker

#### Запуск ClickHouse в Docker:

```bash
# Запустите ClickHouse с минимальной конфигурацией
docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 --ulimit nofile=262144:262144 clickhouse/clickhouse-server

# Или с монтированием тома для постоянного хранения
docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 -v clickhouse_data:/var/lib/clickhouse --ulimit nofile=262144:262144 clickhouse/clickhouse-server

# Подключитесь к серверу через клиент
docker exec -it clickhouse-server clickhouse-client
```

### Метод №4: Установка из пакетов

#### Скачивание и установка вручную:

```bash
# Скачайте пакеты (замените VERSION на актуальную версию)
VERSION=23.8.3.1
wget https://repo.clickhouse.com/rpm/stable/x86_64/clickhouse-server-${VERSION}-2.x86_64.rpm
wget https://repo.clickhouse.com/rpm/stable/x86_64/clickhouse-client-${VERSION}-2.x86_64.rpm

# Установите пакеты
sudo rpm -i clickhouse-server-${VERSION}-2.x86_64.rpm clickhouse-client-${VERSION}-2.x86_64.rpm

# Запустите сервер
sudo systemctl start clickhouse-server
```

## Базовая настройка

### Настройка конфигурационного файла:

- **Основной конфиг:** `/etc/clickhouse-server/config.xml`
- **Конфигурации пользователей:** `/etc/clickhouse-server/users.xml`
- **Дополнительные конфиги:** `/etc/clickhouse-server/config.d/` и `/etc/clickhouse-server/users.d/`

**Пример минимальной настройки:**

```xml
<!-- /etc/clickhouse-server/config.xml -->
<clickhouse>
    <logger>
        <level>trace</level>
        <console>1</console>
    </logger>
    
    <http_port>8123</http_port>
    <tcp_port>9000</tcp_port>
    
    <max_connections>4096</max_connections>
    <keep_alive_timeout>3</keep_alive_timeout>
    
    <max_memory_usage>10000000000</max_memory_usage>
    <max_memory_usage_for_user>10000000000</max_memory_usage_for_user>
    
    <users_config>users.xml</users_config>
    <default_profile>default</default_profile>
    <default_database>default</default_database>
</clickhouse>
```

### Проверка установки:

```bash
# Подключение через клиент
clickhouse-client

# Подключение с указанием хоста и порта
clickhouse-client --host=localhost --port=9000

# Выполнение одного запроса
clickhouse-client --query="SELECT version()"
```

## Архитектура и движки таблиц

### Основные движки таблиц:

#### MergeTree (основной движок):

```sql
-- Создание таблицы с движком MergeTree
CREATE TABLE hits
(
    WatchID UInt64,
    UserID UInt64,
    EventTime DateTime,
    URL String,
    Referer String,
    IP UInt32,
    IsRefresh UInt8
) ENGINE = MergeTree()
ORDER BY (UserID, EventTime);
```

#### ReplicatedMergeTree (для репликации):

```sql
CREATE TABLE hits_replica
(
    WatchID UInt64,
    UserID UInt64,
    EventTime DateTime,
    URL String
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/hits', '{replica}')
ORDER BY (UserID, EventTime);
```

#### Distributed (для шардинга):

```sql
-- Создание распределенной таблицы
CREATE TABLE hits_dist AS hits
ENGINE = Distributed(cluster_name, default, hits, rand());
```

#### SummingMergeTree (для агрегации):

```sql
CREATE TABLE visits
(
    UserID UInt64,
    VisitDate Date,
    Amount Int32,
    Tags Array(String)
) ENGINE = SummingMergeTree(Amount)
ORDER BY (UserID, VisitDate, Tags);
```

#### AggregatingMergeTree (для агрегации):

```sql
CREATE TABLE sessions
(
    SessionID String,
    UserID UInt64,
    Duration UInt32,
    PageViews UInt32
) ENGINE = AggregatingMergeTree()
ORDER BY (UserID, SessionID);
```

## Конфигурация ClickHouse

### Основные параметры config.xml:

#### Подключение и сетевые настройки:

```xml
<http_port>8123</http_port>
<https_port>8443</https_port>
<tcp_port>9000</tcp_port>
<mysql_port>9004</mysql_port>

<listen_host>::</listen_host>
<listen_host>0.0.0.0</listen_host>
<max_connections>4096</max_connections>
```

#### Настройки памяти:

```xml
<max_memory_usage>10000000000</max_memory_usage>
<max_memory_usage_for_user>10000000000</max_memory_usage_for_user>
<max_server_memory_usage_to_ram_ratio>0.9</max_server_memory_usage_to_ram_ratio>
```

#### Настройки производительности:

```xml
<max_threads>16</max_threads>
<max_block_size>65536</max_block_size>
<max_insert_block_size>1048576</max_insert_block_size>
<input_format_values_interpret_expressions>1</input_format_values_interpret_expressions>
```

### Настройка пользователей (users.xml):

```xml
<yandex>
    <users>
        <default>
            <password></password>
            <networks incl="networks" replace="replace">
                <ip>::/0</ip>
            </networks>
            <profile>default</profile>
            <quota>default</quota>
        </default>
        
        <analytics>
            <password_sha256_hex>...</password_sha256_hex>
            <networks>
                <ip>192.168.1.0/24</ip>
            </networks>
            <profile>analytics</profile>
        </analytics>
    </users>
    
    <profiles>
        <analytics>
            <max_memory_usage>10000000000</max_memory_usage>
            <use_uncompressed_cache>0</use_uncompressed_cache>
            <load_balancing>random</load_balancing>
        </analytics>
    </profiles>
</yandex>
```

## Управление пользователями

### Создание пользователя:

```sql
-- Создание пользователя через SQL (требует прав администратора)
CREATE USER analytics IDENTIFIED BY 'password';

-- Назначение прав
GRANT SELECT ON default.* TO analytics;
GRANT INSERT ON default.logs TO analytics;

-- Создание пользователя с ограничениями
CREATE USER limited_user 
    IDENTIFIED BY 'password' 
    SETTINGS max_memory_usage = 1000000000 
    PROFILE 'limited_profile';
```

### Назначение прав:

```sql
-- Назначение прав на базу данных
GRANT ALL ON database_name.* TO username;

-- Назначение конкретных прав
GRANT SELECT, INSERT, CREATE TABLE ON database_name.table_name TO username;

-- Назначение административных прав
GRANT ROLE admin TO username;
```

### Удаление пользователя:

```sql
DROP USER IF EXISTS username;
```

### Просмотр пользователей:

```sql
-- Просмотр всех пользователей
SELECT name, auth_type FROM system.users;

-- Просмотр прав пользователя
SELECT * FROM system.grants WHERE user_name = 'username';
```

## Основные SQL команды

### Подключение к ClickHouse:

```bash
# Подключение через клиент
clickhouse-client

# Подключение с параметрами
clickhouse-client --host=localhost --port=9000 --user=default --password=""
```

### Работа с базами данных:

```sql
-- Создание базы данных
CREATE DATABASE analytics ENGINE = Atomic;

-- Использование базы данных
USE analytics;

-- Просмотр всех баз данных
SHOW DATABASES;

-- Удаление базы данных
DROP DATABASE IF EXISTS analytics;
```

### Работа с таблицами:

```sql
-- Создание таблицы
CREATE TABLE events (
    id UInt64,
    event_time DateTime,
    user_id UInt64,
    event_type String,
    properties Map(String, String)
) ENGINE = MergeTree()
ORDER BY (event_time, user_id);

-- Просмотр всех таблиц
SHOW TABLES;

-- Просмотр структуры таблицы
DESCRIBE TABLE events;
-- или
EXPLAIN QUERY TREE SELECT * FROM events LIMIT 1;

-- Удаление таблицы
DROP TABLE IF EXISTS events;
```

### Основные операции:

```sql
-- Вставка данных
INSERT INTO events VALUES (1, '2023-01-01 10:00:00', 123, 'login', {'source': 'mobile'});

-- Вставка из другого источника
INSERT INTO events SELECT * FROM remote('other-server:9000', 'default', 'events', 'user', 'password');

-- Выборка данных
SELECT * FROM events LIMIT 10;
SELECT user_id, count(*) FROM events GROUP BY user_id ORDER BY count() DESC;

-- Обновление данных (используя Mutation)
ALTER TABLE events UPDATE event_type = 'updated' WHERE id = 1;

-- Удаление данных
ALTER TABLE events DELETE WHERE event_time < '2023-01-01';
```

## Работа с таблицами

### Типы данных ClickHouse:

```sql
-- Числовые типы
UInt8, UInt16, UInt32, UInt64, UInt128, UInt256
Int8, Int16, Int32, Int64, Int128, Int256
Float32, Float64
Decimal(P, S)

-- Текстовые типы
String, FixedString(N)
UUID

-- Дата и время
Date, Date32, DateTime, DateTime64(precision)

-- Специальные типы
Array(T), Tuple(...), Map(K, V)
Nullable(T), LowCardinality(T)
AggregateFunction(...)
```

### Примеры создания таблиц:

```sql
-- Таблица для хранения веб-событий
CREATE TABLE web_events (
    event_id UUID DEFAULT generateUUIDv4(),
    timestamp DateTime DEFAULT now(),
    user_id UInt64,
    session_id String,
    event_type Enum8('page_view' = 1, 'click' = 2, 'purchase' = 3),
    url String,
    referrer Nullable(String),
    user_agent String,
    ip IPv4,
    properties Map(String, String)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, user_id)
SETTINGS index_granularity = 8192;

-- Таблица с композитным первичным ключом
CREATE TABLE sales (
    order_date Date,
    region String,
    product_id UInt32,
    quantity UInt32,
    revenue Decimal(10, 2)
) ENGINE = MergeTree()
PARTITION BY order_date
ORDER BY (region, product_id, order_date)
PRIMARY KEY (region, product_id);
```

### Изменение структуры таблицы:

```sql
-- Добавление столбца
ALTER TABLE events ADD COLUMN campaign_id Nullable(UInt64);

-- Удаление столбца
ALTER TABLE events DROP COLUMN old_column;

-- Изменение типа столбца
ALTER TABLE events MODIFY COLUMN event_type String;

-- Добавление индекса
ALTER TABLE events ADD INDEX idx_event_type event_type TYPE bloom_filter GRANULARITY 1;
```

## Аналитические функции

### Агрегационные функции:

```sql
-- Стандартные агрегаты
SELECT 
    count(*),
    sum(revenue),
    avg(price),
    min(date),
    max(date)
FROM sales;

-- Статистические функции
SELECT 
    quantile(0.5)(amount) as median_amount,
    stddevPop(amount),
    varSamp(amount)
FROM transactions;

-- Уникальные значения
SELECT uniq(user_id) as unique_users FROM events;
SELECT uniqCombined(user_id) as approx_unique_users FROM events;
```

### Оконные функции:

```sql
-- Нумерация строк
SELECT 
    user_id,
    event_time,
    row_number() OVER (PARTITION BY user_id ORDER BY event_time) as event_sequence
FROM user_events;

-- Ранжирование
SELECT 
    product_id,
    revenue,
    rank() OVER (ORDER BY revenue DESC) as revenue_rank
FROM product_revenue;

-- Скользящие агрегаты
SELECT 
    date,
    revenue,
    avg(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM daily_revenue;
```

### Функции для анализа последовательностей:

```sql
-- Поиск шаблонов в последовательностях
SELECT 
    user_id,
    countMatches('.*login.*purchase.*') as login_then_purchase
FROM user_sessions
WHERE match(session_events, '.*login.*purchase.*');
```

## Практические примеры

### Пример №1: Создание аналитической системы событий

```sql
-- Создание базы данных
CREATE DATABASE IF NOT EXISTS analytics;

-- Таблица для сырых событий
CREATE TABLE analytics.raw_events (
    event_id UUID DEFAULT generateUUIDv4(),
    received_time DateTime DEFAULT now(),
    event_time DateTime,
    user_id UInt64,
    session_id String,
    event_type String,
    page_url String,
    referrer Nullable(String),
    user_agent String,
    ip String,
    properties Map(String, String)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, user_id)
SETTINGS index_granularity = 8192;

-- Таблица для агрегированных данных
CREATE TABLE analytics.daily_user_metrics (
    metric_date Date,
    user_id UInt64,
    page_views UInt32,
    sessions UInt32,
    session_duration_avg Float64
) ENGINE = SummingMergeTree()
PARTITION BY toYYYY(metric_date)
ORDER BY (metric_date, user_id)
SETTINGS index_granularity = 8192;
```

### Пример №2: Запросы для анализа пользовательского поведения

```sql
-- Активные пользователи за день
SELECT 
    toDate(event_time) as day,
    count(DISTINCT user_id) as active_users
FROM analytics.raw_events
GROUP BY day
ORDER BY day DESC;

-- Самые популярные страницы
SELECT 
    page_url,
    count(*) as page_views,
    count(DISTINCT user_id) as unique_visitors
FROM analytics.raw_events
WHERE event_type = 'page_view'
GROUP BY page_url
ORDER BY page_views DESC
LIMIT 20;

-- Конверсии
SELECT 
    user_id,
    countIf(event_type = 'purchase') as purchases,
    countIf(event_type = 'cart_add') as cart_adds,
    if(cart_adds > 0, purchases/cart_adds, 0) as conversion_rate
FROM analytics.raw_events
GROUP BY user_id
HAVING purchases > 0;
```

### Пример №3: Импорт данных из CSV

```bash
# Импорт CSV файла в ClickHouse
clickhouse-client --query="INSERT INTO table_name FORMAT CSVWithNames" < data.csv

# Или через HTTP API
curl -sS "http://localhost:8123/?query=INSERT%20INTO%20table_name%20FORMAT%20CSVWithNames" --data-binary @data.csv
```

## Лучшие практики

### 1. Оптимизация производительности:

```sql
-- Используйте подходящие типы данных
-- UInt64 вместо String для ID
-- Date вместо DateTime если не нужна точность до секунды
-- Enum вместо String для ограниченного набора значений

-- Создавайте правильные первичные ключи
-- ORDER BY (high_cardinality_column, low_cardinality_column)
-- Не используйте слишком много столбцов в ORDER BY
```

### 2. Партицирование:

```sql
-- Используйте партицирование для больших таблиц
CREATE TABLE events
...
PARTITION BY toYYYYMM(event_time)  -- по месяцам
ORDER BY (event_time, user_id);

-- Или по дням для меньших партиций
PARTITION BY toDate(event_time);
```

### 3. Использование материализованных представлений:

```sql
-- Создание материализованного представления для агрегации
CREATE MATERIALIZED VIEW daily_stats
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, event_type)
AS SELECT
    toDate(event_time) AS event_date,
    event_type,
    count(*) AS event_count,
    sum(toUInt64(amount)) AS total_amount
FROM raw_events
GROUP BY event_date, event_type;
```

### 4. Настройка кэширования:

```sql
-- Используйте uncompressed cache для часто запрашиваемых данных
-- Настройте max_memory_usage в профилях пользователей
-- Используйте SETTINGS для оптимизации конкретных запросов
```

### 5. Мониторинг и обслуживание:

```sql
-- Проверка состояния таблиц
SELECT 
    database,
    table,
    engine,
    partition_key,
    sorting_key,
    rows,
    bytes_on_disk
FROM system.tables
WHERE database = 'analytics';

-- Мониторинг активных запросов
SELECT 
    query_id,
    user,
    query,
    elapsed,
    memory_usage
FROM system.processes;
```

### 6. Безопасность:

- Используйте аутентификацию с надежными паролями
- Ограничьте права пользователей минимально необходимыми
- Используйте сети для ограничения доступа
- Регулярно обновляйте ClickHouse до последних версий

---

#### 💼 Автор: Дуплей Максим Игоревич

### 📲 Контакты:

- **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)
- **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 26.01.2026

▶️ Версия 1.0

---
> 📧 **Предложения по сотрудничеству:** maksimqwe42@mail.ru

---

### 💼 Профиль на Profi.ru
[![Profi.ru Profile](https://img.shields.io/badge/Profi.ru-Дуплей%20М.И.-FF6B35?style=for-the-badge)](https://profi.ru/profile/DupleyMI)

> Консультации и услуги программирования на платформе Profi.ru

---

### 📚 Услуги обучения
[![Обучение технологиям и языкам программирования на Kwork](https://img.shields.io/badge/Kwork-Обучение%20Программированию-blue?style=for-the-badge&logo=kwork)](https://kwork.ru/usability-testing/42465951/obuchenie-tekhnologiyam-i-yazykam-programmirovaniya)

> Профессиональное обучение технологиям и языкам программирования. Персональные консультации и курсы от опытного преподавателя.

---

### 🏫 О школе
[![Website](https://img.shields.io/badge/Maestro7IT-school--maestro7it.ru-darkgreen?style=for-the-badge)](https://school-maestro7it.ru/)

> Инновационная школа программирования, специализирующаяся на подготовке специалистов в области современных технологий и языков программирования.