/*
 * PCMetrics - Мониторинг системных ресурсов
 * Version: 1.0.0
 * Author: Your Name
 * License: MIT
 */

#include <iostream>
#include <locale>
#include <clocale>
#include <windows.h>
#include "../include/cpu_monitor.h"
#include "../include/disk_monitor.h"
#include "../include/memory_monitor.h"
#include "../include/gpu_monitor.h"

#ifdef _WIN32
#include <windows.h>
#endif

// using namespace std;

/**
 * @brief Функция для настройки кодировки консоли
 * 
 * Настраивает консоль для корректного отображения UTF-8 символов
 * на разных операционных системах.
 */
void setupConsoleEncoding() {
    #ifdef _WIN32
    // Для Windows устанавливаем кодовую страницу UTF-8
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    #else
    // Для Linux используем более простой подход с локалями
    // Пробуем установить стандартную UTF-8 локаль
    try {
        std::locale::global(std::locale("C.UTF-8"));
    } catch (const std::exception& e) {
        try {
            // Альтернативный вариант для некоторых систем
            std::locale::global(std::locale("en_US.UTF-8"));
        } catch (const std::exception& e) {
            // Если не удалось установить локаль, продолжаем без нее
            std::cerr << "Предупреждение: не удалось установить локаль UTF-8: " 
                      << e.what() << std::endl;
        }
    }
    std::cout.imbue(std::locale());
    #endif
}

void printHeader() {
    std::cout << "======================================" << std::endl;
    std::cout << "         PCMetrics v1.0.0            " << std::endl;
    std::cout << "  Мониторинг системных ресурсов ПК   " << std::endl;
    std::cout << "======================================" << std::endl;
}

void printSeparator() {
    std::cout << "\n--------------------------------------\n" << std::endl;
}

int main() {
    // Установка кодировки для корректного отображения русского текста
    // SetConsoleOutputCP(CP_UTF8);
    // setlocale(LC_ALL, "Russian");
    
    // Настройка кодировки консоли
    setupConsoleEncoding();
    
    printHeader();
    
    // CPU мониторинг
    printSeparator();
    CPUMonitor cpuMonitor;
    std::cout << "=== Информация о процессоре ===" << std::endl;
    cpuMonitor.getCPUInfo();
    
    std::cout << "\nМониторинг загрузки CPU (5 секунд)..." << std::endl;
    for (int i = 0; i < 5; i++) {
        Sleep(1000);
        double usage = cpuMonitor.getCPUUsage();
        std::cout << "[" << (i+1) << "/5] CPU загрузка: " 
                  << std::fixed << std::setprecision(2) 
                  << usage << "%" << std::endl;
    }
    
    // Память
    printSeparator();
    MemoryMonitor memMonitor;
    memMonitor.printMemoryInfo();
    
    // Диски
    printSeparator();
    DiskMonitor diskMonitor;
    diskMonitor.printDiskInfo();
    
    // GPU (базовая информация)
    printSeparator();
    GPUMonitor gpuMonitor;
    gpuMonitor.printGPUInfo();
    
    // Завершение
    std::cout << "\n======================================" << std::endl;
    std::cout << "  Мониторинг завершен успешно!" << std::endl;
    std::cout << "======================================" << std::endl;
    
    std::cout << "\nНажмите любую клавишу для выхода..." << std::endl;
    std::cin.get();
    
    return 0;
}