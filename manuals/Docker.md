# 🐳 Полный мануал по Docker: От основ до продвинутых практик

## 📋 Содержание

1. [Введение в Docker](#введение-в-docker)
2. [Установка и настройка](#установка-и-настройка)
3. [Основные концепции](#основные-концепции)
4. [Работа с образами](#работа-с-образами)
5. [Работа с контейнерами](#работа-с-контейнерами)
6. [Dockerfile и сборка образов](#dockerfile-и-сборка-образов)
7. [Сети в Docker](#сети-в-docker)
8. [Хранение данных (Volumes)](#хранение-данных-volumes)
9. [Docker Compose](#docker-compose)
10. [Реестры и репозитории](#реестры-и-репозитории)
11. [Безопасность](#безопасность)
12. [Мониторинг и логирование](#мониторинг-и-логирование)
13. [Продвинутые темы](#продвинутые-темы)
14. [Лучшие практики](#лучшие-практики)

## Введение в Docker

**Docker** — это платформа для разработки, доставки и запуска приложений в контейнерах. Контейнеры позволяют упаковать приложение со всеми его зависимостями в легковесный, переносимый пакет.

### Что такое контейнеры?

Контейнеры — это стандартизированные единицы программного обеспечения, которые объединяют код и все его зависимости, чтобы приложение могло работать быстро и надежно в разных вычислительных средах.

### Преимущества Docker:

- **Переносимость** — "работает везде"
- **Легковесность** — меньше overhead чем VM
- **Быстрый старт** — секунды вместо минут
- **Изоляция** — процессы изолированы друг от друга
- **Масштабируемость** — легко масштабировать приложения
- **Версионирование** — контроль версий образов

### Когда использовать Docker?

✅ **Подходит для:**
- Микросервисных архитектур
- CI/CD pipelines
- Локальной разработки
- Тестирования в изолированной среде
- Деплоя приложений
- Облачных решений

❌ **Не всегда нужно для:**
- Очень простых приложений
- Приложений с тяжелыми зависимостями от ОС
- Систем с высокими требованиями к безопасности (без дополнительных мер)

## Установка и настройка

### Установка на Windows:

#### Вариант 1: Docker Desktop (рекомендуется)

```powershell
# Скачать с официального сайта
# https://www.docker.com/products/docker-desktop

# Или установить через winget
winget install Docker.DockerDesktop

# Или через Chocolatey
choco install docker-desktop
```

#### Вариант 2: WSL 2 Backend

```powershell
# Включить WSL 2
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Установить Linux kernel update package
# https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

# Установить Ubuntu из Microsoft Store
# Затем установить Docker Desktop с WSL 2 backend
```

### Установка на macOS:

```bash
# Через Homebrew (рекомендуется)
brew install --cask docker

# Или скачать с официального сайта
# https://www.docker.com/products/docker-desktop
```

### Установка на Linux (Ubuntu/Debian):

```bash
# Удалить старые версии
sudo apt-get remove docker docker-engine docker.io containerd runc

# Установить зависимости
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Добавить официальный GPG ключ
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Добавить репозиторий
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установить Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER

# Перезайти в систему или выполнить
newgrp docker
```

### Установка на CentOS/RHEL:

```bash
# Удалить старые версии
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# Установить зависимости
sudo yum install -y yum-utils

# Добавить репозиторий
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# Установить Docker Engine
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Запустить и включить автозапуск
sudo systemctl start docker
sudo systemctl enable docker

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER
```

### Проверка установки:

```bash
# Проверить версию
docker --version

# Проверить информацию о системе
docker info

# Запустить тестовый контейнер
docker run hello-world
```

## Основные концепции

### Образы (Images)

**Образ** — это неизменяемый файл, который содержит снимок файловой системы и параметров запуска приложения.

```bash
# Просмотр локальных образов
docker images

# Получение информации об образе
docker inspect ubuntu:20.04
```

### Контейнеры (Containers)

**Контейнер** — это запущенный экземпляр образа.

```bash
# Просмотр запущенных контейнеров
docker ps

# Просмотр всех контейнеров (включая остановленные)
docker ps -a
```

### Реестры (Registries)

**Реестр** — это хранилище образов Docker.

```bash
# Официальный реестр
docker pull nginx

# Частный реестр
docker pull myregistry.com/myimage:tag
```

## Работа с образами

### Поиск образов:

```bash
# Поиск в Docker Hub
docker search nginx

# Поиск с фильтрами
docker search --filter "is-official=true" nginx
docker search --filter "stars=100" nginx
```

### Загрузка образов:

```bash
# Загрузка последней версии
docker pull ubuntu

# Загрузка конкретной версии
docker pull ubuntu:20.04

# Загрузка нескольких тегов
docker pull nginx:latest
docker pull nginx:alpine
```

### Управление образами:

```bash
# Просмотр образов
docker images
docker image ls

# Просмотр образов с фильтрами
docker images --filter "before=ubuntu:20.04"
docker images --filter "since=ubuntu:18.04"

# Удаление образов
docker rmi ubuntu:18.04
docker image rm nginx:alpine

# Удаление неиспользуемых образов
docker image prune
docker image prune -a  # удалить все неиспользуемые

# Получение информации
docker image inspect ubuntu:20.04
docker history ubuntu:20.04
```

### Экспорт и импорт образов:

```bash
# Экспорт образа в tar-файл
docker save ubuntu:20.04 > ubuntu.tar

# Импорт образа из tar-файла
docker load < ubuntu.tar

# Экспорт контейнера в образ
docker export container_name > container.tar
docker import container.tar new_image:tag
```

## Работа с контейнерами

### Запуск контейнеров:

```bash
# Запуск простого контейнера
docker run ubuntu echo "Hello World"

# Интерактивный режим
docker run -it ubuntu bash

# Запуск в фоновом режиме
docker run -d nginx

# Запуск с именем
docker run --name my-nginx -d nginx

# Запуск с портами
docker run -d -p 8080:80 nginx

# Запуск с переменными окружения
docker run -d -e MYSQL_ROOT_PASSWORD=mypass mysql:5.7

# Запуск с томами
docker run -d -v /host/path:/container/path nginx
```

### Управление контейнерами:

```bash
# Просмотр запущенных контейнеров
docker ps

# Просмотр всех контейнеров
docker ps -a

# Получение подробной информации
docker inspect container_name
docker inspect container_id

# Просмотр логов
docker logs container_name
docker logs -f container_name  # следить за логами в реальном времени

# Просмотр ресурсов
docker stats
docker stats container_name
```

### Жизненный цикл контейнеров:

```bash
# Запуск остановленного контейнера
docker start container_name

# Остановка контейнера
docker stop container_name
docker stop container_name -t 30  # с таймаутом 30 секунд

# Перезапуск контейнера
docker restart container_name

# Приостановка контейнера
docker pause container_name

# Возобновление контейнера
docker unpause container_name

# Удаление контейнера
docker rm container_name
docker rm -f container_name  # принудительно

# Удаление всех остановленных контейнеров
docker container prune
```

### Выполнение команд в контейнерах:

```bash
# Выполнение команды
docker exec container_name ls /app

# Интерактивный режим
docker exec -it container_name bash

# Выполнение с пользователем
docker exec -it -u root container_name sh
```

### Копирование файлов:

```bash
# Из контейнера в хост
docker cp container_name:/path/in/container ./local/path

# Из хоста в контейнер
docker cp ./local/file container_name:/path/in/container

# Копирование между контейнерами
docker cp container1:/file container2:/destination
```

## Dockerfile и сборка образов

### Основные инструкции Dockerfile:

```dockerfile
# Базовый образ
FROM ubuntu:20.04

# Информация о мейнтейнере
LABEL maintainer="your@email.com"

# Установка переменных окружения
ENV DEBIAN_FRONTEND=noninteractive
ENV APP_VERSION=1.0.0

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов
COPY requirements.txt /app/
COPY . /app/

# Рабочая директория
WORKDIR /app

# Установка Python зависимостей
RUN pip3 install -r requirements.txt

# Открытие портов
EXPOSE 8000

# Создание пользователя
RUN useradd -m -u 1000 appuser
USER appuser

# Команда по умолчанию
CMD ["python3", "app.py"]
```

### Сборка образов:

```bash
# Сборка с тегом
docker build -t myapp:1.0 .

# Сборка с несколькими тегами
docker build -t myapp:1.0 -t myapp:latest .

# Сборка из другого Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Сборка с аргументами
docker build --build-arg BUILD_VERSION=1.2.3 -t myapp:1.2.3 .

# Сборка без кэша
docker build --no-cache -t myapp:fresh .
```

### Многоступенчатая сборка:

```dockerfile
# Этап сборки
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Финальный этап
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Оптимизация Dockerfile:

```dockerfile
# Плохой пример - много слоев
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get clean

# Хороший пример - минимизация слоев
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Сети в Docker

### Типы сетей:

```bash
# Просмотр сетей
docker network ls

# Создание bridge сети
docker network create my-network

# Создание сети с драйвером
docker network create --driver bridge my-bridge-net
docker network create --driver overlay my-overlay-net

# Создание сети с подсетью
docker network create --subnet=172.20.0.0/16 my-custom-net
```

### Работа с сетями:

```bash
# Подключение контейнера к сети
docker network connect my-network container_name

# Отключение контейнера от сети
docker network disconnect my-network container_name

# Получение информации о сети
docker network inspect my-network

# Удаление сети
docker network rm my-network

# Удаление неиспользуемых сетей
docker network prune
```

### Примеры сетевых конфигураций:

```bash
# Создание изолированной сети
docker network create isolated-net

# Запуск контейнеров в одной сети
docker run -d --name web --network isolated-net nginx
docker run -d --name db --network isolated-net mysql:5.7

# Контейнеры могут общаться по имени
docker exec web ping db
```

### Порты и проброс:

```bash
# Проброс одного порта
docker run -d -p 8080:80 nginx

# Проброс нескольких портов
docker run -d -p 8080:80 -p 8443:443 nginx

# Проброс на конкретный интерфейс
docker run -d -p 127.0.0.1:8080:80 nginx

# Автоматический выбор порта хоста
docker run -d -P nginx  # Docker сам выберет порты
docker port container_name  # посмотреть назначенные порты
```

## Хранение данных (Volumes)

### Типы хранения:

#### 1. Volumes (рекомендуется):

```bash
# Создание volume
docker volume create my-volume

# Просмотр volumes
docker volume ls

# Получение информации
docker volume inspect my-volume

# Использование в контейнере
docker run -d -v my-volume:/data nginx

# Удаление volume
docker volume rm my-volume

# Удаление неиспользуемых volumes
docker volume prune
```

#### 2. Bind Mounts:

```bash
# Монтирование директории
docker run -d -v /host/path:/container/path nginx

# Монтирование файла
docker run -d -v /host/config.conf:/container/config.conf nginx

# Read-only монтирование
docker run -d -v /host/data:/container/data:ro nginx
```

#### 3. tmpfs:

```bash
# Временное хранение в памяти
docker run -d --tmpfs /tmp:rw,noexec,nosuid,size=100m nginx
```

### Примеры использования volumes:

```bash
# Сохранение данных базы
docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=mypass \
  -v mysql-data:/var/lib/mysql \
  mysql:5.7

# Совместное использование данных
docker run -d --name web1 -v shared-data:/app nginx
docker run -d --name web2 -v shared-data:/app nginx

# Резервное копирование volume
docker run --rm -v mysql-data:/data -v $(pwd):/backup ubuntu tar czf /backup/backup.tar.gz -C /data .
```

## Docker Compose

### Установка Docker Compose:

```bash
# Linux
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker-compose --version
```

### Базовый docker-compose.yml:

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example
      MYSQL_DATABASE: myapp
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
```

### Основные команды Compose:

```bash
# Запуск сервисов
docker-compose up
docker-compose up -d  # в фоновом режиме

# Остановка сервисов
docker-compose down

# Просмотр статуса
docker-compose ps

# Просмотр логов
docker-compose logs
docker-compose logs web

# Масштабирование сервисов
docker-compose up --scale web=3

# Пересборка образов
docker-compose build
docker-compose up --build

# Выполнение команд
docker-compose exec web ls /usr/share/nginx/html
docker-compose run web bash
```

### Продвинутый docker-compose.yml:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - ./frontend/src:/app/src
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - app-network

  redis:
    image: redis:alpine
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

## Реестры и репозитории

### Работа с Docker Hub:

```bash
# Авторизация
docker login
docker login -u username -p password

# Загрузка образа
docker push username/repository:tag

# Скачивание образа
docker pull username/repository:tag

# Поиск образов
docker search username/repository
```

### Создание собственного реестра:

```bash
# Запуск локального реестра
docker run -d -p 5000:5000 --name registry registry:2

# Использование локального реестра
docker tag myapp:latest localhost:5000/myapp:latest
docker push localhost:5000/myapp:latest
docker pull localhost:5000/myapp:latest
```

### Приватные реестры:

```bash
# Docker Registry с аутентификацией
docker run -d \
  -p 5000:5000 \
  --name registry \
  -v /auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -v /certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  registry:2
```

## Безопасность

### Пользователи и права:

```dockerfile
# Создание непривилегированного пользователя
FROM ubuntu:20.04
RUN useradd -m -u 1000 appuser
USER appuser
```

```bash
# Запуск с конкретным пользователем
docker run --user 1000:1000 myapp
```

### Capabilities:

```bash
# Удаление небезопасных capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx

# Запуск без capabilities
docker run --cap-drop=ALL nginx
```

### Read-only файловая система:

```bash
# Только чтение для корневой файловой системы
docker run --read-only nginx

# С writable volumes
docker run --read-only -v /tmp:/tmp nginx
```

### Сканирование уязвимостей:

```bash
# Использование Docker Scout
docker scout cves myimage:tag

# Использование Trivy
trivy image myimage:tag
```

## Мониторинг и логирование

### Системные метрики:

```bash
# Просмотр ресурсов контейнеров
docker stats
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Получение информации о контейнере
docker inspect container_name

# Просмотр логов
docker logs container_name
docker logs --tail 100 container_name
docker logs --since 1h container_name
```

### Логирование:

```bash
# Различные драйверы логирования
docker run --log-driver=json-file --log-opt max-size=10m nginx
docker run --log-driver=syslog --log-opt syslog-address=tcp://192.168.1.42:123 nginx
docker run --log-driver=fluentd --log-opt fluentd-address=192.168.1.42:24224 nginx
```

### Мониторинг с Prometheus:

```yaml
# docker-compose.yml для мониторинга
version: '3.8'

services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    devices:
      - /dev/kmsg

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

## Продвинутые темы

### Multi-architecture builds:

```bash
# Создание multi-arch образа
docker buildx create --name mybuilder
docker buildx use mybuilder
docker buildx build --platform linux/amd64,linux/arm64 -t username/myapp:latest --push .
```

### Docker Swarm:

```bash
# Инициализация swarm
docker swarm init

# Добавление ноды
docker swarm join --token TOKEN MANAGER_IP:2377

# Создание сервиса
docker service create --replicas 3 --name my-web nginx

# Масштабирование сервиса
docker service scale my-web=5

# Обновление сервиса
docker service update --image nginx:alpine my-web
```

### Kubernetes с Docker Desktop:

```bash
# Включение Kubernetes в Docker Desktop
# Settings -> Kubernetes -> Enable Kubernetes

# Проверка
kubectl get nodes
```

### Docker в CI/CD:

```yaml
# GitHub Actions пример
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
      
    - name: Login to Docker Hub
      run: echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
      
    - name: Push image
      run: |
        docker tag myapp:${{ github.sha }} username/myapp:latest
        docker push username/myapp:latest
```

## Лучшие практики

### 1. Оптимизация Dockerfile:

```dockerfile
# Плохо
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
COPY . /app
RUN pip3 install -r /app/requirements.txt

# Хорошо
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

### 2. Использование .dockerignore:

```dockerignore
# .dockerignore файл
.git
__pycache__
*.pyc
.env
Dockerfile
README.md
node_modules
```

### 3. Эффективное кэширование:

```dockerfile
# Кэширование зависимостей
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
```

### 4. Минимизация размера образа:

```dockerfile
# Multi-stage build для уменьшения размера
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --only=production
CMD ["node", "dist/index.js"]
```

### 5. Безопасность:

```dockerfile
# Безопасный Dockerfile
FROM alpine:latest
RUN apk --no-cache add python3 py3-pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser -D appuser
USER appuser
EXPOSE 8000
CMD ["python3", "app.py"]
```

### 6. Версионирование:

```bash
# Использование семантического версионирования
docker build -t myapp:1.0.0 .
docker build -t myapp:1.0 .
docker build -t myapp:latest .

# Пуш с тегами
docker push myapp:1.0.0
docker push myapp:1.0
docker push myapp:latest
```

> Этот мануал охватывает основные аспекты Docker. Для более глубокого изучения рекомендуется практиковаться на реальных примерах и изучать официальную документацию.