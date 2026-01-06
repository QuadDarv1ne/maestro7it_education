@echo off
echo Сборка проекта TextAnalyzerPro...
echo.

REM Создаем директорию для скомпилированных классов
if not exist bin mkdir bin

REM Компилируем исходный код с кодировкой UTF-8
echo Компиляция исходного кода...
javac -encoding UTF-8 -d bin ^
    src/analyzer/scanner/*.java ^
    src/analyzer/statistics/*.java ^
    src/analyzer/utils/*.java ^
    src/tasks/*.java ^
    src/*.java

if %errorlevel% neq 0 (
    echo Ошибка компиляции
    pause
    exit /b 1
)

echo ✓ Компиляция успешно завершена
echo.

REM Копируем ресурсы (если есть)
if exist src/resources (
    xcopy /E /Y src/resources bin\resources
)

REM Создаем JAR-файл
echo Создание JAR-файла...
cd bin
jar cfe ../TextAnalyzerPro.jar Main ^
    analyzer/ ^
    tasks/ ^
    *.class
cd ..

if %errorlevel% neq 0 (
    echo Ошибка при создании JAR-файла
    pause
    exit /b 1
)

echo ✓ JAR-файл создан: TextAnalyzerPro.jar
echo.

echo === Сборка завершена успешно ===
echo.
echo Использование:
echo   java -jar TextAnalyzerPro.jar
echo   java -cp bin Main
echo.
pause