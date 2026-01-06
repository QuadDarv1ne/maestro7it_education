@echo off
echo Запуск TextAnalyzerPro с Maven...
echo.

REM Запускаем приложение через Maven
mvn exec:java -Dexec.mainClass="Main" -Dexec.args="%*"

if %errorlevel% neq 0 (
    echo.
    pause
)