#include "../tests/test_framework.h"
#include "../include/memory_monitor.h"

/**
 * @brief Тест инициализации MemoryMonitor
 */
void testMemoryMonitorInitialization() {
    // Arrange
    MemoryMonitor monitor;
    
    // Act & Assert
    ASSERT_TRUE(true, "MemoryMonitor Initialization Test", "MemoryMonitor should be creatable");
}

/**
 * @brief Тест получения информации о памяти
 */
void testMemoryMonitorGetInfo() {
    // Arrange
    MemoryMonitor monitor;
    
    // Act
    MemoryMonitor::MemoryInfo info = monitor.getMemoryInfo();
    
    // Assert
    bool validTotal = info.totalPhys > 0;
    bool validLoad = info.memoryLoad >= 0 && info.memoryLoad <= 100;
    
    ASSERT_TRUE(validTotal, "MemoryMonitor Total Memory Test", "Total physical memory should be greater than 0");
    ASSERT_TRUE(validLoad, "MemoryMonitor Load Test", "Memory load should be between 0 and 100");
}

/**
 * @brief Тест проверки валидности информации о памяти
 */
void testMemoryMonitorValidation() {
    // Arrange
    MemoryMonitor monitor;
    MemoryMonitor::MemoryInfo validInfo;
    validInfo.totalPhys = 1024 * 1024 * 1024; // 1 GB
    validInfo.memoryLoad = 50;
    
    MemoryMonitor::MemoryInfo invalidInfo;
    invalidInfo.totalPhys = 0;
    invalidInfo.memoryLoad = 50;
    
    // Act
    bool validResult = monitor.isValidMemoryInfo(validInfo);
    bool invalidResult = monitor.isValidMemoryInfo(invalidInfo);
    
    // Assert
    ASSERT_TRUE(validResult, "MemoryMonitor Validation Valid Test", "Valid memory info should pass validation");
    ASSERT_TRUE(!invalidResult, "MemoryMonitor Validation Invalid Test", "Invalid memory info should fail validation");
}

/**
 * @brief Запуск всех тестов MemoryMonitor
 */
int runMemoryMonitorTests() {
    TestFramework::clearResults();
    
    testMemoryMonitorInitialization();
    testMemoryMonitorGetInfo();
    testMemoryMonitorValidation();
    
    return TestFramework::runTests();
}