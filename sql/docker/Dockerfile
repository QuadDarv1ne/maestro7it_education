# Dockerfile для SQL Learning Environment
# Создает контейнер с SQLite, Python и всеми необходимыми инструментами
# Поддерживает все учебные базы данных и инструменты тестирования

FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Установка Python зависимостей
RUN pip install --no-cache-dir \
    requests \
    pandas \
    jupyter \
    pytest

# Копирование проекта
# Копирование только необходимых файлов
COPY scripts/ ./scripts/
COPY src/ ./src/
COPY tests/ ./tests/
COPY solutions/ ./solutions/
COPY data/sample_data/ ./data/sample_data/

# Создание структуры директорий
RUN mkdir -p /app/data/databases /app/data/output /app/tests

# Экспозиция портов
EXPOSE 8000 8888

# Команда по умолчанию - интерактивная оболочка
CMD ["bash"]