@echo off
REM Скрипт установки инструментов качества кода

echo ========================================
echo Установка инструментов качества кода
echo ========================================

echo.
echo [1/4] Установка зависимостей...
pip install -r config/requirements.txt

echo.
echo [2/4] Установка pre-commit hooks...
pre-commit install

echo.
echo [3/4] Запуск pre-commit на всех файлах...
pre-commit run --all-files

echo.
echo [4/4] Создание первой миграции Alembic...
alembic revision --autogenerate -m "Initial migration"

echo.
echo ========================================
echo Установка завершена!
echo ========================================
echo.
echo Доступные команды:
echo   pre-commit run --all-files  - Запустить все проверки
echo   pytest --cov=app            - Запустить тесты с coverage
echo   alembic upgrade head        - Применить миграции
echo   alembic history             - История миграций
echo.

pause
