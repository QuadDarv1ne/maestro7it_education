-- Учебная тренировочная база данных для ClickHouse
-- Полный SQL-скрипт с полезными доработками: схемы, оптимизации, TTL, материализованные представления,
-- примеры наполнения синтетическими данными и типовые запросы для обучения.
--
-- Автор: Дуплей Максим Игоревич
-- ORCID: https://orcid.org/0009-0007-7605-539X
-- GitHub: https://github.com/QuadDarv1ne/
-- Язык комментариев: русский
-- Примечание: выполнить скрипт можно через clickhouse-client --multiquery < clickhouse_training_db.sql

/* ======================================================
   Настройки и создание базы
   ====================================================== */

-- Создаём базу данных для тренировки
CREATE DATABASE IF NOT EXISTS training
ENGINE = Ordinary;

USE training;

/* ======================================================
   Пользователи и роли (пример безопасности)
   ====================================================== */

-- Создаём простого пользователя для тренировок (опция: настройте пароль/права под свою среду)
-- Внимание: CREATE USER требует соответствующих прав у текущего пользователя ClickHouse
-- Закомментируйте эти строки, если не хотите менять пользователей на сервере.

-- CREATE USER IF NOT EXISTS training_user IDENTIFIED WITH plaintext_password BY 'training_pass';
-- CREATE ROLE IF NOT EXISTS training_role;
-- GRANT SELECT, INSERT ON training.* TO training_role;
-- GRANT training_role TO training_user;

/* ======================================================
   Справочные таблицы (dimension) — маленькие таблицы
   ====================================================== */

CREATE TABLE IF NOT EXISTS training.dim_countries (
    country_code LowCardinality(String),
    country_name String,
    region LowCardinality(String)
) ENGINE = TinyLog(); -- компактная таблица для справочников

-- Наполним небольшим списком стран
INSERT INTO training.dim_countries VALUES
('US','United States','Americas'),
('RU','Russia','Europe/Asia'),
('DE','Germany','Europe'),
('CH','Switzerland','Europe'),
('IN','India','Asia');

