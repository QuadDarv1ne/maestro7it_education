# Makefile для Simple HR

.PHONY: help install test run clean docker-build docker-up docker-down migrate backup

help:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║          Simple HR - Makefile команды (v2.4)               ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 Установка и окружение:"
	@echo "  make install       - Установить зависимости"
	@echo "  make dev-install   - Установить зависимости + dev tools"
	@echo "  make clean         - Очистить временные файлы"
	@echo ""
	@echo "🧪 Тестирование:"
	@echo "  make test          - Запустить все тесты"
	@echo "  make test-unit     - Запустить только unit тесты"
	@echo "  make test-api      - Запустить API тесты"
	@echo "  make coverage      - Запустить тесты с покрытием"
	@echo ""
	@echo "🎨 Качество кода:"
	@echo "  make lint          - Проверить код (ruff)"
	@echo "  make format        - Форматировать код (black, isort)"
	@echo "  make type-check    - Проверка типов (mypy)"
	@echo "  make quality       - Все проверки качества"
	@echo ""
	@echo "🚀 Запуск приложения:"
	@echo "  make run           - Запустить production"
	@echo "  make dev           - Запустить в режиме разработки"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  make docker-build  - Собрать Docker образ"
	@echo "  make docker-up     - Запустить контейнеры"
	@echo "  make docker-down   - Остановить контейнеры"
	@echo "  make docker-logs   - Просмотр логов"
	@echo ""
	@echo "🗄️  База данных:"
	@echo "  make migrate       - Выполнить миграции БД"
	@echo "  make migrate-init  - Инициализировать миграции"
	@echo "  make migrate-create - Создать новую миграцию"
	@echo "  make backup        - Создать резервную копию БД"
	@echo "  make init-db       - Инициализировать БД"
	@echo "  make seed-db       - Заполнить БД тестовыми данными"
	@echo ""
	@echo "📊 Утилиты:"
	@echo "  make shell         - Flask shell"
	@echo "  make stats         - Статистика БД"
	@echo "  make create-user   - Создать пользователя"
	@echo "  make requirements  - Обновить requirements.txt"
	@echo "  make security-check - Проверка безопасности"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest -v

test-unit:
	pytest -v -m unit

test-api:
	pytest -v -m api

coverage:
	pytest --cov=app --cov-report=html --cov-report=term-missing

lint:
	ruff check app/

format:
	black app/
	isort app/

type-check:
	mypy app/ --ignore-missing-imports

quality: lint type-check

run:
	python run.py

dev:
	set FLASK_ENV=development && python -m flask run --reload

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf *.egg-info/
	rm -rf dist/
	rm -rf build/

lint:
	flake8 app --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 app --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black app/
	isort app/

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

migrate:
	flask db upgrade

migrate-init:
	flask db init

migrate-create:
	flask db migrate -m "$(message)"

backup:
	python -c "from app.utils.backup import backup_database; backup_database()"

init-db:
	flask cli init-db

seed-db:
	flask cli seed-db

create-user:
	flask cli create-user

stats:
	flask cli stats

requirements:
	pip freeze > requirements.txt

security-check:
	safety check
	bandit -r app

shell:
	flask shell
