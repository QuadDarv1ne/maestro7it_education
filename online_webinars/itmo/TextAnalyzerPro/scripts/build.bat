@echo off
echo Сборка TextAnalyzerPro...
echo.

REM Создаем директории
if not exist bin mkdir bin
if not exist test mkdir test
if not exist test\input mkdir test\input
if not exist test\expected mkdir test\expected
if not exist test\actual mkdir test\actual

REM Компилируем все исходные файлы
javac -encoding UTF-8 -d bin ^
    src/analyzer/scanner/*.java ^
    src/analyzer/statistics/*.java ^
    src/analyzer/utils/*.java ^
    src/tasks/*.java ^
    src/*.java

if %errorlevel% neq 0 (
    echo Ошибка компиляции!
    pause
    exit /b 1
)

echo Компиляция успешно завершена.
echo.

REM Создаем JAR-файлы
echo Создание JAR-файлов...
cd bin

echo Создание основного JAR...
jar cfe ../TextAnalyzerPro.jar Main ^
    analyzer/ ^
    tasks/ ^
    *.class

echo Создание JAR для TaskExecutor...
jar cfe ../TaskExecutor.jar tasks.TaskExecutor ^
    analyzer/ ^
    tasks/ ^
    *.class

cd ..

if %errorlevel% neq 0 (
    echo Ошибка создания JAR-файлов!
    pause
    exit /b 1
)

echo JAR-файлы созданы:
echo   TextAnalyzerPro.jar - основное приложение
echo   TaskExecutor.jar - исполнитель задач
echo.
echo Использование:
echo   java -jar TextAnalyzerPro.jar
echo   java -jar TaskExecutor.jar
echo   java -cp bin Main
echo   java -cp bin tasks.TaskExecutor
echo.
echo Для запуска тестов:
echo   java -cp bin TestRunner
echo.
pause