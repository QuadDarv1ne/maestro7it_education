#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <windows.h>

/**
 * @file utils.h
 * @brief Вспомогательные утилиты для проекта PCMetrics
 * @author PCMetrics Team
 * @date 2025
 */

namespace Utils {
    /**
     * @brief Конвертирует широкую строку (wstring) в обычную строку (string)
     * 
     * Использует Windows API для корректной конвертации Unicode строк.
     * Это безопасная альтернатива устаревшему std::wstring_convert.
     * 
     * @param wstr Широкая строка для конвертации
     * @return std::string Сконвертированная UTF-8 строка
     */
    inline std::string wstringToString(const std::wstring& wstr) {
        if (wstr.empty()) return std::string();
        
        int size_needed = WideCharToMultiByte(CP_UTF8, 0, &wstr[0], 
                                              (int)wstr.size(), NULL, 0, NULL, NULL);
        if (size_needed <= 0) return std::string();
        
        std::string strTo(size_needed, 0);
        WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), 
                           &strTo[0], size_needed, NULL, NULL);
        return strTo;
    }

    /**
     * @brief Конвертирует обычную строку (string) в широкую строку (wstring)
     * 
     * Использует Windows API для корректной конвертации UTF-8 строк.
     * 
     * @param str UTF-8 строка для конвертации
     * @return std::wstring Сконвертированная широкая строка
     */
    inline std::wstring stringToWstring(const std::string& str) {
        if (str.empty()) return std::wstring();
        
        int size_needed = MultiByteToWideChar(CP_UTF8, 0, &str[0], 
                                              (int)str.size(), NULL, 0);
        if (size_needed <= 0) return std::wstring();
        
        std::wstring wstrTo(size_needed, 0);
        MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), 
                           &wstrTo[0], size_needed);
        return wstrTo;
    }

    /**
     * @brief Форматирует размер в байтах в читаемый формат
     * 
     * @param bytes Размер в байтах
     * @param precision Количество знаков после запятой
     * @return std::string Отформатированная строка (например, "1.5 GB")
     */
    inline std::string formatBytes(unsigned long long bytes, int precision = 2) {
        const char* units[] = {"B", "KB", "MB", "GB", "TB"};
        int unitIndex = 0;
        double size = static_cast<double>(bytes);
        
        while (size >= 1024.0 && unitIndex < 4) {
            size /= 1024.0;
            unitIndex++;
        }
        
        char buffer[64];
        snprintf(buffer, sizeof(buffer), "%.*f %s", precision, size, units[unitIndex]);
        return std::string(buffer);
    }

    /**
     * @brief Проверяет, является ли строка валидным путём
     * 
     * @param path Путь для проверки
     * @return bool true если путь валиден и существует, false в противном случае
     */
    inline bool isValidPath(const std::string& path) {
        if (path.empty()) return false;
        DWORD attrib = GetFileAttributesA(path.c_str());
        return (attrib != INVALID_FILE_ATTRIBUTES);
    }

    /**
     * @brief Получает текущее время в формате строки
     * 
     * @param format Формат времени (по умолчанию "%Y-%m-%d %H:%M:%S")
     * @return std::string Отформатированная строка времени
     */
    inline std::string getCurrentTimeString(const char* format = "%Y-%m-%d %H:%M:%S") {
        time_t now = time(nullptr);
        struct tm timeinfo;
        localtime_s(&timeinfo, &now);
        
        char buffer[80];
        strftime(buffer, sizeof(buffer), format, &timeinfo);
        return std::string(buffer);
    }
}

#endif // UTILS_H
