#ifndef MEMORY_MONITOR_H
#define MEMORY_MONITOR_H

#include <windows.h>
#include <iostream>

class MemoryMonitor {
public:
    struct MemoryInfo {
        DWORDLONG totalPhys;
        DWORDLONG availPhys;
        DWORDLONG usedPhys;
        DWORD memoryLoad;
        DWORDLONG totalVirtual;
        DWORDLONG availVirtual;
    };
    
    MemoryInfo getMemoryInfo() {
        MEMORYSTATUSEX memInfo;
        memInfo.dwLength = sizeof(MEMORYSTATUSEX);
        GlobalMemoryStatusEx(&memInfo);
        
        MemoryInfo info;
        info.totalPhys = memInfo.ullTotalPhys;
        info.availPhys = memInfo.ullAvailPhys;
        info.usedPhys = memInfo.ullTotalPhys - memInfo.ullAvailPhys;
        info.memoryLoad = memInfo.dwMemoryLoad;
        info.totalVirtual = memInfo.ullTotalVirtual;
        info.availVirtual = memInfo.ullAvailVirtual;
        
        return info;
    }
    
    void printMemoryInfo() {
        MemoryInfo info = getMemoryInfo();
        
        std::cout << "\n=== Информация о памяти ===" << std::endl;
        std::cout << "Всего физической памяти: " 
                  << (info.totalPhys / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Используется физической памяти: " 
                  << (info.usedPhys / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Доступно физической памяти: " 
                  << (info.availPhys / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Использование памяти: " << info.memoryLoad << "%" << std::endl;
        std::cout << "Всего виртуальной памяти: " 
                  << (info.totalVirtual / (1024*1024*1024)) << " ГБ" << std::endl;
        std::cout << "Доступно виртуальной памяти: " 
                  << (info.availVirtual / (1024*1024*1024)) << " ГБ" << std::endl;
    }
};

#endif // MEMORY_MONITOR_H