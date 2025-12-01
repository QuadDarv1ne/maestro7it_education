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
#include <conio.h>  // For _kbhit() and _getch()
#include <iomanip>  // For std::setprecision
#include "../include/cpu_monitor.h"
#include "../include/disk_monitor.h"
#include "../include/memory_monitor.h"
#include "../include/gpu_monitor.h"
#include "../include/metrics_exporter.h"
#include "../include/logger.h"

#ifdef _WIN32
#include <windows.h>
#endif

// Forward declarations for helper functions
void setupConsoleEncoding();
void printHeader();
void printSeparator();
void printContinuousMonitoringInstructions();
void continuousMonitoringMode(CPUMonitor& cpuMonitor, MemoryMonitor& memMonitor, 
                             DiskMonitor& diskMonitor, GPUMonitor& gpuMonitor);

/**
 * @brief Отображает меню экпорта метрик
 * 
 * Позволяет пользователю выбрать формат экспорта (CSV или JSON)
 * и сохранить текущие метрики системы в файл.
 * 
 * @param cpuMonitor Ссылка на монитор CPU
 * @param memMonitor Ссылка на монитор памяти
 * @param diskMonitor Ссылка на монитор дисков
 * @param gpuMonitor Ссылка на монитор GPU
 */
void showExportMenu(CPUMonitor& cpuMonitor, MemoryMonitor& memMonitor, 
                   DiskMonitor& diskMonitor, GPUMonitor& gpuMonitor) {
    Logger::getInstance().info("Отображение меню экспорта метрик");
    
    std::cout << "\n=== Экспорт метрик ===" << std::endl;
    std::cout << "Выберите формат экспорта:" << std::endl;
    std::cout << "1. CSV (значения, разделенные запятыми)" << std::endl;
    std::cout << "2. JSON (JavaScript Object Notation)" << std::endl;
    std::cout << "3. Отмена" << std::endl;
    std::cout << "Введите ваш выбор (1-3): ";
    
    int choice;
    std::cin >> choice;
    
    if (choice == 1 || choice == 2) {
        std::string filename;
        std::cout << "Введите имя файла (например, metrics.csv или metrics.json): ";
        std::cin >> filename;
        
        bool success = false;
        if (choice == 1) {
            Logger::getInstance().info("Экспорт метрик в формат CSV: " + filename);
            success = MetricsExporter::exportToCSV(filename, cpuMonitor, memMonitor, diskMonitor, gpuMonitor);
            if (success) {
                std::cout << "Метрики успешно экспортированы в " << filename << std::endl;
                Logger::getInstance().info("Метрики успешно экспортированы в " + filename);
            } else {
                std::cout << "Ошибка при экспорте в " << filename << std::endl;
                Logger::getInstance().error("Ошибка при экспорте в " + filename);
            }
        } else if (choice == 2) {
            Logger::getInstance().info("Экспорт метрик в формат JSON: " + filename);
            success = MetricsExporter::exportToJSON(filename, cpuMonitor, memMonitor, diskMonitor, gpuMonitor);
            if (success) {
                std::cout << "Метрики успешно экспортированы в " << filename << std::endl;
                Logger::getInstance().info("Метрики успешно экспортированы в " + filename);
            } else {
                std::cout << "Ошибка при экспорте в " << filename << std::endl;
                Logger::getInstance().error("Ошибка при экспорте в " + filename);
            }
        }
    } else {
        Logger::getInstance().info("Экспорт метрик отменен пользователем");
    }
}

/**
 * @brief Основная точка входа в программу
 * 
 * Выполняет инициализацию всех мониторов, собирает информацию о системе,
 * предоставляет пользователю опции для экспорта данных и непрерывного мониторинга.
 * 
 * @return int Код возврата программы (0 при успешном завершении)
 */
int main() {
    // Инициализация логгера
    Logger::getInstance().initialize("pcmetrics.log", Logger::LogLevel::INFO, true);
    Logger::getInstance().info("Запуск PCMetrics v1.0.0");
    
    // Установка кодировки для корректного отображения русского текста
    // SetConsoleOutputCP(CP_UTF8);
    // setlocale(LC_ALL, "Russian");
    
    // Настройка кодировки консоли
    setupConsoleEncoding();
    
    printHeader();
    Logger::getInstance().info("Отображение заголовка программы");
    
    // CPU мониторинг
    printSeparator();
    Logger::getInstance().info("Инициализация монитора CPU");
    CPUMonitor cpuMonitor;
    std::cout << "=== Информация о процессоре ===" << std::endl;
    cpuMonitor.getCPUInfo();
    
    std::cout << "\nМониторинг загрузки CPU (5 секунд)..." << std::endl;
    Logger::getInstance().info("Начало мониторинга загрузки CPU");
    for (int i = 0; i < 5; i++) {
        Sleep(1000);
        double usage = cpuMonitor.getCPUUsage();
        std::cout << "[" << (i+1) << "/5] CPU загрузка: " 
                  << std::fixed << std::setprecision(2) 
                  << usage << "%" << std::endl;
    }
    Logger::getInstance().info("Завершение мониторинга загрузки CPU");
    
    // Память
    printSeparator();
    Logger::getInstance().info("Инициализация монитора памяти");
    MemoryMonitor memMonitor;
    memMonitor.printMemoryInfo();
    
    // Диски
    printSeparator();
    Logger::getInstance().info("Инициализация монитора дисков");
    DiskMonitor diskMonitor;
    diskMonitor.printDiskInfo();
    
    // GPU (базовая информация)
    printSeparator();
    Logger::getInstance().info("Инициализация монитора GPU");
    GPUMonitor gpuMonitor;
    gpuMonitor.printGPUInfo();
    
    // Export option
    std::cout << "\nХотите экспортировать метрики? (y/n): ";
    char exportChoice;
    std::cin >> exportChoice;
    
    if (exportChoice == 'y' || exportChoice == 'Y') {
        showExportMenu(cpuMonitor, memMonitor, diskMonitor, gpuMonitor);
    }
    
    // Continuous monitoring option
    std::cout << "\nХотите перейти в режим непрерывного мониторинга? (y/n): ";
    char choice;
    std::cin >> choice;
    
    if (choice == 'y' || choice == 'Y') {
        Logger::getInstance().info("Переход в режим непрерывного мониторинга");
        continuousMonitoringMode(cpuMonitor, memMonitor, diskMonitor, gpuMonitor);
    }
    
    // Завершение
    std::cout << "\n======================================" << std::endl;
    std::cout << "  Мониторинг завершен успешно!" << std::endl;
    std::cout << "======================================" << std::endl;
    
    std::cout << "\nНажмите любую клавишу для выхода..." << std::endl;
    std::cin.get();
    if (std::cin.peek() == '\n') std::cin.get(); // Handle newline character
    std::cin.get();
    
    Logger::getInstance().info("Завершение работы PCMetrics");
    return 0;
}

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