/* ======================================================
   Главные OLTP-подобные таблицы (messages, users, chats)
   Основные идеи: Partitioning по месяцу, ORDER BY для MergeTree,
   использование LowCardinality, TTL, индексы-пропуски (skip index)
   и проекции для ускорения популярных запросов.
   ====================================================== */

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS training.users (
    user_id UInt64,
    username LowCardinality(String),
    full_name String,
    email LowCardinality(String),
    signup_date DateTime,
    country_code LowCardinality(String),
    is_bot UInt8 DEFAULT 0,
    profile JSON DEFAULT NULL -- пример хранения JSON-профиля (ClickHouse поддерживает JSON)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(signup_date)
ORDER BY (user_id)
SETTINGS index_granularity = 8192;

-- Таблица чатов (группы / приватные)
CREATE TABLE IF NOT EXISTS training.chats (
    chat_id UInt64,
    chat_type Enum8('private' = 1, 'group' = 2, 'channel' = 3),
    title String,
    created_at DateTime,
    member_count UInt32 DEFAULT 0
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (chat_id)
SETTINGS index_granularity = 8192;

-- Таблица сообщений (основная)
-- Полезные приёмы: LowCardinality для часто повторяющихся строк,
-- массивы и Nested для вложённых полей, SKIP INDEX для массивов (быстрый поисковый фильтр)
CREATE TABLE IF NOT EXISTS training.messages (
    message_id UInt64,
    chat_id UInt64,
    user_id UInt64,
    ts DateTime,
    text String,
    text_len UInt32 MATERIALIZED length(text), -- материализованное поле для аналитики
    is_edited UInt8 DEFAULT 0,
    likes UInt32 DEFAULT 0,
    topics LowCardinality(String),
    tags Array(LowCardinality(String)),
    attachment_count UInt8 DEFAULT 0,
    -- Пример вложенной структуры для прикреплений
    attachments Nested(
        id UInt64,
        typ LowCardinality(String),
        size UInt32
    )
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(ts)
ORDER BY (chat_id, ts, message_id)
SAMPLE BY message_id -- позволяет использовать SAMPLE при быстрых аналитических запросах
TTL ts + INTERVAL 365 DAY DELETE -- удаляем старые сообщения через год (пример политики)
SETTINGS index_granularity = 8192;

-- Создадим пропускной (skip) индекс для быстрого поиска по tags (bloom_filter)
ALTER TABLE training.messages
    ADD INDEX IF NOT EXISTS idx_tags (tags) TYPE bloom_filter(0.01) GRANULARITY 4;

/* ======================================================
   Примеры проекций (projections) — ускорение популярных запросов
   (доступно в современных версиях ClickHouse)
   ====================================================== */

-- Пример: проекция для быстрых выборок сообщений за 30 дней
-- Внимание: синтаксис проекций зависит от версии ClickHouse.
-- Если ваша версия не поддерживает проекции, эти блоки можно пропустить.

-- Ниже — демонстрационный синтаксис; отключите, если ваш ClickHouse старой версии.
-- ALTER TABLE training.messages
--     ADD PROJECTION IF NOT EXISTS proj_last_30d (
--         SELECT
--             message_id,
--             chat_id,
--             user_id,
--             ts,
--             text_len
--         WHERE ts >= now() - INTERVAL 30 DAY
--     );

/* ======================================================
   Агрегационные таблицы (AggregatingMergeTree) и materialized views
   Для быстрого получения ежедневной и почасовой статистики
   ====================================================== */

-- Таблица для накопления ежедневной статистики по пользователям
CREATE TABLE IF NOT EXISTS training.msgs_daily_mv (
    day Date,
    user_id UInt64,
    chat_id UInt64,
    cnt UInt64
) ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(day)
ORDER BY (day, user_id, chat_id)
SETTINGS index_granularity = 8192;

-- Материализованное представление, которое будет наполнять msgs_daily_mv в реальном времени
CREATE MATERIALIZED VIEW IF NOT EXISTS training.mv_messages_to_daily
TO training.msgs_daily_mv
AS
SELECT
    toDate(ts) AS day,
    user_id,
    chat_id,
    count() AS cnt
FROM training.messages
GROUP BY day, user_id, chat_id;

-- Таблица почасовой агрегации с AggregatingMergeTree (пример при больших нагрузках)
CREATE TABLE IF NOT EXISTS training.msgs_hourly_agg (
    hour DateTime,
    user_id UInt64,
    cnt_state AggregateFunction(count, UInt64)
) ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (hour, user_id)
SETTINGS index_granularity = 8192;

CREATE MATERIALIZED VIEW IF NOT EXISTS training.mv_messages_to_hourly
TO training.msgs_hourly_agg
AS
SELECT
    toStartOfHour(ts) AS hour,
    user_id,
    countState() AS cnt_state
FROM training.messages
GROUP BY hour, user_id;

/* ======================================================
   Таблица событий/логов для аналитики (event stream)
   ====================================================== */

CREATE TABLE IF NOT EXISTS training.events (
    event_id UInt64,
    user_id UInt64,
    event_type LowCardinality(String),
    event_props JSON,
    ts DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(ts)
ORDER BY (event_type, ts)
SETTINGS index_granularity = 8192;

/* ======================================================
   Примеры наполнения синтетическими данными
   Используем system.numbers для генерации — удобно для обучения
   ====================================================== */

-- 1) Создадим 1000 пользователей
INSERT INTO training.users (user_id, username, full_name, email, signup_date, country_code, is_bot)
SELECT
    number + 1 AS user_id,
    concat('user_', toString(number + 1)) AS username,
    concat('User Fullname ', toString(number + 1)) AS full_name,
    concat('user', toString(number + 1), '@example.com') AS email,
    now() - toIntervalDay(toUInt32(number % 1000)) AS signup_date,
    arrayElement(['US','RU','DE','CH','IN'], toUInt32(number % 5) + 1) AS country_code,
    0
FROM numbers(1000);

-- 2) Создадим 50 чатов
INSERT INTO training.chats (chat_id, chat_type, title, created_at, member_count)
SELECT
    number + 1 AS chat_id,
    if(number % 3 = 0, 'private', if(number % 3 = 1, 'group', 'channel')) AS chat_type,
    concat('Chat ', toString(number + 1)) AS title,
    now() - toIntervalDay(toUInt32(number % 400)) AS created_at,
    10 + toUInt32(number % 90) AS member_count
FROM numbers(50);

-- 3) Наполним таблицу сообщений — 100_000 сообщений (пример)
--    Используем массивы и Nested для attachments и tags
INSERT INTO training.messages (message_id, chat_id, user_id, ts, text, is_edited, likes, topics, tags, attachment_count, attachments.id, attachments.typ, attachments.size)
SELECT
    number + 1 AS message_id,
    toUInt64(number % 50) + 1 AS chat_id,
    toUInt64(number % 1000) + 1 AS user_id,
    now() - toIntervalSecond(toUInt32(number % 86400 * 90)) AS ts,
    concat('Тестовое сообщение номер ', toString(number + 1)) AS text,
    toUInt8(number % 5 = 0) AS is_edited,
    toUInt32(number % 100) AS likes,
    arrayElement(['general','news','dev','random'], toUInt32(number % 4) + 1) AS topics,
    ['tag' || toString(number % 5), 'tag' || toString((number+1) % 7)] AS tags,
    toUInt8(number % 3) AS attachment_count,
    -- вложенные массивы для attachments
    if(number % 3 = 0, [number*10 + 1], if(number % 3 = 1, [number*10 + 1, number*10 + 2], [])) AS attachments_id,
    if(number % 3 = 0, ['image'], if(number % 3 = 1, ['image','file'], [])) AS attachments_typ,
    if(number % 3 = 0, [1024], if(number % 3 = 1, [2048, 512], [])) AS attachments_size
FROM numbers(100000);

-- 4) Наполним events
INSERT INTO training.events (event_id, user_id, event_type, event_props, ts)
SELECT
    number + 1 AS event_id,
    toUInt64(number % 1000) + 1 AS user_id,
    arrayElement(['login','logout','message_send','message_edit','react'], toUInt32(number % 5) + 1) AS event_type,
    JSONBuildObject('meta', concat('info_', toString(number % 10))) AS event_props,
    now() - toIntervalSecond(toUInt32(number % 86400 * 30)) AS ts
