#include "../tests/test_framework.h"
#include "../src/logger.cpp"  // Include implementation directly to avoid linking issues
#include <fstream>
#include <sstream>
#include <string>

// Since we're including the implementation directly, we need to define the static member here
std::vector<TestFramework::TestResult> TestFramework::testResults;

/**
 * @brief Тест инициализации логгера
 */
void testLoggerInitialization() {
    // Arrange
    Logger& logger = Logger::getInstance();
    
    // Act
    logger.initialize("test_logger.log", Logger::LogLevel::DEBUG_LEVEL, false);
    
    // Assert
    // Since there's no direct way to check initialization, we'll check by logging something
    logger.info("Test initialization");
    
    // Check if file was created and has content
    std::ifstream file("test_logger.log");
    bool fileExists = file.good();
    file.close();
    
    ASSERT_TRUE(fileExists, "Logger Initialization Test", "Log file was not created");
}

/**
 * @brief Тест логирования разных уровней
 */
void testLoggerLevels() {
    // Arrange
    Logger& logger = Logger::getInstance();
    logger.initialize("test_levels.log", Logger::LogLevel::DEBUG_LEVEL, false);
    
    // Act
    logger.debug("Debug message");
    logger.info("Info message");
    logger.warning("Warning message");
    logger.error("Error message");
    
    // Assert
    std::ifstream file("test_levels.log");
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();
    file.close();
    
    bool hasDebug = content.find("DEBUG") != std::string::npos;
    bool hasInfo = content.find("INFO") != std::string::npos;
    bool hasWarning = content.find("WARN") != std::string::npos;
    bool hasError = content.find("ERROR") != std::string::npos;
    
    ASSERT_TRUE(hasDebug, "Logger Debug Level Test", "Debug message not found in log");
    ASSERT_TRUE(hasInfo, "Logger Info Level Test", "Info message not found in log");
    ASSERT_TRUE(hasWarning, "Logger Warning Level Test", "Warning message not found in log");
    ASSERT_TRUE(hasError, "Logger Error Level Test", "Error message not found in log");
}

/**
 * @brief Тест фильтрации по уровню логирования
 */
void testLoggerLevelFiltering() {
    // Arrange
    Logger& logger = Logger::getInstance();
    logger.initialize("test_filter.log", Logger::LogLevel::WARNING_LEVEL, false); // Only warnings and errors
    
    // Act
    logger.debug("Debug message");
    logger.info("Info message");
    logger.warning("Warning message");
    logger.error("Error message");
    
    // Assert
    std::ifstream file("test_filter.log");
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();
    file.close();
    
    bool hasDebug = content.find("DEBUG") != std::string::npos;
    bool hasInfo = content.find("INFO") != std::string::npos;
    bool hasWarning = content.find("WARN") != std::string::npos;
    bool hasError = content.find("ERROR") != std::string::npos;
    
    ASSERT_TRUE(!hasDebug, "Logger Debug Filtering Test", "Debug message should not be logged with WARNING_LEVEL minimum");
    ASSERT_TRUE(!hasInfo, "Logger Info Filtering Test", "Info message should not be logged with WARNING_LEVEL minimum");
    ASSERT_TRUE(hasWarning, "Logger Warning Filtering Test", "Warning message should be logged with WARNING_LEVEL minimum");
    ASSERT_TRUE(hasError, "Logger Error Filtering Test", "Error message should be logged with WARNING_LEVEL minimum");
}

/**
 * @brief Запуск всех тестов логгера
 */
int runLoggerTests() {
    TestFramework::clearResults();
    
    testLoggerInitialization();
    testLoggerLevels();
    testLoggerLevelFiltering();
    
    return TestFramework::runTests();
}