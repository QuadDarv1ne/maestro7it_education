#include <iostream>
#include "../tests/test_framework.h"

// Forward declarations for test functions
int runLoggerTests();
int runMemoryMonitorTests();

/**
 * @brief Основная функция для запуска всех тестов
 */
int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "         PCMetrics Test Suite         " << std::endl;
    std::cout << "======================================" << std::endl;
    
    int totalFailedTests = 0;
    
    // Run logger tests
    std::cout << "\nRunning Logger Tests..." << std::endl;
    totalFailedTests += runLoggerTests();
    
    // Run memory monitor tests
    std::cout << "\nRunning Memory Monitor Tests..." << std::endl;
    totalFailedTests += runMemoryMonitorTests();
    
    // Summary
    std::cout << "\n======================================" << std::endl;
    std::cout << "         Test Suite Summary           " << std::endl;
    std::cout << "======================================" << std::endl;
    
    if (totalFailedTests == 0) {
        std::cout << "All tests passed! ✓" << std::endl;
        return 0;
    } else {
        std::cout << "Some tests failed! ✗ (" << totalFailedTests << " failures)" << std::endl;
        return 1;
    }
}