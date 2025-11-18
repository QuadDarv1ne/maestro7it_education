#!/usr/bin/env pwsh
# Скрипт для запуска полного набора тестов
# PowerShell версия для Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Simple HR - Test Runner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Проверка виртуального окружения
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Активация виртуального окружения
Write-Host "[1/5] Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Проверка установленных пакетов
Write-Host "[2/5] Checking dependencies..." -ForegroundColor Green
$pytest = Get-Command pytest -ErrorAction SilentlyContinue
if (-not $pytest) {
    Write-Host "pytest not found. Installing test dependencies..." -ForegroundColor Yellow
    pip install pytest pytest-cov pytest-flask coverage
}

# Очистка предыдущих результатов
Write-Host "[3/5] Cleaning previous test results..." -ForegroundColor Green
if (Test-Path "htmlcov") { Remove-Item -Recurse -Force "htmlcov" }
if (Test-Path ".coverage") { Remove-Item -Force ".coverage" }
if (Test-Path "coverage.xml") { Remove-Item -Force "coverage.xml" }
if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force ".pytest_cache" }

# Запуск тестов с покрытием
Write-Host "[4/5] Running tests with coverage..." -ForegroundColor Green
Write-Host ""
pytest -v --tb=short --cov=app --cov-report=html --cov-report=term-missing --cov-report=xml

$exitCode = $LASTEXITCODE

# Отображение результатов
Write-Host ""
Write-Host "[5/5] Test Summary" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

if ($exitCode -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Coverage report: htmlcov\index.html" -ForegroundColor Cyan
    
    # Опционально: открыть отчет в браузере
    $openReport = Read-Host "Open coverage report in browser? (y/n)"
    if ($openReport -eq 'y') {
        Start-Process "htmlcov\index.html"
    }
} else {
    Write-Host "✗ Some tests failed!" -ForegroundColor Red
    Write-Host "Please review the output above." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan

exit $exitCode
