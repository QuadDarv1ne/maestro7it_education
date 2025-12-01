#include "../include/metrics_exporter.h"
#include <iostream>
#include <algorithm>
#include <codecvt>
#include <locale>

std::string MetricsExporter::getCurrentTimestamp() {
    auto now = std::time(nullptr);
    auto tm = *std::localtime(&now);
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
    return oss.str();
}

std::string MetricsExporter::escapeCSVField(const std::string& field) {
    // Check if field contains commas, quotes, or newlines
    if (field.find_first_of(",\"\n") != std::string::npos) {
        std::string escaped = field;
        // Escape quotes by doubling them
        size_t pos = 0;
        while ((pos = escaped.find("\"", pos)) != std::string::npos) {
            escaped.replace(pos, 1, "\"\"");
            pos += 2;
        }
        // Wrap in quotes
        return "\"" + escaped + "\"";
    }
    return field;
}

std::string MetricsExporter::formatJSONValue(const std::string& key, const std::string& value, bool isLast) {
    std::ostringstream oss;
    oss << "    \"" << key << "\": \"" << value << "\"";
    if (!isLast) {
        oss << ",";
    }
    oss << "\n";
    return oss.str();
}

std::string MetricsExporter::formatJSONNumber(const std::string& key, double value, bool isLast) {
    std::ostringstream oss;
    oss << "    \"" << key << "\": " << std::fixed << std::setprecision(2) << value;
    if (!isLast) {
        oss << ",";
    }
    oss << "\n";
    return oss.str();
}

bool MetricsExporter::exportToCSV(const std::string& filename,
                                 const CPUMonitor& cpuMonitor,
                                 const MemoryMonitor& memMonitor,
                                 const DiskMonitor& diskMonitor,
                                 const GPUMonitor& gpuMonitor) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        return false;
    }
    
    // Write CSV header
    file << "Timestamp,CPU_Usage_Percent,RAM_Total_GB,RAM_Used_GB,RAM_Available_GB,RAM_Usage_Percent";
    
    // Add disk information headers
    auto disks = diskMonitor.getDiskInfo();
    for (size_t i = 0; i < disks.size(); ++i) {
        file << ",Disk_" << i << "_Drive,Disk_" << i << "_Total_GB,Disk_" << i << "_Used_GB,Disk_" << i << "_Available_GB,Disk_" << i << "_Usage_Percent";
    }
    
    file << "\n";
    
    // Write data row
    std::string timestamp = getCurrentTimestamp();
    file << escapeCSVField(timestamp);
    
    // CPU data
    double cpuUsage = cpuMonitor.getCPUUsage();
    file << "," << cpuUsage;
    
    // Memory data
    auto memInfo = memMonitor.getMemoryInfo();
    double ramTotal = static_cast<double>(memInfo.totalPhys) / (1024*1024*1024);
    double ramUsed = static_cast<double>(memInfo.usedPhys) / (1024*1024*1024);
    double ramAvailable = static_cast<double>(memInfo.availPhys) / (1024*1024*1024);
    file << "," << ramTotal << "," << ramUsed << "," << ramAvailable << "," << memInfo.memoryLoad;
    
    // Disk data
    for (const auto& disk : disks) {
        // Convert wide string to narrow string for CSV
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
        std::string driveStr = converter.to_bytes(disk.drive);
        
        double diskTotal = static_cast<double>(disk.totalSpace) / (1024*1024*1024);
        double diskUsed = static_cast<double>(disk.usedSpace) / (1024*1024*1024);
        double diskAvailable = static_cast<double>(disk.freeSpace) / (1024*1024*1024);
        
        file << "," << escapeCSVField(driveStr) 
             << "," << diskTotal 
             << "," << diskUsed 
             << "," << diskAvailable 
             << "," << disk.usagePercent;
    }
    
    file << "\n";
    file.close();
    
    return file.good();
}

bool MetricsExporter::exportToJSON(const std::string& filename,
                                  const CPUMonitor& cpuMonitor,
                                  const MemoryMonitor& memMonitor,
                                  const DiskMonitor& diskMonitor,
                                  const GPUMonitor& gpuMonitor) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        return false;
    }
    
    file << "{\n";
    
    std::string timestamp = getCurrentTimestamp();
    file << formatJSONValue("timestamp", timestamp);
    
    // CPU data
    double cpuUsage = cpuMonitor.getCPUUsage();
    file << formatJSONNumber("cpu_usage_percent", cpuUsage);
    
    // Memory data
    auto memInfo = memMonitor.getMemoryInfo();
    double ramTotal = static_cast<double>(memInfo.totalPhys) / (1024*1024*1024);
    double ramUsed = static_cast<double>(memInfo.usedPhys) / (1024*1024*1024);
    double ramAvailable = static_cast<double>(memInfo.availPhys) / (1024*1024*1024);
    
    file << formatJSONNumber("ram_total_gb", ramTotal);
    file << formatJSONNumber("ram_used_gb", ramUsed);
    file << formatJSONNumber("ram_available_gb", ramAvailable);
    file << formatJSONNumber("ram_usage_percent", memInfo.memoryLoad, true); // Last item in this section
    
    file << "}\n";
    file.close();
    
    return file.good();
}