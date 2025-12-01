#ifndef DISK_MONITOR_H
#define DISK_MONITOR_H

#include <windows.h>
#include <pdh.h>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>

/**
 * @class DiskMonitor
 * @brief Класс для мониторинга дисковой подсистемы
 * 
 * DiskMonitor предоставляет функции для получения информации о всех
 * подключенных дисках системы, включая использование пространства,
 * типы дисков и производительность.
 */
class DiskMonitor {
public:
    /**
     * @struct DiskInfo
     * @brief Структура для хранения информации о диске
     * 
     * Содержит данные о конкретном диске системы.
     */
    struct DiskInfo {
        std::wstring drive;      ///< Буква диска и путь (например, L"C:\\")
        ULONGLONG totalSpace;    ///< Общий объем диска в байтах
        ULONGLONG freeSpace;     ///< Свободное место на диске в байтах
        ULONGLONG usedSpace;     ///< Используемое место на диске в байтах
        double usagePercent;     ///< Процент использования диска (0.0 - 100.0)
        std::wstring type;       ///< Тип диска (жесткий диск, съемный и т.д.)
    };
    
    /**
     * @brief Получает информацию обо всех дисках системы
     * 
     * Сканирует все логические диски системы и собирает информацию
     * о фиксированных и съемных дисках.
     * 
     * @return std::vector<DiskInfo> Вектор со структурами информации о дисках
     */
    std::vector<DiskInfo> getDiskInfo() {
        std::vector<DiskInfo> disks;
        DWORD drives = GetLogicalDrives();
        
        if (drives == 0) {
            std::cerr << "Ошибка получения списка логических дисков" << std::endl;
            return disks;
        }
        
        for (int i = 0; i < 26; i++) {
            if (drives & (1 << i)) {
                wchar_t driveLetter = L'A' + i;
                std::wstring drivePath = std::wstring(1, driveLetter) + L":\\";
                
                UINT driveType = GetDriveTypeW(drivePath.c_str());
                if (driveType == DRIVE_FIXED || driveType == DRIVE_REMOVABLE) {
                    DiskInfo info;
                    info.drive = drivePath;
                    
                    ULARGE_INTEGER freeBytesAvailable, totalBytes, totalFreeBytes;
                    if (GetDiskFreeSpaceExW(drivePath.c_str(), &freeBytesAvailable, 
                                           &totalBytes, &totalFreeBytes)) {
                        // Check for valid data
                        if (totalBytes.QuadPart == 0) {
                            std::cerr << "Некорректные данные для диска " << drivePath << std::endl;
                            continue;
                        }
                        
                        info.totalSpace = totalBytes.QuadPart;
                        info.freeSpace = totalFreeBytes.QuadPart;
                        info.usedSpace = info.totalSpace - info.freeSpace;
                        info.usagePercent = (double)info.usedSpace / info.totalSpace * 100.0;
                        
                        switch(driveType) {
                            case DRIVE_FIXED: info.type = L"Жесткий диск"; break;
                            case DRIVE_REMOVABLE: info.type = L"Съемный диск"; break;
                            default: info.type = L"Другое";
                        }
                        
                        disks.push_back(info);
                    } else {
                        DWORD error = GetLastError();
                        std::cerr << "Ошибка получения информации о диске " << drivePath 
                                  << " (Error code: " << error << ")" << std::endl;
                    }
                }
            }
        }
        return disks;
    }
    
    /**
     * @brief Выводит информацию о дисках в консоль
     * 
     * Отображает подробную информацию о всех найденных дисках,
     * включая общий объем, свободное и используемое пространство.
     */
    void printDiskInfo() {
        auto disks = getDiskInfo();
        
        if (disks.empty()) {
            std::wcout << L"\n=== Информация о дисках ===" << std::endl;
            std::wcout << L"Не удалось получить информацию о дисках" << std::endl;
            return;
        }
        
        std::wcout << L"\n=== Информация о дисках ===" << std::endl;
        
        for (const auto& disk : disks) {
            std::wcout << L"\nДиск: " << disk.drive << std::endl;
            std::wcout << L"Тип: " << disk.type << std::endl;
            std::wcout << L"Всего: " << (disk.totalSpace / (1024*1024*1024)) << L" ГБ" << std::endl;
            std::wcout << L"Свободно: " << (disk.freeSpace / (1024*1024*1024)) << L" ГБ" << std::endl;
            std::wcout << L"Занято: " << (disk.usedSpace / (1024*1024*1024)) << L" ГБ" << std::endl;
            std::wcout << L"Использовано: " << std::fixed << std::setprecision(2) 
                      << disk.usagePercent << L"%" << std::endl;
        }
    }
    
    /**
     * @brief Получает информацию о производительности диска
     * 
     * Использует PDH для получения данных о скорости чтения/записи диска.
     * 
     * @param drive Буква диска для мониторинга (по умолчанию "C:")
     */
    void getDiskPerformance(const char* drive = "C:") {
        std::string counterPath = "\\PhysicalDisk(0 C:)\\Disk Bytes/sec";
        PDH_HQUERY query;
        PDH_HCOUNTER counter;
        
        PDH_STATUS status = PdhOpenQuery(NULL, 0, &query);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка инициализации PDH query для диска: " << status << std::endl;
            return;
        }
        
        status = PdhAddCounterA(query, counterPath.c_str(), 0, &counter);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка добавления счетчика PDH для диска: " << status << std::endl;
            PdhCloseQuery(query);
            return;
        }
        
        PdhCollectQueryData(query);
        Sleep(1000);
        
        PDH_FMT_COUNTERVALUE value;
        status = PdhCollectQueryData(query);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка сбора данных PDH для диска: " << status << std::endl;
            PdhCloseQuery(query);
            return;
        }
        
        status = PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &value);
        if (status != ERROR_SUCCESS) {
            std::cerr << "Ошибка получения форматированного значения PDH для диска: " << status << std::endl;
            PdhCloseQuery(query);
            return;
        }
        
        std::cout << "Скорость диска: " << (value.doubleValue / (1024*1024)) 
                  << " МБ/сек" << std::endl;
        
        PdhCloseQuery(query);
    }
    
    /**
     * @brief Проверяет корректность информации о диске
     * 
     * @param info Ссылка на структуру DiskInfo для проверки
     * @return bool true если информация корректна, false в противном случае
     */
    bool isValidDiskInfo(const DiskInfo& info) const {
        return info.totalSpace > 0 && info.usagePercent >= 0.0 && info.usagePercent <= 100.0;
    }
};

#endif // DISK_MONITOR_H