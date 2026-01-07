@echo off
echo Запуск тестов TextAnalyzerPro с Maven...
echo.

REM Запуск unit тестов через Maven
mvnw.cmd test

if %errorlevel% neq 0 (
    echo.
    pause
)
java -cp target/classes TestRunner

if %errorlevel% neq 0 (
    echo.
    pause
)