FROM numbers(20000);

/* ======================================================
   Полезные запросы для обучения (шпаргалка)
   ====================================================== */

-- 1. Топ-10 пользователей по количеству сообщений за последние 7 дней
/*
SELECT user_id, count() AS cnt
FROM training.messages
WHERE ts >= now() - INTERVAL 7 DAY
GROUP BY user_id
ORDER BY cnt DESC
LIMIT 10;
*/

-- 2. Средняя длина сообщения по чатам за последний месяц
/*
SELECT chat_id, avg(text_len) AS avg_len
FROM training.messages
WHERE ts >= now() - INTERVAL 30 DAY
GROUP BY chat_id
ORDER BY avg_len DESC
LIMIT 20;
*/

-- 3. Количество сообщений по дням (используем materialized view msgs_daily_mv, если MV был создан)
/*
SELECT day, sum(cnt) AS total_messages
FROM training.msgs_daily_mv
GROUP BY day
ORDER BY day DESC
LIMIT 30;
*/

-- 4. Быстрый поиск по тэгам с использованием skip index (bloom_filter)
/*
SELECT count() FROM training.messages
WHERE has(tags, 'tag1')
-- Используйте PROFILE или system.query_log для анализа использования индекса
*/

-- 5. Примеры обновления TTL и политики хранения
-- Увеличить срок хранения до 2 лет:
-- ALTER TABLE training.messages MODIFY TTL ts + INTERVAL 730 DAY DELETE;

/* ======================================================
   Оптимизации и рекомендации (коротко)
   - Используйте LowCardinality для часто повторяющихся строк
   - Компрессия в столбцах: можно указывать CODEC(ZSTD(...)) при создании столбца
   - Стоит настроить index_granularity под ваш размер данных
   - Для реального кластера используйте ReplicatedMergeTree/Distributed
   - Для высоких скоростей агрегирования используйте AggregatingMergeTree / SummingMergeTree
   - Не забудьте резервное копирование (clickhouse-backup или snapshot-инструменты)
   ====================================================== */

-- Пример добавления CODEC к столбцу (если нужна более сильная компрессия):
-- ALTER TABLE training.messages MODIFY COLUMN text CODEC(ZSTD(3));

/* ======================================================
   Конец скрипта
   ====================================================== */
