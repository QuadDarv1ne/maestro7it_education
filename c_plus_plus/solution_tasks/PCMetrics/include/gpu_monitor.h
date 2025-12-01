#ifndef GPU_MONITOR_H
#define GPU_MONITOR_H

#include <iostream>
#include <string>
#include <vector>

#ifdef _WIN32
    #include <windows.h>
#endif

// Conditional compilation for NVIDIA NVML support
#ifdef ENABLE_NVML
    #include <nvml.h>
    #pragma comment(lib, "nvml.lib")
#endif

// Conditional compilation for AMD ADL support
#ifdef ENABLE_ADL
    #include <adl_sdk.h>
    #pragma comment(lib, "ADL.lib")
#endif

// Conditional compilation for Intel GPA support
#ifdef ENABLE_INTEL_GPA
    #include <igpa.h>
    #pragma comment(lib, "igpa.lib")
#endif

/**
 * @class GPUMonitor
 * @brief Класс для мониторинга графического процессора
 * 
 * GPUMonitor предоставляет функции для получения информации о графическом
 * процессоре системы, включая загрузку, температуру и использование памяти.
 * Поддерживает работу с NVIDIA, AMD и Intel GPU через соответствующие библиотеки.
 */
class GPUMonitor {
private:
    bool nvmlInitialized;    ///< Флаг инициализации NVML
    bool adlInitialized;     ///< Флаг инициализации ADL
    bool gpaInitialized;     ///< Флаг инициализации Intel GPA
    
public:
    /**
     * @brief Конструктор класса GPUMonitor
     * 
     * Инициализирует монитор GPU с неинициализированным состоянием всех библиотек.
     */
    GPUMonitor() : nvmlInitialized(false), adlInitialized(false), gpaInitialized(false) {}
    
    /**
     * @brief Деструктор класса GPUMonitor
     * 
     * Корректно завершает работу со всеми GPU библиотеками.
     */
    ~GPUMonitor() {
        shutdownAll();
    }
    
    /**
     * @brief Инициализирует NVML библиотеку
     * 
     * Пытается инициализировать NVIDIA Management Library для работы с GPU.
     * 
     * @return bool true если инициализация успешна, false в противном случае
     */
    bool initNVML();
    
    /**
     * @brief Завершает работу с NVML библиотекой
     * 
     * Освобождает ресурсы NVML при завершении работы.
     */
    void shutdownNVML();
    
    /**
     * @brief Инициализирует AMD ADL библиотеку
     * 
     * Пытается инициализировать AMD Display Library для работы с GPU.
     * 
     * @return bool true если инициализация успешна, false в противном случае
     */
    bool initADL();
    
    /**
     * @brief Завершает работу с AMD ADL библиотекой
     * 
     * Освобождает ресурсы ADL при завершении работы.
     */
    void shutdownADL();
    
    /**
     * @brief Инициализирует Intel GPA библиотеку
     * 
     * Пытается инициализировать Intel Graphics Performance Analyzers для работы с GPU.
     * 
     * @return bool true если инициализация успешна, false в противном случае
     */
    bool initGPA();
    
    /**
     * @brief Завершает работу с Intel GPA библиотекой
     * 
     * Освобождает ресурсы Intel GPA при завершении работы.
     */
    void shutdownGPA();
    
    /**
     * @brief Завершает работу со всеми GPU библиотеками
     * 
     * Освобождает ресурсы всех инициализированных GPU библиотек.
     */
    void shutdownAll();
    
    /**
     * @brief Выводит информацию о GPU в консоль
     * 
     * Отображает информацию о доступных графических процессорах и
     * инструкции по включению расширенного мониторинга.
     */
    void printGPUInfo();
    
    /**
     * @brief Получает информацию об использовании NVIDIA GPU
     * 
     * Собирает данные о загрузке GPU и памяти для NVIDIA графических процессоров.
     */
    void getNVIDIAGPUUsage();
    
    /**
     * @brief Получает информацию об использовании AMD GPU
     * 
     * Собирает данные о загрузке GPU и памяти для AMD графических процессоров.
     */
    void getAMDGPUUsage();
    
    /**
     * @brief Получает информацию об использовании Intel GPU
     * 
     * Собирает данные о загрузке GPU и памяти для Intel графических процессоров.
     */
    void getIntelGPUUsage();
    
    /**
     * @struct GPUInfo
     * @brief Структура для хранения информации о графическом процессоре
     * 
     * Содержит данные о конкретном GPU системы.
     */
    struct GPUInfo {
        std::string name;                 ///< Название графического процессора
        std::string vendor;               ///< Производитель графического процессора
        unsigned int temperature;         ///< Температура GPU в градусах Цельсия
        unsigned int gpuUtilization;      ///< Загрузка GPU в процентах (0-100)
        unsigned int memoryUtilization;   ///< Использование видеопамяти в процентах (0-100)
        unsigned long long memoryTotal;   ///< Общий объем видеопамяти в байтах
        unsigned long long memoryUsed;    ///< Используемый объем видеопамяти в байтах
        unsigned int fanSpeed;            ///< Скорость вентилятора в процентах (0-100)
    };
    
    /**
     * @brief Получает информацию обо всех доступных GPU
     * 
     * Собирает данные обо всех графических процессорах системы.
     * 
     * @return std::vector<GPUInfo> Вектор со структурами информации о GPU
     */
    std::vector<GPUInfo> getAllGPUInfo();
};

#endif // GPU_MONITOR_H