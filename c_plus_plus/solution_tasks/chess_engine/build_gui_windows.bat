@echo off
:: Скрипт сборки графического шахматного движка с SFML

echo Сборка графического шахматного движка с SFML...
echo ================================================

:: Проверка наличия необходимых инструментов
where cmake >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: CMake не найден в PATH
    echo Пожалуйста, установите CMake с https://cmake.org/download/
    pause
    exit /b 1
)

:: Проверка наличия SFML
if not exist "%VCPKG_ROOT%" (
    echo Предупреждение: VCPKG_ROOT не установлен
    echo Для установки SFML рекомендуется использовать vcpkg:
    echo git clone https://github.com/Microsoft/vcpkg.git
    echo cd vcpkg
    echo .\bootstrap-vcpkg.bat
    echo .\vcpkg install sfml
    echo set VCPKG_ROOT=путь_к_vcpkg
    echo.
)

:: Создание директории сборки
if not exist "build_gui" mkdir build_gui
cd build_gui

:: Настройка CMake для GUI версии
echo Настройка CMake для графической версии...
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release -DBUILD_GUI=ON
if %errorlevel% neq 0 (
    echo Ошибка при настройке CMake для GUI
    echo Попробуйте установить SFML через vcpkg
    cd ..
    pause
    exit /b 1
)

:: Компиляция
echo Компиляция графической версии...
mingw32-make -j%NUMBER_OF_PROCESSORS%
if %errorlevel% neq 0 (
    echo Ошибка при сборке графической версии
    cd ..
    pause
    exit /b 1
)

echo Сборка графической версии завершена успешно!
echo Исполняемый файл: build_gui/chess_engine_gui.exe

:: Копирование в корневую директорию
copy chess_engine_gui.exe ..\chess_engine_gui.exe >nul

echo Файл скопирован в корневую директорию проекта

cd ..

:: Создание скрипта запуска GUI
echo @echo off > run_gui.bat
echo echo Запуск графического шахматного движка >> run_gui.bat
echo chess_engine_gui.exe >> run_gui.bat

echo Создан скрипт запуска: run_gui.bat

echo.
echo Для запуска графического интерфейса выполните:
echo run_gui.bat
echo.
echo Управление:
echo - Кликните на фигуру для выбора
echo - Кликните на цель для хода  
echo - R - перезапуск игры
echo - ESC - выход

pause