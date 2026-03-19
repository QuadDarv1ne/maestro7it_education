@echo off
REM Stress test script for sieve
REM Запускает тесты с разными N и собирает результаты

echo ========================================
echo Stress Test: Sieve of Eratosthenes
echo ========================================
echo.

set RESULTS_FILE=results.csv
echo N,CPU_time_ms,GPU_kernel_ms,GPU_total_ms,CPU_count,GPU_count,Speedup,Correct > %RESULTS_FILE%

set TEST_VALUES=1000 10000 100000 500000 1000000 2000000 5000000 10000000

echo Running tests...
echo.

for %%N in (%TEST_VALUES%) do (
    echo Testing N=%%N...
    .\sieve.exe %%N --json --no-info >> test_output.txt 2>&1
    
    REM Извлекаем данные из JSON (упрощенно)
    for /f "tokens=2 delims=:" %%A in ('findstr "\"limit\"" test_output.txt') do set N_OUT=%%A
    for /f "tokens=2 delims=:" %%A in ('findstr "\"time_ms\"" test_output.txt') do set CPU_TIME=%%A
    for /f "tokens=2 delims=:" %%A in ('findstr "\"kernel_time_ms\"" test_output.txt') do set GPU_KERNEL=%%A
    for /f "tokens=2 delims=:" %%A in ('findstr "\"total_time_ms\"" test_output.txt') do set GPU_TOTAL=%%A
    for /f "tokens=2 delims=:" %%A in ('findstr "\"count\":" test_output.txt ^| findstr /v "gpu" ^| findstr /v "cpu"') do set CPU_COUNT=%%A
    for /f "tokens=2 delims=:" %%A in ('findstr "\"count\":" test_output.txt ^| findstr "gpu"') do set GPU_COUNT=%%A
    for /f "tokens=2 delims=:" %%A in ('findstr "\"speedup\"" test_output.txt') do set SPEEDUP=%%A
    for /f "tokens=2 delims=:" %%A in ('findstr "\"correct\"" test_output.txt') do set CORRECT=%%A
    
    echo %N%,%CPU_TIME%,%GPU_KERNEL%,%GPU_TOTAL%,%CPU_COUNT%,%GPU_COUNT%,%SPEEDUP%,%CORRECT% >> %RESULTS_FILE%
    
    del test_output.txt
)

echo.
echo Results saved to %RESULTS_FILE%
echo.
type %RESULTS_FILE%
