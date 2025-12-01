#ifndef TEST_FRAMEWORK_H
#define TEST_FRAMEWORK_H

#include <iostream>
#include <string>
#include <vector>
#include <chrono>

/**
 * @class TestFramework
 * @brief Простой фреймворк для модульного тестирования
 * 
 * TestFramework предоставляет базовую функциональность для создания и запуска модульных тестов.
 */
class TestFramework {
public:
    /**
     * @struct TestResult
     * @brief Результат выполнения теста
     */
    struct TestResult {
        std::string testName;
        bool passed;
        std::string errorMessage;
        double executionTime; // in milliseconds
    };

    /**
     * @brief Добавляет результат теста
     * 
     * @param name Название теста
     * @param passed Результат теста (true - успешно, false - ошибка)
     * @param errorMsg Сообщение об ошибке (если есть)
     * @param execTime Время выполнения теста в миллисекундах
     */
    static void addTestResult(const std::string& name, bool passed, const std::string& errorMsg = "", double execTime = 0.0);

    /**
     * @brief Запускает все тесты и выводит отчет
     * 
     * @return int Количество проваленных тестов
     */
    static int runTests();

    /**
     * @brief Очищает результаты предыдущих тестов
     */
    static void clearResults();
};

/**
 * @brief Макрос для проверки условий в тестах
 * 
 * @param condition Условие для проверки
 * @param testName Название теста
 * @param errorMsg Сообщение об ошибке
 */
#define ASSERT_TRUE(condition, testName, errorMsg) \
    do { \
        auto start = std::chrono::high_resolution_clock::now(); \
        bool result = (condition); \
        auto end = std::chrono::high_resolution_clock::now(); \
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start); \
        TestFramework::addTestResult(testName, result, result ? "" : errorMsg, duration.count() / 1000.0); \
    } while(0)

/**
 * @brief Макрос для проверки равенства двух значений
 * 
 * @param expected Ожидаемое значение
 * @param actual Фактическое значение
 * @param testName Название теста
 */
#define ASSERT_EQUAL(expected, actual, testName) \
    do { \
        auto start = std::chrono::high_resolution_clock::now(); \
        bool result = ((expected) == (actual)); \
        auto end = std::chrono::high_resolution_clock::now(); \
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start); \
        std::string errorMsg = "Expected: " + std::to_string(expected) + ", Actual: " + std::to_string(actual); \
        TestFramework::addTestResult(testName, result, result ? "" : errorMsg, duration.count() / 1000.0); \
    } while(0)

/**
 * @brief Макрос для проверки равенства двух строк
 * 
 * @param expected Ожидаемая строка
 * @param actual Фактическая строка
 * @param testName Название теста
 */
#define ASSERT_STRING_EQUAL(expected, actual, testName) \
    do { \
        auto start = std::chrono::high_resolution_clock::now(); \
        bool result = ((expected) == (actual)); \
        auto end = std::chrono::high_resolution_clock::now(); \
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start); \
        std::string errorMsg = "Expected: " + std::string(expected) + ", Actual: " + std::string(actual); \
        TestFramework::addTestResult(testName, result, result ? "" : errorMsg, duration.count() / 1000.0); \
    } while(0)

#endif // TEST_FRAMEWORK_H