#include "../include/config.h"
#include "../include/logger.h"
#include <iostream>
#include <algorithm>

// Инициализация статического члена
Config* Config::instance = nullptr;

/**
 * @brief Удаляет пробелы из строки
 * 
 * @param str Строка для обработки
 * @return std::string Строка без пробелов
 */
std::string Config::trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \t\n\r");
    if (first == std::string::npos) return "";
    
    size_t last = str.find_last_not_of(" \t\n\r");
    return str.substr(first, (last - first + 1));
}

/**
 * @brief Парсит простой JSON файл
 * 
 * Упрощенный парсер JSON для базовых пар ключ-значение.
 * Поддерживает строки, числа и булевы значения.
 * 
 * @param content Содержимое JSON файла
 * @return bool true если парсинг успешен, false в противном случае
 */
bool Config::parseJSON(const std::string& content) {
    Logger::getInstance().debug("Начало парсинга JSON конфигурации");
    
    std::string line;
    std::istringstream stream(content);
    
    while (std::getline(stream, line)) {
        line = trim(line);
        
        // Пропускаем пустые строки, комментарии и скобки
        if (line.empty() || line[0] == '{' || line[0] == '}' || 
            line.substr(0, 2) == "//") {
            continue;
        }
        
        // Ищем двоеточие
        size_t colonPos = line.find(':');
        if (colonPos == std::string::npos) continue;
        
        // Извлекаем ключ
        std::string key = line.substr(0, colonPos);
        key = trim(key);
        
        // Удаляем кавычки из ключа
        if (!key.empty() && key.front() == '"') key.erase(0, 1);
        if (!key.empty() && key.back() == '"') key.pop_back();
        
        // Извлекаем значение
        std::string value = line.substr(colonPos + 1);
        value = trim(value);
        
        // Удаляем завершающую запятую если есть
        if (!value.empty() && value.back() == ',') value.pop_back();
        
        // Удаляем кавычки из значения если это строка
        value = trim(value);
        if (!value.empty() && value.front() == '"') value.erase(0, 1);
        if (!value.empty() && value.back() == '"') value.pop_back();
        
        settings[key] = value;
        Logger::getInstance().debug("Загружена настройка: " + key + " = " + value);
    }
    
    Logger::getInstance().info("JSON конфигурация успешно распарсена. Загружено настроек: " + 
                               std::to_string(settings.size()));
    return true;
}

/**
 * @brief Загружает конфигурацию из файла
 * 
 * @param filepath Путь к конфигурационному файлу
 * @return bool true если загрузка успешна, false в противном случае
 */
