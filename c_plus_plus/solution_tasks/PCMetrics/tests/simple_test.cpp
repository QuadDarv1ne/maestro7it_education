#include <iostream>
#include <string>
#include "../include/logger.h"
#include "../include/memory_monitor.h"

int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "         Simple PCMetrics Test        " << std::endl;
    std::cout << "======================================" << std::endl;
    
    // Test Logger
    std::cout << "\n--- Testing Logger ---" << std::endl;
    Logger& logger = Logger::getInstance();
    logger.initialize("test.log", Logger::LogLevel::DEBUG_LEVEL, true);
    logger.info("Logger test started");
    logger.debug("This is a debug message");
    logger.warning("This is a warning message");
    logger.error("This is an error message");
    logger.info("Logger test completed");
    
    // Test MemoryMonitor
    std::cout << "\n--- Testing MemoryMonitor ---" << std::endl;
    MemoryMonitor memMonitor;
    MemoryMonitor::MemoryInfo memInfo = memMonitor.getMemoryInfo();
    
    std::cout << "Total Physical Memory: " << (memInfo.totalPhys / (1024*1024*1024)) << " GB" << std::endl;
    std::cout << "Available Physical Memory: " << (memInfo.availPhys / (1024*1024*1024)) << " GB" << std::endl;
    std::cout << "Memory Load: " << memInfo.memoryLoad << "%" << std::endl;
    
    // Test validation
    bool isValid = memMonitor.isValidMemoryInfo(memInfo);
    std::cout << "Memory info validation: " << (isValid ? "PASSED" : "FAILED") << std::endl;
    
    std::cout << "\n======================================" << std::endl;
    std::cout << "         Test Completed               " << std::endl;
    std::cout << "======================================" << std::endl;
    
    return 0;
}