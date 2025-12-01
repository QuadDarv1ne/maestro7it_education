#ifndef GPU_MONITOR_H
#define GPU_MONITOR_H

#include <iostream>
#include <string>
#include <vector>

#ifdef _WIN32
    #include <windows.h>
#endif

// Conditional compilation for NVIDIA NVML support
#ifdef ENABLE_NVML
    #include <nvml.h>
    #pragma comment(lib, "nvml.lib")
#endif

class GPUMonitor {
private:
    bool nvmlInitialized;
    
public:
    GPUMonitor() : nvmlInitialized(false) {}
    
    ~GPUMonitor() {
        shutdownNVML();
    }
    
    bool initNVML();
    void shutdownNVML();
    void printGPUInfo();
    void getNVIDIAGPUUsage();
    
    // Structure to hold GPU information
    struct GPUInfo {
        std::string name;
        unsigned int temperature;
        unsigned int gpuUtilization;
        unsigned int memoryUtilization;
        unsigned long long memoryTotal;
        unsigned long long memoryUsed;
        unsigned int fanSpeed;
    };
    
    std::vector<GPUInfo> getAllGPUInfo();
};

#endif // GPU_MONITOR_H