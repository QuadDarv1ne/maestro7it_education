#ifndef MEMORY_MONITOR_H
#define MEMORY_MONITOR_H

#include <windows.h>
#include <iostream>
#include <sstream>
#include <string>

/**
 * @class MemoryMonitor
 * @brief Класс для мониторинга использования памяти системы
 * 
 * MemoryMonitor предоставляет функции для получения информации о физической
 * и виртуальной памяти системы, включая общее количество, доступное и
 * используемое пространство.
 */
class MemoryMonitor {
public:
    /**
     * @struct MemoryInfo
     * @brief Структура для хранения информации о памяти
     * 
     * Содержит данные о физической и виртуальной памяти системы.
     */
    struct MemoryInfo {
        DWORDLONG totalPhys;      ///< Общий объем физической памяти в байтах
        DWORDLONG availPhys;      ///< Доступная физическая память в байтах
        DWORDLONG usedPhys;       ///< Используемая физическая память в байтах
        DWORD memoryLoad;         ///< Процент использования памяти (0-100)
        DWORDLONG totalVirtual;   ///< Общий объем виртуальной памяти в байтах
        DWORDLONG availVirtual;   ///< Доступная виртуальная память в байтах
        DWORDLONG totalPageFile;  ///< Общий объем файла подкачки в байтах
        DWORDLONG availPageFile;  ///< Доступный объем файла подкачки в байтах
    };
    
    /**
     * @brief Получает информацию о памяти системы
     * 
     * Использует GlobalMemoryStatusEx для получения актуальной информации
     * о состоянии памяти системы.
     * 
     * @return MemoryInfo Структура с информацией о памяти или пустая структура в случае ошибки
     */
    MemoryInfo getMemoryInfo() const {
        MEMORYSTATUSEX memInfo;
        memInfo.dwLength = sizeof(MEMORYSTATUSEX);
        
        if (!GlobalMemoryStatusEx(&memInfo)) {
            // Handle error
            MemoryInfo errorInfo = {0, 0, 0, 0, 0, 0, 0, 0};
            std::cerr << "Ошибка получения информации о памяти: " << GetLastError() << std::endl;
            return errorInfo;
        }
        
        MemoryInfo info;
        info.totalPhys = memInfo.ullTotalPhys;
        info.availPhys = memInfo.ullAvailPhys;
        info.usedPhys = memInfo.ullTotalPhys - memInfo.ullAvailPhys;
        info.memoryLoad = memInfo.dwMemoryLoad;
        info.totalVirtual = memInfo.ullTotalVirtual;
        info.availVirtual = memInfo.ullAvailVirtual;
        info.totalPageFile = memInfo.ullTotalPageFile;
        info.availPageFile = memInfo.ullAvailPageFile;
        
        // Validate data
        if (info.totalPhys == 0) {
            std::cerr << "Получены некорректные данные о памяти" << std::endl;
        }
        
        return info;
    }
    
    /**
     * @brief Выводит информацию о памяти в консоль
     * 
     * Отображает подробную информацию о физической и виртуальной памяти,
     * включая общие объемы, доступное и используемое пространство.
     */
    void printMemoryInfo() {
        MemoryInfo info = getMemoryInfo();
        
        if (info.totalPhys == 0) {
            std::cout << "Не удалось получить информацию о памяти" << std::endl;
            return;
        }
        
        std::cout << "\n=== Информация о памяти ===" << std::endl;
        std::cout << "Всего физической памяти: " 
                  << formatBytes(info.totalPhys) << std::endl;
        std::cout << "Используется физической памяти: " 
                  << formatBytes(info.usedPhys) << std::endl;
        std::cout << "Доступно физической памяти: " 
                  << formatBytes(info.availPhys) << std::endl;
        std::cout << "Использование памяти: " << info.memoryLoad << "%" << std::endl;
        std::cout << "Всего виртуальной памяти: " 
                  << formatBytes(info.totalVirtual) << std::endl;
        std::cout << "Доступно виртуальной памяти: " 
                  << formatBytes(info.availVirtual) << std::endl;
        std::cout << "Всего файла подкачки: " 
                  << formatBytes(info.totalPageFile) << std::endl;
        std::cout << "Доступно файла подкачки: " 
                  << formatBytes(info.availPageFile) << std::endl;
    }
    
    /**
     * @brief Проверяет корректность информации о памяти
     * 
     * @param info Ссылка на структуру MemoryInfo для проверки
     * @return bool true если информация корректна, false в противном случае
     */
    bool isValidMemoryInfo(const MemoryInfo& info) const {
        // Проверяем, что общая память больше нуля и процент использования в допустимом диапазоне
        return info.totalPhys > 0 && info.memoryLoad <= 100 && info.memoryLoad >= 0;
    }
    
    /**
     * @brief Получает время работы системы
     * 
     * @return std::string Время работы в формате "X days, Y hours, Z minutes"
     */
    std::string getSystemUptime() const {
        ULONGLONG uptime = GetTickCount64() / 1000; // секунды
        
        unsigned long days = uptime / 86400;
        unsigned long hours = (uptime % 86400) / 3600;
        unsigned long minutes = (uptime % 3600) / 60;
        unsigned long seconds = uptime % 60;
        
        std::ostringstream oss;
        if (days > 0) {
            oss << days << " д. ";
        }
        oss << hours << " ч. " << minutes << " мин. " << seconds << " сек.";
        
        return oss.str();
    }
    
private:
    /**
     * @brief Форматирует количество байт в удобочитаемый формат
     * 
     * @param bytes Количество байт
     * @return std::string Отформатированная строка с размером
     */
    std::string formatBytes(DWORDLONG bytes) const {
        const char* units[] = {"Б", "КБ", "МБ", "ГБ", "ТБ"};
        int unitIndex = 0;
        double size = static_cast<double>(bytes);
        
        while (size >= 1024.0 && unitIndex < 4) {
            size /= 1024.0;
            unitIndex++;
        }
        
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << size << " " << units[unitIndex];
        return oss.str();
    }
};

#endif // MEMORY_MONITOR_H