/*
 * PCMetrics - Мониторинг системных ресурсов
 * Version: 1.0.0
 * Author: Your Name
 * License: MIT
 */

#include <iostream>
#include <windows.h>
#include "../include/cpu_monitor.h"
#include "../include/disk_monitor.h"
#include "../include/memory_monitor.h"
#include "../include/gpu_monitor.h"

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
    SetConsoleOutputCP(CP_UTF8);
    setlocale(LC_ALL, "Russian");
    
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