#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <map>
#include <fstream>
#include <sstream>

/**
 * @class Config
 * @brief Класс для управления конфигурацией приложения
 * 
 * Config предоставляет функции для загрузки и управления настройками приложения
 * из JSON конфигурационного файла.
 */
class Config {
private:
    static Config* instance;
    std::map<std::string, std::string> settings;
    std::string configFilePath;
    bool loaded;

    Config() : configFilePath("config.json"), loaded(false) {}
    
    /**
     * @brief Парсит простой JSON файл
     * 
     * @param content Содержимое JSON файла
     * @return bool true если парсинг успешен, false в противном случае
     */
    bool parseJSON(const std::string& content);
    
    /**
     * @brief Удаляет пробелы из строки
     * 
     * @param str Строка для обработки
     * @return std::string Строка без пробелов
     */
    std::string trim(const std::string& str);

public:
    Config(const Config&) = delete;
    Config& operator=(const Config&) = delete;
    
    /**
     * @brief Получает единственный экземпляр класса Config
     * 
     * @return Config& Ссылка на единственный экземпляр
     */
    static Config& getInstance() {
        if (!instance) {
            instance = new Config();
        }
        return *instance;
    }
    
    /**
     * @brief Загружает конфигурацию из файла
     * 
     * @param filepath Путь к конфигурационному файлу
     * @return bool true если загрузка успешна, false в противном случае
     */
    bool loadFromFile(const std::string& filepath);
    
    /**
     * @brief Создает конфигурационный файл по умолчанию
     * 
     * @param filepath Путь к создаваемому файлу
     * @return bool true если создание успешно, false в противном случае
     */
    bool createDefaultConfig(const std::string& filepath);
    
    /**
     * @brief Получает строковое значение настройки
     * 
     * @param key Ключ настройки
     * @param defaultValue Значение по умолчанию
     * @return std::string Значение настройки
     */
    std::string getString(const std::string& key, const std::string& defaultValue = "") const;
    
    /**
     * @brief Получает целочисленное значение настройки
     * 
     * @param key Ключ настройки
     * @param defaultValue Значение по умолчанию
     * @return int Значение настройки
     */
    int getInt(const std::string& key, int defaultValue = 0) const;
    
    /**
     * @brief Получает логическое значение настройки
     * 
     * @param key Ключ настройки
     * @param defaultValue Значение по умолчанию
     * @return bool Значение настройки
     */
    bool getBool(const std::string& key, bool defaultValue = false) const;
    
    /**
     * @brief Получает значение с плавающей точкой
     * 
     * @param key Ключ настройки
     * @param defaultValue Значение по умолчанию
     * @return double Значение настройки
     */
    double getDouble(const std::string& key, double defaultValue = 0.0) const;
    
    /**
     * @brief Проверяет, загружена ли конфигурация
     * 
     * @return bool true если конфигурация загружена
     */
    bool isLoaded() const { return loaded; }
    
    /**
     * @brief Выводит все настройки в консоль
     */
    void printSettings() const;
};

#endif // CONFIG_H
