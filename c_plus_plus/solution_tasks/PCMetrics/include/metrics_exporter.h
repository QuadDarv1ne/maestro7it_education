#ifndef METRICS_EXPORTER_H
#define METRICS_EXPORTER_H

#include <string>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <ctime>
#include "../include/cpu_monitor.h"
#include "../include/memory_monitor.h"
#include "../include/disk_monitor.h"
#include "../include/gpu_monitor.h"

/**
 * @class MetricsExporter
 * @brief Класс для экспорта системных метрик в различные форматы
 * 
 * MetricsExporter предоставляет функции для экспорта собранной информации
 * о системе в форматы CSV и JSON для дальнейшего анализа.
 */
class MetricsExporter {
public:
    /**
     * @brief Экспортирует метрики в формат CSV
     * 
     * Создает CSV файл с текущими метриками системы, включая информацию
     * о CPU, памяти, дисках и GPU.
     * 
     * @param filename Имя файла для экспорта
     * @param cpuMonitor Ссылка на монитор CPU
     * @param memMonitor Ссылка на монитор памяти
     * @param diskMonitor Ссылка на монитор дисков
     * @param gpuMonitor Ссылка на монитор GPU
     * @return bool true если экспорт успешен, false в противном случае
     */
    static bool exportToCSV(const std::string& filename, 
                           const CPUMonitor& cpuMonitor,
                           const MemoryMonitor& memMonitor,
                           const DiskMonitor& diskMonitor,
                           const GPUMonitor& gpuMonitor);
    
    /**
     * @brief Экспортирует метрики в формат JSON
     * 
     * Создает JSON файл с текущими метриками системы.
     * 
     * @param filename Имя файла для экспорта
     * @param cpuMonitor Ссылка на монитор CPU
     * @param memMonitor Ссылка на монитор памяти
     * @param diskMonitor Ссылка на монитор дисков
     * @param gpuMonitor Ссылка на монитор GPU
     * @return bool true если экспорт успешен, false в противном случае
     */
    static bool exportToJSON(const std::string& filename,
                            const CPUMonitor& cpuMonitor,
                            const MemoryMonitor& memMonitor,
                            const DiskMonitor& diskMonitor,
                            const GPUMonitor& gpuMonitor);
    
private:
    /**
     * @brief Получает текущую временную метку
     * 
     * @return std::string Строка с текущей датой и временем в формате YYYY-MM-DD HH:MM:SS
     */
    static std::string getCurrentTimestamp();
    
    /**
     * @brief Экранирует поле CSV
     * 
     * Добавляет кавычки вокруг поля и удваивает внутренние кавычки при необходимости.
     * 
     * @param field Поле для экранирования
     * @return std::string Экранированное поле
     */
    static std::string escapeCSVField(const std::string& field);
    
    /**
     * @brief Форматирует строковое значение для JSON
     * 
     * @param key Ключ JSON
     * @param value Значение JSON
     * @param isLast Флаг, указывающий, является ли это последним элементом
     * @return std::string Отформатированная строка JSON
     */
    static std::string formatJSONValue(const std::string& key, const std::string& value, bool isLast = false);
    
    /**
     * @brief Форматирует числовое значение для JSON
     * 
     * @param key Ключ JSON
     * @param value Числовое значение
     * @param isLast Флаг, указывающий, является ли это последним элементом
     * @return std::string Отформатированная строка JSON
     */
    static std::string formatJSONNumber(const std::string& key, double value, bool isLast = false);
};

#endif // METRICS_EXPORTER_H