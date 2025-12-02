#include "../include/logger.h"
#include "../include/color_output.h"
#include <ctime>
#include <iomanip>
#include <sstream>

Logger& Logger::getInstance() {
    static Logger instance;
    return instance;
}

Logger::Logger() : minimumLevel(LogLevel::INFO_LEVEL), outputToConsole(true), initialized(false) {}

Logger::~Logger() {
    if (logFile.is_open()) {
        logFile.close();
    }
}

void Logger::initialize(const std::string& filename, LogLevel minLevel, bool consoleOutput) {
    std::lock_guard<std::mutex> lock(logMutex);
    minimumLevel = minLevel;
    outputToConsole = consoleOutput;
    
    if (!filename.empty()) {
        logFile.open(filename, std::ios::app);
        if (logFile.is_open()) {
            initialized = true;
            log(LogLevel::INFO_LEVEL, "Logger инициализирован. Файл: " + filename);
        }
    } else {
        initialized = true;
    }
}

std::string Logger::getCurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(
        now.time_since_epoch()) % 1000;
    
    std::tm tm;
#ifdef _WIN32
    localtime_s(&tm, &time);
#else
    localtime_r(&time, &tm);
#endif
    
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%d %H:%M:%S");
    oss << '.' << std::setfill('0') << std::setw(3) << ms.count();
    
    return oss.str();
}

std::string Logger::levelToString(LogLevel level) {
    switch (level) {
        case LogLevel::DEBUG_LEVEL:   return "DEBUG";
        case LogLevel::INFO_LEVEL:    return "INFO";
        case LogLevel::WARNING_LEVEL: return "WARNING";
        case LogLevel::ERROR_LEVEL:   return "ERROR";
        default:                      return "UNKNOWN";
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
    
    // Вывод в консоль
    if (outputToConsole) {
        ColorOutput::Color color;
        switch (level) {
            case LogLevel::DEBUG_LEVEL:   color = debugColor; break;
            case LogLevel::INFO_LEVEL:    color = infoColor; break;
            case LogLevel::WARNING_LEVEL: color = warningColor; break;
            case LogLevel::ERROR_LEVEL:   color = errorColor; break;
            default:                      color = ColorOutput::DEFAULT; break;
        }
        
        ColorOutput::print("[" + levelStr + "] ", color);
        std::cout << message << std::endl;
    }
    
    // Запись в файл
    if (logFile.is_open()) {
        logFile << logMessage << std::endl;
        logFile.flush(); // Сразу сбрасываем в файл для надежности
    }
}

void Logger::debug(const std::string& message) {
    log(LogLevel::DEBUG_LEVEL, message);
}

void Logger::info(const std::string& message) {
    log(LogLevel::INFO_LEVEL, message);
}

void Logger::warning(const std::string& message) {
    log(LogLevel::WARNING_LEVEL, message);
}

void Logger::error(const std::string& message) {
    log(LogLevel::ERROR_LEVEL, message);
}