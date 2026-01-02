#!/bin/bash

# Скрипт сборки проекта WordStatPlusPlus

set -e  # Завершать скрипт при ошибке

echo "========================================="
echo "Сборка проекта WordStatPlusPlus"
echo "========================================="

# Создаем директорию для скомпилированных классов
mkdir -p bin

# Компилируем Java файлы с кодировкой UTF-8
echo "Компиляция исходных файлов..."
javac -encoding UTF-8 -d bin src/*.java

# Проверяем успешность компиляции
if [ $? -eq 0 ]; then
    echo "✅ Компиляция успешно завершена"
    echo "Скомпилированные файлы находятся в директории: bin/"
    
    # Создаем JAR файл (опционально)
    echo ""
    echo "Создание JAR файла..."
    cd bin
    jar cfe ../WordStatPlusPlus.jar WordStatPlusPlus *.class
    cd ..
    
    if [ $? -eq 0 ]; then
        echo "✅ JAR файл создан: WordStatPlusPlus.jar"
        echo ""
        echo "Использование:"
        echo "  java -jar WordStatPlusPlus.jar input.txt output.txt"
        echo "  или"
        echo "  java -cp bin WordStatPlusPlus input.txt output.txt"
    else
        echo "❌ Ошибка при создании JAR файла"
        exit 1
    fi
else
    echo "❌ Ошибка компиляции"
    exit 1
fi

echo ""
echo "========================================="
echo "Сборка завершена успешно"
echo "========================================="