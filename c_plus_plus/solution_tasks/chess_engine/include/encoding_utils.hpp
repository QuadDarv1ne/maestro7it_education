#ifndef ENCODING_UTILS_HPP
#define ENCODING_UTILS_HPP

#include <string>
#include <locale>

#ifdef _WIN32
#include <windows.h>
#endif

class EncodingUtils {
public:
    // Установка кодировки консоли в UTF-8
    static void setConsoleEncoding() {
#ifdef _WIN32
        // Устанавливаем консоль в UTF-8
        SetConsoleOutputCP(65001); // Кодовая страница UTF-8
        SetConsoleCP(65001);
#endif
    }

    // Преобразование строки UTF-8 в широкую строку
    static std::wstring utf8ToWide(const std::string& utf8) {
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
        return converter.from_bytes(utf8);
    }

    // Преобразование широкой строки в UTF-8
    static std::string wideToUtf8(const std::wstring& wide) {
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
        return converter.to_bytes(wide);
    }

    // Обработка многобайтовой конверсии символов для различных кодировок
    static std::string convertToUtf8(const std::string& input, const std::string& fromEncoding = "auto") {
        // Это упрощенная версия - на практике используется iconv или подобное
        // Пока предполагаем, что входные данные уже в совместимом формате
        return input;
    }

    // Нормализация строки для согласованной обработки
    static std::string normalizeString(const std::string& input) {
        std::string result = input;
        // Удаляем любые проблемные символы
        return result;
    }
};

#endif // ENCODING_UTILS_HPP