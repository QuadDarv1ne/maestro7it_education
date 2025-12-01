#ifndef CPU_MONITOR_H
#define CPU_MONITOR_H

#include <windows.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <iostream>

#pragma comment(lib, "pdh.lib")

class CPUMonitor {
private:
    PDH_HQUERY query;
    PDH_HCOUNTER counter;
    
public:
    CPUMonitor() {
        PdhOpenQuery(NULL, 0, &query);
        PdhAddCounter(query, L"\\Processor(_Total)\\% Processor Time", 0, &counter);
        PdhCollectQueryData(query);
    }
    
    ~CPUMonitor() {
        PdhCloseQuery(query);
    }
    
    double getCPUUsage() {
        PDH_FMT_COUNTERVALUE value;
        PdhCollectQueryData(query);
        PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &value);
        return value.doubleValue;
    }
    
    void getCPUInfo() {
        SYSTEM_INFO sysInfo;
        GetSystemInfo(&sysInfo);
        std::cout << "Количество процессоров: " << sysInfo.dwNumberOfProcessors << std::endl;
        std::cout << "Архитектура: ";
        switch(sysInfo.wProcessorArchitecture) {
            case PROCESSOR_ARCHITECTURE_AMD64:
                std::cout << "x64 (AMD or Intel)" << std::endl;
                break;
            case PROCESSOR_ARCHITECTURE_INTEL:
                std::cout << "x86" << std::endl;
                break;
            case PROCESSOR_ARCHITECTURE_ARM:
                std::cout << "ARM" << std::endl;
                break;
            default:
                std::cout << "Unknown" << std::endl;
        }
    }
    
    int getProcessorCount() {
        SYSTEM_INFO sysInfo;
        GetSystemInfo(&sysInfo);
        return sysInfo.dwNumberOfProcessors;
    }
};

#endif // CPU_MONITOR_H