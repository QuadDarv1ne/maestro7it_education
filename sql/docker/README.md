# SQL Обучающая среда - Настройка Docker

## Быстрый старт

### 1. Запуск всего окружения
```bash
cd docker
docker-compose up -d
```

### 2. Доступ к сервисам:
- **Jupyter Notebook**: http://localhost:8888
- **SQLite Web Interface**: http://localhost:8080
- **SQL Learning Container**: docker exec -it sql-learning-environment bash

## Компоненты

### Основной контейнер (sql-learning)
- Python 3.9 с необходимыми библиотеками
- SQLite3
- Автоматическая загрузка баз данных
- Тестирование SQL-запросов

### Веб-интерфейс SQLite (sqlite-web)
- Графический интерфейс для работы с базами данных
- Поддержка всех учебных баз данных
- Простая навигация по таблицам

### Jupyter Notebook
- Интерактивные notebook'ы для обучения
- Предустановленные библиотеки (pandas, matplotlib, seaborn)
- Возможность создания собственных анализов

## Полезные команды

### Управление контейнерами
```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f

# Пересборка контейнеров
docker-compose build --no-cache
```

### Работа с основным контейнером
```bash
# Вход в контейнер
docker exec -it sql-learning-environment bash

# Запуск загрузчика баз данных
docker exec sql-learning-environment python scripts/download_databases.py

# Запуск тестера SQL
docker exec sql-learning-environment python scripts/sql_tester.py
```

### Работа с базами данных
```bash
# Подключение к SQLite напрямую
docker exec -it sql-learning-environment sqlite3 /data/databases/chinook.db

# Выполнение SQL-скрипта
docker exec -i sql-learning-environment sqlite3 /data/databases/northwind.db < src/northwind/northwind_queries.sql
```

## Персистентность данных

Все данные сохраняются в локальных директориях:
- `../data/databases/` - загруженные базы данных
- `../notebooks/` - Jupyter notebook'ы
- `../src/` - SQL-скрипты

## Настройка окружения

### Переменные окружения
```yaml
environment:
  PYTHONPATH: /app
  SQLITE_DATABASE: chinook.db  # по умолчанию
```

### Порты
- 8000: Основное приложение (если используется)
- 8080: Веб-интерфейс SQLite
- 8888: Jupyter Notebook

## Решение проблем

### Если порты заняты:
```bash
# Проверка занятых портов
netstat -an | grep 8080

# Изменение портов в docker-compose.yml
ports:
  - "8081:8080"  # изменить локальный порт
```

### Если контейнеры не запускаются:
```bash
# Проверка логов
docker-compose logs sql-learning

# Пересборка с логами
docker-compose build --no-cache
docker-compose up
```

### Обновление данных:
```bash
# Очистка и перезапуск
docker-compose down -v
docker-compose up -d
```

## Расширение функционала

### Добавление новых баз данных:
1. Добавьте URL в `scripts/download_databases.py`
2. Пересоберите контейнер: `docker-compose build`
3. Перезапустите: `docker-compose up -d`

### Установка дополнительных Python-библиотек:
1. Добавьте в `requirements.txt`
2. Пересоберите контейнер
3. Или установите в работающем контейнере:
   ```bash
   docker exec sql-learning-environment pip install library_name
   ```