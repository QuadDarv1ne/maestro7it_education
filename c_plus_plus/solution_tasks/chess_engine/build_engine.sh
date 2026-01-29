#!/bin/bash

# Скрипт сборки шахматного движка для Linux/macOS

echo "Сборка профессионального шахматного движка..."
echo "=============================================="

# Создание директории сборки
mkdir -p build
cd build

# Настройка CMake
echo "Настройка CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Release

# Компиляция
echo "Компиляция..."
make -j$(nproc)

# Проверка успешности сборки
if [ $? -eq 0 ]; then
    echo "Сборка завершена успешно!"
    echo "Исполняемые файлы находятся в директории build/"
    
    # Копирование исполняемых файлов в корневую директорию
    cp chess_engine ../chess_engine
    cp comprehensive_benchmark ../benchmark
    
    echo "Файлы скопированы в корневую директорию проекта"
else
    echo "Ошибка при сборке"
    exit 1
fi

cd ..

# Создание скрипта запуска
echo "#!/bin/bash" > run_engine.sh
echo "echo 'Запуск шахматного движка'" >> run_engine.sh
echo "./chess_engine" >> run_engine.sh
chmod +x run_engine.sh

echo "#!/bin/bash" > run_benchmark.sh
echo "echo 'Запуск бенчмарка производительности'" >> run_benchmark.sh
echo "./benchmark" >> run_benchmark.sh
chmod +x run_benchmark.sh

echo "Созданы скрипты запуска:"
echo "- run_engine.sh - запуск шахматного движка"
echo "- run_benchmark.sh - запуск тестов производительности"