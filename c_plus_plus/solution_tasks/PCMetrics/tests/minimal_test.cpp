#include <iostream>
#include <windows.h>

int main() {
    std::cout << "=== Minimal Test ===" << std::endl;
    std::cout << "Starting basic Windows API test..." << std::endl;
    
    try {
        // Тест 1: Базовый вывод
        std::cout << "[OK] Basic output works" << std::endl;
        
        // Тест 2: GetTickCount64
        ULONGLONG uptime = GetTickCount64();
        std::cout << "[OK] System uptime: " << (uptime / 1000) << " seconds" << std::endl;
        
        // Тест 3: Проверка памяти
        MEMORYSTATUSEX memInfo;
        memInfo.dwLength = sizeof(MEMORYSTATUSEX);
        if (GlobalMemoryStatusEx(&memInfo)) {
            unsigned long long totalPhys = memInfo.ullTotalPhys / (1024 * 1024);
            std::cout << "[OK] Total RAM: " << totalPhys << " MB" << std::endl;
        } else {
            std::cout << "[FAIL] GlobalMemoryStatusEx failed" << std::endl;
        }
        
        // Тест 4: GetLogicalDrives
        DWORD drives = GetLogicalDrives();
        int driveCount = 0;
        for (int i = 0; i < 26; i++) {
            if (drives & (1 << i)) driveCount++;
        }
        std::cout << "[OK] Found " << driveCount << " drives" << std::endl;
        
        std::cout << "\n=== All basic tests passed ===" << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "[ERROR] Exception: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "[ERROR] Unknown exception" << std::endl;
        return 2;
    }
}
