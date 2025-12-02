/**
 * @file gpu_monitor.cpp
 * @brief Реализация класса GPUMonitor для мониторинга графических процессоров
 * @author PCMetrics Team
 * @date 2025
 * 
 * Поддерживает мониторинг GPU от NVIDIA (через NVML), AMD (через ADL) и Intel (через GPA).
 * Функциональность включается условной компиляцией при наличии соответствующих библиотек.
 */

#include "../include/gpu_monitor.h"
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>

#ifdef ENABLE_NVML
#include <nvml.h>
#endif

#ifdef ENABLE_ADL
#include <adl_sdk.h>
// ADL function pointers
typedef int (*ADL_MAIN_CONTROL_CREATE)(ADL_MAIN_MALLOC_CALLBACK, int);
typedef int (*ADL_MAIN_CONTROL_DESTROY)();
typedef int (*ADL_ADAPTER_NUMBEROFADAPTERS_GET)(int*);
typedef int (*ADL_ADAPTER_ADAPTERINFO_GET)(LPAdapterInfo, int);
typedef int (*ADL_OVERDRIVE_CAPS)(int, int*, int*, int*);
typedef int (*ADL_OVERDRIVE5_CURRENTACTIVITY_GET)(int, ADLPMActivity*);

// Global function pointers
ADL_MAIN_CONTROL_CREATE          ADL_Main_Control_Create;
ADL_MAIN_CONTROL_DESTROY         ADL_Main_Control_Destroy;
ADL_ADAPTER_NUMBEROFADAPTERS_GET ADL_Adapter_NumberOfAdapters_Get;
ADL_ADAPTER_ADAPTERINFO_GET      ADL_Adapter_AdapterInfo_Get;
ADL_OVERDRIVE_CAPS              ADL_Overdrive_Caps;
ADL_OVERDRIVE5_CURRENTACTIVITY_GET ADL_Overdrive5_CurrentActivity_Get;
#endif

#ifdef ENABLE_INTEL_GPA
// Intel GPA headers would go here
// For now, we'll use placeholder functionality
#endif

/**
 * @brief Инициализирует NVML библиотеку
 * 
 * Пытается инициализировать NVIDIA Management Library для работы с GPU.
 * Устанавливает флаг nvmlInitialized в зависимости от результата.
 * 
 * @return bool true если инициализация успешна, false в противном случае
 */
bool GPUMonitor::initNVML() {
#ifdef ENABLE_NVML
    nvmlReturn_t result = nvmlInit();
    if (result == NVML_SUCCESS) {
        nvmlInitialized = true;
        return true;
    } else {
        std::cerr << "Ошибка инициализации NVML: " << result << std::endl;
    }
#endif
    nvmlInitialized = false;
    return false;
}

/**
 * @brief Завершает работу с NVML библиотекой
 * 
 * Освобождает ресурсы NVML при завершении работы и сбрасывает флаг инициализации.
 */
void GPUMonitor::shutdownNVML() {
#ifdef ENABLE_NVML
    if (nvmlInitialized) {
        nvmlShutdown();
        nvmlInitialized = false;
    }
#endif
}

/**
 * @brief Инициализирует AMD ADL библиотеку
 * 
 * Пытается инициализировать AMD Display Library для работы с GPU.
 * Устанавливает флаг adlInitialized в зависимости от результата.
 * 
 * @return bool true если инициализация успешна, false в противном случае
 */
bool GPUMonitor::initADL() {
#ifdef ENABLE_ADL
    // ADL initialization code would go here
    // For now, we'll just set the flag
    adlInitialized = true;
    return true;
#endif
    adlInitialized = false;
    return false;
}

/**
 * @brief Завершает работу с AMD ADL библиотекой
 * 
 * Освобождает ресурсы ADL при завершении работы и сбрасывает флаг инициализации.
 */
void GPUMonitor::shutdownADL() {
#ifdef ENABLE_ADL
    if (adlInitialized) {
        // ADL shutdown code would go here
        adlInitialized = false;
    }
#endif
}

/**
 * @brief Инициализирует Intel GPA библиотеку
 * 
 * Пытается инициализировать Intel Graphics Performance Analyzers для работы с GPU.
 * Устанавливает флаг gpaInitialized в зависимости от результата.
 * 
 * @return bool true если инициализация успешна, false в противном случае
 */
bool GPUMonitor::initGPA() {
#ifdef ENABLE_INTEL_GPA
    // Intel GPA initialization code would go here
    // For now, we'll just set the flag
    gpaInitialized = true;
    return true;
#endif
    gpaInitialized = false;
    return false;
}

