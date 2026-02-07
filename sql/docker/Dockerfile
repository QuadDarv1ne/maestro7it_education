# Dockerfile для SQL Learning Environment
# Создает контейнер с SQLite, Python и всеми необходимыми инструментами

FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements (если есть)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание точек монтирования для данных
RUN mkdir -p /data/databases /data/output

# Экспозиция порта для веб-интерфейса (если будет)
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "scripts/download_databases.py"]