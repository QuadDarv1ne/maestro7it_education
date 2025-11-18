#!/usr/bin/env pwsh
# Скрипт для проверки здоровья приложения
# PowerShell версия для Windows

param(
    [string]$Url = "http://localhost:5000"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Simple HR - Health Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$endpoints = @(
    @{Name="Liveness";  Path="/health/live";   Description="Basic app availability"},
    @{Name="Health";    Path="/health";        Description="Application health"},
    @{Name="Readiness"; Path="/health/ready";  Description="Ready for requests"},
    @{Name="Metrics";   Path="/health/metrics"; Description="System metrics"}
)

$allHealthy = $true

foreach ($endpoint in $endpoints) {
    Write-Host "Checking $($endpoint.Name) ($($endpoint.Description))..." -NoNewline
    
    try {
        $response = Invoke-WebRequest -Uri "$Url$($endpoint.Path)" -Method Get -TimeoutSec 5 -UseBasicParsing
        
        if ($response.StatusCode -eq 200) {
            Write-Host " ✓ OK" -ForegroundColor Green
            
            # Показываем JSON ответ для метрик
            if ($endpoint.Name -eq "Metrics") {
                $json = $response.Content | ConvertFrom-Json
                Write-Host "  CPU: $($json.system.cpu_percent)% | Memory: $($json.system.memory_percent)% | Disk: $($json.system.disk_percent)%" -ForegroundColor Gray
            }
        } else {
            Write-Host " ✗ FAIL (Status: $($response.StatusCode))" -ForegroundColor Red
            $allHealthy = $false
        }
    }
    catch {
        Write-Host " ✗ ERROR" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Yellow
        $allHealthy = $false
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allHealthy) {
    Write-Host "✓ Application is HEALTHY" -ForegroundColor Green
    exit 0
} else {
    Write-Host "✗ Application has ISSUES" -ForegroundColor Red
    exit 1
}
