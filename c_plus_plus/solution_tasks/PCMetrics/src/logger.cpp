#include "../include/logger.h"
#include "../include/color_output.h"

Logger& Logger::getInstance() {
    static Logger instance;
    return instance;
}

Logger::Logger() : currentLevel(INFO_LEVEL), consoleOutputEnabled(true) {}

Logger::~Logger() {
    if (logFile.is_open()) {
        logFile.close();
    }
}

void Logger::initialize(const std::string& filename, LogLevel level, bool consoleOutput) {
    currentLevel = level;
    consoleOutputEnabled = consoleOutput;
    logFile.open(filename, std::ios::app);
}

void Logger::debug(const std::string& message) {
    if (currentLevel <= DEBUG_LEVEL) {
        if (consoleOutputEnabled) {
            ColorOutput::print("[DEBUG] ", debugColor);
            std::cout << message << std::endl;
        }
        if (logFile.is_open()) {
            logFile << "[DEBUG] " << message << std::endl;
        }
    }
}

void Logger::info(const std::string& message) {
    if (currentLevel <= INFO_LEVEL) {
        if (consoleOutputEnabled) {
            ColorOutput::print("[INFO] ", infoColor);
            std::cout << message << std::endl;
        }
        if (logFile.is_open()) {
            logFile << "[INFO] " << message << std::endl;
        }
    }
}

void Logger::warning(const std::string& message) {
    if (currentLevel <= WARNING_LEVEL) {
        if (consoleOutputEnabled) {
            ColorOutput::print("[WARNING] ", warningColor);
            std::cout << message << std::endl;
        }
        if (logFile.is_open()) {
            logFile << "[WARNING] " << message << std::endl;
        }
    }
}

void Logger::error(const std::string& message) {
    if (currentLevel <= ERROR_LEVEL) {
        if (consoleOutputEnabled) {
            ColorOutput::print("[ERROR] ", errorColor);
            std::cout << message << std::endl;
        }
        if (logFile.is_open()) {
            logFile << "[ERROR] " << message << std::endl;
        }
    }
}