#ifndef DISK_MONITOR_H
#define DISK_MONITOR_H

#include <windows.h>
#include <pdh.h>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>

class DiskMonitor {
public:
    struct DiskInfo {
        std::wstring drive;
        ULONGLONG totalSpace;
        ULONGLONG freeSpace;
        ULONGLONG usedSpace;
        double usagePercent;
        std::wstring type;
    };
    
    std::vector<DiskInfo> getDiskInfo() {
        std::vector<DiskInfo> disks;
        DWORD drives = GetLogicalDrives();
        
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
                    }
                }
            }
        }
        return disks;
    }
    
    void printDiskInfo() {
        auto disks = getDiskInfo();
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
    
    void getDiskPerformance(const wchar_t* drive) {
        std::wstring counterPath = L"\\PhysicalDisk(0 C:)\\Disk Bytes/sec";
        PDH_HQUERY query;
        PDH_HCOUNTER counter;
        
        PdhOpenQuery(NULL, 0, &query);
        PdhAddCounter(query, counterPath.c_str(), 0, &counter);
        PdhCollectQueryData(query);
        Sleep(1000);
        
        PDH_FMT_COUNTERVALUE value;
        PdhCollectQueryData(query);
        PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &value);
        
        std::cout << "Скорость диска: " << (value.doubleValue / (1024*1024)) 
                  << " МБ/сек" << std::endl;
        
        PdhCloseQuery(query);
    }
};

#endif // DISK_MONITOR_H