/**
 * @brief Завершает работу с Intel GPA библиотекой
 * 
 * Освобождает ресурсы Intel GPA при завершении работы и сбрасывает флаг инициализации.
 */
void GPUMonitor::shutdownGPA() {
#ifdef ENABLE_INTEL_GPA
    if (gpaInitialized) {
        // Intel GPA shutdown code would go here
        gpaInitialized = false;
    }
#endif
}

/**
 * @brief Завершает работу со всеми GPU библиотеками
 * 
 * Освобождает ресурсы всех инициализированных GPU библиотек.
 */
void GPUMonitor::shutdownAll() {
    shutdownNVML();
    shutdownADL();
    shutdownGPA();
}

/**
 * @brief Получает информацию обо всех доступных GPU
 * 
 * Собирает данные обо всех графических процессорах системы через доступные библиотеки.
 * Возвращает пустой вектор, если ни одна библиотека не инициализирована или не доступна.
 * 
 * @return std::vector<GPUInfo> Вектор со структурами информации о GPU
 */
std::vector<GPUMonitor::GPUInfo> GPUMonitor::getAllGPUInfo() {
    std::vector<GPUInfo> gpus;
    
#ifdef ENABLE_NVML
    if (!nvmlInitialized) {
        if (!initNVML()) {
            // If NVML init failed, continue to check other libraries
        }
    }
    
    if (nvmlInitialized) {
        unsigned int deviceCount = 0;
        nvmlReturn_t result = nvmlDeviceGetCount(&deviceCount);
        
        if (result == NVML_SUCCESS) {
            for (unsigned int i = 0; i < deviceCount; i++) {
                nvmlDevice_t device;
                result = nvmlDeviceGetHandleByIndex(i, &device);
                
                if (result == NVML_SUCCESS) {
                    GPUInfo gpuInfo;
                    gpuInfo.vendor = "NVIDIA";
                    
                    // Get GPU name
                    char name[NVML_DEVICE_NAME_BUFFER_SIZE];
                    result = nvmlDeviceGetName(device, name, NVML_DEVICE_NAME_BUFFER_SIZE);
                    gpuInfo.name = (result == NVML_SUCCESS) ? std::string(name) : "Unknown NVIDIA GPU";
                    
                    // Get temperature
                    unsigned int temperature;
                    result = nvmlDeviceGetTemperature(device, NVML_TEMPERATURE_GPU, &temperature);
                    gpuInfo.temperature = (result == NVML_SUCCESS) ? temperature : 0;
                    
                    // Get utilization rates
                    nvmlUtilization_t utilization;
                    result = nvmlDeviceGetUtilizationRates(device, &utilization);
                    if (result == NVML_SUCCESS) {
                        gpuInfo.gpuUtilization = utilization.gpu;
                        gpuInfo.memoryUtilization = utilization.memory;
                    } else {
                        gpuInfo.gpuUtilization = 0;
                        gpuInfo.memoryUtilization = 0;
                    }
                    
                    // Get memory info
                    nvmlMemory_t memory;
                    result = nvmlDeviceGetMemoryInfo(device, &memory);
                    if (result == NVML_SUCCESS) {
                        gpuInfo.memoryTotal = memory.total;
                        gpuInfo.memoryUsed = memory.used;
                    } else {
                        gpuInfo.memoryTotal = 0;
                        gpuInfo.memoryUsed = 0;
                    }
                    
                    // Get fan speed
                    unsigned int fanSpeed;
                    result = nvmlDeviceGetFanSpeed(device, &fanSpeed);
                    gpuInfo.fanSpeed = (result == NVML_SUCCESS) ? fanSpeed : 0;
                    
                    gpus.push_back(gpuInfo);
                }
            }
        }
    }
#endif
    
#ifdef ENABLE_ADL
    if (!adlInitialized) {
        if (!initADL()) {
            // If ADL init failed, continue to check other libraries
        }
    }
    
    if (adlInitialized) {
        // AMD GPU detection and information gathering code would go here
        // Placeholder implementation
        GPUInfo gpuInfo;
        gpuInfo.vendor = "AMD";
        gpuInfo.name = "AMD GPU (ADL support placeholder)";
        gpuInfo.temperature = 0;
        gpuInfo.gpuUtilization = 0;
        gpuInfo.memoryUtilization = 0;
        gpuInfo.memoryTotal = 0;
        gpuInfo.memoryUsed = 0;
        gpuInfo.fanSpeed = 0;
        gpus.push_back(gpuInfo);
    }
#endif
    
#ifdef ENABLE_INTEL_GPA
    if (!gpaInitialized) {
        if (!initGPA()) {
            // If GPA init failed, continue to check other libraries
        }
    }
    
    if (gpaInitialized) {
        // Intel GPU detection and information gathering code would go here
        // Placeholder implementation
        GPUInfo gpuInfo;
        gpuInfo.vendor = "Intel";
        gpuInfo.name = "Intel GPU (GPA support placeholder)";
        gpuInfo.temperature = 0;
        gpuInfo.gpuUtilization = 0;
        gpuInfo.memoryUtilization = 0;
        gpuInfo.memoryTotal = 0;
        gpuInfo.memoryUsed = 0;
        gpuInfo.fanSpeed = 0;
        gpus.push_back(gpuInfo);
    }
#endif
    
    // If no GPUs were found, add a generic entry
    if (gpus.empty()) {
        GPUInfo genericGPU;
        genericGPU.vendor = "Unknown";
        genericGPU.name = "No compatible GPU detected";
        genericGPU.temperature = 0;
        genericGPU.gpuUtilization = 0;
        genericGPU.memoryUtilization = 0;
        genericGPU.memoryTotal = 0;
        genericGPU.memoryUsed = 0;
        genericGPU.fanSpeed = 0;
        gpus.push_back(genericGPU);
    }
    
    return gpus;
}

