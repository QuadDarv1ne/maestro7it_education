/**
 * @file cpu_monitor.cpp
 * @brief Реализация класса CPUMonitor для мониторинга процессора
 * @author PCMetrics Team
 * @date 2025
 */

#include "../include/cpu_monitor.h"
#include <iostream>
#include <pdh.h>
#include <windows.h>
#include <iomanip>
#include <vector>
#include <string>
#include "../include/logger.h"

/**
 * @brief Инициализирует монитор CPU
 * 
 * Настраивает PDH (Performance Data Helper) для сбора данных о загрузке процессора.
 * 
 * @return bool true если инициализация успешна, false в противном случае
 */
bool CPUMonitor::initialize() {
    Logger::getInstance().debug("Инициализация монитора CPU");
    
    PDH_STATUS status = PdhOpenQuery(NULL, 0, &query);
    if (status != ERROR_SUCCESS) {
        Logger::getInstance().error("Ошибка инициализации PDH query: " + std::to_string(status));
        std::cerr << "Ошибка инициализации PDH query: " << status << std::endl;
        initialized = false;
        return false;
    }
    
    status = PdhAddCounterA(query, "\\Processor(_Total)\\% Processor Time", 0, &counter);
    if (status != ERROR_SUCCESS) {
        Logger::getInstance().error("Ошибка добавления счетчика PDH: " + std::to_string(status));
        std::cerr << "Ошибка добавления счетчика PDH: " << status << std::endl;
        PdhCloseQuery(query);
        initialized = false;
        return false;
    }
    
    // Первый сбор данных для инициализации
    PdhCollectQueryData(query);
    
    initialized = true;
    Logger::getInstance().info("Монитор CPU успешно инициализирован");
    return true;
}

/**
 * @brief Получает текущую загрузку процессора
 * 
 * Собирает данные о загрузке процессора за последний интервал времени.
 * 
 * @return double Значение загрузки CPU в процентах (0.0 - 100.0) или -1.0 в случае ошибки
 */
double CPUMonitor::getCPUUsage() const {
    if (!initialized) {
        Logger::getInstance().warning("CPU монитор не инициализирован");
        std::cerr << "CPU монитор не инициализирован" << std::endl;
        return -1.0;
    }
    
    PDH_FMT_COUNTERVALUE value;
    Sleep(100); // Small delay between measurements
    
    PDH_STATUS status = PdhCollectQueryData(query);
    if (status != ERROR_SUCCESS) {
        Logger::getInstance().error("Ошибка сбора данных CPU: " + std::to_string(status));
        std::cerr << "Ошибка сбора данных CPU: " << status << std::endl;
        return -1.0;
    }
    
    status = PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &value);
    if (status != ERROR_SUCCESS) {
        Logger::getInstance().error("Ошибка получения форматированного значения CPU: " + std::to_string(status));
        std::cerr << "Ошибка получения форматированного значения CPU: " << status << std::endl;
        return -1.0;
    }
    
    // Ensure value is within reasonable bounds
    if (value.doubleValue < 0.0 || value.doubleValue > 100.0) {
        Logger::getInstance().warning("Получено некорректное значение загрузки CPU: " + std::to_string(value.doubleValue));
        std::cerr << "Получено некорректное значение загрузки CPU: " << value.doubleValue << std::endl;
        return -1.0;
    }
    
    Logger::getInstance().debug("Загрузка CPU: " + std::to_string(value.doubleValue) + "%");
    return value.doubleValue;
}

/**
 * @brief Выводит информацию о процессоре
 * 
 * Отображает количество ядер и архитектуру процессора.
 */
void CPUMonitor::getCPUInfo() {
    Logger::getInstance().debug("Получение информации о процессоре");
    
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
    
    Logger::getInstance().info("Информация о процессоре получена");
}

/**
 * @brief Получает количество процессоров в системе
 * 
 * @return int Количество логических процессоров в системе
 */
int CPUMonitor::getProcessorCount() {
    Logger::getInstance().debug("Получение количества процессоров");
    
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    int count = sysInfo.dwNumberOfProcessors;
    Logger::getInstance().debug("Количество процессоров: " + std::to_string(count));
    return count;
}

/**
 * @brief Проверяет, инициализирован ли монитор
 * 
 * @return bool true если монитор успешно инициализирован, false в противном случае
 */
bool CPUMonitor::isInitialized() const {
    return initialized;
}

/**
 * @brief Получает текущую частоту процессора
 * 
 * @return unsigned long Частота процессора в МГц
 */
unsigned long CPUMonitor::getCPUFrequency() {
    HKEY hKey;
    unsigned long frequency = 0;
    
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, 
        "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
        0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        
        DWORD mhz = 0;
        DWORD size = sizeof(DWORD);
        
        if (RegQueryValueExA(hKey, "~MHz", NULL, NULL, 
            (LPBYTE)&mhz, &size) == ERROR_SUCCESS) {
            frequency = mhz;
        }
        
        RegCloseKey(hKey);
    }
    
    Logger::getInstance().debug("Частота CPU: " + std::to_string(frequency) + " МГц");
    return frequency;
}

/**
 * @brief Получает название процессора
 * 
 * @return std::string Название модели процессора
 */
std::string CPUMonitor::getCPUName() {
    HKEY hKey;
    char buffer[256] = {0};
    DWORD size = sizeof(buffer);
    
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE,
        "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
        0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        
        if (RegQueryValueExA(hKey, "ProcessorNameString", NULL, NULL,
            (LPBYTE)buffer, &size) == ERROR_SUCCESS) {
            RegCloseKey(hKey);
            
            // Убираем лишние пробелы
            std::string name(buffer);
            size_t start = name.find_first_not_of(" \t");
            size_t end = name.find_last_not_of(" \t");
            return (start != std::string::npos) ? name.substr(start, end - start + 1) : name;
        }
        
        RegCloseKey(hKey);
    }
    
    return "Unknown CPU";
}

/**
 * @brief Получает информацию о кэше процессора
 * 
 * @param level Уровень кэша
 * @return std::string Размер кэша в читаемом формате
 */
std::string CPUMonitor::getCacheSize(int level) {
    DWORD length = 0;
    GetLogicalProcessorInformation(NULL, &length);
    
    if (GetLastError() != ERROR_INSUFFICIENT_BUFFER) {
        return "N/A";
    }
    
    std::vector<SYSTEM_LOGICAL_PROCESSOR_INFORMATION> buffer(length / sizeof(SYSTEM_LOGICAL_PROCESSOR_INFORMATION));
    
    if (!GetLogicalProcessorInformation(&buffer[0], &length)) {
        return "N/A";
    }
    
    for (const auto& info : buffer) {
        if (info.Relationship == RelationCache) {
            if (info.Cache.Level == level) {
                double sizeKB = info.Cache.Size / 1024.0;
                if (sizeKB >= 1024) {
                    return std::to_string(static_cast<int>(sizeKB / 1024)) + " MB";
                } else {
                    return std::to_string(static_cast<int>(sizeKB)) + " KB";
                }
            }
        }
    }
    
    return "N/A";
}