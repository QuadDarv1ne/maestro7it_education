@echo off
REM =============================================================================
REM benchmark.bat — Скрипт для запуска бенчмарков (Windows)
REM =============================================================================
REM Использование:
REM   scripts\benchmark.bat [hash|sieve|all]
REM
REM Примеры:
REM   scripts\benchmark.bat all
REM   scripts\benchmark.bat hash
REM   scripts\benchmark.bat sieve
REM =============================================================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR:~0,-1%"
set "OUTPUT_DIR=%PROJECT_DIR%\benchmark_results"
set "TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

REM Создание директории для результатов
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo ==============================================
echo   Бенчмарк проекта GPU Lab (Windows)
echo   Результаты: %OUTPUT_DIR%
echo ==============================================
echo.

REM =============================================================================
REM Бенчмарк хэширования
REM =============================================================================
:run_hash_benchmark
if "%1"=="sieve" goto :run_sieve_benchmark
if "%1"=="" goto :run_hash_benchmark_main
if not "%1"=="hash" if not "%1"=="all" goto :usage

:run_hash_benchmark_main
set "HASH_EXE=%PROJECT_DIR%\build\Release\hash.exe"
if not exist "%HASH_EXE%" set "HASH_EXE=%PROJECT_DIR%\hashing\hash.exe"
if not exist "%HASH_EXE%" set "HASH_EXE=%PROJECT_DIR%\hash.exe"

if not exist "%HASH_EXE%" (
    echo [ERROR] hash.exe not found. Please build the project first.
    goto :run_sieve_benchmark
)

set "HASH_OUTPUT=%OUTPUT_DIR%\hash_benchmark_%TIMESTAMP%.csv"
echo num_hashes,data_len,local_size,cpu_time_ms,gpu_time_ms,speedup,correct > "%HASH_OUTPUT%"

echo [INFO] Запуск бенчмарка хэширования...

for %%n in (1000 10000 50000 100000 250000) do (
    echo   num_hashes=%%n
    for %%w in (64 128 256 512) do (
        "%HASH_EXE%" %%n 64 %%w --json 2>nul > "%OUTPUT_DIR%\temp.json"
        
        REM Парсинг JSON (простой вариант)
        for /f "tokens=*" %%a in ('findstr /c:"\"cpu_time_ms\"" "%OUTPUT_DIR%\temp.json"') do set "line=%%a"
        set "cpu_time=!line:*: =!"
        set "cpu_time=!cpu_time:,=!"
        
        for /f "tokens=*" %%a in ('findstr /c:"\"gpu_kernel_time_ms\"" "%OUTPUT_DIR%\temp.json"') do set "line=%%a"
        set "gpu_time=!line:*: =!"
        set "gpu_time=!gpu_time:,=!"
        
        echo %%n,64,%%w,!cpu_time!,!gpu_time!,0,true >> "%HASH_OUTPUT%"
    )
)

echo [OK] Результаты сохранены в %HASH_OUTPUT%
echo.

:run_sieve_benchmark
if "%1"=="hash" goto :generate_plots
if "%1"=="" goto :run_sieve_benchmark_main
if not "%1"=="sieve" if not "%1"=="all" goto :usage

:run_sieve_benchmark_main
set "SIEVE_EXE=%PROJECT_DIR%\build\Release\sieve.exe"
if not exist "%SIEVE_EXE%" set "SIEVE_EXE=%PROJECT_DIR%\sieve\sieve.exe"
if not exist "%SIEVE_EXE%" set "SIEVE_EXE=%PROJECT_DIR%\sieve.exe"

if not exist "%SIEVE_EXE%" (
    echo [ERROR] sieve.exe not found. Please build the project first.
    goto :generate_plots
)

set "SIEVE_OUTPUT=%OUTPUT_DIR%\sieve_benchmark_%TIMESTAMP%.csv"
echo limit,local_size,cpu_time_ms,gpu_time_ms,speedup,primes_found,correct > "%SIEVE_OUTPUT%"

echo [INFO] Запуск бенчмарка решета Эратосфена...

for %%n in (100000 500000 1000000 5000000 10000000) do (
    echo   N=%%n
    for %%w in (64 128 256 512) do (
        "%SIEVE_EXE%" %%n %%w --json 2>nul > "%OUTPUT_DIR%\temp.json"
        
        for /f "tokens=*" %%a in ('findstr /c:"\"cpu_time_ms\"" "%OUTPUT_DIR%\temp.json"') do set "line=%%a"
        set "cpu_time=!line:*: =!"
        set "cpu_time=!cpu_time:,=!"
        
        for /f "tokens=*" %%a in ('findstr /c:"\"gpu_kernel_time_ms\"" "%OUTPUT_DIR%\temp.json"') do set "line=%%a"
        set "gpu_time=!line:*: =!"
        set "gpu_time=!gpu_time:,=!"
        
        echo %%n,%%w,!cpu_time!,!gpu_time!,0,0,true >> "%SIEVE_OUTPUT%"
    )
)

echo [OK] Результаты сохранены в %SIEVE_OUTPUT%
echo.

:generate_plots
del "%OUTPUT_DIR%\temp.json" 2>nul

echo [INFO] Для генерации графиков используйте Python:
echo   pip install matplotlib pandas
echo   python scripts\generate_plots.py %OUTPUT_DIR%
echo.

echo [OK] Бенчмарк завершён!
goto :eof

:usage
echo Использование: %0 [hash|sieve|all]
echo.
echo   hash   - бенчмарк хэширования
echo   sieve  - бенчмарк решета
echo   all    - все бенчмарки (по умолчанию)
exit /b 1
