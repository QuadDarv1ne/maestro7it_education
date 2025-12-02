/**
 * @file network_monitor.cpp
 * @brief Реализация класса NetworkMonitor
 */

#include "../include/network_monitor.h"
#include "../include/logger.h"
#include "../include/color_output.h"
#include <iomanip>
#include <sstream>

/**
 * @brief Конструктор класса NetworkMonitor
 */
NetworkMonitor::NetworkMonitor() {
    Logger::getInstance().debug("NetworkMonitor создан");
}

/**
 * @brief Деструктор класса NetworkMonitor
 */
NetworkMonitor::~NetworkMonitor() {
    Logger::getInstance().debug("NetworkMonitor уничтожен");
}

/**
 * @brief Получает список сетевых интерфейсов
 * 
 * @return std::vector<NetworkInfo> Вектор с информацией о сетевых интерфейсах
 */
std::vector<NetworkInfo> NetworkMonitor::getNetworkInterfaces() {
    interfaces.clear();
    
    ULONG bufferSize = 0;
    DWORD result = GetIfTable(NULL, &bufferSize, FALSE);
    
    if (result != ERROR_INSUFFICIENT_BUFFER) {
        Logger::getInstance().error("Не удалось получить размер буфера для сетевых интерфейсов");
        return interfaces;
    }
    
    MIB_IFTABLE* ifTable = (MIB_IFTABLE*)malloc(bufferSize);
    if (ifTable == NULL) {
        Logger::getInstance().error("Не удалось выделить память");
        return interfaces;
    }
    
    result = GetIfTable(ifTable, &bufferSize, FALSE);
    if (result != NO_ERROR) {
        Logger::getInstance().error("Ошибка при получении таблицы интерфейсов");
        free(ifTable);
        return interfaces;
    }
    
    for (DWORD i = 0; i < ifTable->dwNumEntries; i++) {
        MIB_IFROW& row = ifTable->table[i];
        
        NetworkInfo info;
        info.name = std::string(reinterpret_cast<char*>(row.bDescr), row.dwDescrLen);
        info.description = info.name;
        info.bytesReceived = row.dwInOctets;
        info.bytesSent = row.dwOutOctets;
        info.speed = row.dwSpeed;
        info.isUp = (row.dwOperStatus == IF_OPER_STATUS_OPERATIONAL);
        
        // Фильтруем loopback и неактивные интерфейсы
        if (row.dwType != IF_TYPE_SOFTWARE_LOOPBACK && info.isUp) {
            interfaces.push_back(info);
        }
    }
    
    free(ifTable);
    Logger::getInstance().debug("Найдено активных интерфейсов: " + std::to_string(interfaces.size()));
    
    return interfaces;
}

/**
 * @brief Выводит информацию о сетевых интерфейсах
 */
void NetworkMonitor::printNetworkInfo() {
    getNetworkInterfaces();
    
    std::cout << "\n=== Сетевые интерфейсы ===" << std::endl;
    
    if (interfaces.empty()) {
        ColorOutput::print("Активные сетевые интерфейсы не найдены\n", ColorOutput::Color::YELLOW);
        return;
    }
    
    for (size_t i = 0; i < interfaces.size(); i++) {
        const NetworkInfo& info = interfaces[i];
        
        std::cout << "\n[" << (i + 1) << "] " << info.name << std::endl;
        std::cout << "  Статус: ";
        
        if (info.isUp) {
            ColorOutput::print("Активен\n", ColorOutput::Color::GREEN);
        } else {
            ColorOutput::print("Неактивен\n", ColorOutput::Color::RED);
        }
        
        if (info.speed > 0) {
            double speedMbps = info.speed / 1000000.0;
            std::cout << "  Скорость: " << std::fixed << std::setprecision(0) 
                      << speedMbps << " Мбит/с" << std::endl;
        }
        
        std::cout << "  Получено: " << formatDataSize(info.bytesReceived) << std::endl;
        std::cout << "  Отправлено: " << formatDataSize(info.bytesSent) << std::endl;
        
        unsigned long long total = info.bytesReceived + info.bytesSent;
        std::cout << "  Всего: " << formatDataSize(total) << std::endl;
    }
    
    // Общая статистика
    unsigned long long totalReceived = 0, totalSent = 0;
    getTotalNetworkStats(totalReceived, totalSent);
    
    std::cout << "\n=== Общая статистика сети ===" << std::endl;
    std::cout << "Всего получено: " << formatDataSize(totalReceived) << std::endl;
    std::cout << "Всего отправлено: " << formatDataSize(totalSent) << std::endl;
    std::cout << "Общий трафик: " << formatDataSize(totalReceived + totalSent) << std::endl;
}

/**
 * @brief Получает общую статистику сети
 * 
 * @param totalReceived Общее количество принятых байт
 * @param totalSent Общее количество отправленных байт
 */
void NetworkMonitor::getTotalNetworkStats(unsigned long long& totalReceived, unsigned long long& totalSent) {
    totalReceived = 0;
    totalSent = 0;
    
    for (const auto& info : interfaces) {
        totalReceived += info.bytesReceived;
        totalSent += info.bytesSent;
    }
}

/**
 * @brief Форматирует размер данных в читаемый вид
 * 
 * @param bytes Размер в байтах
 * @return std::string Отформатированная строка
 */
std::string NetworkMonitor::formatDataSize(unsigned long long bytes) {
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
