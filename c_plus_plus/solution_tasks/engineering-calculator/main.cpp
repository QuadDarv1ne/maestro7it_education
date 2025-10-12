#include <iostream>
#include <iomanip>
#include <windows.h>
#include "Tokenizer.h"
#include "Calculator.h"

int main() {
    SetConsoleCP(CP_UTF8);
    SetConsoleOutputCP(CP_UTF8);

    std::cout << "Инженерный калькулятор\n";
    std::cout << "Поддерживаемые операции: +, -, *, /, ^\n";
    std::cout << "Функции: sin, cos, tan, asin, acos, atan, ln, log, sqrt, exp\n";
    std::cout << "Константы: pi, e\n";
    std::cout << "Углы — в радианах.\n";
    std::cout << "Примеры:\n";
    std::cout << "  2 + 3 * sin(pi/2)\n";
    std::cout << "  sqrt(16) + ln(e^2)\n";
    std::cout << "  -5 + 3\n";
    std::cout << "Для выхода введите 'выход' или 'quit'.\n\n";

    std::string input;
    while (true) {
        std::cout << "> ";
        std::getline(std::cin, input);

        if (input == "выход" || input == "quit") break;
        if (input.empty()) continue;

        try {
            auto tokens = tokenizeExpression(input);
            double result = Calculator::evaluate(tokens);
            std::cout << std::fixed << std::setprecision(6);
            std::cout << "= " << result << "\n";
        } catch (const std::exception& e) {
            std::cerr << "Ошибка: " << e.what() << "\n";
        }
    }

    return 0;
}
