# Структура проекта Chess Calendar RU

## Обзор структуры

```
ChessCalendar-RU/
├── .github/                    # GitHub конфигурация
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
│
├── app/                        # Основное приложение
│   ├── models/                # Модели данных
│   ├── utils/                 # Утилиты
│   │   ├── cache_manager.py  # Многоуровневое кэширование
│   │   ├── cache.py           # Базовый кэш
│   │   └── ...
│   ├── views/                 # Views (контроллеры)
│   ├── tasks/                 # Celery задачи
│   │   ├── parser_tasks.py   # Парсинг турниров
│   │   ├── notification_tasks.py
│   │   ├── analytics_tasks.py
│   │   └── maintenance_tasks.py
│   ├── celery_app.py          # Конфигурация Celery
│   └── __init__.py
│
├── services/                   # Микросервисы
│   ├── api-gateway/           # API Gateway
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── tournament-service/
│   ├── user-service/
│   ├── parser-service/
│   ├── notification-service/
│   ├── recommendation-service/
│   ├── favorites-service/
│   ├── calendar-service/
│   ├── image-optimization-service/
│   └── cdn-service/
│
├── scripts/                    # Скрипты
│   ├── deployment/            # Развертывание
│   │   ├── deploy-production.sh
│   │   └── rollback.sh
│   ├── maintenance/           # Обслуживание
│   │   ├── backup.sh
│   │   ├── health-check.sh
│   │   └── monitor.sh
│   ├── start-all.sh           # Запуск (Linux/Mac)
│   ├── start-all.bat          # Запуск (Windows)
│   ├── dev-setup.sh           # Настройка dev окружения
│   └── test.sh                # Запуск тестов
│
├── docs/                       # Документация
│   ├── ARCHITECTURE.md        # Архитектура
│   ├── QUICK_START.md         # Быстрый старт
│   ├── DEPLOYMENT.md          # Развертывание
│   ├── MONITORING.md          # Мониторинг
│   ├── PROJECT_STRUCTURE.md   # Этот файл
│   └── ...
│
├── monitoring/                 # Конфигурация мониторинга
│   ├── prometheus.yml         # Prometheus config
│   ├── alerts/                # Правила алертов
│   │   ├── api-alerts.yml
│   │   └── system-alerts.yml
│   └── grafana/
│       └── dashboards/
│           └── overview.json
│
├── templates/                  # HTML шаблоны
├── static/                     # Статические файлы
├── tests/                      # Тесты
├── logs/                       # Логи
├── backups/                    # Резервные копии
├── instance/                   # Данные приложения
│
├── docker-compose.yml          # Docker Compose (основной)
├── docker-compose.monitoring.yml  # Мониторинг
├── Dockerfile                  # Docker образ приложения
├── Makefile                    # Команды для разработки
├── requirements.txt            # Python зависимости
├── .env.example                # Шаблон переменных окружения
├── .gitignore                  # Git ignore
├── config.py                   # Конфигурация
├── manage.py                   # Скрипт управления
├── run.py                      # Запуск приложения
└── README.md                   # Основной README
```

## Описание директорий

### `/app` - Основное приложение

Содержит весь код основного приложения Flask.

#### `/app/models`
Модели данных (SQLAlchemy):
- `tournament.py` - Турниры
- `user.py` - Пользователи
- `notification.py` - Уведомления
- `favorite.py` - Избранное
- `rating.py` - Рейтинги
- И другие...

#### `/app/utils`
Утилиты и вспомогательные функции:
- `cache_manager.py` - Многоуровневое кэширование (NEW)
- `cache.py` - Базовый кэш
- `fide_parser.py` - Парсер FIDE
- `cfr_parser.py` - Парсер CFR
- `notifications.py` - Система уведомлений
- `recommendations.py` - Рекомендации
- `analytics.py` - Аналитика
- `backup.py` - Резервное копирование
- И другие...

#### `/app/views`
Views (контроллеры):
- `main.py` - Основные маршруты
- `admin.py` - Админ панель
- `user.py` - Пользовательские маршруты
- `api.py` - API эндпоинты
- `forum.py` - Форум
- `api_docs.py` - API документация

#### `/app/tasks` (NEW)
Celery задачи для асинхронной обработки:
- `parser_tasks.py` - Парсинг турниров
- `notification_tasks.py` - Отправка уведомлений
- `analytics_tasks.py` - Генерация аналитики
- `maintenance_tasks.py` - Обслуживание системы

### `/services` - Микросервисы

Независимые микросервисы с собственными Docker образами.

#### `/services/api-gateway` (NEW)
Единая точка входа:
- JWT аутентификация
- Rate limiting
- Маршрутизация к микросервисам
- Кэширование ответов
- Health checks

#### Другие сервисы
- `tournament-service` - Управление турнирами
- `user-service` - Управление пользователями
- `parser-service` - Парсинг данных
- `notification-service` - Уведомления
- `recommendation-service` - Рекомендации
- `favorites-service` - Избранное
- `calendar-service` - Календари
- `image-optimization-service` - Оптимизация изображений
- `cdn-service` - CDN интеграция

### `/scripts` (NEW)
Скрипты для автоматизации.

#### `/scripts/deployment`
Скрипты развертывания:
- `deploy-production.sh` - Production развертывание
- `rollback.sh` - Откат к предыдущей версии

#### `/scripts/maintenance`
Скрипты обслуживания:
- `backup.sh` - Автоматическое резервное копирование
- `health-check.sh` - Проверка здоровья системы
- `monitor.sh` - Real-time мониторинг

