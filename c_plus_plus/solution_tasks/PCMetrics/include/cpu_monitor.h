#ifndef CPU_MONITOR_H
#define CPU_MONITOR_H

#include <windows.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <iostream>

#pragma comment(lib, "pdh.lib")

class CPUMonitor {
private:
    PDH_HQUERY query;
    PDH_HCOUNTER counter;
    bool initialized;
    
public:
    CPUMonitor() : initialized(false) {
        // Initialize PDH query and counter
        PDH_STATUS status = PdhOpenQuery(NULL, 0, &query);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка инициализации PDH query: " << status << std::endl;
            return;
        }
        
        status = PdhAddCounterA(query, "\\Processor(_Total)\\% Processor Time", 0, &counter);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка добавления счетчика PDH: " << status << std::endl;
            PdhCloseQuery(query);
            return;
        }
        
        // First collection to initialize
        PdhCollectQueryData(query);
        Sleep(100);
        status = PdhCollectQueryData(query);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка сбора данных PDH: " << status << std::endl;
            PdhCloseQuery(query);
            return;
        }
        
        initialized = true;
    }
    
    ~CPUMonitor() {
        if (initialized) {
            PdhCloseQuery(query);
        }
    }
    
    double getCPUUsage() {
        if (!initialized) {
            std::cerr << "CPU монитор не инициализирован" << std::endl;
            return -1.0;
        }
        
        PDH_FMT_COUNTERVALUE value;
        Sleep(100); // Small delay between measurements
        
        PDH_STATUS status = PdhCollectQueryData(query);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка сбора данных CPU: " << status << std::endl;
            return -1.0;
        }
        
        status = PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &value);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка получения форматированного значения CPU: " << status << std::endl;
            return -1.0;
        }
        
        // Ensure value is within reasonable bounds
        if (value.doubleValue < 0.0 || value.doubleValue > 100.0) {
            std::cerr << "Получено некорректное значение загрузки CPU: " << value.doubleValue << std::endl;
            return -1.0;
        }
        
        return value.doubleValue;
    }
    
    void getCPUInfo() {
        SYSTEM_INFO sysInfo;
        GetSystemInfo(&sysInfo);
        std::cout << "Количество процессоров: " << sysInfo.dwNumberOfProcessors << std::endl;
        std::cout << "Архитектура: ";
        switch(sysInfo.wProcessorArchitecture) {
            case PROCESSOR_ARCHITECTURE_AMD64:
                std::cout << "x64 (AMD or Intel)" << std::endl;
                break;
            case PROCESSOR_ARCHITECTURE_INTEL:
                std::cout << "x86" << std::endl;
                break;
            case PROCESSOR_ARCHITECTURE_ARM:
                std::cout << "ARM" << std::endl;
                break;
            default:
                std::cout << "Unknown" << std::endl;
        }
    }
    
    int getProcessorCount() {
        SYSTEM_INFO sysInfo;
        GetSystemInfo(&sysInfo);
        return sysInfo.dwNumberOfProcessors;
    }
    
    bool isInitialized() const {
        return initialized;
    }
};

#endif // CPU_MONITOR_H