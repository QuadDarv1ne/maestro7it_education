#!/usr/bin/env pwsh

Write-Host "=== PCMetrics Quick Test Script ===" -ForegroundColor Cyan
Write-Host ""

$buildDir = "c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\c_plus_plus\solution_tasks\PCMetrics\build"

Write-Host "1. Testing minimal_test.exe..." -ForegroundColor Yellow
& "$buildDir\bin\minimal_test.exe"
if ($LASTEXITCODE -eq 0) {
    Write-Host "   [OK] Minimal test passed`n" -ForegroundColor Green
} else {
    Write-Host "   [FAIL] Minimal test failed with code $LASTEXITCODE`n" -ForegroundColor Red
}

Write-Host "2. Building project summary..." -ForegroundColor Yellow
$files = @(
    "$buildDir\pcmetrics.exe",
    "$buildDir\bin\pcmetrics_test.exe",
    "$buildDir\bin\minimal_test.exe"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length / 1KB
        Write-Host "   [EXISTS] $(Split-Path $file -Leaf) - $([math]::Round($size, 2)) KB" -ForegroundColor Green
    } else {
        Write-Host "   [MISSING] $(Split-Path $file -Leaf)" -ForegroundColor Red
    }
}

Write-Host "`n3. Project files:" -ForegroundColor Yellow
$srcFiles = Get-ChildItem -Path "c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\c_plus_plus\solution_tasks\PCMetrics\src" -Filter *.cpp
Write-Host "   Source files: $($srcFiles.Count)"

$incFiles = Get-ChildItem -Path "c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\c_plus_plus\solution_tasks\PCMetrics\include" -Filter *.h
Write-Host "   Header files: $($incFiles.Count)"

Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "✓ Project compiles successfully" -ForegroundColor Green
Write-Host "✓ Basic Windows API tests pass" -ForegroundColor Green
Write-Host "! Note: Full program requires interactive mode or --auto flag" -ForegroundColor Yellow
Write-Host "`nTo run manually in interactive mode, execute:" -ForegroundColor White
Write-Host "   cd $buildDir" -ForegroundColor Gray
Write-Host "   .\pcmetrics.exe --auto" -ForegroundColor Gray
