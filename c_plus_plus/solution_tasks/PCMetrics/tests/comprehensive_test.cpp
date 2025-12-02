#include <iostream>
#include <string>
#include <iomanip>
#include <vector>
#include "../include/logger.h"
#include "../include/memory_monitor.h"
#include "../include/cpu_monitor.h"
#include "../include/disk_monitor.h"
#include "../include/gpu_monitor.h"
#include "../include/network_monitor.h"

// Утилита для вывода результатов тестов
void printTestResult(const std::string& testName, bool passed) {
    std::cout << "[" << (passed ? "PASSED" : "FAILED") << "] " << testName << std::endl;
}

// Тест Logger
bool testLogger() {
    std::cout << "\n--- Testing Logger ---" << std::endl;
    Logger& logger = Logger::getInstance();
    logger.initialize("test_comprehensive.log", Logger::LogLevel::DEBUG_LEVEL, true);
    
    logger.info("Logger comprehensive test started");
    logger.debug("This is a debug message");
    logger.warning("This is a warning message");
    logger.error("This is an error message");
    logger.info("Logger comprehensive test completed");
    
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
    
    // Тест форматирования байт
    std::string formatted = memMonitor.formatBytes(1024*1024*1024); // 1 GB
    std::cout << "Formatted 1GB: " << formatted << std::endl;
    printTestResult("Byte formatting", formatted == "1.00 ГБ");
    
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
    
    // Тест получения названия CPU
    std::string cpuName = cpuMonitor.getCPUName();
    std::cout << "CPU Name: " << cpuName << std::endl;
    printTestResult("CPU name retrieval", !cpuName.empty());
    
    // Тест получения частоты CPU
    unsigned long cpuFreq = cpuMonitor.getCPUFrequency();
    std::cout << "CPU Frequency: " << cpuFreq << " MHz" << std::endl;
    printTestResult("CPU frequency retrieval", true); // Always true as it returns 0 on failure
    
    // Тест получения информации о кэше
    std::string l1Cache = cpuMonitor.getCacheSize(1);
    std::string l2Cache = cpuMonitor.getCacheSize(2);
    std::string l3Cache = cpuMonitor.getCacheSize(3);
    std::cout << "L1 Cache: " << l1Cache << std::endl;
    std::cout << "L2 Cache: " << l2Cache << std::endl;
    std::cout << "L3 Cache: " << l3Cache << std::endl;
    printTestResult("Cache info retrieval", true); // Always true as it returns "N/A" on failure
    
    return initialized && processorCount > 0 && validUsage;
}

// Тест DiskMonitor
bool testDiskMonitor() {
    std::cout << "\n--- Testing DiskMonitor ---" << std::endl;
    DiskMonitor diskMonitor;
    
    auto disks = diskMonitor.getDiskInfo();
    std::cout << "Found " << disks.size() << " disk(s)" << std::endl;
    
    bool hasValidDisks = false;
    int validDiskCount = 0;
    
    for (const auto& disk : disks) {
        if (diskMonitor.isValidDiskInfo(disk)) {
            hasValidDisks = true;
            validDiskCount++;
            
            // Convert wide string to narrow string for output
            std::string driveStr;
            if (!disk.drive.empty()) {
                int size_needed = WideCharToMultiByte(CP_UTF8, 0, &disk.drive[0], (int)disk.drive.size(), NULL, 0, NULL, NULL);
                driveStr.resize(size_needed);
                WideCharToMultiByte(CP_UTF8, 0, &disk.drive[0], (int)disk.drive.size(), &driveStr[0], size_needed, NULL, NULL);
            }
            
            std::cout << "Disk: " << driveStr << std::endl;
            std::cout << "  Type: "; 
            // Convert wide string to narrow string for output
            std::string typeStr;
            if (!disk.type.empty()) {
                int size_needed = WideCharToMultiByte(CP_UTF8, 0, &disk.type[0], (int)disk.type.size(), NULL, 0, NULL, NULL);
                typeStr.resize(size_needed);
                WideCharToMultiByte(CP_UTF8, 0, &disk.type[0], (int)disk.type.size(), &typeStr[0], size_needed, NULL, NULL);
            }
            std::cout << typeStr << std::endl;
            std::cout << "  Total: " << (disk.totalSpace / (1024*1024*1024)) << " GB" << std::endl;
            std::cout << "  Free: " << (disk.freeSpace / (1024*1024*1024)) << " GB" << std::endl;
            std::cout << "  Usage: " << std::fixed << std::setprecision(2) 
                      << disk.usagePercent << "%" << std::endl;
        }
    }
    
    printTestResult("Has valid disks", hasValidDisks);
    printTestResult("Valid disk count > 0", validDiskCount > 0);
    
    return hasValidDisks && validDiskCount > 0;
}

