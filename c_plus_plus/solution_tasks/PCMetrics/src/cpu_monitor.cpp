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
    
    // Проверяем, не инициализирован ли уже монитор
    if (initialized) {
        Logger::getInstance().warning("Монитор CPU уже инициализирован");
        return true;
    }
    
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
        query = NULL;
        initialized = false;
        return false;
    }
    
    // Первый сбор данных для инициализации
    status = PdhCollectQueryData(query);
    if (status != ERROR_SUCCESS) {
        Logger::getInstance().warning("Предупреждение при первом сборе данных CPU: " + std::to_string(status));
    }
    
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
    if (value.doubleValue < 0.0) {
        Logger::getInstance().warning("Получено отрицательное значение загрузки CPU: " + std::to_string(value.doubleValue));
        return 0.0;
    }
    
    if (value.doubleValue > 100.0) {
        Logger::getInstance().warning("Получено значение загрузки CPU больше 100%: " + std::to_string(value.doubleValue));
        return 100.0;
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
    
    // Дополнительная информация о процессоре
    std::string cpuName = getCPUName();
    if (cpuName != "Unknown CPU") {
        std::cout << "Название процессора: " << cpuName << std::endl;
    }
    
    unsigned long frequency = getCPUFrequency();
    if (frequency > 0) {
        std::cout << "Частота процессора: " << frequency << " МГц" << std::endl;
    }
    
    // Информация о кэше
    std::string l1Cache = getCacheSize(1);
    std::string l2Cache = getCacheSize(2);
    std::string l3Cache = getCacheSize(3);
    
    if (l1Cache != "N/A") {
        std::cout << "L1 кэш: " << l1Cache << std::endl;
    }
    if (l2Cache != "N/A") {
        std::cout << "L2 кэш: " << l2Cache << std::endl;
    }
    if (l3Cache != "N/A") {
        std::cout << "L3 кэш: " << l3Cache << std::endl;
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
    
    LONG result = RegOpenKeyExA(HKEY_LOCAL_MACHINE, 
        "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
        0, KEY_READ, &hKey);
        
    if (result != ERROR_SUCCESS) {
        Logger::getInstance().warning("Не удалось открыть реестр для получения частоты CPU: " + std::to_string(result));
        return 0;
    }
    
    DWORD mhz = 0;
    DWORD size = sizeof(DWORD);
    
    result = RegQueryValueExA(hKey, "~MHz", NULL, NULL, 
        (LPBYTE)&mhz, &size);
        
    if (result == ERROR_SUCCESS) {
        frequency = mhz;
    } else {
        Logger::getInstance().warning("Не удалось получить частоту CPU из реестра: " + std::to_string(result));
    }
    
    RegCloseKey(hKey);
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
    
    LONG result = RegOpenKeyExA(HKEY_LOCAL_MACHINE,
        "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
        0, KEY_READ, &hKey);
        
    if (result != ERROR_SUCCESS) {
        Logger::getInstance().warning("Не удалось открыть реестр для получения названия CPU: " + std::to_string(result));
        return "Unknown CPU";
    }
    
    result = RegQueryValueExA(hKey, "ProcessorNameString", NULL, NULL,
        (LPBYTE)buffer, &size);
        
    RegCloseKey(hKey);
    
    if (result == ERROR_SUCCESS) {
        // Убираем лишние пробелы
        std::string name(buffer);
        size_t start = name.find_first_not_of(" \t");
        if (start == std::string::npos) {
            return "Unknown CPU";
        }
        size_t end = name.find_last_not_of(" \t");
        return name.substr(start, end - start + 1);
    } else {
        Logger::getInstance().warning("Не удалось получить название CPU из реестра: " + std::to_string(result));
        return "Unknown CPU";
    }
}

/**
 * @brief Получает информацию о кэше процессора
 * 
 * @param level Уровень кэша
 * @return std::string Размер кэша в читаемом формате
 */
std::string CPUMonitor::getCacheSize(int level) {
    if (level < 1 || level > 3) {
        Logger::getInstance().warning("Недопустимый уровень кэша: " + std::to_string(level));
        return "N/A";
    }
    
    DWORD length = 0;
    GetLogicalProcessorInformation(NULL, &length);
    
    if (GetLastError() != ERROR_INSUFFICIENT_BUFFER) {
        Logger::getInstance().warning("Ошибка при получении информации о логическом процессоре: " + std::to_string(GetLastError()));
        return "N/A";
    }
    
    if (length == 0) {
        Logger::getInstance().warning("Получен нулевой размер буфера для информации о процессоре");
        return "N/A";
    }
    
    std::vector<SYSTEM_LOGICAL_PROCESSOR_INFORMATION> buffer(length / sizeof(SYSTEM_LOGICAL_PROCESSOR_INFORMATION));
    
    if (!GetLogicalProcessorInformation(&buffer[0], &length)) {
        Logger::getInstance().warning("Ошибка при получении информации о логическом процессоре: " + std::to_string(GetLastError()));
        return "N/A";
    }
    
    for (const auto& info : buffer) {
        if (info.Relationship == RelationCache) {
            if (info.Cache.Level == level) {
                // Проверяем, что размер кэша положительный
                if (info.Cache.Size == 0) {
                    continue;
                }
                
                double sizeKB = info.Cache.Size / 1024.0;
                if (sizeKB >= 1024) {
                    return std::to_string(static_cast<int>(sizeKB / 1024)) + " MB";
                } else {
                    return std::to_string(static_cast<int>(sizeKB)) + " KB";
                }
            }
        }
    }
    
    Logger::getInstance().debug("Информация о кэше уровня " + std::to_string(level) + " не найдена");
    return "N/A";
}