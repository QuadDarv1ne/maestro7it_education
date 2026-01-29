@echo off
chcp 65001 >nul
title Тестирование UTF-8 поддержки

echo Тестирование поддержки UTF-8 и русских символов
echo ================================================

echo.
echo Компиляция тестового файла...
cd build
cmake .. >nul 2>&1
make utf8_test >nul 2>&1
cd ..

echo Запуск теста UTF-8...
echo ======================
build\utf8_test.exe

echo.
echo Тест завершен!
pause