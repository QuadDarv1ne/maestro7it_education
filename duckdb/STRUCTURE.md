# Структура проекта DuckDB

## Обзор директорий

- `src/` - Исходный код проекта
  - `main.py` - Главная точка входа
  - `config.py` - Конфигурация проекта
  - `utils.py` - Вспомогательные функции
  - `ozon_db_setup.py` - Настройка базы данных
  - `analytics.py` - Модуль аналитики
  - `advanced_analytics.py` - Расширенная аналитика
  - `backup_manager.py` - Резервное копирование
  - `data_validator.py` - Валидация данных
  - `performance_monitor.py` - Мониторинг производительности
  - `query_optimizer.py` - Оптимизация запросов
  - `data_visualizer.py` - Визуализация данных
  - `error_recovery.py` - Восстановление после ошибок
  - `db_migration.py` - Миграции базы данных
  - `demo_complete.py` - Полная демонстрация
  - `setup_project.py` - Установка проекта
  - `test_duckdb.py` - Тестирование DuckDB

- `docs/` - Документация
  - `README.md` - Основная документация
  - `duckdb_install_guide.txt` - Руководство по установке

- `data/` - Данные проекта

- `exports/` - Экспортированные файлы

- `charts/` - Графики и визуализации

- `logs/` - Файлы логов

- `backups/` - Резервные копии базы данных

- `migrations/` - Файлы миграций базы данных

- `recovery_points/` - Точки восстановления

- `tests/` - Тесты (будет добавлено позже)

## Файлы в корне

- `README.md` - Основная документация проекта
- `requirements.txt` - Зависимости Python
- `run_examples.bat` - Скрипт для запуска примеров
- `ozon_products.duckdb` - База данных образца