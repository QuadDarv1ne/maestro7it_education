@echo off
echo Сборка проекта TextAnalyzerPro с Maven...
echo.

REM Компилируем проект с Maven
mvn clean compile

if %errorlevel% neq 0 (
    echo Ошибка компиляции
    pause
    exit /b 1
)

echo ✓ Компиляция успешно завершена
echo.

REM Создаем JAR-файл
mvn package -DskipTests

if %errorlevel% neq 0 (
    echo Ошибка при создании JAR-файла
    pause
    exit /b 1
)

echo ✓ JAR-файл создан: target/TextAnalyzerPro-1.0.0.jar
echo.

echo === Сборка завершена успешно ===
echo.
echo Использование:
echo   java -jar TextAnalyzerPro.jar
echo   java -cp bin Main
echo.
pause