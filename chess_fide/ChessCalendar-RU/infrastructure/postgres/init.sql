-- Инициализация PostgreSQL базы данных для Chess Calendar RU

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Для полнотекстового поиска
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- Для индексов

-- Создание схем
CREATE SCHEMA IF NOT EXISTS tournaments;
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Установка search_path
ALTER DATABASE chess_calendar SET search_path TO public, tournaments, users, analytics;

-- Создание функции для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Создание индексов для оптимизации поиска
-- Будут созданы после миграции таблиц через Alembic

COMMENT ON SCHEMA tournaments IS 'Схема для данных турниров';
COMMENT ON SCHEMA users IS 'Схема для данных пользователей';
COMMENT ON SCHEMA analytics IS 'Схема для аналитических данных';
