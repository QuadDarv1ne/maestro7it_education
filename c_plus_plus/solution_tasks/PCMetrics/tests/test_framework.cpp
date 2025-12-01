#include "test_framework.h"

// Definition of static member
std::vector<TestFramework::TestResult> TestFramework::testResults;

// Implementation of static methods
void TestFramework::addTestResult(const std::string& name, bool passed, const std::string& errorMsg, double execTime) {
    TestResult result;
    result.testName = name;
    result.passed = passed;
    result.errorMessage = errorMsg;
    result.executionTime = execTime;
    testResults.push_back(result);
}

int TestFramework::runTests() {
    std::cout << "======================================" << std::endl;
    std::cout << "         Запуск модульных тестов      " << std::endl;
    std::cout << "======================================" << std::endl;

    int passedTests = 0;
    int failedTests = 0;
    double totalExecutionTime = 0.0;

    for (const auto& result : testResults) {
        if (result.passed) {
            std::cout << "[PASSED] " << result.testName << " (" << result.executionTime << " ms)" << std::endl;
            passedTests++;
        } else {
            std::cout << "[FAILED] " << result.testName << " (" << result.executionTime << " ms)" << std::endl;
            std::cout << "         Error: " << result.errorMessage << std::endl;
            failedTests++;
        }
        totalExecutionTime += result.executionTime;
    }

    std::cout << "\n======================================" << std::endl;
    std::cout << "         Результаты тестирования      " << std::endl;
    std::cout << "======================================" << std::endl;
    std::cout << "Всего тестов: " << (passedTests + failedTests) << std::endl;
    std::cout << "Успешных: " << passedTests << std::endl;
    std::cout << "Проваленных: " << failedTests << std::endl;
    std::cout << "Общее время выполнения: " << totalExecutionTime << " ms" << std::endl;
    std::cout << "======================================" << std::endl;

    return failedTests;
}

void TestFramework::clearResults() {
    testResults.clear();
}