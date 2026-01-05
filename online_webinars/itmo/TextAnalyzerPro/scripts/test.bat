@echo off
echo Запуск тестов TextAnalyzerPro...
echo.

REM Проверяем, скомпилирован ли проект
if not exist bin\Main.class (
    echo Проект не скомпилирован. Запустите build.bat
    pause
    exit /b 1
)

REM Компилируем тесты
javac -encoding UTF-8 -cp bin -d bin test/TestRunner.java

if %errorlevel% neq 0 (
    echo Ошибка компиляции тестов!
    pause
    exit /b 1
)

REM Создаем тестовые файлы, если их нет
if not exist test\input mkdir test\input
if not exist test\expected mkdir test\expected

REM Создаем пример тестовых файлов
if not exist test\input\reverse.txt (
    echo Создание тестовых файлов...
    
    echo 1 2 3 > test\input\reverse.txt
    echo 4 5 6 >> test\input\reverse.txt
    echo 7 8 9 >> test\input\reverse.txt
    
    echo 9 8 7 > test\expected\reverse_output.txt
    echo 6 5 4 >> test\expected\reverse_output.txt
    echo 3 2 1 >> test\expected\reverse_output.txt
    
    echo To be or not to be > test\input\wordstat_plus.txt
    echo That is the question! >> test\input\wordstat_plus.txt
    
    echo to 2 1 5 > test\expected\wordstat_plus_output.txt
    echo be 2 2 6 >> test\expected\wordstat_plus_output.txt
    echo or 1 3 >> test\expected\wordstat_plus_output.txt
    echo not 1 4 >> test\expected\wordstat_plus_output.txt
    echo that 1 7 >> test\expected\wordstat_plus_output.txt
    echo is 1 8 >> test\expected\wordstat_plus_output.txt
    echo the 1 9 >> test\expected\wordstat_plus_output.txt
    echo question 1 10 >> test\expected\wordstat_plus_output.txt
)

REM Запускаем тесты
java -cp bin TestRunner

if %errorlevel% neq 0 (
    echo.
    pause
)