/**
 * @brief Получает информацию об использовании NVIDIA GPU
 * 
 * Собирает и отображает данные о загрузке GPU и памяти для NVIDIA графических процессоров.
 * Если NVML не доступен, выводит сообщение с инструкцией по включению поддержки.
 */
void GPUMonitor::getNVIDIAGPUUsage() {
#ifdef ENABLE_NVML
    if (!nvmlInitialized) {
        if (!initNVML()) {
            std::cout << "Ошибка инициализации NVML" << std::endl;
            return;
        }
    }
    
    unsigned int deviceCount = 0;
    nvmlReturn_t result = nvmlDeviceGetCount(&deviceCount);
    
    if (result != NVML_SUCCESS) {
        std::cout << "Не удалось получить количество GPU устройств" << std::endl;
        return;
    }
    
    std::cout << "Найдено GPU устройств: " << deviceCount << std::endl;
    
    for (unsigned int i = 0; i < deviceCount; i++) {
        nvmlDevice_t device;
        result = nvmlDeviceGetHandleByIndex(i, &device);
        
        if (result != NVML_SUCCESS) {
            std::cout << "Не удалось получить доступ к GPU #" << i << std::endl;
            continue;
        }
        
        char name[NVML_DEVICE_NAME_BUFFER_SIZE];
        result = nvmlDeviceGetName(device, name, NVML_DEVICE_NAME_BUFFER_SIZE);
        std::cout << "\nGPU #" << i << ": " << ((result == NVML_SUCCESS) ? name : "Unknown") << std::endl;
        
        nvmlUtilization_t utilization;
        result = nvmlDeviceGetUtilizationRates(device, &utilization);
        if (result == NVML_SUCCESS) {
            std::cout << "  Загрузка GPU: " << utilization.gpu << "%" << std::endl;
            std::cout << "  Загрузка памяти: " << utilization.memory << "%" << std::endl;
        }
        
        unsigned int temperature;
        result = nvmlDeviceGetTemperature(device, NVML_TEMPERATURE_GPU, &temperature);
        if (result == NVML_SUCCESS) {
            std::cout << "  Температура: " << temperature << "°C" << std::endl;
        }
        
        nvmlMemory_t memory;
        result = nvmlDeviceGetMemoryInfo(device, &memory);
        if (result == NVML_SUCCESS) {
            std::cout << "  Память GPU: " << formatBytes(memory.used) << " / " 
                      << formatBytes(memory.total) << std::endl;
        }
    }
#else
    std::cout << "Поддержка NVML не включена. Для включения добавьте флаг компиляции -DENABLE_NVML" << std::endl;
    std::cout << "Подробнее см. в документации README.md" << std::endl;
#endif
}

/**
 * @brief Получает информацию об использовании AMD GPU
 * 
 * Собирает и отображает данные о загрузке GPU и памяти для AMD графических процессоров.
 * Если ADL не доступен, выводит сообщение с инструкцией по включению поддержки.
 */
