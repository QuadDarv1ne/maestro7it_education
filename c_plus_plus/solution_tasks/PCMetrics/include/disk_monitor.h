#ifndef DISK_MONITOR_H
#define DISK_MONITOR_H

#include <windows.h>
#include <pdh.h>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>
#include <locale>
#include <codecvt>

// Вспомогательная функция для конвертации wstring в string
inline std::string wstringToString(const std::wstring& wstr) {
    if (wstr.empty()) return std::string();
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), NULL, 0, NULL, NULL);
    std::string strTo(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, &wstr[0], (int)wstr.size(), &strTo[0], size_needed, NULL, NULL);
    return strTo;
}

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
        std::wstring volumeName; ///< Метка тома диска
        std::wstring fileSystem; ///< Файловая система диска
        bool isReady;           ///< Готовность диска (true если можно получить доступ)
    };
    
    /**
     * @brief Получает информацию обо всех дисках системы
     * 
     * Сканирует все логические диски системы и собирает информацию
     * о фиксированных и съемных дисках.
     * 
     * @return std::vector<DiskInfo> Вектор со структурами информации о дисках
     */
    std::vector<DiskInfo> getDiskInfo() const {
        std::vector<DiskInfo> disks;
        DWORD drives = GetLogicalDrives();
        
        if (drives == 0) {
            std::cerr << "Ошибка получения списка логических дисков: " << GetLastError() << std::endl;
            return disks;
        }
        
        for (int i = 0; i < 26; i++) {
            if (drives & (1 << i)) {
                wchar_t driveLetter = L'A' + i;
                std::wstring drivePath = std::wstring(1, driveLetter) + L":\\";
                
                UINT driveType = GetDriveTypeW(drivePath.c_str());
                // Обрабатываем только фиксированные и съемные диски
                if (driveType == DRIVE_FIXED || driveType == DRIVE_REMOVABLE) {
                    DiskInfo info;
                    info.drive = drivePath;
                    info.isReady = (GetDiskFreeSpaceExW(drivePath.c_str(), NULL, NULL, NULL) != 0);
                    
                    // Получаем информацию о диске только если он готов
                    if (info.isReady) {
                        ULARGE_INTEGER freeBytesAvailable, totalBytes, totalFreeBytes;
                        if (GetDiskFreeSpaceExW(drivePath.c_str(), &freeBytesAvailable, 
                                               &totalBytes, &totalFreeBytes)) {
                            // Проверяем корректность данных
                            if (totalBytes.QuadPart == 0) {
                                // Convert wide string to narrow string for output
                                std::string drivePathStr = wstringToString(drivePath);
                                std::cerr << "Некорректные данные для диска " << drivePathStr << std::endl;
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
                            
                            // Получаем метку тома и файловую систему
                            wchar_t volumeName[MAX_PATH] = L"";
                            wchar_t fileSystemName[MAX_PATH] = L"";
                            DWORD serialNumber, maxComponentLength, fileSystemFlags;
                            
                            if (GetVolumeInformationW(
                                    drivePath.c_str(),
                                    volumeName,
                                    MAX_PATH,
                                    &serialNumber,
                                    &maxComponentLength,
                                    &fileSystemFlags,
                                    fileSystemName,
                                    MAX_PATH)) {
                                info.volumeName = volumeName;
                                info.fileSystem = fileSystemName;
                            } else {
                                info.volumeName = L"Не определено";
                                info.fileSystem = L"Не определено";
                            }
                            
                            disks.push_back(info);
                        } else {
                            DWORD error = GetLastError();
                            // Convert wide string to narrow string for output
                            std::string drivePathStr = wstringToString(drivePath);
                            std::cerr << "Ошибка получения информации о диске " << drivePathStr 
                                      << " (Error code: " << error << ")" << std::endl;
                        }
                    } else {
                        // Диск не готов (например, CD-ROM без диска)
                        info.totalSpace = 0;
                        info.freeSpace = 0;
                        info.usedSpace = 0;
                        info.usagePercent = 0.0;
                        
                        switch(driveType) {
                            case DRIVE_FIXED: info.type = L"Жесткий диск (не готов)"; break;
                            case DRIVE_REMOVABLE: info.type = L"Съемный диск (не готов)"; break;
                            default: info.type = L"Другое (не готов)";
                        }
                        
                        info.volumeName = L"Не готов";
                        info.fileSystem = L"Не готов";
                        disks.push_back(info);
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
            
            if (disk.isReady) {
                std::wcout << L"Тип: " << disk.type << std::endl;
                std::wcout << L"Метка тома: " << disk.volumeName << std::endl;
                std::wcout << L"Файловая система: " << disk.fileSystem << std::endl;
                std::wcout << L"Всего: " << formatBytes(disk.totalSpace) << std::endl;
                std::wcout << L"Свободно: " << formatBytes(disk.freeSpace) << std::endl;
                std::wcout << L"Занято: " << formatBytes(disk.usedSpace) << std::endl;
                std::wcout << L"Использовано: " << std::fixed << std::setprecision(2) 
                          << disk.usagePercent << L"%" << std::endl;
                          
                // Предупреждение при высоком использовании диска
                if (disk.usagePercent > 90.0) {
                    std::wcout << L"ПРЕДУПРЕЖДЕНИЕ: Диск почти полностью заполнен!" << std::endl;
                } else if (disk.usagePercent > 80.0) {
                    std::wcout << L"Внимание: Диск заполнен более чем на 80%" << std::endl;
                }
            } else {
                std::wcout << L"Статус: " << disk.type << std::endl;
                std::wcout << L"Метка тома: " << disk.volumeName << std::endl;
                std::wcout << L"Файловая система: " << disk.fileSystem << std::endl;
                std::wcout << L"Диск не готов к использованию" << std::endl;
            }
        }
    }
    
    /**
     * @brief Получает информацию о производительности диска
     * 
     * Использует PDH для получения данных о скорости чтения/записи диска.
     * 
     * @param drive Буква диска для мониторинга (по умолчанию "C:")
     */
    void getDiskPerformance([[maybe_unused]] const char* drive = "C:") {
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
        
        std::cout << "Скорость диска: " << formatBytesPerSecond(value.doubleValue) << std::endl;
        
        PdhCloseQuery(query);
    }
    
    /**
     * @brief Проверяет корректность информации о диске
     * 
     * @param info Ссылка на структуру DiskInfo для проверки
     * @return bool true если информация корректна, false в противном случае
     */
    bool isValidDiskInfo(const DiskInfo& info) const {
        // Проверяем корректность только для готовых дисков
        if (info.isReady) {
            return info.totalSpace > 0 && info.usagePercent >= 0.0 && info.usagePercent <= 100.0;
        }
        // Для неготовых дисков проверяем только логическую структуру
        return !info.drive.empty();
    }
    
private:
    /**
     * @brief Форматирует количество байт в удобочитаемый формат
     * 
     * @param bytes Количество байт
     * @return std::wstring Отформатированная строка с размером
     */
    std::wstring formatBytes(ULONGLONG bytes) const {
        const wchar_t* units[] = {L"Б", L"КБ", L"МБ", L"ГБ", L"ТБ"};
        int unitIndex = 0;
        double size = static_cast<double>(bytes);
        
        while (size >= 1024.0 && unitIndex < 4) {
            size /= 1024.0;
            unitIndex++;
        }
        
        std::wostringstream woss;
        woss << std::fixed << std::setprecision(2) << size << L" " << units[unitIndex];
        return woss.str();
    }
    
    /**
     * @brief Форматирует скорость передачи данных
     * 
     * @param bytesPerSecond Скорость в байтах в секунду
     * @return std::string Отформатированная строка со скоростью
     */
    std::string formatBytesPerSecond(double bytesPerSecond) const {
        const char* units[] = {"Б/с", "КБ/с", "МБ/с", "ГБ/с"};
        int unitIndex = 0;
        double speed = bytesPerSecond;
        
        while (speed >= 1024.0 && unitIndex < 3) {
            speed /= 1024.0;
            unitIndex++;
        }
        
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << speed << " " << units[unitIndex];
        return oss.str();
    }
};

#endif // DISK_MONITOR_H