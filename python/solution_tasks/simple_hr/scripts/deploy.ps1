#!/usr/bin/env pwsh
# Скрипт для деплоя приложения
# PowerShell версия для Windows

param(
    [ValidateSet('dev', 'staging', 'production')]
    [string]$Environment = 'dev',
    
    [switch]$SkipTests = $false,
    [switch]$SkipBackup = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Simple HR - Deployment Script" -ForegroundColor Cyan
Write-Host "  Environment: $Environment" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Функция для логирования
function Write-Step {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message" -ForegroundColor Green
}

function Write-Error-Step {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERROR: $Message" -ForegroundColor Red
}

# 1. Проверка окружения
Write-Step "Step 1/8: Checking environment..."

if (-not (Test-Path ".env")) {
    Write-Error-Step ".env file not found!"
    exit 1
}

if (-not (Test-Path "venv")) {
    Write-Error-Step "Virtual environment not found! Run: python -m venv venv"
    exit 1
}

# 2. Активация виртуального окружения
Write-Step "Step 2/8: Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"

# 3. Обновление зависимостей
Write-Step "Step 3/8: Installing/updating dependencies..."
pip install -r requirements.txt --quiet

# 4. Бэкап базы данных (если не пропущено)
if (-not $SkipBackup -and $Environment -ne 'dev') {
    Write-Step "Step 4/8: Creating database backup..."
    python scripts/backup.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Step "Backup failed!"
        exit 1
    }
} else {
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Step 4/8: Skipping backup..." -ForegroundColor Yellow
}

# 5. Запуск тестов (если не пропущено)
if (-not $SkipTests) {
    Write-Step "Step 5/8: Running tests..."
    pytest -v --tb=short -x
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Step "Tests failed! Deployment aborted."
        exit 1
    }
} else {
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Step 5/8: Skipping tests..." -ForegroundColor Yellow
}

# 6. Применение миграций
Write-Step "Step 6/8: Applying database migrations..."
flask db upgrade
if ($LASTEXITCODE -ne 0) {
    Write-Error-Step "Database migration failed!"
    exit 1
}

# 7. Сборка статики (если есть)
Write-Step "Step 7/8: Building static assets..."
if (Test-Path "static") {
    Write-Host "  Static files ready" -ForegroundColor Gray
}

# 8. Перезапуск приложения
Write-Step "Step 8/8: Restarting application..."

if ($Environment -eq 'dev') {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "✓ Deployment complete!" -ForegroundColor Green
    Write-Host "Starting development server..." -ForegroundColor Yellow
    Write-Host ""
    python run.py
} else {
    # Production/Staging
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "✓ Deployment complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "For production, use:" -ForegroundColor Yellow
    Write-Host "  gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'" -ForegroundColor Cyan
    Write-Host "or start Docker container:" -ForegroundColor Yellow
    Write-Host "  docker-compose up -d" -ForegroundColor Cyan
}

Write-Host "========================================" -ForegroundColor Cyan
