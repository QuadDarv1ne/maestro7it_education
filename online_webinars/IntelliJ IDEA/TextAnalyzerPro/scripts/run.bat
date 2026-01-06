@echo off
echo Запуск TextAnalyzerPro...
echo.

REM Проверяем, скомпилирован ли проект
if not exist bin\Main.class (
    echo Проект не скомпилирован. Запустите build.bat
    pause
    exit /b 1
)

REM Запускаем приложение
java -cp bin Main %*

if %errorlevel% neq 0 (
    echo.
    pause
)