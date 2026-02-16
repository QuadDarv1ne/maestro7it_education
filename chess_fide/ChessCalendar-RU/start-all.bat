@echo off
REM Скрипт для быстрого запуска всей инфраструктуры Chess Calendar RU (Windows)

echo 🚀 Запуск Chess Calendar RU...

REM Проверка наличия .env файла
if not exist .env (
    echo ⚠️  Файл .env не найден. Создаю из .env.example...
    copy .env.example .env
    echo ✅ Файл .env создан. Пожалуйста, отредактируйте его перед запуском.
    echo    Минимум измените SECRET_KEY!
    pause
    exit /b 1
)

REM Создание необходимых директорий
echo 📁 Создание директорий...
if not exist logs mkdir logs
if not exist backups mkdir backups
if not exist data\tournaments mkdir data\tournaments
if not exist data\users mkdir data\users

REM Остановка существующих контейнеров
echo 🛑 Остановка существующих контейнеров...
docker-compose down

REM Сборка образов
echo 🔨 Сборка Docker образов...
docker-compose build

REM Запуск сервисов
echo ▶️  Запуск сервисов...
docker-compose up -d

REM Ожидание запуска
echo ⏳ Ожидание запуска сервисов...
timeout /t 15 /nobreak

REM Проверка статуса
echo 📊 Проверка статуса сервисов...
docker-compose ps

echo.
echo 🎉 Запуск завершен!
echo.
echo 📍 Доступные сервисы:
echo    - API Gateway: http://localhost:5000
echo    - Flower (Celery): http://localhost:5555
echo    - Tournament Service: http://localhost:5001
echo    - User Service: http://localhost:5002
echo.
echo 📚 Документация:
echo    - Архитектура: ARCHITECTURE.md
echo    - Быстрый старт: QUICK_START.md
echo.
echo 🔧 Полезные команды:
echo    - Просмотр логов: docker-compose logs -f
echo    - Остановка: docker-compose down
echo    - Перезапуск: docker-compose restart
echo.
echo 👤 Создание администратора:
echo    docker-compose exec api-gateway python manage.py --action create-admin ^
echo      --username admin --email admin@example.com --password YourPassword
echo.
pause
