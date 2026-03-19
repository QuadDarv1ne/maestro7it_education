@echo off
REM =============================================================================
REM Скрипт автоматической сборки, тестирования и бенчмарка проекта GPU Lab
REM =============================================================================
REM Использование:
REM   build_and_test.bat [опции]
REM
REM Опции:
REM   -c, --clean       Очистить сборку перед сборкой
REM   -d, --debug       Debug сборка (по умолчанию Release)
REM   -t, --test        Запустить тесты (по умолчанию да)
REM   -b, --benchmark   Запустить бенчмарки
REM   -h, --help        Показать эту справку
REM =============================================================================

setlocal enabledelayedexpansion

REM Переменные
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR:~0,-1%
set BUILD_DIR=%PROJECT_DIR%\build
set CLEAN_BUILD=false
set RUN_TESTS=true
set RUN_BENCHMARKS=false
set BUILD_TYPE=Release

REM =============================================================================
REM Парсинг аргументов
REM =============================================================================

:parse_args
if "%~1"=="" goto :main
if /i "%~1"=="-c" set CLEAN_BUILD=true & shift & goto :parse_args
if /i "%~1"=="--clean" set CLEAN_BUILD=true & shift & goto :parse_args
if /i "%~1"=="-d" set BUILD_TYPE=Debug & shift & goto :parse_args
if /i "%~1"=="--debug" set BUILD_TYPE=Debug & shift & goto :parse_args
if /i "%~1"=="-t" set RUN_TESTS=true & shift & goto :parse_args
if /i "%~1"=="--test" set RUN_TESTS=true & shift & goto :parse_args
if /i "%~1"=="-b" set RUN_BENCHMARKS=true & shift & goto :parse_args
if /i "%~1"=="--benchmark" set RUN_BENCHMARKS=true & shift & goto :parse_args
if /i "%~1"=="-h" goto :help
if /i "%~1"=="--help" goto :help
echo Неизвестная опция: %~1
goto :help

:help
echo.
echo GPU Lab - Сборка и тесты
echo.
echo Использование: build_and_test.bat [опции]
echo.
echo Опции:
echo   -c, --clean       Очистить сборку
echo   -d, --debug       Debug сборка
echo   -t, --test        Запустить тесты
echo   -b, --benchmark   Запустить бенчмарки
echo   -h, --help        Эта справка
echo.
echo Примеры:
echo   build_and_test.bat              Сборка + тесты
echo   build_and_test.bat -c -b        Очистка + сборка + бенчмарки
echo   build_and_test.bat --debug      Debug сборка + тесты
echo.
goto :eof

:main
REM =============================================================================
REM Основной процесс
REM =============================================================================

echo.
echo ========================================
echo GPU Lab - Автоматическая сборка и тесты
echo ========================================
echo.
echo Проект: %PROJECT_DIR%
echo Сборка: %BUILD_DIR%
echo Тип:    %BUILD_TYPE%
echo.

if "%CLEAN_BUILD%"=="true" (
    call :clean_build
)

call :configure
if %errorlevel% neq 0 goto :error

call :build
if %errorlevel% neq 0 goto :error

if "%RUN_TESTS%"=="true" (
    call :run_tests
)

if "%RUN_BENCHMARKS%"=="true" (
    call :run_benchmarks
)

call :summary

echo.
echo ========================================
echo Все операции завершены успешно!
echo ========================================
goto :eof

:error
echo.
echo ========================================
echo ОШИБКА сборки!
echo ========================================
exit /b 1

REM =============================================================================
REM Функции
REM =============================================================================

:clean_build
echo.
echo ========================================
echo Очистка сборки
echo ========================================
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
    echo [OK] Директория build удалена
) else (
    echo [INFO] Директория build не существует
)
goto :eof

:configure
echo.
echo ========================================
echo Конфигурация проекта (CMake)
echo ========================================
cd /d "%PROJECT_DIR%"
cmake -S . -B "%BUILD_DIR%" ^
    -DCMAKE_BUILD_TYPE=%BUILD_TYPE% ^
    -DBUILD_TESTS=ON ^
    -DBUILD_BENCHMARKS=ON ^
    -DENABLE_PROFILING=ON
if %errorlevel% neq 0 exit /b %errorlevel%
echo [OK] CMake конфигурация завершена
goto :eof

:build
echo.
echo ========================================
echo Сборка проекта
echo ========================================
cd /d "%BUILD_DIR%"
cmake --build . --config %BUILD_TYPE%
if %errorlevel% neq 0 exit /b %errorlevel%
echo [OK] Сборка завершена
goto :eof

:run_tests
echo.
echo ========================================
echo Запуск тестов (CTest)
echo ========================================
cd /d "%BUILD_DIR%"
ctest -C %BUILD_TYPE% --output-on-failure --verbose
if %errorlevel% neq 0 exit /b %errorlevel%
echo [OK] Все тесты пройдены
goto :eof

:run_benchmarks
echo.
echo ========================================
echo Запуск бенчмарков
echo ========================================
cd /d "%BUILD_DIR%"

if not exist "%BUILD_DIR%\sieve.exe" (
    echo [ERROR] sieve.exe не найден
    goto :eof
)

if not exist "%BUILD_DIR%\hash.exe" (
    echo [ERROR] hash.exe не найден
    goto :eof
)

echo.
echo Бенчмарк: Решето Эратосфена
echo ----------------------------------------
sieve.exe 10000000 256

echo.
echo Бенчмарк: Параллельное хэширование
echo ----------------------------------------
hash.exe 100000 64 256

echo [OK] Бенчмарки завершены
goto :eof

:summary
echo.
echo ========================================
echo Итоги сборки
echo ========================================
echo.
echo Директория сборки: %BUILD_DIR%
echo Тип сборки:        %BUILD_TYPE%
echo.
if exist "%BUILD_DIR%" (
    echo Собранные файлы:
    for %%f in ("%BUILD_DIR%\*.exe") do (
        echo   - %%~nxf
    )
)
echo.
echo Для запуска тестов:
echo   cd %BUILD_DIR% ^&^& ctest --verbose
echo.
echo Для запуска бенчмарков:
echo   cd %BUILD_DIR% ^&^& sieve.exe 10000000 256
echo   cd %BUILD_DIR% ^&^& hash.exe 100000 64 256
echo.
if exist "%BUILD_DIR%\docs" (
    echo Документация:
    echo   Откройте %BUILD_DIR%\docs\html\index.html
)
goto :eof
