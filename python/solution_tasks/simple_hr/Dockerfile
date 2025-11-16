# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаём директории для логов и instance
RUN mkdir -p logs instance

# Устанавливаем переменные окружения
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Открываем порт
EXPOSE 5000

# Команда запуска
CMD ["python", "run.py"]
