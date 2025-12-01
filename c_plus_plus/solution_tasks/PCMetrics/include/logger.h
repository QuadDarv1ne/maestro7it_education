#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <fstream>
#include <iostream>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <mutex>

/**
 * @class Logger
 * @brief Класс для логирования событий приложения
 * 
 * Logger предоставляет функциональность для записи логов различных уровней
 * (DEBUG, INFO, WARNING, ERROR) в файл и/или консоль.
 */
class Logger {
public:
    /**
     * @enum LogLevel
     * @brief Уровни логирования
     */
    enum class LogLevel {
        DEBUG_LEVEL,    ///< Отладочная информация
        INFO_LEVEL,     ///< Информационные сообщения
        WARNING_LEVEL,  ///< Предупреждения
        ERROR_LEVEL     ///< Ошибки
    };

    /**
     * @brief Получает экземпляр логгера (Singleton)
     * 
     * @return Logger& Ссылка на экземпляр логгера
     */
    static Logger& getInstance();

    /**
     * @brief Инициализирует логгер с указанным файлом и минимальным уровнем логирования
     * 
     * @param filename Имя файла для логирования
     * @param minLevel Минимальный уровень логирования
     * @param consoleOutput Флаг вывода в консоль
     */
    void initialize(const std::string& filename, LogLevel minLevel = LogLevel::INFO_LEVEL, bool consoleOutput = true);

    /**
     * @brief Записывает сообщение в лог
     * 
     * @param level Уровень логирования
     * @param message Сообщение для логирования
     */
    void log(LogLevel level, const std::string& message);

    /**
     * @brief Записывает отладочное сообщение
     * 
     * @param message Сообщение для логирования
     */
    void debug(const std::string& message);

    /**
     * @brief Записывает информационное сообщение
     * 
     * @param message Сообщение для логирования
     */
    void info(const std::string& message);

    /**
     * @brief Записывает предупреждение
     * 
     * @param message Сообщение для логирования
     */
    void warning(const std::string& message);

    /**
     * @brief Записывает сообщение об ошибке
     * 
     * @param message Сообщение для логирования
     */
    void error(const std::string& message);

    /**
     * @brief Преобразует уровень логирования в строку
     * 
     * @param level Уровень логирования
     * @return std::string Строковое представление уровня
     */
    static std::string levelToString(LogLevel level);

private:
    /**
     * @brief Конструктор класса Logger
     */
    Logger();

    /**
     * @brief Деструктор класса Logger
     */
    ~Logger();

    /**
     * @brief Получает текущую временную метку
     * 
     * @return std::string Строка с текущей датой и временем
     */
    std::string getCurrentTimestamp();

    // Запрещаем копирование
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    std::ofstream logFile;          ///< Файл для записи логов
    LogLevel minimumLevel;           ///< Минимальный уровень логирования
    bool outputToConsole;           ///< Флаг вывода в консоль
    bool initialized;               ///< Флаг инициализации
    std::mutex logMutex;            ///< Мьютекс для потокобезопасности
};

#endif // LOGGER_H