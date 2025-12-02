#ifndef COLOR_OUTPUT_H
#define COLOR_OUTPUT_H

#include <iostream>
#include <string>

#ifdef _WIN32
    #include <windows.h>
#endif

/**
 * @class ColorOutput
 * @brief Класс для цветного вывода в консоль
 * 
 * ColorOutput предоставляет функции для вывода текста в консоль
 * с различными цветами на Windows и Unix-подобных системах.
 */
class ColorOutput {
public:
    /**
     * @enum Color
     * @brief Цвета для вывода в консоль
     */
    enum Color {
        BLACK = 0,      ///< Черный цвет
        BLUE = 1,       ///< Синий цвет
        GREEN = 2,      ///< Зеленый цвет
        CYAN = 3,       ///< Голубой цвет
        RED = 4,        ///< Красный цвет
        MAGENTA = 5,    ///< Пурпурный цвет
        YELLOW = 6,     ///< Желтый цвет
        WHITE = 7,      ///< Белый цвет
        GRAY = 8,       ///< Серый цвет
        DEFAULT = 15    ///< Цвет по умолчанию
    };

    /**
     * @brief Выводит текст в консоль с указанным цветом
     * 
     * @param text Текст для вывода
     * @param color Цвет текста
     */
    static void print(const std::string& text, Color color = DEFAULT) {
#ifdef _WIN32
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        CONSOLE_SCREEN_BUFFER_INFO consoleInfo;
        GetConsoleScreenBufferInfo(hConsole, &consoleInfo);
        WORD saved_attributes = consoleInfo.wAttributes;

        // Установка цвета
        WORD colorAttribute = 0;
        switch (color) {
            case BLACK:   colorAttribute = 0; break;
            case BLUE:    colorAttribute = FOREGROUND_BLUE | FOREGROUND_INTENSITY; break;
            case GREEN:   colorAttribute = FOREGROUND_GREEN | FOREGROUND_INTENSITY; break;
            case CYAN:    colorAttribute = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_INTENSITY; break;
            case RED:     colorAttribute = FOREGROUND_RED | FOREGROUND_INTENSITY; break;
            case MAGENTA: colorAttribute = FOREGROUND_RED | FOREGROUND_BLUE | FOREGROUND_INTENSITY; break;
            case YELLOW:  colorAttribute = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_INTENSITY; break;
            case WHITE:   colorAttribute = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY; break;
            case GRAY:    colorAttribute = FOREGROUND_INTENSITY; break;
            case DEFAULT: colorAttribute = saved_attributes; break;
        }

        SetConsoleTextAttribute(hConsole, colorAttribute);
        std::cout << text;
        SetConsoleTextAttribute(hConsole, saved_attributes);
#else
        // ANSI escape codes для Unix-подобных систем
        std::string colorCode;
        switch (color) {
            case BLACK:   colorCode = "\033[30m"; break;
            case BLUE:    colorCode = "\033[34;1m"; break;
            case GREEN:   colorCode = "\033[32;1m"; break;
            case CYAN:    colorCode = "\033[36;1m"; break;
            case RED:     colorCode = "\033[31;1m"; break;
            case MAGENTA: colorCode = "\033[35;1m"; break;
            case YELLOW:  colorCode = "\033[33;1m"; break;
            case WHITE:   colorCode = "\033[37;1m"; break;
            case GRAY:    colorCode = "\033[90m"; break;
            case DEFAULT: colorCode = "\033[0m"; break;
        }
        std::cout << colorCode << text << "\033[0m";
#endif
    }

    /**
     * @brief Выводит текст с переводом строки с указанным цветом
     * 
     * @param text Текст для вывода
     * @param color Цвет текста
     */
    static void println(const std::string& text, Color color = DEFAULT) {
        print(text, color);
        std::cout << std::endl;
    }

    /**
     * @brief Сбрасывает цвет консоли на значение по умолчанию
     */
    static void reset() {
#ifdef _WIN32
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
        SetConsoleTextAttribute(hConsole, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
#else
        std::cout << "\033[0m";
#endif
    }
};

#endif // COLOR_OUTPUT_H
