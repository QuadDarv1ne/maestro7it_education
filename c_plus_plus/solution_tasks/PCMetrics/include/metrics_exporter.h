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

class MetricsExporter {
public:
    // Export to CSV format
    static bool exportToCSV(const std::string& filename, 
                           const CPUMonitor& cpuMonitor,
                           const MemoryMonitor& memMonitor,
                           const DiskMonitor& diskMonitor,
                           const GPUMonitor& gpuMonitor);
    
    // Export to JSON format
    static bool exportToJSON(const std::string& filename,
                            const CPUMonitor& cpuMonitor,
                            const MemoryMonitor& memMonitor,
                            const DiskMonitor& diskMonitor,
                            const GPUMonitor& gpuMonitor);
    
private:
    // Helper functions
    static std::string getCurrentTimestamp();
    static std::string escapeCSVField(const std::string& field);
    static std::string formatJSONValue(const std::string& key, const std::string& value, bool isLast = false);
    static std::string formatJSONNumber(const std::string& key, double value, bool isLast = false);
};

#endif // METRICS_EXPORTER_H