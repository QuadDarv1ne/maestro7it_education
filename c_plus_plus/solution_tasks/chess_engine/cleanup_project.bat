@echo off
chcp 65001 >nul
title Очистка проекта шахмат

echo Очистка проекта шахмат
echo ======================

echo Удаление временных файлов...
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
for /d %%i in (*.__pycache__) do rmdir /s /q "%%i"
del /q *.pyc 2>nul
del /q *.pyo 2>nul
del /q *.log 2>nul

echo Удаление файлов сборки C++...
del /q *.obj 2>nul
del /q *.exe 2>nul
del /q *.dll 2>nul
del /q *.lib 2>nul

echo Очистка завершена!
echo.
echo Удалены:
echo - Директория build
echo - Файлы кэша Python
echo - Временные файлы компиляции
echo.

pause