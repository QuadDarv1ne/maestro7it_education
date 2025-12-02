#ifndef CPU_MONITOR_H
#define CPU_MONITOR_H

#include <windows.h>
#include <pdh.h>
#include <iostream>

/**
 * @class CPUMonitor
 * @brief Класс для мониторинга процессора
 * 
 * CPUMonitor предоставляет функции для получения информации о процессоре системы,
 * включая загрузку, количество ядер и архитектуру.
 */
class CPUMonitor {
private:
    PDH_HQUERY query;           ///< PDH query handle для сбора данных
    PDH_HCOUNTER counter;       ///< PDH counter для измерения загрузки CPU
    bool initialized;           ///< Флаг инициализации монитора
    
public:
    /**
     * @brief Конструктор класса CPUMonitor
     * 
     * Инициализирует монитор CPU с неинициализированным состоянием.
     */
    CPUMonitor() : query(NULL), counter(NULL), initialized(false) {
        initialize();
    }
    
    /**
     * @brief Деструктор класса CPUMonitor
     * 
     * Корректно завершает работу с PDH и освобождает ресурсы.
     */
    ~CPUMonitor() {
        if (initialized && query) {
            PdhCloseQuery(query);
        }
    }
    
    /**
     * @brief Инициализирует монитор CPU
     * 
     * Настраивает PDH (Performance Data Helper) для сбора данных о загрузке процессора.
     * 
     * @return bool true если инициализация успешна, false в противном случае
     */
    bool initialize();
    
    /**
     * @brief Получает текущую загрузку процессора
     * 
     * Собирает данные о загрузке процессора за последний интервал времени.
     * 
     * @return double Значение загрузки CPU в процентах (0.0 - 100.0) или -1.0 в случае ошибки
     */
    double getCPUUsage() const;
    
    /**
     * @brief Выводит информацию о процессоре
     * 
     * Отображает количество ядер и архитектуру процессора.
     */
    void getCPUInfo();
    
    /**
     * @brief Получает количество процессоров в системе
     * 
     * @return int Количество логических процессоров в системе
     */
    int getProcessorCount();
    
    /**
     * @brief Проверяет, инициализирован ли монитор
     * 
     * @return bool true если монитор успешно инициализирован, false в противном случае
     */
    bool isInitialized() const;
    
    /**
     * @brief Получает текущую частоту процессора
     * 
     * @return unsigned long Частота процессора в МГц, или 0 в случае ошибки
     */
    unsigned long getCPUFrequency();
    
    /**
     * @brief Получает информацию о кэше процессора
     * 
     * @param level Уровень кэша (1, 2, или 3)
     * @return std::string Размер кэша в читаемом формате
     */
    std::string getCacheSize(int level);
    
    /**
     * @brief Получает название процессора
     * 
     * @return std::string Название модели процессора
     */
    std::string getCPUName();
};

#endif // CPU_MONITOR_H