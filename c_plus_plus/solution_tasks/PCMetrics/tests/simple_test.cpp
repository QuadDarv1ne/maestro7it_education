#include <iostream>
#include <string>
#include <iomanip>
#include "../include/logger.h"
#include "../include/memory_monitor.h"
#include "../include/cpu_monitor.h"
#include "../include/disk_monitor.h"

// Утилита для вывода результатов тестов
void printTestResult(const std::string& testName, bool passed) {
    std::cout << "[" << (passed ? "PASSED" : "FAILED") << "] " << testName << std::endl;
}

// Тест Logger
bool testLogger() {
    std::cout << "\n--- Testing Logger ---" << std::endl;
    Logger& logger = Logger::getInstance();
    logger.initialize("test.log", Logger::LogLevel::DEBUG_LEVEL, true);
    
    logger.info("Logger test started");
    logger.debug("This is a debug message");
    logger.warning("This is a warning message");
    logger.error("This is an error message");
    logger.info("Logger test completed");
    
    return true; // Logger не имеет возвращаемых значений для проверки
}

// Тест MemoryMonitor
bool testMemoryMonitor() {
    std::cout << "\n--- Testing MemoryMonitor ---" << std::endl;
    MemoryMonitor memMonitor;
    MemoryMonitor::MemoryInfo memInfo = memMonitor.getMemoryInfo();
    
    std::cout << "Total Physical Memory: " << (memInfo.totalPhys / (1024*1024*1024)) << " GB" << std::endl;
    std::cout << "Available Physical Memory: " << (memInfo.availPhys / (1024*1024*1024)) << " GB" << std::endl;
    std::cout << "Memory Load: " << memInfo.memoryLoad << "%" << std::endl;
    
    // Проверка валидности данных
    bool isValid = memMonitor.isValidMemoryInfo(memInfo);
    printTestResult("Memory info validation", isValid);
    
    return isValid && memInfo.totalPhys > 0;
}

// Тест CPUMonitor
bool testCPUMonitor() {
    std::cout << "\n--- Testing CPUMonitor ---" << std::endl;
    CPUMonitor cpuMonitor;
    
    // Проверка инициализации
    bool initialized = cpuMonitor.isInitialized();
    printTestResult("CPU monitor initialization", initialized);
    
    if (!initialized) {
        return false;
    }
    
    // Получение информации о процессоре
    std::cout << "CPU Information:" << std::endl;
    cpuMonitor.getCPUInfo();
    
    int processorCount = cpuMonitor.getProcessorCount();
    std::cout << "Processor count: " << processorCount << std::endl;
    printTestResult("Processor count > 0", processorCount > 0);
    
    // Проверка загрузки CPU
    std::cout << "Collecting CPU usage data..." << std::endl;
    Sleep(1000); // Подождем секунду для сбора данных
    double cpuUsage = cpuMonitor.getCPUUsage();
    std::cout << "CPU Usage: " << std::fixed << std::setprecision(2) << cpuUsage << "%" << std::endl;
    
    bool validUsage = (cpuUsage >= 0.0 && cpuUsage <= 100.0);
    printTestResult("Valid CPU usage range", validUsage);
    
    return initialized && processorCount > 0 && validUsage;
}

// Тест DiskMonitor
bool testDiskMonitor() {
    std::cout << "\n--- Testing DiskMonitor ---" << std::endl;
    DiskMonitor diskMonitor;
    
    auto disks = diskMonitor.getDiskInfo();
    std::cout << "Found " << disks.size() << " disk(s)" << std::endl;
    
    bool hasValidDisks = false;
    for (const auto& disk : disks) {
        if (diskMonitor.isValidDiskInfo(disk)) {
            hasValidDisks = true;
            std::wcout << L"Disk: " << disk.drive << std::endl;
            std::wcout << L"  Total: " << (disk.totalSpace / (1024*1024*1024)) << L" GB" << std::endl;
            std::wcout << L"  Free: " << (disk.freeSpace / (1024*1024*1024)) << L" GB" << std::endl;
            std::wcout << L"  Usage: " << std::fixed << std::setprecision(2) 
                      << disk.usagePercent << L"%" << std::endl;
        }
    }
    
    printTestResult("Has valid disks", hasValidDisks);
    return hasValidDisks;
}

// Основная функция тестирования
int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "    PCMetrics Comprehensive Test     " << std::endl;
    std::cout << "======================================" << std::endl;
    
    int totalTests = 0;
    int passedTests = 0;
    
    // Запуск тестов
    std::cout << "\nRunning test suite..." << std::endl;
    
    // Тест Logger
    totalTests++;
    if (testLogger()) {
        passedTests++;
    }
    
    // Тест MemoryMonitor
    totalTests++;
    if (testMemoryMonitor()) {
        passedTests++;
    }
    
    // Тест CPUMonitor
    totalTests++;
    if (testCPUMonitor()) {
        passedTests++;
    }
    
    // Тест DiskMonitor
    totalTests++;
    if (testDiskMonitor()) {
        passedTests++;
    }
    
    // Итоговая статистика
    std::cout << "\n======================================" << std::endl;
    std::cout << "         Test Results Summary         " << std::endl;
    std::cout << "======================================" << std::endl;
    std::cout << "Total tests: " << totalTests << std::endl;
    std::cout << "Passed: " << passedTests << std::endl;
    std::cout << "Failed: " << (totalTests - passedTests) << std::endl;
    std::cout << "Success rate: " << std::fixed << std::setprecision(1) 
              << (100.0 * passedTests / totalTests) << "%" << std::endl;
    std::cout << "======================================" << std::endl;
    
    if (passedTests == totalTests) {
        std::cout << "\n✓ All tests passed successfully!" << std::endl;
        return 0;
    } else {
        std::cout << "\n✗ Some tests failed!" << std::endl;
        return 1;
    }
}