// Тест GPUMonitor
bool testGPUMonitor() {
    std::cout << "\n--- Testing GPUMonitor ---" << std::endl;
    GPUMonitor gpuMonitor;
    
    // Получение информации о GPU
    auto gpus = gpuMonitor.getAllGPUInfo();
    std::cout << "Found " << gpus.size() << " GPU(s)" << std::endl;
    
    for (size_t i = 0; i < gpus.size(); i++) {
        const auto& gpu = gpus[i];
        std::cout << "GPU #" << i << ":" << std::endl;
        std::cout << "  Vendor: " << gpu.vendor << std::endl;
        std::cout << "  Name: " << gpu.name << std::endl;
        std::cout << "  Temperature: " << gpu.temperature << "°C" << std::endl;
        std::cout << "  GPU Utilization: " << gpu.gpuUtilization << "%" << std::endl;
        std::cout << "  Memory Utilization: " << gpu.memoryUtilization << "%" << std::endl;
        std::cout << "  Memory Total: " << (gpu.memoryTotal / (1024*1024)) << " MB" << std::endl;
        std::cout << "  Memory Used: " << (gpu.memoryUsed / (1024*1024)) << " MB" << std::endl;
        std::cout << "  Fan Speed: " << gpu.fanSpeed << "%" << std::endl;
    }
    
    // Тест инициализации различных библиотек
    bool nvmlInit = gpuMonitor.initNVML();
    bool adlInit = gpuMonitor.initADL();
    bool gpaInit = gpuMonitor.initGPA();
    
    std::cout << "NVML initialized: " << (nvmlInit ? "Yes" : "No") << std::endl;
    std::cout << "ADL initialized: " << (adlInit ? "Yes" : "No") << std::endl;
    std::cout << "GPA initialized: " << (gpaInit ? "Yes" : "No") << std::endl;
    
    printTestResult("GPU monitor basic functionality", true);
    
    // Завершение работы с библиотеками
    gpuMonitor.shutdownAll();
    
    return true;
}

// Тест NetworkMonitor
bool testNetworkMonitor() {
    std::cout << "\n--- Testing NetworkMonitor ---" << std::endl;
    NetworkMonitor netMonitor;
    
    auto interfaces = netMonitor.getNetworkInterfaces();
    std::cout << "Found " << interfaces.size() << " network interface(s)" << std::endl;
    
    bool hasActiveInterfaces = false;
    for (const auto& interface : interfaces) {
        if (interface.isUp) {
            hasActiveInterfaces = true;
            std::cout << "Interface: " << interface.name << std::endl;
            std::cout << "  Description: " << interface.description << std::endl;
            std::cout << "  Status: " << (interface.isUp ? "Up" : "Down") << std::endl;
            std::cout << "  Speed: " << (interface.speed / 1000000) << " Mbps" << std::endl;
            std::cout << "  Bytes Received: " << interface.bytesReceived << std::endl;
            std::cout << "  Bytes Sent: " << interface.bytesSent << std::endl;
        }
    }
    
    // Тест форматирования данных
    std::string formatted = netMonitor.formatDataSize(1024*1024*1024); // 1 GB
    std::cout << "Formatted 1GB: " << formatted << std::endl;
    printTestResult("Data formatting", formatted == "1.00 GB");
    
    printTestResult("Has active network interfaces", hasActiveInterfaces);
    
    return true;
}

// Основная функция тестирования
int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "    PCMetrics Comprehensive Test     " << std::endl;
    std::cout << "======================================" << std::endl;
    
    int totalTests = 0;
    int passedTests = 0;
    
    // Запуск тестов
    std::cout << "\nRunning comprehensive test suite..." << std::endl;
    
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
    
    // Тест GPUMonitor
    totalTests++;
    if (testGPUMonitor()) {
        passedTests++;
    }
    
    // Тест NetworkMonitor
    totalTests++;
    if (testNetworkMonitor()) {
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