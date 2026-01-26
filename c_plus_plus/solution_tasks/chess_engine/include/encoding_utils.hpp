#ifndef ENCODING_UTILS_HPP
#define ENCODING_UTILS_HPP

#include <string>
#include <locale>

#ifdef _WIN32
#include <windows.h>
#endif

class EncodingUtils {
public:
    // Set console encoding to UTF-8
    static void setConsoleEncoding() {
#ifdef _WIN32
        // Set console to UTF-8
        SetConsoleOutputCP(65001); // UTF-8 code page
        SetConsoleCP(65001);
#endif
    }

    // Convert UTF-8 string to wide string
    static std::wstring utf8ToWide(const std::string& utf8) {
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
        return converter.from_bytes(utf8);
    }

    // Convert wide string to UTF-8
    static std::string wideToUtf8(const std::wstring& wide) {
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
        return converter.to_bytes(wide);
    }

    // Handle multi-byte character conversion for different encodings
    static std::string convertToUtf8(const std::string& input, const std::string& fromEncoding = "auto") {
        // This is a simplified version - in practice, you'd use iconv or similar
        // For now, assume input is already in a compatible format
        return input;
    }

    // Normalize string for consistent processing
    static std::string normalizeString(const std::string& input) {
        std::string result = input;
        // Remove any problematic characters
        return result;
    }
};

#endif // ENCODING_UTILS_HPP