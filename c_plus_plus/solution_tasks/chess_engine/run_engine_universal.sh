#!/bin/bash

# Универсальный скрипт запуска шахматного движка
# Поддерживает автоматическое определение операционной системы

echo "Запуск профессионального шахматного движка"
echo "=========================================="

# Определение операционной системы
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if [ -f "./chess_engine" ]; then
        echo "Запуск на Linux..."
        ./chess_engine
    elif [ -f "./chess_engine.exe" ]; then
        echo "Запуск Windows-версии на Linux (Wine)..."
        wine ./chess_engine.exe
    else
        echo "Ошибка: исполняемый файл не найден"
        echo "Пожалуйста, сначала выполните сборку проекта"
        exit 1
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [ -f "./chess_engine" ]; then
        echo "Запуск на macOS..."
        ./chess_engine
    else
        echo "Ошибка: исполняемый файл не найден"
        echo "Пожалуйста, сначала выполните сборку проекта"
        exit 1
    fi
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash, MSYS2)
    if [ -f "./chess_engine.exe" ]; then
        echo "Запуск на Windows..."
        ./chess_engine.exe
    else
        echo "Ошибка: исполняемый файл не найден"
        echo "Пожалуйста, сначала выполните сборку проекта"
        exit 1
    fi
    
else
    echo "Неизвестная операционная система: $OSTYPE"
    echo "Поддерживаемые системы: Linux, macOS, Windows"
    exit 1
fi

echo "Программа завершена"