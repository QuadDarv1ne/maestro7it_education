/**
 * @file network_monitor.h
 * @brief Мониторинг сетевых интерфейсов и статистики
 * @author PCMetrics Team
 * @date 2025
 */

#ifndef NETWORK_MONITOR_H
#define NETWORK_MONITOR_H

#include <windows.h>
#include <iphlpapi.h>
#include <iostream>
#include <string>
#include <vector>

// Для MSVC линковка библиотеки
#ifdef _MSC_VER
#pragma comment(lib, "iphlpapi.lib")
#endif

/**
 * @struct NetworkInfo
 * @brief Структура для хранения информации о сетевом интерфейсе
 */
struct NetworkInfo {
    std::string name;              ///< Имя интерфейса
    std::string description;       ///< Описание интерфейса
    unsigned long long bytesReceived;  ///< Байт получено
    unsigned long long bytesSent;      ///< Байт отправлено
    unsigned long speed;           ///< Скорость интерфейса (бит/с)
    bool isUp;                     ///< Статус интерфейса
};

/**
 * @class NetworkMonitor
 * @brief Класс для мониторинга сетевых интерфейсов
 * 
 * Предоставляет методы для получения информации о сетевых интерфейсах,
 * статистики трафика и скорости передачи данных
 */
class NetworkMonitor {
private:
    std::vector<NetworkInfo> interfaces;  ///< Список сетевых интерфейсов
    
public:
    /**
     * @brief Конструктор класса NetworkMonitor
     */
    NetworkMonitor();
    
    /**
     * @brief Деструктор класса NetworkMonitor
     */
    ~NetworkMonitor();
    
    /**
     * @brief Получает список сетевых интерфейсов
     * 
     * @return std::vector<NetworkInfo> Вектор с информацией о сетевых интерфейсах
     */
    std::vector<NetworkInfo> getNetworkInterfaces();
    
    /**
     * @brief Выводит информацию о сетевых интерфейсах
     */
    void printNetworkInfo();
    
    /**
     * @brief Получает общую статистику сети
     * 
     * @param totalReceived Общее количество принятых байт
     * @param totalSent Общее количество отправленных байт
     */
    void getTotalNetworkStats(unsigned long long& totalReceived, unsigned long long& totalSent);
    
    /**
     * @brief Форматирует размер данных в читаемый вид
     * 
     * @param bytes Размер в байтах
     * @return std::string Отформатированная строка
     */
    std::string formatDataSize(unsigned long long bytes);
};

#endif // NETWORK_MONITOR_H
