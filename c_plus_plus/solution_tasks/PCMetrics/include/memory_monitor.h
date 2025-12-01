#ifndef MEMORY_MONITOR_H
#define MEMORY_MONITOR_H

#include <windows.h>
#include <iostream>

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
    };
    
    /**
     * @brief Получает информацию о памяти системы
     * 
     * Использует GlobalMemoryStatusEx для получения актуальной информации
     * о состоянии памяти системы.
     * 
     * @return MemoryInfo Структура с информацией о памяти или пустая структура в случае ошибки
     */
    MemoryInfo getMemoryInfo() {
        MEMORYSTATUSEX memInfo;
        memInfo.dwLength = sizeof(MEMORYSTATUSEX);
        
        if (!GlobalMemoryStatusEx(&memInfo)) {
            // Handle error
            MemoryInfo errorInfo = {0};
            std::cerr << "Ошибка получения информации о памяти" << std::endl;
            return errorInfo;
        }
        
        MemoryInfo info;
        info.totalPhys = memInfo.ullTotalPhys;
        info.availPhys = memInfo.ullAvailPhys;
        info.usedPhys = memInfo.ullTotalPhys - memInfo.ullAvailPhys;
        info.memoryLoad = memInfo.dwMemoryLoad;
        info.totalVirtual = memInfo.ullTotalVirtual;
        info.availVirtual = memInfo.ullAvailVirtual;
        
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
                  << (info.totalPhys / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Используется физической памяти: " 
                  << (info.usedPhys / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Доступно физической памяти: " 
                  << (info.availPhys / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Использование памяти: " << info.memoryLoad << "%" << std::endl;
        std::cout << "Всего виртуальной памяти: " 
                  << (info.totalVirtual / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Доступно виртуальной памяти: " 
                  << (info.availVirtual / (1024*1024*1024)) << " ГБ" << std::endl;
    }
    
    /**
     * @brief Проверяет корректность информации о памяти
     * 
     * @param info Ссылка на структуру MemoryInfo для проверки
     * @return bool true если информация корректна, false в противном случае
     */
    bool isValidMemoryInfo(const MemoryInfo& info) const {
        return info.totalPhys > 0 && info.memoryLoad <= 100;
    }
};

#endif // MEMORY_MONITOR_H