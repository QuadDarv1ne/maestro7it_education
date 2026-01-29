@echo off
:: Скрипт очистки проекта от временных файлов

echo Очистка проекта от временных файлов...
echo ======================================

:: Удаление временных файлов сборки
echo Удаление временных файлов сборки...
if exist "build\CMakeFiles" rmdir /s /q "build\CMakeFiles" >nul 2>&1
if exist "build\*.cmake" del /q "build\*.cmake" >nul 2>&1
if exist "build\CMakeCache.txt" del /q "build\CMakeCache.txt" >nul 2>&1

:: Удаление объектных файлов
echo Удаление объектных файлов...
del /s /q "*.obj" >nul 2>&1
del /s /q "*.o" >nul 2>&1

:: Удаление временных файлов
echo Удаление временных файлов...
del /s /q "*.tmp" >nul 2>&1
del /s /q "*.temp" >nul 2>&1
del /s /q "*.log" >nul 2>&1
del /s /q "*.bak" >nul 2>&1

:: Удаление файлов кэша
echo Удаление файлов кэша...
del /s /q "*.cache" >nul 2>&1
del /s /q "*.pch" >nul 2>&1

:: Очистка директории сборки (сохраняем только исполняемые файлы)
echo Очистка директории сборки...
cd build
if exist "*.obj" del /q "*.obj" >nul 2>&1
if exist "*.o" del /q "*.o" >nul 2>&1
cd ..

:: Удаление временных Python файлов
echo Удаление временных Python файлов...
del /s /q "*.pyc" >nul 2>&1
del /s /q "__pycache__" >nul 2>&1

echo.
echo Очистка завершена!
echo Проект готов к работе.
pause