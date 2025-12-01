#include "../include/logger.h"
#include <iostream>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <mutex>
#include <ctime>

// Static instance for singleton pattern
Logger& Logger::getInstance() {
    static Logger instance;
    return instance;
}

Logger::Logger() : minimumLevel(LogLevel::INFO), outputToConsole(true), initialized(false) {}

Logger::~Logger() {
    if (logFile.is_open()) {
        logFile.close();
    }
}

void Logger::initialize(const std::string& filename, LogLevel minLevel, bool consoleOutput) {
    std::lock_guard<std::mutex> lock(logMutex);
    
    if (logFile.is_open()) {
        logFile.close();
    }
    
    logFile.open(filename, std::ios::app);
    minimumLevel = minLevel;
    outputToConsole = consoleOutput;
    initialized = true;
    
    if (!logFile.is_open()) {
        std::cerr << "Ошибка открытия файла логов: " << filename << std::endl;
    }
}

std::string Logger::getCurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        now.time_since_epoch()) % 1000;
    
    std::stringstream ss;
    ss << std::put_time(std::localtime(&time_t), "%Y-%m-%d %H:%M:%S");
    ss << '.' << std::setfill('0') << std::setw(3) << ms.count();
    return ss.str();
}

std::string Logger::levelToString(LogLevel level) {
    switch (level) {
        case LogLevel::DEBUG:   return "DEBUG";
        case LogLevel::INFO:    return "INFO";
        case LogLevel::WARNING: return "WARN";
        case LogLevel::ERROR:   return "ERROR";
        default:                return "UNKNOWN";
    }
}

void Logger::log(LogLevel level, const std::string& message) {
    if (!initialized || level < minimumLevel) {
        return;
    }
    
    std::lock_guard<std::mutex> lock(logMutex);
    
    std::string timestamp = getCurrentTimestamp();
    std::string levelStr = levelToString(level);
    
    std::string logMessage = "[" + timestamp + "] [" + levelStr + "] " + message;
    
    if (logFile.is_open()) {
        logFile << logMessage << std::endl;
        logFile.flush();
    }
    
    if (outputToConsole) {
        switch (level) {
            case LogLevel::ERROR:
                std::cerr << logMessage << std::endl;
                break;
            case LogLevel::WARNING:
                std::cout << logMessage << std::endl;
                break;
            default:
                std::cout << logMessage << std::endl;
                break;
        }
    }
}

void Logger::debug(const std::string& message) {
    log(LogLevel::DEBUG, message);
}

void Logger::info(const std::string& message) {
    log(LogLevel::INFO, message);
}

void Logger::warning(const std::string& message) {
    log(LogLevel::WARNING, message);
}

void Logger::error(const std::string& message) {
    log(LogLevel::ERROR, message);
}