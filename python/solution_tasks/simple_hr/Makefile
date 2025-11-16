# Makefile для Simple HR

.PHONY: help install test run clean docker-build docker-up docker-down migrate backup

help:
	@echo "Simple HR - Makefile команды"
	@echo ""
	@echo "Доступные команды:"
	@echo "  make install       - Установить зависимости"
	@echo "  make test          - Запустить тесты"
	@echo "  make coverage      - Запустить тесты с покрытием"
	@echo "  make run           - Запустить приложение"
	@echo "  make dev           - Запустить в режиме разработки"
	@echo "  make clean         - Очистить временные файлы"
	@echo "  make lint          - Проверить код с помощью flake8"
	@echo "  make format        - Форматировать код с помощью black"
	@echo "  make docker-build  - Собрать Docker образ"
	@echo "  make docker-up     - Запустить Docker контейнеры"
	@echo "  make docker-down   - Остановить Docker контейнеры"
	@echo "  make migrate       - Выполнить миграции БД"
	@echo "  make backup        - Создать резервную копию БД"
	@echo "  make init-db       - Инициализировать БД"
	@echo "  make seed-db       - Заполнить БД тестовыми данными"

install:
	pip install -r requirements.txt

test:
	pytest -v

coverage:
	pytest --cov=app --cov-report=html --cov-report=term

run:
	python run.py

dev:
	export FLASK_ENV=development && flask run --reload

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
