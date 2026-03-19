#!/usr/bin/env pwsh
# =============================================================================
# GPU Lab Clean Script - Очистка от мусора (с сохранением .exe файлов)
# =============================================================================
# Использование:
#   ./clean.ps1 [--dry-run]
#
# Опции:
#   --dry-run    Показать, что будет удалено, но не удалять
# =============================================================================

param(
    [switch]$DryRun
)

$ProjectDir = Split-Path -Parent $PSScriptRoot
if ($PSScriptRoot -match 'scripts$') {
    $ProjectDir = Split-Path -Parent $PSScriptRoot
}

Write-Host "========================================" -ForegroundColor Blue
Write-Host "GPU Lab Clean" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host "Project: $ProjectDir"
if ($DryRun) {
    Write-Host "Mode: DRY-RUN (no files will be deleted)" -ForegroundColor Yellow
} else {
    Write-Host "Mode: CLEAN" -ForegroundColor Green
}
Write-Host "========================================"
Write-Host ""

$DeletedCount = 0

# Extensions to delete
$Extensions = @('o', 'obj', 'a', 'lib', 'so', 'dll', 'dylib', 'gcda', 'gcno', 'gcov', 'log', 'tmp', 'temp', 'bak', 'swp', 'swn', 'swo', 'pdb', 'pyc', 'pyo')

Write-Host "Cleaning files by extension..." -ForegroundColor Cyan

foreach ($ext in $Extensions) {
    $Files = Get-ChildItem -Path $ProjectDir -Recurse -Filter "*.$ext" -File -ErrorAction SilentlyContinue
    foreach ($file in $Files) {
        if ($DryRun) {
            Write-Host "[SKIP] $($file.FullName)" -ForegroundColor Yellow
            $DeletedCount++
        } else {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
            Write-Host "[DEL] $($file.FullName)" -ForegroundColor Green
            $DeletedCount++
        }
    }
}

# Directories to delete
$Dirs = @('CMakeFiles', '_CPack_Packages', 'Testing', 'test_results', 'benchmark_results', 'bin', 'obj', 'CMakeTmp', '__pycache__')

Write-Host ""
Write-Host "Cleaning directories..." -ForegroundColor Cyan

foreach ($dir in $Dirs) {
    $FullPath = Join-Path $ProjectDir $dir
    if (Test-Path $FullPath -PathType Container) {
        if ($DryRun) {
            Write-Host "[SKIP DIR] $dir" -ForegroundColor Yellow
            $DeletedCount++
        } else {
            Remove-Item -Path $FullPath -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "[DEL DIR] $dir" -ForegroundColor Green
            $DeletedCount++
        }
    }
}

# CMake files in root
$CMakeFiles = @('CMakeCache.txt', 'cmake_install.cmake', 'Makefile', 'compile_commands.json')

Write-Host ""
Write-Host "Cleaning CMake files..." -ForegroundColor Cyan

foreach ($file in $CMakeFiles) {
    $FullPath = Join-Path $ProjectDir $file
    if (Test-Path $FullPath -PathType Leaf) {
        if ($DryRun) {
            Write-Host "[SKIP] $file" -ForegroundColor Yellow
            $DeletedCount++
        } else {
            Remove-Item -Path $FullPath -Force -ErrorAction SilentlyContinue
            Write-Host "[DEL] $file" -ForegroundColor Green
            $DeletedCount++
        }
    }
}

# Preserved files (.exe)
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "PRESERVED (.exe files):" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$ExeFiles = Get-ChildItem -Path $ProjectDir -Recurse -Filter "*.exe" -File -ErrorAction SilentlyContinue
foreach ($exe in $ExeFiles) {
    Write-Host "[KEEP] $($exe.FullName)" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "Total items: $DeletedCount" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue

if ($DryRun) {
    Write-Host ""
    Write-Host "Run without --dry-run to actually delete files" -ForegroundColor Yellow
}

Write-Host ""
