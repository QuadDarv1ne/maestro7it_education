#include "../include/gpu_monitor.h"
#include <iostream>
#include <iomanip>

#ifdef ENABLE_NVML
#include <nvml.h>
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
 * @brief Получает информацию обо всех доступных GPU
 * 
 * Собирает данные обо всех графических процессорах системы через NVML.
 * Возвращает пустой вектор, если NVML не инициализирован или не доступен.
 * 
 * @return std::vector<GPUInfo> Вектор со структурами информации о GPU
 */
std::vector<GPUMonitor::GPUInfo> GPUMonitor::getAllGPUInfo() {
    std::vector<GPUInfo> gpus;
    
#ifdef ENABLE_NVML
    if (!nvmlInitialized) {
        if (!initNVML()) {
            return gpus; // Return empty vector if NVML init failed
        }
    }
    
    unsigned int deviceCount = 0;
    nvmlReturn_t result = nvmlDeviceGetCount(&deviceCount);
    
    if (result != NVML_SUCCESS) {
        return gpus;
    }
    
    for (unsigned int i = 0; i < deviceCount; i++) {
        nvmlDevice_t device;
        result = nvmlDeviceGetHandleByIndex(i, &device);
        
        if (result != NVML_SUCCESS) {
            continue;
        }
        
        GPUInfo gpuInfo;
        
        // Get GPU name
        char name[NVML_DEVICE_NAME_BUFFER_SIZE];
        result = nvmlDeviceGetName(device, name, NVML_DEVICE_NAME_BUFFER_SIZE);
        gpuInfo.name = (result == NVML_SUCCESS) ? std::string(name) : "Unknown";
        
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
#endif
    
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
            std::cout << "  Память GPU: " << (memory.used / (1024*1024)) << " / " 
                      << (memory.total / (1024*1024)) << " МБ" << std::endl;
        }
    }
#else
    std::cout << "Поддержка NVML не включена. Для включения добавьте флаг компиляции -DENABLE_NVML" << std::endl;
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
    
#ifdef ENABLE_NVML
    auto gpus = getAllGPUInfo();
    
    if (gpus.empty()) {
        std::cout << "NVIDIA GPU устройства не найдены или драйвер не установлен" << std::endl;
        return;
    }
    
    for (size_t i = 0; i < gpus.size(); i++) {
        const auto& gpu = gpus[i];
        std::cout << "\nGPU #" << i << ": " << gpu.name << std::endl;
        std::cout << "  Загрузка GPU: " << gpu.gpuUtilization << "%" << std::endl;
        std::cout << "  Загрузка памяти: " << gpu.memoryUtilization << "%" << std::endl;
        std::cout << "  Температура: " << gpu.temperature << "°C" << std::endl;
        std::cout << "  Память GPU: " << (gpu.memoryUsed / (1024*1024)) << " / " 
                  << (gpu.memoryTotal / (1024*1024)) << " МБ" << std::endl;
        std::cout << "  Скорость вентилятора: " << gpu.fanSpeed << "%" << std::endl;
    }
#else
    std::cout << "Для мониторинга GPU требуются дополнительные библиотеки:" << std::endl;
    std::cout << "- NVIDIA: NVML (NVIDIA Management Library)" << std::endl;
    std::cout << "- AMD: ADL SDK (AMD Display Library)" << std::endl;
    std::cout << "- Intel: Intel Graphics Performance Analyzers" << std::endl;
    std::cout << "\nДля включения поддержки NVIDIA GPU:" << std::endl;
    std::cout << "1. Установите NVIDIA драйверы" << std::endl;
    std::cout << "2. Скачайте NVIDIA NVML SDK" << std::endl;
    std::cout << "3. Соберите с флагом -DENABLE_NVML" << std::endl;
#endif
}