#!/bin/bash

# Скрипт тестирования проекта WordStatPlusPlus
# Проверяет корректность работы на тестовых данных

set -e  # Завершать скрипт при ошибке

echo "========================================="
echo "Тестирование WordStatPlusPlus"
echo "========================================="

# Проверяем, скомпилирован ли проект
if [ ! -d "bin" ] || [ ! -f "bin/WordStatPlusPlus.class" ]; then
    echo "❌ Проект не скомпилирован. Запустите build.sh сначала."
    exit 1
fi

# Создаем временную директорию для результатов
mkdir -p test_results

# Функция для запуска теста
run_test() {
    local test_name=$1
    local input_file=$2
    local expected_file=$3
    local output_file="test_results/${test_name}_output.txt"
    
    echo ""
    echo "Запуск теста: ${test_name}"
    echo "Входной файл: ${input_file}"
    
    # Запускаем программу
    java -cp bin WordStatPlusPlus "${input_file}" "${output_file}"
    
    # Проверяем существование выходного файла
    if [ ! -f "${output_file}" ]; then
        echo "❌ Ошибка: Выходной файл не создан"
        return 1
    fi
    
    # Сравниваем с ожидаемым результатом
    if diff -q "${expected_file}" "${output_file}" > /dev/null; then
        echo "✅ Тест пройден: ${test_name}"
        return 0
    else
        echo "❌ Тест не пройден: ${test_name}"
        echo "Различия:"
        diff "${expected_file}" "${output_file}" || true
        return 1
    fi
}

# Запускаем все тесты
passed_tests=0
total_tests=3

run_test "test1" "test/input1.txt" "test/expected1.txt" && ((passed_tests++))
# run_test "test2" "test/input2.txt" "test/expected2.txt" && ((passed_tests++))
# run_test "test3" "test/input3.txt" "test/expected3.txt" && ((passed_tests++))

echo ""
echo "========================================="
echo "Результаты тестирования:"
echo "Пройдено тестов: ${passed_tests}/${total_tests}"
echo "========================================="

if [ ${passed_tests} -eq ${total_tests} ]; then
    echo "✅ Все тесты пройдены успешно!"
    exit 0
else
    echo "❌ Некоторые тесты не пройдены"
    exit 1
fi