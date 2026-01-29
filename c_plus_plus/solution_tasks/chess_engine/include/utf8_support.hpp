#ifndef UTF8_SUPPORT_HPP
#define UTF8_SUPPORT_HPP

#include <string>
#include <locale>
#include <codecvt>
#include <iostream>

#ifdef _WIN32
#include <windows.h>
#include <io.h>
#include <fcntl.h>
#endif

/**
 * @brief Класс для поддержки UTF-8 и русских символов
 * 
 * Обеспечивает корректную работу с Unicode символами
 * в консольном и файловом вводе/выводе.
 */
class UTF8Support {
public:
    /**
     * @brief Инициализация поддержки UTF-8
     * 
     * Настраивает консоль и потоки для корректной работы с Unicode
     */
    static void initialize() {
#ifdef _WIN32
        // Установка кодовой страницы UTF-8 для консоли Windows
        SetConsoleOutputCP(CP_UTF8);
        SetConsoleCP(CP_UTF8);
        
        // Настройка потоков для работы с UTF-8
        _setmode(_fileno(stdout), _O_U8TEXT);
        _setmode(_fileno(stderr), _O_U8TEXT);
        _setmode(_fileno(stdin), _O_U8TEXT);
#else
        // Для Unix-систем обычно UTF-8 используется по умолчанию
        std::setlocale(LC_ALL, "en_US.UTF-8");
        std::setlocale(LC_CTYPE, "en_US.UTF-8");
#endif
    }
    
    /**
     * @brief Преобразование строки из UTF-8 в wide string
     * @param utf8_str Строка в кодировке UTF-8
     * @return Wide string
     */
    static std::wstring utf8ToWide(const std::string& utf8_str) {
        try {
            std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
            return converter.from_bytes(utf8_str);
        } catch (const std::exception& e) {
            // В случае ошибки возвращаем пустую строку
            return L"";
        }
    }
    
    /**
     * @brief Преобразование wide string в UTF-8
     * @param wide_str Wide string
     * @return Строка в кодировке UTF-8
     */
    static std::string wideToUtf8(const std::wstring& wide_str) {
        try {
            std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
            return converter.to_bytes(wide_str);
        } catch (const std::exception& e) {
            // В случае ошибки возвращаем пустую строку
            return "";
        }
    }
    
    /**
     * @brief Проверка корректности UTF-8 строки
     * @param str Строка для проверки
     * @return true если строка корректна в UTF-8
     */
    static bool isValidUTF8(const std::string& str) {
        try {
            std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
            converter.from_bytes(str);
            return true;
        } catch (const std::exception& e) {
            return false;
        }
    }
    
    /**
     * @brief Вывод строки с поддержкой UTF-8
     * @param text Текст для вывода
     */
    static void printUTF8(const std::string& text) {
#ifdef _WIN32
        // Для Windows используем wide string вывод
        std::wstring wide_text = utf8ToWide(text);
        std::wcout << wide_text;
#else
        // Для Unix-систем обычный вывод
        std::cout << text;
#endif
    }
    
    /**
     * @brief Получение длины строки в символах (не в байтах)
     * @param utf8_str Строка в UTF-8
     * @return Количество Unicode символов
     */
    static size_t getCharacterCount(const std::string& utf8_str) {
        size_t count = 0;
        for (size_t i = 0; i < utf8_str.length(); ) {
            // Определение длины текущего UTF-8 символа
            unsigned char byte = static_cast<unsigned char>(utf8_str[i]);
            size_t char_length = 1;
            
            if ((byte & 0x80) == 0) {
                // ASCII символ (1 байт)
                char_length = 1;
            } else if ((byte & 0xE0) == 0xC0) {
                // 2-байтный символ
                char_length = 2;
            } else if ((byte & 0xF0) == 0xE0) {
                // 3-байтный символ
                char_length = 3;
            } else if ((byte & 0xF8) == 0xF0) {
                // 4-байтный символ
                char_length = 4;
            }
            
            count++;
            i += char_length;
        }
        return count;
    }
};

// Макросы для удобного использования
#define UTF8_PRINT(text) UTF8Support::printUTF8(text)
#define UTF8_INIT() UTF8Support::initialize()

#endif // UTF8_SUPPORT_HPP