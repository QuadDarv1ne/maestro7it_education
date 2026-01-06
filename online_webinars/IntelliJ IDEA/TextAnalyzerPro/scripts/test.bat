@echo off
echo Запуск тестов TextAnalyzerPro с Maven...
echo.

REM Запуск unit тестов через Maven
mvn test

if %errorlevel% neq 0 (
    echo.
    pause
)
java -cp bin TestRunner

if %errorlevel% neq 0 (
    echo.
    pause
)