void GPUMonitor::getAMDGPUUsage() {
#ifdef ENABLE_ADL
    if (!adlInitialized) {
        if (!initADL()) {
            std::cout << "Ошибка инициализации ADL" << std::endl;
            return;
        }
    }
    
    std::cout << "AMD GPU мониторинг в разработке..." << std::endl;
    // AMD GPU monitoring implementation would go here
#else
    std::cout << "Поддержка AMD ADL не включена. Для включения добавьте флаг компиляции -DENABLE_ADL" << std::endl;
    std::cout << "Подробнее см. в документации README.md" << std::endl;
#endif
}

/**
 * @brief Получает информацию об использовании Intel GPU
 * 
 * Собирает и отображает данные о загрузке GPU и памяти для Intel графических процессоров.
 * Если Intel GPA не доступен, выводит сообщение с инструкцией по включению поддержки.
 */
void GPUMonitor::getIntelGPUUsage() {
#ifdef ENABLE_INTEL_GPA
    if (!gpaInitialized) {
        if (!initGPA()) {
            std::cout << "Ошибка инициализации Intel GPA" << std::endl;
            return;
        }
    }
    
    std::cout << "Intel GPU мониторинг в разработке..." << std::endl;
    // Intel GPU monitoring implementation would go here
#else
    std::cout << "Поддержка Intel GPA не включена. Для включения добавьте флаг компиляции -DENABLE_INTEL_GPA" << std::endl;
    std::cout << "Подробнее см. в документации README.md" << std::endl;
#endif
}

/**
 * @brief Выводит информацию о GPU в консоль
 * 
 * Отображает информацию о доступных графических процессорах и
 * инструкции по включению расширенного мониторинга.
 */
void GPUMonitor::printGPUInfo() {
    std::cout << "\n=== Информация о GPU ===" << std::endl;
    
    auto gpus = getAllGPUInfo();
    
    if (gpus.empty() || (gpus.size() == 1 && gpus[0].vendor == "Unknown")) {
        std::cout << "Для мониторинга GPU требуются дополнительные библиотеки:" << std::endl;
        std::cout << "- NVIDIA: NVML (NVIDIA Management Library)" << std::endl;
        std::cout << "- AMD: ADL SDK (AMD Display Library)" << std::endl;
        std::cout << "- Intel: Intel Graphics Performance Analyzers" << std::endl;
        std::cout << "\nДля включения поддержки GPU:" << std::endl;
        std::cout << "1. Установите соответствующие драйверы GPU" << std::endl;
        std::cout << "2. Скачайте необходимые SDK в директорию libs/" << std::endl;
        std::cout << "3. Соберите с соответствующими флагами (-DENABLE_NVML, -DENABLE_ADL, -DENABLE_INTEL_GPA)" << std::endl;
        return;
    }
    
    bool hasGPUs = false;
    
    for (size_t i = 0; i < gpus.size(); i++) {
        const auto& gpu = gpus[i];
        
        // Skip generic unknown entries
        if (gpu.vendor == "Unknown" && gpu.name == "No compatible GPU detected") {
            continue;
        }
        
        hasGPUs = true;
        std::cout << "\nGPU #" << i << " (" << gpu.vendor << "): " << gpu.name << std::endl;
        std::cout << "  Загрузка GPU: " << gpu.gpuUtilization << "%" << std::endl;
        std::cout << "  Загрузка памяти: " << gpu.memoryUtilization << "%" << std::endl;
        std::cout << "  Температура: " << gpu.temperature << "°C" << std::endl;
        std::cout << "  Память GPU: " << formatBytes(gpu.memoryUsed) << " / " 
                  << formatBytes(gpu.memoryTotal) << std::endl;
        std::cout << "  Скорость вентилятора: " << gpu.fanSpeed << "%" << std::endl;
    }
    
    if (!hasGPUs) {
        std::cout << "Не удалось обнаружить совместимые GPU устройства" << std::endl;
        std::cout << "\nДля мониторинга GPU требуются дополнительные библиотеки:" << std::endl;
        std::cout << "- NVIDIA: NVML (NVIDIA Management Library)" << std::endl;
        std::cout << "- AMD: ADL SDK (AMD Display Library)" << std::endl;
        std::cout << "- Intel: Intel Graphics Performance Analyzers" << std::endl;
    }
}

/**
 * @brief Форматирует количество байт в удобочитаемый формат
 * 
 * @param bytes Количество байт
 * @return std::string Отформатированная строка с размером
 */
std::string GPUMonitor::formatBytes(unsigned long long bytes) {
    const char* units[] = {"B", "KB", "MB", "GB", "TB"};
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