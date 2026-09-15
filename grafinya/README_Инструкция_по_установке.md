# Платформа мониторинга «Пульт» — Руководство по установке

> **Автор:** Дуплей Максим Игоревич | **Дата:** 10.06.2026 | **Версия документа:** 2026H1

![Docker](https://img.shields.io/badge/Docker-24.0%2B-2496ED?logo=docker&logoColor=white) ![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2.20%2B-2496ED?logo=docker&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248?logo=mongodb&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?logo=postgresql&logoColor=white) ![ClickHouse](https://img.shields.io/badge/ClickHouse-23.8%2B-FFCC00?logo=clickhouse&logoColor=black) ![Реестр РФ ПО](https://img.shields.io/badge/%D0%A0%D0%B5%D0%B5%D1%81%D1%82%D1%80_%D0%A0%D0%A4_%D0%9F%D0%9E-31563-green)

Руководство по установке и настройке компонентов платформы мониторинга **Пульт**, разработанной ООО «Лаборатория Числитель»:

| Компонент | Назначение | Документация |
|-----------|-----------|--------------|
| **Графиня** | Визуализация и аналитика: дашборды, графики, плагины источников данных | [docs.pult.tech/grafinya/install](https://docs.pult.tech/grafinya/install) |
| **Конструктор** | Генератор конфигурации развёртывания Графини (docker-compose, .env) | [docs.pult.tech/constructor](https://docs.pult.tech/constructor) |
| **Пульт** | Серверная часть мониторинга: сбор метрик, хранение, алертинг | [docs.pult.tech/docs/installation](https://docs.pult.tech/docs/installation/) |

---

## Содержание

1. [О продукте Графиня](#1-о-продукте-графиня)
2. [Обзор архитектуры](#2-обзор-архитектуры)
3. [Quick Start](#3-quick-start)
4. [Предварительные требования](#4-предварительные-требования)
5. [Профили установки](#5-профили-установки)
6. [Установка Графини](#6-установка-графини)
   - 6.1. [Подготовка окружения](#61-подготовка-окружения)
   - 6.2. [Конфигурация docker-compose.yml](#62-конфигурация-docker-composeyml)
   - 6.3. [Создание .env-файлов](#63-создание-env-файлов)
   - 6.4. [Плагины Графини](#64-плагины-графини)
   - 6.5. [Аутентификация в Docker Registry](#65-аутентификация-в-docker-registry)
   - 6.6. [Запуск и проверка сервисов](#66-запуск-и-проверка-сервисов)
   - 6.7. [Первый вход и настройка](#67-первый-вход-и-настройка)
7. [Использование Конструктора установки](#7-использование-конструктора-установки)
8. [Установка Пульт](#8-установка-пульт)
   - 8.1. [Установка PostgreSQL](#81-установка-postgresql)
   - 8.2. [Установка ClickHouse](#82-установка-clickhouse)
   - 8.3. [Установка Пульт (контейнеры)](#83-установка-пульт-контейнеры)
   - 8.4. [Установка Пульт (пакеты)](#84-установка-пульт-пакеты)
   - 8.5. [Установка High Availability](#85-установка-high-availability)
9. [Настройка HTTPS / TLS](#9-настройка-https--tls)
10. [Проверка здоровья системы](#10-проверка-здоровья-системы)
11. [Обновление и миграция](#11-обновление-и-миграция)
12. [Важные замечания для production](#12-важные-замечания-для-production)
13. [Troubleshooting](#13-troubleshooting)
14. [Полезные ссылки](#14-полезные-ссылки)

---

## 1. О продукте Графиня

**Графиня** — первый и единственный российский аналог Grafana, входящий в единый реестр российского ПО (реестровая запись № 31 563 от 30.12.2025). Это инструмент для визуализации, мониторинга и анализа данных в реальном времени, разработанный ООО «Лаборатория Числитель». Графиня обеспечивает полный импортозамещающий переход с Grafana, сохраняя привычный интерфейс и позволяя перенести существующие дашборды менее чем за 15 минут.

![Графиня — Витрины данных](./grafinya_dashboard.png)

### Ключевые преимущества

| Преимущество | Описание |
|-------------|----------|
| **Единственная альтернатива Grafana** | Полностью собственная разработка без кода Grafana, устраняющая ограничения и нестабильность оригинальной платформы |
| **Миграция за < 15 минут** | Лёгкий перенос дашбордов и наработок из Grafana без потери данных и экспертизы сотрудников |
| **Реестр российского ПО** | Соответствие требованиям импортозамещения и рекомендациям трансформации российского бизнеса (запись № 31 563) |
| **Неограниченные метрики и пользователи** | Нет ограничений на количество метрик, дашбордов и пользователей — в отличие от коммерческих аналогов |
| **Enterprise «из коробки»** | Корпоративный функционал доступен без дополнительных лицензий: ролевая модель, внешняя авторизация, модульная архитектура |
| **Сертификация ФСТЭК** | Скоро сертификат ФСТЭК по 4 уровню доверия (план на 2026H2) |

![Графиня — Возможности продукта](./grafinya_features.png)

### Возможности витрин данных

Графиня предоставляет расширенные возможности работы с интерактивными витринами данных, которые включают:

- **Переменные и трансформации** — динамические параметры, фильтры и трансформация данных позволяют изменять срезы информации в режиме реального времени, агрегировать показатели и подстраивать представление данных под конкретные сценарии анализа без изменения исходных источников
- **Различные типы виджетов** — линейные, столбчатые и круговые графики, таблицы с фильтрацией и сортировкой, индикаторы состояния и KPI-панели, адаптированные под разные типы аналитики
- **Объединение данных из разных источников** — данные из нескольких систем отображаются в одном виджете, что избавляет от необходимости переключаться между приложениями
- **Контекстные переходы (drill-down)** — углубление в детали данных прямо с панели витрины: от агрегированных показателей к отдельным транзакциям и событиям с сохранением контекста анализа
- **Отображение в реальном времени** — актуальные показатели без задержек, что критично для мониторинга процессов и принятия оперативных решений

### Поддерживаемые источники данных

Графиня работает с множеством источников данных, включая базы данных, форматы CSV, JSON, а также популярные системы мониторинга:

- **Пульт** — собственная система мониторинга Лаборатории Числитель
- **Prometheus** — запросы через PromQL
- **Victoria Metrics** — совместимый с Prometheus протокол
- **Zabbix** — интеграция через плагин
- **PostgreSQL** — прямые SQL-запросы
- **ClickHouse** — аналитические запросы к большим данным
- **Elasticsearch** — поиск и агрегация
- **GitLab** — CI/CD метрики и проекты
- **CSV / JSON** — загрузка и визуализация файлов

### Сравнение Графини с Grafana

![Сравнение Графиня vs Grafana](./grafinya_comparison.png)

| Критерий | Grafana 12.x OSS | Grafana 12.x Enterprise | Графиня |
|----------|-------------------|------------------------|----------|
| Дашборды, виджеты, переменные | Да | Да | Да |
| Алертинг | Да | Да | Да (расширенный) |
| Управление инцидентами (On-call) | Прекращено | Прекращено | 2026H2 |
| Автоматическое построение РСМ из Zabbix/Пульт | Нет | Нет | Да |
| Реестр российского ПО | Нет | Нет | Да (№ 31 563) |
| Сертификация ФСТЭК | Нет | Нет | 2026H2 (4 уровень) |
| Расширенные функции безопасности | Ограничены | Да | Да |
| Многоуровневое кеширование | Нет | Частично | Да (Tarantool) |
| Техническая поддержка | Нет | Недоступна в РФ | Да |
| Неограниченная кастомизация | Ограничена | Ограничена | Да (модульная архитектура) |
| Ролевая модель и внешняя авторизация | Нет (OSS) | Да | Да (из коробки) |
| Стабильность виджетов при обновлениях | Нестабильна | Нестабильна | Да |

### Миграция с Grafana

Перенос дашбордов из Grafana в Графиню занимает менее 15 минут. Процесс миграции включает:

1. **Экспорт дашборда** из Grafana в формате JSON
2. **Импорт** в Графиню через веб-интерфейс или API
3. **Подключение источников данных** — настройка плагинов для существующих Prometheus, PostgreSQL и других систем
4. **Проверка** корректности отображения виджетов и данных

При миграции сохраняются: структура дашбордов, переменные, трансформации, ссылки и контекстные переходы. Благодаря знакомому интерфейсу сотрудникам не нужно переучиваться.

---

## 2. Обзор архитектуры

Платформа «Пульт» состоит из нескольких взаимосвязанных компонентов, каждый из которых решает свою задачу в цепочке мониторинга. Понимание их взаимодействия помогает корректно спланировать развёртывание и избежать ошибок при настройке.

### Диаграмма архитектуры

```mermaid
graph LR
    subgraph "Графиня (визуализация)"
        FE[Frontend<br/>Nginx + React] --> BE[Backend<br/>Express API]
        BE --> DB[(MongoDB)]
        BE --> CACHE[(Tarantool<br/>Cache)]
        BE --> CW[Cache Worker]
        FE -->|Запросы данных| PLUGINS
    end

    subgraph "Плагины источников данных"
        PLUGINS[Plugin Router] --> PROM[Prometheus<br/>:8080]
        PLUGINS --> PULT[Pult Plugin<br/>:8081]
        PLUGINS --> CSV[CSV Plugin<br/>:8082]
        PLUGINS --> PG[PostgreSQL<br/>:8083]
        PLUGINS --> JSON[JSON Plugin<br/>:8084]
        PLUGINS --> GL[GitLab Plugin<br/>:8085]
        PLUGINS --> ES[Elasticsearch<br/>:8086]
        PLUGINS --> CH[ClickHouse<br/>:8087]
    end

    subgraph "Пульт (сервер мониторинга)"
        PULT_SVC[Pult Server] --> PULT_PG[(PostgreSQL)]
        PULT_SVC --> PULT_CH[(ClickHouse)]
    end

    subgraph "Модуль РСМ"
        RSM_API[RSM API<br/>:8102] --> RSM_UI[RSM UI<br/>:8202]
    end

    PULT -->|Метрики| PROM
    PULT -->|Метрики| CH
    PULT_SVC -->|Данные мониторинга| PULT
    RSM_API --> BE

    USER[Пользователь<br/>в браузере] --> FE
```

### Описание компонентов

**Графиня** — веб-интерфейс визуализации, построенный на React + Express. Она предоставляет пользователям дашборды, виджеты, графики и аналитические инструменты. Графиня обращается к различным источникам данных через систему плагинов (Prometheus, PostgreSQL, ClickHouse, CSV, JSON, GitLab, Elasticsearch и др.) и отображает результаты в удобном виде. В качестве СУБД для хранения пользовательских настроек, конфигураций дашбордов и метаданных используется MongoDB. Для кеширования часто запрашиваемых данных дашбордов может применяться Tarantool.

**Конструктор установки** — веб-утилита, которая пошагово проводит администратора через настройку параметров развёртывания Графини (хост, порты, учётные данные БД, JWT-секреты, набор плагинов, кеширование, модули) и генерирует готовые файлы `docker-compose.yml`, `.env_mongo`, `.env_backend`, `.env_frontend` и краткий `README.md`. Конструктор значительно упрощает процесс установки и снижает вероятность ошибок в конфигурации.

**Пульт** — серверный компонент, отвечающий за сбор, обработку и хранение метрик мониторинга. Он использует PostgreSQL как основную реляционную СУБД и ClickHouse для хранения больших объёмов временных рядов. Пульт может разворачиваться как в Docker-контейнерах, так и в виде системных пакетов (RPM/DEB). Для отказоустойчивых конфигураций предусмотрен режим High Availability.

**Типичный поток данных:**

```
Пульт (сбор метрик) → Pult Plugin → Графиня (визуализация) → Пользователь
```

---

## 3. Quick Start

> Если вам нужно быстро развернуть Графиню для оценки или тестирования — используйте этот сокращённый вариант. Для production-установки перейдите к [разделу 6](#6-установка-графини).

### Установка за 5 команд

```bash
# 1. Создайте директорию проекта
mkdir grafinya && cd grafinya

# 2. Войдите в Docker-реестр
docker login registry.pult.chislitellab.ru:8124

# 3. Сгенерируйте конфигурацию через Конструктор
#    Откройте https://docs.pult.tech/constructor в браузере
#    Скачайте сгенерированные файлы в текущую директорию

# 4. Запустите сервисы
docker compose up -d

# 5. Проверьте статус
docker compose ps
```

Затем откройте `http://<IP-сервера>` в браузере и войдите с логином `admin` и паролем `123456`. Система попросит сменить пароль при первом входе.

### Минимальный docker-compose.yml (для оценки)

Если вы хотите запустить Графиню вручную без Конструктора, вот минимальная конфигурация без кеширования и плагинов:

```yaml
services:
  mongo:
    image: registry.pult.chislitellab.ru:8124/portal/database-app:2026H1
    env_file: .env_mongo
    restart: unless-stopped
    volumes:
      - mongo-data:/data/db
    networks:
      - grafinya

  backend:
    image: registry.pult.chislitellab.ru:8124/portal/backend-app:2026H1
    restart: unless-stopped
    ports:
      - "5000:5000"
    env_file: .env_backend
    depends_on:
      - mongo
    networks:
      - grafinya

  frontend:
    image: registry.pult.chislitellab.ru:8124/portal/frontend-app:2026H1
    restart: unless-stopped
    env_file: .env_frontend
    ports:
      - "80:80"
    networks:
      - grafinya

volumes:
  mongo-data:

networks:
  grafinya:
    driver: bridge
```

> Для полноценной установки следуйте подробной инструкции ниже.

---

## 4. Предварительные требования

Перед началом установки убедитесь, что на целевом сервере выполнены все перечисленные ниже условия. Отсутствие хотя бы одного из компонентов приведёт к ошибкам на этапе запуска или некорректной работе сервисов.

### Общие требования

| Требование | Минимальная версия | Проверка |
|-----------|-------------------|----------|
| **Операционная система** | Linux (Ubuntu 22.04+, CentOS 8+, РЕД ОС 8+) | `cat /etc/os-release` |
| **Docker Engine** | 24.0+ | `docker --version` |
| **Docker Compose** | 2.20+ (плагин) | `docker compose version` |
| **Свободное место на диске** | от 20 ГБ | `df -h` |
| **Доступ к реестру** | `registry.pult.chislitellab.ru:8124` | `curl -I https://registry.pult.chislitellab.ru:8124/v2/` |
| **Доступ к реестру РСМ** | `registry.pult.chislitellab.ru:8126` (опционально) | `curl -I https://registry.pult.chislitellab.ru:8126/v2/` |

### Установка Docker (если не установлен)

```bash
# Ubuntu / Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Проверка
docker --version
docker compose version
```

### Ресурсы сервера

| Конфигурация | CPU | RAM | Диск | Подходит для |
|-------------|-----|-----|------|-------------|
| Минимальная (Графиня без кеша) | 2 ядра | 4 ГБ | 20 ГБ | Оценка, демо |
| Стандартная (Графиня + кеш + плагины) | 4 ядра | 8 ГБ | 40 ГБ | Небольшая команда |
| С Пультом | 4 ядра | 8 ГБ | 50 ГБ + метрики | Мониторинг продакшена |
| Полный стек (Графиня + Пульт + HA) | 8+ ядер | 16+ ГБ | 100+ ГБ | Enterprise, отказоустойчивость |

### Сетевые порты

| Порт | Сервис | Доступ |
|------|--------|--------|
| `80` | Frontend (Nginx) | Внешний |
| `443` | Frontend (HTTPS, при наличии reverse proxy) | Внешний |
| `5000` | Backend API | Внутренний / Внешний |
| `27017` | MongoDB | Только внутренний |
| `3301` | Tarantool Cache | Только внутренний |
| `8080` | Prometheus Plugin | Только внутренний |
| `8081` | Pult Plugin | Только внутренний |
| `8082` | CSV Plugin | Только внутренний |
| `8083` | PostgreSQL Plugin | Только внутренний |
| `8084` | JSON Plugin | Только внутренний |
| `8085` | GitLab Plugin | Только внутренний |
| `8086` | Elasticsearch Plugin | Только внутренний |
| `8087` | ClickHouse Plugin | Только внутренний |
| `8102` | RSM Module API | Внутренний |
| `8202` | RSM Module UI | Внешний (из браузера) |

---

## 5. Профили установки

Выберите подходящий профиль в зависимости от ваших задач. Каждый профиль определяет набор сервисов, плагинов и требований к ресурсам.

### Профиль 1: Минимальный (оценка / демо)

Подходит для первичного знакомства с системой, проведения демо-презентаций или разработки плагинов. Разворачивается на одном сервере с минимальными ресурсами, не требует кеширования и дополнительных модулей.

**Что входит:**
- MongoDB
- Backend
- Frontend
- 2 плагина: `pult`, `prometheus`

**Чего нет:** кеширования (Tarantool), модуля РСМ, большинства плагинов.

**PLUGIN_PRESET:** `pult,prometheus`

**.env_backend (минимальный):**

```env
MONGO_URI=mongodb://admin:Str0ngP@ssw0rd!@mongo:27017/grafinya?authSource=admin
PORT=5000
JWT_SECRET=<сгенерируйте_openssl_rand_-hex_32>
JWT_REFRESH_SECRET=<сгенерируйте_openssl_rand_-hex_32>
EXPIRES_TOKEN=24h
EXPIRES_REFRESH_TOKEN=7d
ALLOWED_ORIGIN=http://<HOST>
INACTIVE_USER_DEACTIVATION_CHECK_INTERVAL_MINUTES=60
ADMIN_MAX_CONCURRENT_SESSIONS=2
INTERNAL_TOKEN=<сгенерируйте_openssl_rand_-hex_32>
PLUGIN_PRESET=pult,prometheus
FEATURE_DASHBOARD_CACHE=false
```

### Профиль 2: Стандартный (небольшая команда)

Подходит для рабочих команд до 50 пользователей. Включает кеширование для ускорения загрузки дашбордов и расширенный набор плагинов для подключения к различным источникам данных. Модуль РСМ при необходимости добавляется отдельно.

**Что входит:**
- MongoDB
- Tarantool Cache + Cache Worker
- Backend
- Frontend
- 5 плагинов: `pult`, `prometheus`, `postgres`, `csv`, `json`

**PLUGIN_PRESET:** `pult,prometheus,postgres,csv,json`

**.env_backend (стандартный):**

```env
MONGO_URI=mongodb://admin:Str0ngP@ssw0rd!@mongo:27017/grafinya?authSource=admin
PORT=5000
JWT_SECRET=<сгенерируйте_openssl_rand_-hex_32>
JWT_REFRESH_SECRET=<сгенерируйте_openssl_rand_-hex_32>
EXPIRES_TOKEN=24h
EXPIRES_REFRESH_TOKEN=7d
ALLOWED_ORIGIN=http://<HOST>
INACTIVE_USER_DEACTIVATION_CHECK_INTERVAL_MINUTES=60
ADMIN_MAX_CONCURRENT_SESSIONS=2
SECURITY_LOG_FILE_PATH=/app-data/security/security.log
INTERNAL_TOKEN=<сгенерируйте_openssl_rand_-hex_32>
PLUGIN_PRESET=pult,prometheus,postgres,csv,json
FEATURE_DASHBOARD_CACHE=true
INTERNAL_WARMUP_URL=http://backend:5000/internal/cache/warmup-dashboard
CACHE_WORKER_INTERVAL_SEC=30
CACHE_HARD_MAX_STALE_SEC=900
TARANTOOL_CACHE_HOST=tarantool-cache
TARANTOOL_CACHE_PORT=3301
```

### Профиль 3: Полный (enterprise)

Полная конфигурация со всеми плагинами, кешированием и модулем РСМ. Подходит для крупных организаций с большим количеством пользователей, множеством источников данных и требованиями к отказоустойчивости.

**Что входит:**
- Все сервисы из стандартного профиля
- Все 8 плагинов
- Модуль РСМ (API + UI)

**PLUGIN_PRESET:** `pult,prometheus,postgres,csv,json,gitlab,elasticsearch,clickhouse`

**MODULE_PRESET:** `rsm`

> Полный пример `docker-compose.yml` и `.env`-файлов приведён в [разделе 6](#6-установка-графини).

---

## 6. Установка Графини

Система «Графиня» разворачивается в Docker-контейнерах при помощи Docker Compose. В качестве СУБД используется MongoDB. После установки веб-интерфейс будет доступен по адресу `http://<HOST>` или `http://<HOST>:<PORT>`, в зависимости от настроенного порта frontend.

**Данные для авторизации по умолчанию:**

| Параметр | Значение |
|----------|----------|
| Логин | `admin` |
| Пароль | `123456` |

> **Безопасность:** При первом входе система запросит смену пароля. Обязательно укажите надёжный пароль!

### 6.1. Подготовка окружения

Создайте рабочую директорию для проекта и перейдите в неё:

```bash
mkdir grafinya && cd grafinya
```

Проверьте, что Docker работает:

```bash
docker info
docker compose version
```

Проверьте доступ к реестру образов:

```bash
docker login registry.pult.chislitellab.ru:8124
# Введите учётные данные при запросе
# Успешный ответ: Login Succeeded
```

### 6.2. Конфигурация docker-compose.yml

Создайте файл `docker-compose.yml` в рабочей директории. Ниже приведён полный пример для версии **2026H1 «Ассамблея»** с включённым кешированием и модулем РСМ:

```yaml
services:
  # ============================================================
  # БАЗА ДАННЫХ
  # ============================================================
  mongo:
    image: registry.pult.chislitellab.ru:8124/portal/database-app:2026H1
    env_file: .env_mongo
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    networks:
      - grafinya

  # ============================================================
  # КЕШИРОВАНИЕ (опционально — уберите, если не нужно)
  # ============================================================
  tarantool-cache:
    image: tarantool/tarantool:2.11
    restart: unless-stopped
    expose:
      - "3301"
    networks:
      - grafinya

  # ============================================================
  # BACKEND
  # ============================================================
  backend:
    image: registry.pult.chislitellab.ru:8124/portal/backend-app:2026H1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "-e", "const url = new URL(process.env.HEALTHCHECK_URL || 'http://127.0.0.1:5000/healthz'); const client = url.protocol === 'https:' ? require('https') : require('http'); const req = client.get(url, (res) => process.exit(res.statusCode === 200 ? 0 : 1)); req.on('error', () => process.exit(1)); req.setTimeout(4000, () => { req.destroy(); process.exit(1); });"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
    ports:
      - "5000:5000"
    env_file: .env_backend
    environment:
      SECURITY_LOG_FILE_PATH: ${SECURITY_LOG_FILE_PATH:-/app-data/security/security.log}
    volumes:
      - security-log-data:/app-data/security
    depends_on:
      - mongo
      - tarantool-cache
    networks:
      - grafinya

  # Фоновый воркер обновления кеша дашбордов
  cache-worker:
    image: registry.pult.chislitellab.ru:8124/portal/backend-app:2026H1
    restart: unless-stopped
    env_file: .env_backend
    command: npm run worker:cache
    healthcheck:
      test: ["CMD-SHELL", "ps | grep -Eq '[c]acheWorker\\.(ts|js)'"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
    depends_on:
      - mongo
      - tarantool-cache
      - backend
    networks:
      - grafinya

  # ============================================================
  # FRONTEND
  # ============================================================
  frontend:
    image: registry.pult.chislitellab.ru:8124/portal/frontend-app:2026H1
    restart: unless-stopped
    env_file: .env_frontend
    ports:
      - "80:80"
    networks:
      - grafinya

  # ============================================================
  # ПЛАГИНЫ ИСТОЧНИКОВ ДАННЫХ
  # ============================================================
  prometheus-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/prometheus:1.3.0
    restart: unless-stopped
    ports:
      - "8080:8080"
    networks:
      - grafinya

  pult-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/pult:1.3.0
    restart: unless-stopped
    ports:
      - "8081:8080"
    networks:
      - grafinya

  csv-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/csv-plugin:1.3.0
    restart: unless-stopped
    ports:
      - "8082:8080"
    networks:
      - grafinya

  postgres-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/postgres-plugin:1.3.0
    restart: unless-stopped
    ports:
      - "8083:8080"
    networks:
      - grafinya

  json-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/json-plugin:1.3.0
    restart: unless-stopped
    ports:
      - "8084:8080"
    networks:
      - grafinya

  gitlab-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/gitlab-plugin:1.3.0
    restart: unless-stopped
    ports:
      - "8085:8080"
    networks:
      - grafinya

  elasticsearch-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/elasticsearch-plugin:1.3.0
    restart: unless-stopped
    ports:
      - "8086:8080"
    networks:
      - grafinya

  clickhouse-plugin:
    image: registry.pult.chislitellab.ru:8124/portal/plugins/clickhouse-plugin:1.3.0
    restart: unless-stopped
    ports:
      - "8087:8080"
    networks:
      - grafinya

  # ============================================================
  # МОДУЛЬ РСМ (опционально — уберите, если не нужен)
  # ============================================================
  rsm-module-api:
    image: registry.pult.chislitellab.ru:8126/portal/modules/rsm-module-api:1.3.0
    restart: unless-stopped
    environment:
      FRONTEND_HOST: "http://<HOST_IP>:8202"
    ports:
      - "8102:8080"
    networks:
      - grafinya

  rsm-module-ui:
    image: registry.pult.chislitellab.ru:8126/portal/modules/rsm-module-ui:1.3.0
    restart: unless-stopped
    env_file: .env_backend
    ports:
      - "8202:3000"
    networks:
      - grafinya

volumes:
  mongo-data:
  security-log-data:

networks:
  grafinya:
    driver: bridge
```

> **Важно:** Параметр `FRONTEND_HOST` у сервиса `rsm-module-api` должен указывать на внешний URL `rsm-module-ui`, доступный из браузера пользователя. По умолчанию это `http://<HOST_IP>:8202`, но при необходимости укажите другой домен или порт.

> Если какие-то плагины или модуль РСМ не нужны — удалите соответствующие сервисы из `docker-compose.yml` и скорректируйте переменную `PLUGIN_PRESET` в `.env_backend` (см. раздел [6.4](#64-плагины-графини)).

### 6.3. Создание .env-файлов

В рабочей директории создайте три файла окружения. Обязательно замените значения в угловых скобках `<...>` на реальные данные.

> **Совет:** Для генерации безопасных секретов используйте команду:
> ```bash
> openssl rand -hex 32
> ```
> Выполните её трижды для `JWT_SECRET`, `JWT_REFRESH_SECRET` и `INTERNAL_TOKEN`.

#### a. Файл `.env_mongo`

```env
MONGO_INITDB_ROOT_USERNAME=<DB_LOGIN>
MONGO_INITDB_ROOT_PASSWORD=<DB_PASSWORD>
MONGO_INITDB_DATABASE=grafinya
```

Пример с тестовыми значениями (для production используйте надёжные пароли):

```env
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=Str0ngP@ssw0rd!
MONGO_INITDB_DATABASE=grafinya
```

> **Внимание:** Обязательно укажите свои `DB_LOGIN` и `DB_PASSWORD`, иначе система не запустится корректно. Учётные данные должны совпадать с теми, что указаны в `MONGO_URI` файла `.env_backend`.

#### b. Файл `.env_backend`

```env
# =============================================================
# Подключение к MongoDB
# =============================================================
MONGO_URI=mongodb://<DB_LOGIN>:<DB_PASSWORD>@mongo:27017/grafinya?authSource=admin

# =============================================================
# Express / runtime
# =============================================================
PORT=5000

# =============================================================
# JWT-токены (ОБЯЗАТЕЛЬНО замените на свои безопасные значения!)
# =============================================================
JWT_SECRET=<JWT_SECRET>
JWT_REFRESH_SECRET=<JWT_REFRESH_SECRET>
EXPIRES_TOKEN=24h
EXPIRES_REFRESH_TOKEN=7d

# =============================================================
# CORS / origins
# =============================================================
ALLOWED_ORIGIN=http://<HOST>

# =============================================================
# Безопасность / служебные
# =============================================================
INACTIVE_USER_DEACTIVATION_CHECK_INTERVAL_MINUTES=60
ADMIN_MAX_CONCURRENT_SESSIONS=2
SECURITY_LOG_FILE_PATH=/app-data/security/security.log
INTERNAL_TOKEN=<RANDOM_INTERNAL_TOKEN>

# =============================================================
# Плагины и модули
# =============================================================
PLUGIN_PRESET=pult,prometheus,postgres,csv,json,gitlab,elasticsearch,clickhouse
MODULE_PRESET=rsm

# =============================================================
# Кеширование (уберите блок, если FEATURE_DASHBOARD_CACHE=false)
# =============================================================
FEATURE_DASHBOARD_CACHE=true
INTERNAL_WARMUP_URL=http://backend:5000/internal/cache/warmup-dashboard
CACHE_WORKER_INTERVAL_SEC=30
CACHE_HARD_MAX_STALE_SEC=900
TARANTOOL_CACHE_HOST=tarantool-cache
TARANTOOL_CACHE_PORT=3301

# =============================================================
# RSM модуль (уберите блок, если MODULE_PRESET не задан)
# =============================================================
RSM_MODULE_VERSION=1.3.0
RSM_MODULE_API_BASE_URL=http://rsm-module-api:8080
RSM_MODULE_FRONTEND_HOST=http://<HOST_IP>:8202
RSM_MODULE_BUILD_TIMESTAMP=
```

> **Обязательно замените:**
> - `DB_LOGIN` и `DB_PASSWORD` на реальные учётные данные MongoDB (те же, что в `.env_mongo`)
> - `JWT_SECRET`, `JWT_REFRESH_SECRET` и `INTERNAL_TOKEN` на собственные безопасные значения
> - `ALLOWED_ORIGIN` на фактический адрес frontend
> - `RSM_MODULE_FRONTEND_HOST` на внешний адрес `rsm-module-ui`

> Параметр `SECURITY_LOG_FILE_PATH` остаётся в `.env_backend`, а в `docker-compose.yml` дополнительно прокидывается в контейнер backend с fallback-значением `/app-data/security/security.log`. Для сохранения журнала между перезапусками используется volume `security-log-data`.

#### c. Файл `.env_frontend`

```env
# URL backend API, доступный из браузера пользователя
VITE_API_BASE_URL=http://<HOST>:5000/api/v1

# Фичи кеширования и прогноза (true / false, НЕ пустое значение!)
VITE_FEATURE_DASHBOARD_CACHE=true
VITE_FEATURE_DASHBOARD_FORECAST=true

# Настройки Nginx (опционально)
NGINX_HOST=<HOST>
NGINX_PORT=80
```

Пример с конкретными значениями:

```env
VITE_API_BASE_URL=http://192.168.0.1:5000/api/v1
VITE_FEATURE_DASHBOARD_CACHE=true
VITE_FEATURE_DASHBOARD_FORECAST=true
NGINX_HOST=192.168.0.1
NGINX_PORT=80
```

> **Обязательно замените `VITE_API_BASE_URL`** на адрес backend API, доступный из браузера пользователя.

> Параметры `NGINX_HOST` и `NGINX_PORT` необязательны и используются только при необходимости явно настроить host и port для Nginx-контейнера.

> Параметры `VITE_FEATURE_DASHBOARD_CACHE` и `VITE_FEATURE_DASHBOARD_FORECAST` должны быть заданы явно как `true` или `false`; пустое значение приведёт к некорректной генерации runtime-конфига frontend.

### 6.4. Плагины Графини

Конструктор установки поддерживает следующие плагины, каждый из которых запускается в собственном контейнере. Плагины не зависят друг от друга — вы можете подключать только те, которые нужны для ваших источников данных.

| Плагин | Образ | Порт | Назначение |
|--------|-------|------|-----------|
| `prometheus-plugin` | `plugins/prometheus:1.3.0` | 8080 | Запрос метрик из Prometheus через PromQL |
| `pult-plugin` | `plugins/pult:1.3.0` | 8081 | Получение данных мониторинга из сервера Пульт |
| `csv-plugin` | `plugins/csv-plugin:1.3.0` | 8082 | Загрузка и визуализация данных из CSV-файлов |
| `postgres-plugin` | `plugins/postgres-plugin:1.3.0` | 8083 | SQL-запросы к базам данных PostgreSQL |
| `json-plugin` | `plugins/json-plugin:1.3.0` | 8084 | Подключение к JSON API и REST-источникам |
| `gitlab-plugin` | `plugins/gitlab-plugin:1.3.0` | 8085 | Интеграция с GitLab (CI/CD метрики, проекты) |
| `elasticsearch-plugin` | `plugins/elasticsearch-plugin:1.3.0` | 8086 | Поиск и агрегация данных из Elasticsearch |
| `clickhouse-plugin` | `plugins/clickhouse-plugin:1.3.0` | 8087 | Аналитические запросы к ClickHouse |

Если нужен не полный набор плагинов, удалите ненужные сервисы из `docker-compose.yml` и скорректируйте переменную `PLUGIN_PRESET` в `.env_backend`, перечислив только нужные плагины через запятую. Например, для минимальной конфигурации:

```env
PLUGIN_PRESET=pult,prometheus
```

> Удаление плагина из `docker-compose.yml` без обновления `PLUGIN_PRESET` приведёт к ошибкам при запуске backend — он будет пытаться подключиться к несуществующим плагинам.

### 6.5. Аутентификация в Docker Registry

Для установки Графини и модуля РСМ выполните вход в приватные Docker-реестры, используя учётные данные, предоставленные Лабораторией Числитель:

```bash
# Основной реестр (обязательно)
docker login registry.pult.chislitellab.ru:8124

# Реестр модуля РСМ (только если используется РСМ)
docker login registry.pult.chislitellab.ru:8126
```

Введите логин и пароль при запросе. Успешный ответ: `Login Succeeded`.

> Если аутентификация не проходит, убедитесь, что учётные данные корректны и у вас есть права на скачивание образов. Обратитесь к администратору или в Лабораторию Числитель.

### 6.6. Запуск и проверка сервисов

#### Запуск

Выполните команду из рабочей директории, где находятся `docker-compose.yml` и `.env`-файлы:

```bash
docker compose up -d
```

Docker Compose скачает необходимые образы и запустит все сервисы в фоновом режиме. Первый запуск может занять несколько минут в зависимости от скорости интернет-соединения.

#### Мониторинг запуска

Следите за процессом запуска в реальном времени:

```bash
docker compose logs -f
```

Дождитесь, пока backend пройдёт healthcheck (статус `healthy`). Обычно это занимает 30–60 секунд после старта.

#### Проверка статуса

Убедитесь, что все контейнеры работают:

```bash
docker compose ps
```

Ожидаемый результат для полного профиля:

```
NAME                 STATUS              PORTS
mongo                running             0.0.0.0:27017->27017/tcp
tarantool-cache      running             3301/tcp
backend              running (healthy)   0.0.0.0:5000->5000/tcp
cache-worker         running
frontend             running             0.0.0.0:80->80/tcp
prometheus-plugin    running             0.0.0.0:8080->8080/tcp
pult-plugin          running             0.0.0.0:8081->8080/tcp
csv-plugin           running             0.0.0.0:8082->8080/tcp
postgres-plugin      running             0.0.0.0:8083->8080/tcp
json-plugin          running             0.0.0.0:8084->8080/tcp
gitlab-plugin        running             0.0.0.0:8085->8080/tcp
elasticsearch-plugin running             0.0.0.0:8086->8080/tcp
clickhouse-plugin    running             0.0.0.0:8087->8080/tcp
rsm-module-api       running             0.0.0.0:8102->8080/tcp
rsm-module-ui        running             0.0.0.0:8202->3000/tcp
```

#### Если контейнер не запустился

```bash
# Логи конкретного сервиса
docker compose logs backend
docker compose logs frontend

# Логи в реальном времени
docker compose logs -f backend

# Перезапуск одного сервиса
docker compose restart backend

# Полная пересборка и перезапуск
docker compose down && docker compose up -d
```

### 6.7. Первый вход и настройка

1. Откройте в браузере `http://<HOST>` (или `http://<HOST>:80`)
2. Введите учётные данные по умолчанию:
   - **Логин:** `admin`
   - **Пароль:** `123456`
3. Система предложит сменить пароль — укажите новый надёжный пароль (минимум 12 символов, буквы, цифры, спецсимволы)
4. После входа откройте настройки и подключите нужные источники данных через плагины

---

## 7. Использование Конструктора установки

**Конструктор установки** ([docs.pult.tech/constructor](https://docs.pult.tech/constructor)) — интерактивный веб-инструмент, который пошагово проводит через настройку параметров развёртывания Графини и генерирует готовые конфигурационные файлы. Это рекомендуемый способ подготовки файлов для установки — он минимизирует вероятность ошибок и автоматически синхронизирует параметры между файлами.

### Шаги конструктора

| Шаг | Название | Что настраивается |
|-----|----------|-------------------|
| 1 | Параметры установки | IP или домен сервера, порты frontend и backend API |
| 2 | База данных (MongoDB) | Учётные данные, имя базы данных |
| 3 | Настройки backend | JWT-секреты, токены, CORS-origins |
| 4 | Настройки frontend | API URL, параметры Nginx |
| 5 | Плагины | Выбор плагинов из поддерживаемого набора |
| 6 | Кеширование | Включение/отключение кеша дашбордов, Tarantool |
| 7 | Модули | Подключение модуля РСМ |
| 8 | Проверка | Сводка по конфигурации перед генерацией |
| 9 | Готовая конфигурация | Просмотр и скачивание файлов |

### Генерируемые файлы

| Файл | Описание |
|------|----------|
| `docker-compose.yml` | Основной файл оркестрации контейнеров |
| `.env_mongo` | Переменные окружения для MongoDB |
| `.env_backend` | Переменные окружения для backend и cache-worker |
| `.env_frontend` | Переменные окружения для frontend (Nginx + React) |
| `README.md` | Краткая сводка по выбранной конфигурации |

### Рекомендации по использованию

- Используйте Конструктор при первой установке — это существенно ускоряет процесс и снижает вероятность ошибок в `.env`-файлах
- При обновлении конфигурации можно заново пройти Конструктор и сравнить сгенерированные файлы с текущими
- Если кеширование или модуль РСМ не нужны, Конструктор автоматически уберёт соответствующие сервисы и переменные
- После скачивания файлов обязательно проверьте и при необходимости скорректируйте значения секретов (`JWT_SECRET`, `INTERNAL_TOKEN` и т.д.) — не используйте значения-заглушки в production

---

## 8. Установка Пульт

Серверная часть «Пульт» (версия 2.3.0) отвечает за сбор, обработку и хранение метрик мониторинга. Установка Пульта состоит из нескольких этапов: сначала подготавливаются СУБД (PostgreSQL и ClickHouse), затем разворачивается сам Пульт.

Актуальная документация: [docs.pult.tech/docs/installation](https://docs.pult.tech/docs/installation/)

### 8.1. Установка PostgreSQL

PostgreSQL используется как основная реляционная СУБД для хранения конфигурационных данных Пульта: учётных записей пользователей, настроек алертов, конфигураций сбора метрик, правил маршрутизации и других служебных данных. Без правильно настроенного экземпляра PostgreSQL Пульт не сможет функционировать, поэтому этот этап является обязательным и должен быть выполнен до установки самого Пульта.

Подробная инструкция доступна на странице «Установка PostgreSQL» в официальной документации.

**Ключевые шаги:**

1. **Установите PostgreSQL** поддерживаемой версии (актуальный список поддерживаемых версий указан в документации Пульта). Рекомендуется использовать PostgreSQL 15 или выше для оптимальной производительности и безопасности.

2. **Создайте базу данных и пользователя:**
   ```sql
   CREATE USER pult_user WITH PASSWORD '<надёжный_пароль>';
   CREATE DATABASE pult_db OWNER pult_user;
   GRANT ALL PRIVILEGES ON DATABASE pult_db TO pult_user;
   ```

3. **Настройте аутентификацию** — отредактируйте `pg_hba.conf`, разрешив подключение от сервера Пульта. Рекомендуется использовать метод `scram-sha-256` для максимальной безопасности.

4. **Настройте параметры** — в `postgresql.conf` увеличьте `max_connections`, `shared_buffers` и `work_mem` в соответствии с ожидаемой нагрузкой. Для систем с 8 ГБ RAM рекомендуется: `shared_buffers = 2GB`, `max_connections = 200`.

5. **Проверьте подключение:**
   ```bash
   psql -h <HOST> -U pult_user -d pult_db -c "SELECT version();"
   ```

### 8.2. Установка ClickHouse

ClickHouse используется для хранения больших объёмов временных рядов — метрик мониторинга, которые собирает Пульт. ClickHouse обеспечивает высокую скорость записи (сотни тысяч строк в секунду) и аналитических запросов к временным рядам, что критично для систем мониторинга с большим потоком данных. Правильная настройка ClickHouse напрямую влияет на производительность системы при работе с историческими данными и построении графиков за длительные периоды.

Подробная инструкция доступна на странице «Установка ClickHouse» в официальной документации.

**Ключевые шаги:**

1. **Установите ClickHouse Server и Client** из официальных пакетов. Рекомендуемая версия — 23.8 или выше.

2. **Настройте конфигурацию сервера** — в файле `/etc/clickhouse-server/config.xml` укажите:
   - Сетевые интерфейсы для прослушивания (`listen_host`)
   - Лимиты памяти (`max_server_memory_usage`)
   - Порты для HTTP (8123) и нативного (9000) интерфейсов
   - Настройки логирования

3. **Создайте базу данных и таблицы** для метрик. Пульт автоматически создаёт необходимую схему при первом запуске, но базу данных нужно создать заранее:
   ```sql
   CREATE DATABASE IF NOT EXISTS pult_metrics;
   ```

4. **Настройте подключение из Пульта** — укажите хост, порт и учётные данные ClickHouse в конфигурации Пульта.

5. **Проверьте подключение:**
   ```bash
   clickhouse-client -h <HOST> --user default --password '<пароль>' -q "SELECT version()"
   ```

### 8.3. Установка Пульт (контейнеры)

Развёртывание Пульта в Docker-контейнерах — рекомендуемый способ для большинства сценариев. Контейнерная установка обеспечивает изоляцию компонентов, простоту обновления и воспроизводимость окружения, а также упрощает масштабирование при росте нагрузки.

Подробная инструкция доступна на странице «Установка Пульт (контейнеры)» в официальной документации.

**Общий порядок действий:**

1. Убедитесь, что PostgreSQL и ClickHouse установлены, настроены и доступны по сети с сервера, где будет развёрнут Пульт
2. Выполните вход в Docker-реестр:
   ```bash
   docker login registry.pult.chislitellab.ru:8124
   ```
3. Создайте рабочую директорию и подготовьте `docker-compose.yml` для Пульта
4. Настройте переменные окружения — укажите параметры подключения к PostgreSQL, ClickHouse, порты и секреты
5. Запустите сервисы:
   ```bash
   docker compose up -d
   ```
6. Проверьте статус контейнеров и логи:
   ```bash
   docker compose ps
   docker compose logs -f pult
   ```

### 8.4. Установка Пульт (пакеты)

Для сред, где использование Docker нежелательно или невозможно (например, из-за требований безопасности, отсутствия поддержки контейнеризации на сервере или необходимости тесной интеграции с системными службами), Пульт можно установить в виде системных пакетов. Поддерживаются форматы RPM (для RHEL/CentOS/РЕД ОС) и DEB (для Debian/Ubuntu). Пакетная установка обеспечивает управление через systemd, автоматические обновления через пакетный менеджер и интеграцию с системным логированием.

Подробная инструкция доступна на странице «Установка Пульт (пакеты)» в официальной документации.

**Общий порядок действий:**

1. **Подключите репозиторий** пакетов Лаборатории Числитель:
   ```bash
   # RPM (RHEL/CentOS/РЕД ОС)
   sudo cat > /etc/yum.repos.d/pult.repo <<EOF
   [pult]
   name=Pult Repository
   baseurl=https://<репозиторий_URL>/rpm
   enabled=1
   gpgcheck=1
   gpgkey=https://<репозиторий_URL>/RPM-GPG-KEY-pult
   EOF

   # DEB (Debian/Ubuntu)
   sudo apt-get install -y curl gnupg
   curl -fsSL https://<репозиторий_URL>/gpg | sudo apt-key add -
   echo "deb https://<репозиторий_URL>/deb stable main" | sudo tee /etc/apt/sources.list.d/pult.list
   sudo apt-get update
   ```

2. **Установите пакет Пульта:**
   ```bash
   # RPM
   sudo yum install pult-server

   # DEB
   sudo apt-get install pult-server
   ```

3. **Настройте конфигурационные файлы** — укажите параметры подключения к PostgreSQL и ClickHouse в файле конфигурации Пульта (обычно `/etc/pult/config.yml` или аналогичном)

4. **Запустите службу и включите автозапуск:**
   ```bash
   sudo systemctl enable pult-server
   sudo systemctl start pult-server
   sudo systemctl status pult-server
   ```

5. **Проверьте статус службы** и убедитесь, что нет ошибок в журнале:
   ```bash
   sudo journalctl -u pult-server -f
   ```

### 8.5. Установка High Availability

Для обеспечения отказоустойчивости и непрерывности мониторинга Пульт может быть развёрнут в конфигурации High Availability (HA). В такой конфигурации при выходе из строя одного узла системы другие автоматически берут на себя его нагрузку, обеспечивая бесперебойный сбор и отображение метрик. HA-конфигурация рекомендуется для production-окружений с высокими требованиями к доступности.

Подробная инструкция доступна на странице «Установка High Availability» в официальной документации.

**Ключевые компоненты HA-конфигурации:**

| Компонент | Решение | Назначение |
|-----------|---------|-----------|
| Балансировщик нагрузки | Nginx / HAProxy | Распределение трафика между экземплярами Пульта |
| Пульт | 2+ экземпляра | Горизонтальное масштабирование и отказоустойчивость |
| PostgreSQL | Streaming Replication / Patroni | Репликация данных, автоматический failover |
| ClickHouse | ReplicatedMergeTree | Репликация данных между узлами ClickHouse |
| Мониторинг Пульта | Health checks | Автоматическое обнаружение и исключение недоступных узлов |

**Минимальная HA-конфигурация:** 2 экземпляра Пульта + балансировщик + реплицированные PostgreSQL и ClickHouse.

---

## 9. Настройка HTTPS / TLS

Для production-окружения настоятельно рекомендуется настроить HTTPS, чтобы защитить передачу данных между браузером пользователя и сервером. Это особенно важно, поскольку система передаёт учётные данные, JWT-токены и конфиденциальные данные мониторинга.

### Вариант 1: Reverse Proxy (рекомендуется)

Добавьте Nginx или Caddy перед контейнерами Графини в качестве reverse proxy с терминированием TLS:

```nginx
# /etc/nginx/sites-available/grafinya.conf
server {
    listen 443 ssl http2;
    server_name grafinya.example.com;

    ssl_certificate     /etc/ssl/certs/grafinya.crt;
    ssl_certificate_key /etc/ssl/private/grafinya.key;

    # Рекомендуемые настройки безопасности
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Редирект HTTP -> HTTPS
server {
    listen 80;
    server_name grafinya.example.com;
    return 301 https://$host$request_uri;
}
```

После настройки reverse proxy обновите `.env_frontend`:

```env
VITE_API_BASE_URL=https://grafinya.example.com/api/v1
NGINX_HOST=grafinya.example.com
NGINX_PORT=80
```

И `.env_backend`:

```env
ALLOWED_ORIGIN=https://grafinya.example.com
```

### Вариант 2: Let's Encrypt (автоматические сертификаты)

Для автоматического получения и обновления сертификатов Let's Encrypt используйте Certbot:

```bash
# Установка Certbot
sudo apt-get install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d grafinya.example.com

# Автоматическое обновление (проверьте, что cron-задача активна)
sudo certbot renew --dry-run
```

---

## 10. Проверка здоровья системы

После установки регулярно проверяйте состояние компонентов системы. Ниже приведены основные endpoints и команды для мониторинга.

### Health Endpoints

| Endpoint | Метод | Ожидаемый ответ | Описание |
|----------|-------|-----------------|----------|
| `http://<HOST>:5000/healthz` | GET | `200 OK` | Проверка здоровья backend |
| `http://<HOST>:8080/health` | GET | `200 OK` | Проверка здоровья Prometheus Plugin |
| `http://<HOST>:8081/health` | GET | `200 OK` | Проверка здоровья Pult Plugin |

### Команды проверки

```bash
# Статус всех контейнеров
docker compose ps

# Проверка здоровья backend через curl
curl -f http://localhost:5000/healthz || echo "Backend UNHEALTHY"

# Проверка подключения к MongoDB
docker compose exec mongo mongosh -u admin -p '<пароль>' --eval "db.runCommand({ping:1})"

# Проверка кеша Tarantool
docker compose exec tarantool-cache console
# В консоли Tarantool:
# box.info.status  → "running"

# Использование ресурсов контейнерами
docker stats --no-stream

# Размер volumes
docker volume ls
docker system df -v
```

### Мониторинг логов безопасности

```bash
# Просмотр журнала безопасности
docker compose exec backend cat /app-data/security/security.log

# Мониторинг в реальном времени
docker compose logs -f backend | grep -i "security\|error\|auth"
```

---

## 11. Обновление и миграция

Регулярное обновление компонентов платформы важно для получения исправлений безопасности, новых функций и улучшений производительности. Перед каждым обновлением обязательно создавайте резервные копии.

### Общий порядок обновления Графини

```bash
# 1. Создайте резервную копию данных
docker compose exec mongo mongodump --out /data/db/backup
# Или создайте snapshot volumes

# 2. Остановите сервисы
docker compose down

# 3. Обновите теги образов в docker-compose.yml
# Замените :2025H2 на :2026H1 и т.д.

# 4. Войдите в реестр (если сессия истекла)
docker login registry.pult.chislitellab.ru:8124

# 5. Скачайте новые образы
docker compose pull

# 6. Запустите сервисы с новыми образами
docker compose up -d

# 7. Проверьте статус и логи
docker compose ps
docker compose logs -f backend
```

### Обновление плагинов

При обновлении плагинов обратите внимание на совместимость версий. Теги плагинов следуют семантическому версионированию (например, `1.3.0` → `1.4.0`). Минорные обновления (1.3.0 → 1.3.1) обычно обратно совместимы, а мажорные (1.x → 2.x) могут требовать изменений в конфигурации.

```bash
# Обновление только плагинов
docker compose pull prometheus-plugin pult-plugin csv-plugin
docker compose up -d prometheus-plugin pult-plugin csv-plugin
```

### Откат на предыдущую версию

Если после обновления возникли проблемы, можно откатиться:

```bash
# 1. Остановите сервисы
docker compose down

# 2. Верните старые теги образов в docker-compose.yml

# 3. Запустите сервисы
docker compose up -d

# 4. При необходимости восстановите данные из резервной копии
docker compose exec mongo mongorestore /data/db/backup
```

---

## 12. Важные замечания для production

При развёртывании платформы в production-окружении обязательно соблюдайте следующие правила безопасности и настройки. Игнорирование этих рекомендаций может привести к уязвимостям, потере данных или нестабильной работе системы.

### Безопасность

- **JWT-секреты:** Используйте уникальные, криптографически стойкие значения для `JWT_SECRET`, `JWT_REFRESH_SECRET` и `INTERNAL_TOKEN`. Генерируйте их с помощью `openssl rand -hex 32` или аналогичных инструментов. Никогда не используйте значения по умолчанию в production. Периодически обновляйте секреты, особенно если есть подозрение на компрометацию.

- **CORS:** Укажите корректный `ALLOWED_ORIGIN`, ограничивающий доступ к API только с разрешённых доменов. Не используйте `*` в production — это позволяет любому сайту обращаться к вашему API.

- **Пароль администратора:** Обязательно смените пароль по умолчанию (`123456`) при первом входе. Используйте пароль длиной не менее 12 символов, содержащий буквы (верхний и нижний регистр), цифры и специальные символы.

- **Сетевая безопасность:** Ограничьте доступ к внутренним портам с помощью файрвола. Порты MongoDB (27017), Tarantool (3301), плагинов (8080–8087) и RSM API (8102) должны быть доступны только из внутренней сети. Единственный порт, открытый для пользователей — это порт frontend (80/443).

- **HTTPS:** Всегда используйте HTTPS в production для защиты передачи учётных данных и токенов (см. [раздел 8](#8-настройка-https--tls)).

### Кеширование

- Если кеширование дашбордов не требуется, отключите его — удалите сервисы `tarantool-cache` и `cache-worker` из `docker-compose.yml`, а также уберите переменные `FEATURE_DASHBOARD_CACHE`, `INTERNAL_WARMUP_URL`, `CACHE_WORKER_INTERVAL_SEC`, `CACHE_HARD_MAX_STALE_SEC`, `TARANTOOL_CACHE_HOST`, `TARANTOOL_CACHE_PORT` из `.env_backend`.
- Установите `VITE_FEATURE_DASHBOARD_CACHE=false` в `.env_frontend` при отключении кеширования.
- При включённом кешировании настройте `CACHE_HARD_MAX_STALE_SEC` (по умолчанию 900 секунд = 15 минут) в зависимости от допустимой задержки обновления данных на дашбордах.

### Модуль РСМ

- Если модуль РСМ не используется, удалите сервисы `rsm-module-api` и `rsm-module-ui` из `docker-compose.yml`, уберите переменные `MODULE_PRESET`, `RSM_MODULE_*` из `.env_backend` и удалите вход в реестр `:8126`.

### Резервное копирование

Настройте регулярное резервное копирование критических данных. Рекомендуемая частота — ежедневные полные бэкапы с хранением не менее 30 дней.

```bash
# Резервная копия MongoDB
docker compose exec mongo mongodump --out /data/db/backup_$(date +%Y%m%d)

# Резервная копия security log
docker cp grafinya-backend-1:/app-data/security/security.log ./backup/security_$(date +%Y%m%d).log

# Для PostgreSQL (Пульт)
pg_dump -h <HOST> -U pult_user pult_db > backup_pult_$(date +%Y%m%d).sql

# Для ClickHouse (Пульт)
clickhouse-client --query "BACKUP DATABASE pult_metrics TO Disk('backups', 'backup_$(date +%Y%m%d)')"
```

- Проверяйте восстанавливаемость резервных копий на тестовом стенде не реже одного раза в месяц
- Храните резервные копии на отдельном сервере или в облачном хранилище

### Настройка файрвола

```bash
# Разрешить только необходимые порты (пример для UFW)
sudo ufw allow 80/tcp      # Frontend HTTP
sudo ufw allow 443/tcp     # Frontend HTTPS
sudo ufw allow 5000/tcp    # Backend API (если нужен внешний доступ)
sudo ufw deny 27017/tcp    # MongoDB — только внутренний доступ
sudo ufw deny 3301/tcp     # Tarantool — только внутренний доступ
sudo ufw deny 8080:8087/tcp # Плагины — только внутренний доступ
sudo ufw enable
```

---

## 13. Troubleshooting

### Backend не запускается или падает с ошибкой

**Симптомы:** Контейнер `backend` перезапускается, в логах ошибки подключения к MongoDB.

**Решение:**

1. Проверьте, что MongoDB запущена и доступна:
   ```bash
   docker compose ps mongo
   docker compose logs mongo
   ```

2. Убедитесь, что `MONGO_URI` в `.env_backend` корректен и учётные данные совпадают с `.env_mongo`:
   ```bash
   # Проверьте подключение вручную
   docker compose exec mongo mongosh -u admin -p '<пароль>' --eval "db.runCommand({ping:1})"
   ```

3. Проверьте, что контейнер `backend` находится в той же Docker-сети, что и `mongo`:
   ```bash
   docker network inspect grafinya_grafinya
   ```

### Frontend не подключается к Backend API

**Симптомы:** Страница загружается, но данные не отображаются, в консоли браузера ошибки CORS или `ERR_CONNECTION_REFUSED`.

**Решение:**

1. Убедитесь, что `VITE_API_BASE_URL` в `.env_frontend` указывает на адрес, доступный из браузера пользователя (не `localhost`, если вы обращаетесь с другого компьютера)
2. Проверьте, что `ALLOWED_ORIGIN` в `.env_backend` совпадает с адресом, по которому пользователь открывает frontend
3. Проверьте доступность backend API:
   ```bash
   curl http://<HOST>:5000/healthz
   ```
4. После изменения `.env_frontend` необходимо пересоздать контейнер frontend:
   ```bash
   docker compose up -d --force-recreate frontend
   ```

### Плагины не подключаются

**Симптомы:** Backend показывает ошибки подключения к плагинам, дашборды не могут получить данные.

**Решение:**

1. Проверьте, что `PLUGIN_PRESET` в `.env_backend` совпадает с набором запущенных плагинов в `docker-compose.yml`
2. Убедитесь, что все плагины запущены:
   ```bash
   docker compose ps | grep plugin
   ```
3. Проверьте логи конкретного плагина:
   ```bash
   docker compose logs prometheus-plugin
   ```
4. Проверьте сетевую связность между backend и плагинами:
   ```bash
   docker compose exec backend wget -qO- http://prometheus-plugin:8080/health
   ```

### Ошибка аутентификации в Docker Registry

**Симптомы:** `docker compose pull` завершается с ошибкой `unauthorized` или `access denied`.

**Решение:**

1. Проверьте учётные данные:
   ```bash
   docker login registry.pult.chislitellab.ru:8124
   ```
2. Убедитесь, что у вашей учётной записи есть права на скачивание образов
3. Если используется модуль РСМ, выполните вход также в `registry.pult.chislitellab.ru:8126`
4. Проверьте, что Docker настроен на работу с приватным реестром (нет блокирующих прокси)

### Кеширование не работает

**Симптомы:** Дашборды загружаются медленно, при включённом `FEATURE_DASHBOARD_CACHE=true` данные не кешируются.

**Решение:**

1. Проверьте, что `tarantool-cache` и `cache-worker` запущены:
   ```bash
   docker compose ps tarantool-cache cache-worker
   ```
2. Проверьте логи cache-worker:
   ```bash
   docker compose logs cache-worker
   ```
3. Убедитесь, что `TARANTOOL_CACHE_HOST=tarantool-cache` и `TARANTOOL_CACHE_PORT=3301` корректны
4. Проверьте, что `VITE_FEATURE_DASHBOARD_CACHE=true` в `.env_frontend`

### Модуль РСМ недоступен

**Симптомы:** UI модуля РСМ не открывается по адресу `http://<HOST>:8202`, или API возвращает ошибки.

**Решение:**

1. Проверьте, что `rsm-module-api` и `rsm-module-ui` запущены:
   ```bash
   docker compose ps rsm-module-api rsm-module-ui
   ```
2. Убедитесь, что `FRONTEND_HOST` в `docker-compose.yml` для `rsm-module-api` указывает на внешний URL `rsm-module-ui`, доступный из браузера пользователя
3. Проверьте, что `RSM_MODULE_FRONTEND_HOST` в `.env_backend` корректен
4. Проверьте логи:
   ```bash
   docker compose logs rsm-module-api
   docker compose logs rsm-module-ui
   ```

---

## 14. Полезные ссылки

| Ресурс | URL |
|--------|-----|
| Сайт продукта Графиня | [chislitellab.ru/grafinya](https://chislitellab.ru/grafinya) |
| Документация Графини | [docs.pult.tech/grafinya/install](https://docs.pult.tech/grafinya/install) |
| Конструктор установки | [docs.pult.tech/constructor](https://docs.pult.tech/constructor) |
| Документация Пульт | [docs.pult.tech/docs/installation](https://docs.pult.tech/docs/installation/) |
| Сообщество | [chislitellab.ru](https://chislitellab.ru) |
| Личный кабинет | [chislitellab.ru](https://chislitellab.ru) |
| Релизы | [docs.pult.tech](https://docs.pult.tech) |
| Реестр образов (основной) | `registry.pult.chislitellab.ru:8124` |
| Реестр образов (РСМ) | `registry.pult.chislitellab.ru:8126` |

---

*Документ подготовлен на основе официальной документации платформы «Пульт» (ООО «Лаборатория Числитель"). Для получения актуальных инструкций всегда обращайтесь к [docs.pult.tech](https://docs.pult.tech).*

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram №1:** [@quadd4rv1n7](https://t.me/quadd4rv1n7)

📲 **Telegram №2:** [@dupley_maxim_1999](https://t.me/dupley_maxim_1999)

📅 **Дата:** 10.06.2026

▶️ **Версия 1.0**

```textline
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```

[![maestro7it_education](https://api.star-history.com/svg?repos=QuadDarv1ne/maestro7it_education&type=Date)](https://star-history.com/#QuadDarv1ne/maestro7it_education&Date)