/**
 * @brief Выводит заголовок программы
 * 
 * Отображает приветственное сообщение и информацию о версии программы.
 */
void printHeader() {
    std::cout << "======================================" << std::endl;
    std::cout << "         PCMetrics v1.0.0            " << std::endl;
    std::cout << "  Мониторинг системных ресурсов ПК   " << std::endl;
    std::cout << "======================================" << std::endl;
}

/**
 * @brief Выводит разделитель между секциями
 * 
 * Используется для визуального разделения различных секций вывода программы.
 */
void printSeparator() {
    std::cout << "\n--------------------------------------\n" << std::endl;
}

/**
 * @brief Выводит инструкции для режима непрерывного мониторинга
 * 
 * Отображает информацию о том, как управлять режимом непрерывного мониторинга.
 */
void printContinuousMonitoringInstructions() {
    std::cout << "\n=== Режим непрерывного мониторинга ===" << std::endl;
    std::cout << "Нажмите 'q' или 'Q' для выхода из режима непрерывного мониторинга" << std::endl;
    std::cout << "Нажмите любую другую клавишу для паузы/продолжения" << std::endl;
}

/**
 * @brief Режим непрерывного мониторинга системы
 * 
 * Обеспечивает реальное время обновление информации о системе с возможностью
 * паузы и возобновления мониторинга.
 * 
 * @param cpuMonitor Ссылка на монитор CPU
 * @param memMonitor Ссылка на монитор памяти
 * @param diskMonitor Ссылка на монитор дисков
 * @param gpuMonitor Ссылка на монитор GPU
 */
void continuousMonitoringMode(CPUMonitor& cpuMonitor, MemoryMonitor& memMonitor, 
                             DiskMonitor& diskMonitor, GPUMonitor& gpuMonitor) {
    printContinuousMonitoringInstructions();
    
    bool paused = false;
    int updateInterval = 1000; // 1 second
    
    while (true) {
        if (_kbhit()) {
            char ch = _getch();
            if (ch == 'q' || ch == 'Q') {
                Logger::getInstance().info("Выход из режима непрерывного мониторинга");
                break; // Exit continuous monitoring mode
            } else {
                paused = !paused;
                if (paused) {
                    Logger::getInstance().info("Пауза в режиме непрерывного мониторинга");
                    std::cout << "\n[ПАУЗА] Мониторинг приостановлен. Нажмите любую клавишу для продолжения." << std::endl;
                } else {
                    Logger::getInstance().info("Возобновление режима непрерывного мониторинга");
                    std::cout << "\n[ВОЗОБНОВЛЕНИЕ] Мониторинг продолжается..." << std::endl;
                }
            }
        }
        
        if (!paused) {
            // Clear screen (Windows specific)
            system("cls");
            
            // Print header
            printHeader();
            
            // CPU monitoring
            std::cout << "\n=== Загрузка процессора ===" << std::endl;
            double cpuUsage = cpuMonitor.getCPUUsage();
            std::cout << "CPU загрузка: " << std::fixed << std::setprecision(2) 
                      << cpuUsage << "%" << std::endl;
            
            // Memory monitoring
            std::cout << "\n=== Использование памяти ===" << std::endl;
            auto memInfo = memMonitor.getMemoryInfo();
            std::cout << "Использование RAM: " << memInfo.memoryLoad << "%" << std::endl;
            std::cout << "Доступно: " << (memInfo.availPhys / (1024*1024*1024)) << " ГБ из " 
                      << (memInfo.totalPhys / (1024*1024*1024)) << " ГБ" << std::endl;
            
            // Disk monitoring (show only C: drive for brevity)
            std::cout << "\n=== Использование диска C: ===" << std::endl;
            auto disks = diskMonitor.getDiskInfo();
            for (const auto& disk : disks) {
                if (disk.drive.find(L"C:") != std::wstring::npos) {
                    std::wcout << L"Диск C: использовано " << std::fixed << std::setprecision(2) 
                              << disk.usagePercent << L"%" << std::endl;
                    break;
                }
            }
            
            // GPU monitoring
            std::cout << "\n=== Загрузка GPU ===" << std::endl;
#ifdef ENABLE_NVML
            gpuMonitor.getNVIDIAGPUUsage();
#else
            std::cout << "GPU мониторинг недоступен (не включена поддержка NVML)" << std::endl;
#endif
            
            std::cout << "\nОбновление каждые " << (updateInterval/1000) << " секунд..." << std::endl;
            std::cout << "Нажмите 'q' для выхода, любую другую клавишу для паузы" << std::endl;
        }
        
        Sleep(updateInterval);
    }
}