#### Корневые скрипты
- `start-all.sh` / `start-all.bat` - Быстрый запуск
- `dev-setup.sh` - Настройка dev окружения
- `test.sh` - Запуск тестов

### `/docs` (NEW)
Документация проекта.

- `ARCHITECTURE.md` - Подробная архитектура
- `QUICK_START.md` - Быстрый старт с примерами
- `DEPLOYMENT.md` - Руководство по развертыванию
- `MONITORING.md` - Настройка мониторинга
- `PROJECT_STRUCTURE.md` - Этот файл
- `CHANGELOG_ARCHITECTURE.md` - История изменений
- `IMPROVEMENTS_SUMMARY.md` - Резюме улучшений

### `/monitoring` (NEW)
Конфигурация мониторинга.

#### `/monitoring/alerts`
Правила алертов для Prometheus:
- `api-alerts.yml` - Алерты API
- `system-alerts.yml` - Системные алерты

#### `/monitoring/grafana`
Конфигурация Grafana:
- `dashboards/` - Дашборды

### `/templates`
HTML шаблоны Jinja2 для веб-интерфейса.

### `/static`
Статические файлы (CSS, JS, изображения).

### `/tests`
Тесты приложения (pytest).

## Конфигурационные файлы

### Docker
- `Dockerfile` - Образ основного приложения
- `docker-compose.yml` - Основные сервисы
- `docker-compose.monitoring.yml` - Мониторинг

### Python
- `requirements.txt` - Зависимости
- `config.py` - Конфигурация приложения
- `manage.py` - CLI для управления
- `run.py` - Точка входа

### CI/CD
- `.github/workflows/ci.yml` - GitHub Actions pipeline

### Разработка
- `Makefile` - Команды для разработки
- `.env.example` - Шаблон переменных окружения
- `.gitignore` - Игнорируемые файлы

## Файлы данных

### `/instance`
Данные приложения (SQLite базы данных).

### `/logs`
Логи приложения.

### `/backups`
Резервные копии базы данных.

### `/data`
Данные микросервисов:
- `/data/tournaments` - Данные tournament-service
- `/data/users` - Данные user-service

## Порты сервисов

| Сервис | Порт | Описание |
|--------|------|----------|
| API Gateway | 5000 | Единая точка входа |
| Tournament Service | 5001 | Управление турнирами |
| User Service | 5002 | Управление пользователями |
| Parser Service | 5003 | Парсинг данных |
| CDN Service | 5004 | CDN интеграция |
| Image Service | 5005 | Оптимизация изображений |
| Calendar Service | 5006 | Календари |
| Notification Service | 5007 | Уведомления |
| Recommendation Service | 5008 | Рекомендации |
| Favorites Service | 5009 | Избранное |
| Flower | 5555 | Мониторинг Celery |
| Redis | 6379 | Кэш и брокер |
| Nginx | 80, 443 | Reverse proxy |
| Prometheus | 9090 | Сбор метрик |
| Grafana | 3000 | Визуализация |
| Alertmanager | 9093 | Управление алертами |
| cAdvisor | 8080 | Метрики контейнеров |

## Зависимости между компонентами

```
┌─────────────┐
│   Клиент    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │ ◄── JWT, Rate Limiting
│   (Port 5000)   │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┬─────────┐
    ▼         ▼        ▼          ▼         ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌────────┐ ┌──────┐
│Tourna- │ │User  │ │Parser│ │Notifi- │ │ ... │
│ment    │ │Service│ │Service│ │cation  │ │     │
│Service │ │      │ │      │ │Service │ │     │
└────┬───┘ └───┬──┘ └───┬──┘ └────┬───┘ └──┬───┘
     │         │        │         │        │
     └─────────┴────────┴─────────┴────────┘
                        │
                        ▼
               ┌────────────────┐
               │     Redis      │ ◄── Кэш + Брокер
               └────────┬───────┘
                        │
                        ▼
               ┌────────────────┐
               │  Celery Worker │ ◄── Async Tasks
               └────────────────┘
                        │
                        ▼
               ┌────────────────┐
               │   PostgreSQL   │ ◄── База данных
               └────────────────┘
```

## Workflow разработки

### 1. Настройка окружения
```bash
./scripts/dev-setup.sh
```

### 2. Разработка
```bash
# Активация venv
source venv/bin/activate

# Запуск в dev режиме
python run.py
```

### 3. Тестирование
```bash
make test
make lint
```

### 4. Коммит
```bash
git add .
git commit -m "Feature: ..."
# Pre-commit hooks запустятся автоматически
```

### 5. Push и CI/CD
```bash
git push origin develop
# GitHub Actions запустит CI pipeline
```

### 6. Развертывание
```bash
make deploy
# или
./scripts/deployment/deploy-production.sh
```

## Полезные команды

См. `Makefile` для полного списка команд:

```bash
make help           # Показать все команды
make start          # Запустить сервисы
make stop           # Остановить сервисы
make logs           # Показать логи
make test           # Запустить тесты
make health         # Проверка здоровья
make backup         # Создать бэкап
make deploy         # Развернуть в production
```

## Дополнительная информация

- [ARCHITECTURE.md](ARCHITECTURE.md) - Подробная архитектура
- [QUICK_START.md](QUICK_START.md) - Быстрый старт
- [DEPLOYMENT.md](DEPLOYMENT.md) - Развертывание
- [MONITORING.md](MONITORING.md) - Мониторинг
