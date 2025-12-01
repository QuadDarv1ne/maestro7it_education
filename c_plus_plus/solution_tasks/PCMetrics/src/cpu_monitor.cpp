#include "../include/cpu_monitor.h"
#include <iostream>
#include <windows.h>
#include <pdh.h>
#include <pdhmsg.h>
#include <iomanip>

void CPUMonitor::getCPUInfo() {
    // TODO: Реализовать вывод информации о CPU
    std::cout << "CPU: Информация о процессоре (заглушка)" << std::endl;
}

double CPUMonitor::getCPUUsage() {
    // TODO: Реализовать получение загрузки CPU
    return 0.0;
}