bool Config::loadFromFile(const std::string& filepath) {
    Logger::getInstance().info("Загрузка конфигурации из файла: " + filepath);
    
    std::ifstream file(filepath);
    if (!file.is_open()) {
        Logger::getInstance().warning("Не удалось открыть файл конфигурации: " + filepath);
        return false;
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string content = buffer.str();
    file.close();
    
    loaded = parseJSON(content);
    if (loaded) {
        configFilePath = filepath;
        Logger::getInstance().info("Конфигурация успешно загружена из: " + filepath);
    } else {
        Logger::getInstance().error("Ошибка парсинга конфигурации из: " + filepath);
    }
    
    return loaded;
}

/**
 * @brief Создает конфигурационный файл по умолчанию
 * 
 * @param filepath Путь к создаваемому файлу
 * @return bool true если создание успешно, false в противном случае
 */
bool Config::createDefaultConfig(const std::string& filepath) {
    Logger::getInstance().info("Создание файла конфигурации по умолчанию: " + filepath);
    
    std::ofstream file(filepath);
    if (!file.is_open()) {
        Logger::getInstance().error("Не удалось создать файл конфигурации: " + filepath);
        return false;
    }
    
    file << "{\n";
    file << "  \"monitoring.interval_ms\": \"1000\",\n";
    file << "  \"monitoring.enable_cpu\": \"true\",\n";
    file << "  \"monitoring.enable_memory\": \"true\",\n";
    file << "  \"monitoring.enable_disk\": \"true\",\n";
    file << "  \"monitoring.enable_gpu\": \"true\",\n";
    file << "  \"monitoring.cpu_samples\": \"5\",\n";
    file << "  \n";
    file << "  \"alerts.enable\": \"false\",\n";
    file << "  \"alerts.cpu_threshold\": \"80\",\n";
    file << "  \"alerts.memory_threshold\": \"90\",\n";
    file << "  \"alerts.disk_threshold\": \"95\",\n";
    file << "  \n";
    file << "  \"export.auto_export\": \"false\",\n";
    file << "  \"export.format\": \"json\",\n";
    file << "  \"export.path\": \"./metrics\",\n";
    file << "  \n";
    file << "  \"logging.level\": \"INFO\",\n";
    file << "  \"logging.console_output\": \"true\",\n";
    file << "  \"logging.file_output\": \"true\",\n";
    file << "  \"logging.filename\": \"pcmetrics.log\",\n";
    file << "  \n";
    file << "  \"ui.colored_output\": \"true\",\n";
    file << "  \"ui.show_header\": \"true\",\n";
    file << "  \"ui.refresh_rate_ms\": \"1000\"\n";
    file << "}\n";
    
    file.close();
    
    Logger::getInstance().info("Файл конфигурации по умолчанию успешно создан: " + filepath);
    return true;
}

/**
 * @brief Получает строковое значение настройки
 * 
 * @param key Ключ настройки
 * @param defaultValue Значение по умолчанию
 * @return std::string Значение настройки
 */
std::string Config::getString(const std::string& key, const std::string& defaultValue) const {
    auto it = settings.find(key);
    if (it != settings.end()) {
        return it->second;
    }
    Logger::getInstance().debug("Настройка не найдена, используется значение по умолчанию: " + 
                                key + " = " + defaultValue);
    return defaultValue;
}

/**
 * @brief Получает целочисленное значение настройки
 * 
 * @param key Ключ настройки
 * @param defaultValue Значение по умолчанию
 * @return int Значение настройки
 */
int Config::getInt(const std::string& key, int defaultValue) const {
    auto it = settings.find(key);
    if (it != settings.end()) {
        try {
            return std::stoi(it->second);
        } catch (const std::exception& e) {
            Logger::getInstance().warning("Ошибка преобразования настройки в int: " + 
                                         key + " = " + it->second);
            return defaultValue;
        }
    }
    return defaultValue;
}

/**
 * @brief Получает логическое значение настройки
 * 
 * @param key Ключ настройки
 * @param defaultValue Значение по умолчанию
 * @return bool Значение настройки
 */
bool Config::getBool(const std::string& key, bool defaultValue) const {
    auto it = settings.find(key);
    if (it != settings.end()) {
        std::string value = it->second;
        // Приводим к нижнему регистру для сравнения
        std::transform(value.begin(), value.end(), value.begin(), ::tolower);
        
        if (value == "true" || value == "1" || value == "yes") {
            return true;
        } else if (value == "false" || value == "0" || value == "no") {
            return false;
        }
    }
    return defaultValue;
}

/**
 * @brief Получает значение с плавающей точкой
 * 
 * @param key Ключ настройки
 * @param defaultValue Значение по умолчанию
 * @return double Значение настройки
 */
double Config::getDouble(const std::string& key, double defaultValue) const {
    auto it = settings.find(key);
    if (it != settings.end()) {
        try {
            return std::stod(it->second);
        } catch (const std::exception& e) {
            Logger::getInstance().warning("Ошибка преобразования настройки в double: " + 
                                         key + " = " + it->second);
            return defaultValue;
        }
    }
    return defaultValue;
}

/**
 * @brief Выводит все настройки в консоль
 */
void Config::printSettings() const {
    std::cout << "\n=== Текущие настройки конфигурации ===" << std::endl;
    
    if (settings.empty()) {
        std::cout << "  (настройки не загружены)" << std::endl;
        return;
    }
    
    for (const auto& setting : settings) {
        std::cout << "  " << setting.first << " = " << setting.second << std::endl;
    }
    
    std::cout << "======================================" << std::endl;
}
