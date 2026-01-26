# 🗄️ Полный мануал по MySQL: Установка, Настройка и Использование

## 📋 Содержание

1. [Введение в MySQL](#введение-в-mysql)
2. [Системные требования](#системные-требования)
3. [Установка MySQL](#установка-mysql)
4. [Базовая настройка](#базовая-настройка)
5. [Структура базы данных](#структура-базы-данных)
6. [Конфигурация MySQL](#конфигурация-mysql)
7. [Управление пользователями](#управление-пользователями)
8. [Основные SQL команды](#основные-sql-команды)
9. [Работа с таблицами](#работа-с-таблицами)
10. [Индексы и оптимизация](#индексы-и-оптимизация)
11. [Практические примеры](#практические-примеры)
12. [Лучшие практики](#лучшие-практики)

## Введение в MySQL

**MySQL** — это одна из самых популярных систем управления реляционными базами данных (`RDBMS`) с открытым исходным кодом. Она широко используется в веб-приложениях и работает как часть пакета `LAMP` (`Linux`, `Apache`, `MySQL`, `PHP`).

**Основные особенности MySQL:**

- Высокая производительность
- Надежность и стабильность
- Поддержка больших объемов данных
- Множество интерфейсов и API
- Совместимость с SQL стандартом
- Поддержка транзакций
- Безопасность и права доступа

## Системные требования

### Минимальные требования:

- **Операционная система:** Windows 7+, Linux, macOS 10.12+
- **Процессор:** 32-бит или 64-бит (рекомендуется 64-бит)
- **Память:** 256 МБ RAM (рекомендуется 1 ГБ+)
- **Место на диске:** 300 МБ свободного места
- **Свободная память:** 200 МБ для выполнения запросов

### Рекомендуемые требования:

- **Операционная система:** Windows 10+, Ubuntu 18.04+, macOS 11+
- **Процессор:** Multi-core, 64-бит
- **Память:** 4 ГБ+ RAM
- **Место на диске:** 1 ГБ+ свободного места
- **Свободная память:** 1 ГБ+ для выполнения запросов

### Поддерживаемые версии MySQL:

- **MySQL 8.0** (актуальная стабильная)
- **MySQL 5.7** (поддерживается)
- **MySQL 5.6** (EOL: 2021)

## Установка MySQL

### Метод №1: Установка на Windows (рекомендуется)

#### Установка с помощью MySQL Installer:

1. **Скачайте MySQL Installer:**
   - Перейдите на https://dev.mysql.com/downloads/installer/
   - Скачайте MySQL Installer (web-community или full)

2. **Запустите установку:**
   - Запустите установочный файл как администратор
   - Выберите "Developer Default" или "Server only"

3. **Настройте продукты:**
   - Выберите MySQL Server для установки
   - Добавьте MySQL Workbench (рекомендуется)

4. **Настройте конфигурацию:**
   - Выберите "Standalone MySQL Server"
   - Установите порт (по умолчанию 3306)
   - Настройте пароль root пользователя

#### Установка с помощью Laragon (для разработки):

1. **Установите Laragon** (если еще не установлен)
2. **Laragon автоматически установит MySQL**
3. **Запустите MySQL через панель Laragon**

### Метод №2: Установка на Linux

#### Ubuntu/Debian:

```bash
# Обновите пакеты
sudo apt update

# Установите MySQL Server
sudo apt install mysql-server

# Запустите безопасную установку
sudo mysql_secure_installation

# Запустите сервис
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### CentOS/RHEL/Fedora:

```bash
# Установите MySQL Server
sudo yum install mysql-server
# или для Fedora
sudo dnf install mysql-server

# Запустите безопасную установку
sudo mysql_secure_installation

# Запустите сервис
sudo systemctl start mysqld
sudo systemctl enable mysqld
```

### Метод №3: Установка на macOS

#### С помощью Homebrew:

```bash
# Установите MySQL
brew install mysql

# Запустите безопасную установку
mysql_secure_installation

# Запустите MySQL
brew services start mysql
```

#### С помощью официального установщика:

1. Скачайте с https://dev.mysql.com/downloads/mysql/
2. Запустите установочный файл
3. Следуйте инструкциям установщика

## Базовая настройка

### Настройка root пароля:

**После установки важно установить безопасный пароль для root пользователя:**

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';
FLUSH PRIVILEGES;
```

### Настройка конфигурационного файла my.cnf:

- **Windows:** `C:\\ProgramData\\MySQL\\MySQL Server 8.0\\my.ini`
- **Linux:** `/etc/mysql/my.cnf` или `/etc/my.cnf`
- **macOS:** `/usr/local/mysql/my.cnf` или `/etc/my.cnf`

**Пример минимальной конфигурации:**

```ini
[mysqld]
port = 3306
bind-address = 127.0.0.1
max_connections = 200
innodb_buffer_pool_size = 256M
```

## Структура базы данных

### Основные компоненты:

- **Сервер MySQL** - основной процесс базы данных
- **Базы данных** - контейнеры для таблиц
- **Таблицы** - структуры для хранения данных
- **Строки и столбцы** - данные в таблицах
- **Индексы** - ускоряют поиск данных
- **Пользователи и права** - управление доступом

### Типичная структура:

```textline
MySQL Server
├── Database 1
│   ├── Table 1
│   │   ├── Column 1
│   │   ├── Column 2
│   │   └── Index 1
│   ├── Table 2
│   └── Views
├── Database 2
│   └── Tables...
└── System databases (information_schema, mysql, performance_schema)
```

## Конфигурация MySQL

### Основные параметры my.cnf:

#### [mysqld] раздел - основной сервер:

```ini
[mysqld]
# Порт подключения
port = 3306

# Адрес привязки
bind-address = 127.0.0.1

# Максимальное количество соединений
max_connections = 200

# Размер буфера InnoDB
innodb_buffer_pool_size = 256M

# Размер ключевого буфера
key_buffer_size = 16M

# Размер буфера таблиц
table_open_cache = 64

# Размер сортировки
sort_buffer_size = 512K

# Размер соединения
join_buffer_size = 256K

# Размер стека
thread_stack = 256K

# Размер временных таблиц
tmp_table_size = 32M

# Включение бинарного лога
log-bin = mysql-bin

# Уровень логирования
log-error = /var/log/mysql/error.log
```

#### [client] раздел - клиентские настройки:

```ini
[client]
port = 3306
socket = /var/run/mysqld/mysqld.sock
default-character-set = utf8mb4
```

## Управление пользователями

### Создание нового пользователя:

```sql
-- Создание пользователя с паролем
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';

-- Создание пользователя с доступом с любого хоста
CREATE USER 'newuser'@'%' IDENTIFIED BY 'password';

-- Создание пользователя с доступом с определенного IP
CREATE USER 'newuser'@'192.168.1.%' IDENTIFIED BY 'password';
```

### Назначение прав:

```sql
-- Назначение всех прав на определенную базу
GRANT ALL PRIVILEGES ON database_name.* TO 'newuser'@'localhost';

-- Назначение конкретных прав
GRANT SELECT, INSERT, UPDATE, DELETE ON database_name.table_name TO 'newuser'@'localhost';

-- Назначение прав на все базы
GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'newuser'@'localhost';

-- Применение изменений
FLUSH PRIVILEGES;
```

### Удаление пользователя:

```sql
DROP USER 'username'@'hostname';
FLUSH PRIVILEGES;
```

### Просмотр пользователей:

```sql
SELECT User, Host FROM mysql.user;
```

## Основные SQL команды

### Подключение к MySQL:

```bash
# Подключение с указанием пользователя
mysql -u root -p

# Подключение к определенной базе
mysql -u root -p database_name

# Подключение к удаленному серверу
mysql -h hostname -u username -p
```

### Работа с базами данных:

```sql
-- Создание базы данных
CREATE DATABASE database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Использование базы данных
USE database_name;

-- Просмотр всех баз данных
SHOW DATABASES;

-- Удаление базы данных
DROP DATABASE database_name;
```

### Работа с таблицами:

```sql
-- Создание таблицы
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Просмотр всех таблиц
SHOW TABLES;

-- Просмотр структуры таблицы
DESCRIBE table_name;
-- или
SHOW CREATE TABLE table_name;

-- Удаление таблицы
DROP TABLE table_name;
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

### Типы данных:

```sql
-- Числовые типы
INT, TINYINT, SMALLINT, MEDIUMINT, BIGINT
DECIMAL(M,D), FLOAT, DOUBLE

-- Текстовые типы
VARCHAR(N), CHAR(N), TEXT, MEDIUMTEXT, LONGTEXT

-- Дата и время
DATE, TIME, DATETIME, TIMESTAMP, YEAR

-- Булевый тип
BOOLEAN (хранится как TINYINT(1))
```

### Ограничения:

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Внешний ключ
    FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    -- Уникальное ограничение
    UNIQUE KEY unique_name (name),
    
    -- Индекс
    INDEX idx_price (price)
);
```

### Изменение структуры таблицы:

```sql
-- Добавление столбца
ALTER TABLE users ADD COLUMN age INT;

-- Удаление столбца
ALTER TABLE users DROP COLUMN age;

-- Изменение столбца
ALTER TABLE users MODIFY COLUMN name VARCHAR(150);

-- Переименование столбца
ALTER TABLE users CHANGE COLUMN old_name new_name VARCHAR(100);

-- Добавление внешнего ключа
ALTER TABLE orders ADD FOREIGN KEY (user_id) REFERENCES users(id);
```

## Индексы и оптимизация

### Создание индексов:

```sql
-- Простой индекс
CREATE INDEX idx_email ON users(email);

-- Уникальный индекс
CREATE UNIQUE INDEX idx_username ON users(username);

-- Композитный индекс
CREATE INDEX idx_name_age ON users(name, age);

-- Полный текстовый индекс (для MyISAM и InnoDB 5.6+)
CREATE FULLTEXT INDEX idx_description ON articles(description);
```

### Удаление индексов:

```sql
DROP INDEX idx_email ON users;
```

### Просмотр индексов:

```sql
SHOW INDEX FROM table_name;
```

### Оптимизация запросов:

```sql
-- Использование EXPLAIN для анализа запроса
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';

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
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE blog_db;

-- Таблица пользователей
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица категорий
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL
);

-- Таблица статей
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    user_id INT NOT NULL,
    category_id INT,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    
    INDEX idx_published (published_at),
    INDEX idx_user (user_id)
);

-- Создание индексов
CREATE INDEX idx_title ON posts(title);
CREATE FULLTEXT INDEX idx_content ON posts(content);
```

### Пример №2: Основные запросы для блога

```sql
-- Создание пользователя
INSERT INTO users (username, email, password) 
VALUES ('johndoe', 'john@example.com', 'hashed_password');

-- Создание категории
INSERT INTO categories (name, slug) VALUES ('Technology', 'technology');

-- Создание статьи
INSERT INTO posts (title, content, user_id, category_id, published_at) 
VALUES (
    'Introduction to MySQL', 
    'MySQL is a popular database...', 
    1, 
    1, 
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
WHERE p.published_at IS NOT NULL
ORDER BY p.published_at DESC;

-- Поиск статей по ключевому слову
SELECT * FROM posts 
WHERE MATCH(content) AGAINST('MySQL' IN NATURAL LANGUAGE MODE);
```

### Пример №3: Резервное копирование и восстановление

```bash
# Создание резервной копии всей базы данных
mysqldump -u root -p database_name > backup.sql

# Создание резервной копии конкретной таблицы
mysqldump -u root -p database_name table_name > table_backup.sql

# Создание резервной копии всех баз данных
mysqldump -u root -p --all-databases > all_databases_backup.sql

# Восстановление из резервной копии
mysql -u root -p database_name < backup.sql

# Восстановление всех баз данных
mysql -u root -p < all_databases_backup.sql
```

## Лучшие практики

### 1. Используйте правильные типы данных

```sql
-- Хорошо: используйте подходящий размер для VARCHAR
VARCHAR(255) -- для обычных текстов
TEXT -- для длинных текстов

-- Плохо: использование слишком больших размеров
VARCHAR(10000) -- если не нужен такой размер
```

### 2. Используйте индексы эффективно

```sql
-- Создавайте индексы на столбцах, используемых в WHERE
CREATE INDEX idx_user_email ON users(email);

-- Избегайте чрезмерного индексирования
-- Каждый индекс замедляет INSERT/UPDATE/DELETE
```

### 3. Используйте подготовленные выражения

```sql
-- Вместо:
SELECT * FROM users WHERE id = 123;

-- Используйте подготовленные выражения в приложении:
PREPARE stmt FROM 'SELECT * FROM users WHERE id = ?';
```

### 4. Нормализуйте данные

- Избегайте дублирования информации
- Используйте связи между таблицами
- Разделяйте данные на логические сущности

### 5. Используйте транзакции для целостности данных

```sql
START TRANSACTION;

INSERT INTO accounts (user_id, balance) VALUES (1, 1000);
INSERT INTO transactions (from_account, to_account, amount) VALUES (NULL, 1, 1000);

COMMIT; -- или ROLLBACK; если произошла ошибка
```

### 6. Защита от SQL-инъекций

- Используйте подготовленные выражения
- Проверяйте и очищайте входные данные
- Не используйте конкатенацию строк в SQL-запросах

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