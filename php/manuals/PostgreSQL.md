# 🗄️ Полный мануал по PostgreSQL: Установка, Настройка и Использование

## 📋 Содержание

1. [Введение в PostgreSQL](#введение-в-postgresql)
2. [Системные требования](#системные-требования)
3. [Установка PostgreSQL](#установка-postgresql)
4. [Базовая настройка](#базовая-настройка)
5. [Структура базы данных](#структура-базы-данных)
6. [Конфигурация PostgreSQL](#конфигурация-postgresql)
7. [Управление пользователями](#управление-пользователями)
8. [Основные SQL команды](#основные-sql-команды)
9. [Работа с таблицами](#работа-с-таблицами)
10. [Индексы и оптимизация](#индексы-и-оптимизация)
11. [Практические примеры](#практические-примеры)
12. [Лучшие практики](#лучшие-практики)

## Введение в PostgreSQL

**PostgreSQL** — это мощная объектно-реляционная система управления базами данных (`ORDBMS`) с более чем 30-летней историей активной разработки.

Это открытый проект, разрабатываемый командой экспертов со всего мира.

**Основные особенности PostgreSQL:**

- Поддержка сложных запросов
- Надежность и стабильность
- Поддержка расширений
- Расширенные возможности типов данных
- Поддержка JSON, массивов, UUID и других типов
- Поддержка полнотекстового поиска
- Безопасность и права доступа
- Репликация и масштабируемость

## Системные требования

### Минимальные требования:

- **Операционная система:** Windows 7+, Linux, macOS 10.12+
- **Процессор:** 32-бит или 64-бит (рекомендуется 64-бит)
- **Память:** 256 МБ RAM (рекомендуется 1 ГБ+)
- **Место на диске:** 500 МБ свободного места
- **Свободная память:** 200 МБ для выполнения запросов

### Рекомендуемые требования:

- **Операционная система:** Windows 10+, Ubuntu 18.04+, macOS 11+
- **Процессор:** Multi-core, 64-бит
- **Память:** 4 ГБ+ RAM
- **Место на диске:** 2 ГБ+ свободного места
- **Свободная память:** 1 ГБ+ для выполнения запросов

### Поддерживаемые версии PostgreSQL:

- **PostgreSQL 15** (актуальная стабильная)
- **PostgreSQL 14** (рекомендуемая LTS)
- **PostgreSQL 13** (поддерживается)
- **PostgreSQL 12** (EOL: 2024)

## Установка PostgreSQL

### Метод №1: Установка на Windows (рекомендуется)

#### Установка с помощью официального установщика:

1. **Скачайте установщик:**
   - Перейдите на https://www.postgresql.org/download/windows/
   - Скачайте последнюю версию установщика

2. **Запустите установку:**
   - Запустите установочный файл как администратор
   - Следуйте инструкциям мастера установки

3. **Настройте параметры установки:**
   - Выберите компоненты для установки
   - Укажите каталог установки (по умолчанию `C:\\Program Files\\PostgreSQL\\`)
   - Установите порт (по умолчанию 5432)
   - Установите пароль для пользователя postgres

4. **Настройте дополнительные параметры:**
   - Выберите локаль (рекомендуется `English_United States.1252`)
   - Установите каталог данных

#### Установка с помощью Chocolatey:

```powershell
choco install postgresql
```

### Метод №2: Установка на Linux

#### Ubuntu/Debian:

```bash
# Обновите пакеты
sudo apt update

# Установите PostgreSQL
sudo apt install postgresql postgresql-contrib

# Запустите сервис
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### CentOS/RHEL/Fedora:

```bash
# Установите PostgreSQL
sudo yum install postgresql-server postgresql-contrib
# или для Fedora
sudo dnf install postgresql-server postgresql-contrib

# Инициализируйте базу данных
sudo postgresql-setup --initdb

# Запустите сервис
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Метод №3: Установка на macOS

#### С помощью Homebrew:

```bash
# Установите PostgreSQL
brew install postgresql

# Запустите PostgreSQL
brew services start postgresql
```

#### С помощью официального установщика:

1. Скачайте с https://www.postgresql.org/download/macosx/
2. Запустите установочный файл
3. Следуйте инструкциям установщика

## Базовая настройка

### Настройка пользователя postgres:

**После установки важно настроить начальные параметры:**

```bash
# Переключитесь на пользователя postgres (Linux/macOS)
sudo -i -u postgres

# Или подключитесь к PostgreSQL (Windows)
psql -U postgres
```

### Создание нового пользователя:

```sql
CREATE USER newuser WITH PASSWORD 'password';
ALTER USER newuser CREATEDB;
ALTER USER newuser CREATEROLE;
```

### Настройка конфигурационного файла postgresql.conf:

- **Windows:** `C:\\Program Files\\PostgreSQL\\[version]\\data\\postgresql.conf`
- **Linux:** `/etc/postgresql/[version]/main/postgresql.conf` или `/var/lib/pgsql/data/postgresql.conf`
- **macOS:** `/usr/local/var/postgres/postgresql.conf`

**Пример минимальной конфигурации:**

```
listen_addresses = 'localhost'
port = 5432
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

## Структура базы данных

### Основные компоненты:

- **PostgreSQL Server** - основной процесс базы данных
- **Кластеры** - коллекции баз данных
- **Базы данных** - контейнеры для схем
- **Схемы** - контейнеры для объектов базы данных
- **Таблицы** - структуры для хранения данных
- **Индексы** - ускоряют поиск данных
- **Пользователи и роли** - управление доступом

### Типичная структура:

```
PostgreSQL Cluster
├── Database 1
│   ├── Schema public
│   │   ├── Table 1
│   │   │   ├── Column 1
│   │   │   ├── Column 2
│   │   │   └── Index 1
│   │   ├── View 1
│   │   └── Function 1
│   └── Schema custom
│       └── Tables...
├── Database 2
│   └── Schemas...
└── Template databases (template0, template1)
```

## Конфигурация PostgreSQL

### Основные параметры postgresql.conf:

#### Подключение и управление:

```
# Параметры прослушивания
listen_addresses = '*'  # или 'localhost'
port = 5432

# Максимальное количество соединений
max_connections = 100

# Типы соединений
superuser_reserved_connections = 3
```

#### Память:

```
# Общие настройки памяти
shared_buffers = 256MB  # Рекомендуется 25% от RAM
huge_pages = try

# Настройки рабочей памяти
work_mem = 4MB
maintenance_work_mem = 64MB
autovacuum_work_mem = -1
```

#### Журналы:

```
# Настройки журнала
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'error'
log_min_duration_statement = 1000
```

### Настройка pg_hba.conf:

Файл `pg_hba.conf` управляет аутентификацией клиентов.

Пример содержимого:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
host    all             all             0.0.0.0/0               md5
```

## Управление пользователями

### Создание роли (пользователя):

```sql
-- Создание базовой роли
CREATE ROLE username LOGIN PASSWORD 'password';

-- Создание роли с привилегиями
CREATE ROLE username WITH LOGIN PASSWORD 'password' CREATEDB CREATEROLE SUPERUSER;

-- Создание роли и назначение ей другой роли
CREATE ROLE app_user INHERIT;
GRANT app_user TO username;
```

### Назначение прав:

```sql
-- Назначение прав на базу данных
GRANT CONNECT ON DATABASE database_name TO username;
GRANT USAGE ON SCHEMA schema_name TO username;

-- Назначение прав на таблицы
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO username;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO username;

-- Назначение прав на будущие таблицы
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO username;
```

### Удаление роли:

```sql
-- Удаление роли
DROP ROLE IF EXISTS username;
```

### Просмотр ролей:

```sql
-- Просмотр всех ролей
SELECT rolname FROM pg_roles;

-- Просмотр привилегий
\du  -- в psql
```

## Основные SQL команды

### Подключение к PostgreSQL:

```bash
# Подключение с указанием пользователя
psql -U username -d database_name

# Подключение к определенной базе
psql -U postgres -d postgres

# Подключение к удаленному серверу
psql -h hostname -U username -d database_name
```

### Работа с базами данных:

```sql
-- Создание базы данных
CREATE DATABASE database_name OWNER username ENCODING 'UTF8';

-- Просмотр всех баз данных
\l  -- в psql
-- или
SELECT datname FROM pg_database;

-- Удаление базы данных
DROP DATABASE IF EXISTS database_name;
```

### Работа с схемами:

```sql
-- Создание схемы
CREATE SCHEMA schema_name AUTHORIZATION username;

-- Использование схемы
SET search_path TO schema_name;

-- Просмотр всех схем
\dn  -- в psql
```

### Работа с таблицами:

```sql
-- Создание таблицы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Просмотр всех таблиц
\dt  -- в psql
-- или
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- Просмотр структуры таблицы
\d table_name  -- в psql
-- или
SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'users';

-- Удаление таблицы
DROP TABLE IF EXISTS table_name;
```

### Основные операции CRUD:

```sql
-- Вставка данных
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

-- Выборка данных
SELECT * FROM users;
SELECT name, email FROM users WHERE id = 1;

-- Обновление данных
UPDATE users SET name = 'Jane Doe' WHERE id = 1;

-- Удаление данных
DELETE FROM users WHERE id = 1;
```

## Работа с таблицами

### Типы данных PostgreSQL:

```sql
-- Числовые типы
INTEGER, BIGINT, SMALLINT, SERIAL
DECIMAL(P,S), NUMERIC(P,S), REAL, DOUBLE PRECISION

-- Текстовые типы
VARCHAR(N), CHAR(N), TEXT
NAME, BPCHAR

-- Дата и время
DATE, TIME, TIMESTAMP, TIMESTAMPTZ, INTERVAL

-- Логический тип
BOOLEAN

-- Бинарные данные
BYTEA

-- JSON типы
JSON, JSONB

-- Массивы
INTEGER[], TEXT[], VARCHAR(10)[]
```

### Ограничения:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Внешний ключ
    CONSTRAINT fk_products_category 
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    -- Уникальное ограничение
    CONSTRAINT unique_product_name UNIQUE (name),
    
    -- Индекс
    INDEX idx_price (price)
);
```

### Изменение структуры таблицы:

```sql
-- Добавление столбца
ALTER TABLE users ADD COLUMN age INTEGER;

-- Удаление столбца
ALTER TABLE users DROP COLUMN age;

-- Изменение столбца
ALTER TABLE users ALTER COLUMN name TYPE VARCHAR(150);

-- Добавление ограничения
ALTER TABLE users ADD CONSTRAINT unique_email UNIQUE (email);

-- Добавление внешнего ключа
ALTER TABLE orders ADD CONSTRAINT fk_orders_users 
    FOREIGN KEY (user_id) REFERENCES users(id);
```

## Индексы и оптимизация

### Создание индексов:

```sql
-- Простой индекс
CREATE INDEX idx_users_email ON users(email);

-- Уникальный индекс
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Композитный индекс
CREATE INDEX idx_users_name_age ON users(name, age);

-- Индекс GiST для геометрических данных
CREATE INDEX idx_locations_gist ON locations USING GIST (geom);

-- Индекс GIN для JSONB и массивов
CREATE INDEX idx_properties_gin ON products USING GIN (properties);
```

### Удаление индексов:

```sql
DROP INDEX IF EXISTS idx_users_email;
```

### Просмотр индексов:

```sql
-- В psql
\d table_name

-- Или SQL запрос
SELECT indexname FROM pg_indexes WHERE tablename = 'users';
```

### Оптимизация запросов:

```sql
-- Использование EXPLAIN ANALYZE для анализа запроса
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'john@example.com';

-- Использование LIMIT для ограничения результатов
SELECT * FROM users LIMIT 10;

-- Использование JOIN вместо подзапросов (часто быстрее)
SELECT u.name, p.title 
FROM users u 
JOIN posts p ON u.id = p.user_id;

-- Использование индексов в WHERE условиях
SELECT * FROM products WHERE category_id = 5 AND price < 100;
```

## Практические примеры

### Пример №1: Создание блога базы данных

```sql
-- Создание базы данных
CREATE DATABASE blog_db OWNER postgres ENCODING 'UTF8';

-- Подключитесь к новой базе и создайте таблицы
\c blog_db

-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица категорий
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL
);

-- Таблица статей
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    user_id INTEGER NOT NULL,
    category_id INTEGER,
    published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    
    INDEX idx_published (published),
    INDEX idx_user (user_id)
);

-- Создание индексов
CREATE INDEX idx_posts_title ON posts(title);
CREATE INDEX idx_posts_published_at ON posts(published_at);
```

### Пример №2: Основные запросы для блога

```sql
-- Создание пользователя
INSERT INTO users (username, email, password_hash) 
VALUES ('johndoe', 'john@example.com', 'hashed_password');

-- Создание категории
INSERT INTO categories (name, slug) VALUES ('Technology', 'technology');

-- Создание статьи
INSERT INTO posts (title, content, user_id, category_id, published, published_at) 
VALUES (
    'Introduction to PostgreSQL', 
    'PostgreSQL is a powerful database...', 
    1, 
    1, 
    TRUE, 
    NOW()
);

-- Получение опубликованных статей с авторами и категориями
SELECT 
    p.title,
    p.content,
    p.published_at,
    u.username,
    c.name AS category_name
FROM posts p
JOIN users u ON p.user_id = u.id
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.published = TRUE
ORDER BY p.published_at DESC;

-- Поиск статей по ключевому слову
SELECT * FROM posts 
WHERE content ILIKE '%PostgreSQL%';
```

### Пример №3: Резервное копирование и восстановление

```bash
# Создание резервной копии всей базы данных
pg_dump -U username -d database_name > backup.sql

# Создание резервной копии конкретной таблицы
pg_dump -U username -d database_name -t table_name > table_backup.sql

# Создание резервной копии всех баз данных
pg_dumpall -U postgres > all_databases_backup.sql

# Восстановление из резервной копии
psql -U username -d database_name < backup.sql

# Восстановление всех баз данных
psql -U postgres < all_databases_backup.sql
```

## Лучшие практики

### 1. Используйте правильные типы данных

```sql
-- Хорошо: используйте подходящий тип для конкретной задачи
SERIAL -- для автоинкрементных первичных ключей
TIMESTAMP WITH TIME ZONE -- для дат с учетом часового пояса
UUID -- для уникальных идентификаторов
JSONB -- для полнотекстового поиска в JSON
```

### 2. Используйте индексы эффективно

```sql
-- Создавайте индексы на столбцах, используемых в WHERE
CREATE INDEX idx_users_email ON users(email);

-- Используйте составные индексы для сложных запросов
CREATE INDEX idx_posts_user_status ON posts(user_id, status);

-- Избегайте чрезмерного индексирования
-- Каждый индекс замедляет INSERT/UPDATE/DELETE
```

### 3. Используйте транзакции для целостности данных

```sql
BEGIN;

INSERT INTO accounts (user_id, balance) VALUES (1, 1000);
INSERT INTO transactions (from_account, to_account, amount) VALUES (NULL, 1, 1000);

COMMIT; -- или ROLLBACK; если произошла ошибка
```

### 4. Нормализуйте данные

- Избегайте дублирования информации
- Используйте связи между таблицами
- Разделяйте данные на логические сущности

### 5. Используйте подготовленные выражения

```sql
-- В приложении используйте подготовленные выражения:
PREPARE stmt AS 'SELECT * FROM users WHERE id = $1';
EXECUTE stmt(123);
```

### 6. Защита от SQL-инъекций

- Используйте подготовленные выражения
- Проверяйте и очищайте входные данные
- Не используйте конкатенацию строк в SQL-запросах

### 7. Используйте расширенные возможности PostgreSQL

```sql
-- JSONB для хранения полуструктурированных данных
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    properties JSONB
);

-- Массивы для списков значений
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tags TEXT[]
);

-- Временные таблицы для промежуточных результатов
CREATE TEMPORARY TABLE temp_results AS
SELECT * FROM complex_calculation();
```

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