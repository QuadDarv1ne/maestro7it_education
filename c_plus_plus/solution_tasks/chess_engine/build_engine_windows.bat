@echo off
:: Скрипт сборки шахматного движка для Windows

echo Сборка профессионального шахматного движка...
echo ==============================================

:: Проверка наличия CMake
where cmake >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: CMake не найден в PATH
    echo Пожалуйста, установите CMake с https://cmake.org/download/
    pause
    exit /b 1
)

:: Создание директории сборки
if not exist "build" mkdir build
cd build

:: Настройка CMake
echo Настройка CMake...
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
if %errorlevel% neq 0 (
    echo Ошибка при настройке CMake
    cd ..
    pause
    exit /b 1
)

:: Компиляция
echo Компиляция...
mingw32-make -j%NUMBER_OF_PROCESSORS%
if %errorlevel% neq 0 (
    echo Ошибка при сборке
    cd ..
    pause
    exit /b 1
)

echo Сборка завершена успешно!
echo Исполняемые файлы находятся в директории build/

:: Копирование исполняемых файлов в корневую директорию
copy chess_engine.exe ..\chess_engine.exe >nul
copy comprehensive_benchmark.exe ..\benchmark.exe >nul

echo Файлы скопированы в корневую директорию проекта

cd ..

:: Создание скриптов запуска
echo @echo off > run_engine.bat
echo echo Запуск шахматного движка >> run_engine.bat
echo chess_engine.exe >> run_engine.bat

echo @echo off > run_benchmark.bat
echo echo Запуск бенчмарка производительности >> run_benchmark.bat
echo benchmark.exe >> run_benchmark.bat

echo Созданы скрипты запуска:
echo - run_engine.bat - запуск шахматного движка
echo - run_benchmark.bat - запуск тестов производительности

pause