#include "Tokenizer.h"
#include <cctype>
#include <stdexcept>

std::vector<std::string> tokenizeExpression(const std::string& expr) {
    std::vector<std::string> tokens;
    std::string current;

    for (size_t i = 0; i < expr.length(); ++i) {
        char c = expr[i];

        if (std::isspace(c)) {
            if (!current.empty()) {
                tokens.push_back(current);
                current.clear();
            }
            continue;
        }

        if (std::isdigit(c) || c == '.') {
            // Начало числа
            current += c;
            while (i + 1 < expr.length() &&
                   (std::isdigit(expr[i + 1]) || expr[i + 1] == '.' || expr[i + 1] == 'e' || expr[i + 1] == 'E')) {
                ++i;
                if (expr[i] == 'e' || expr[i] == 'E') {
                    if (i + 1 < expr.length() && (expr[i + 1] == '+' || expr[i + 1] == '-'))
                        current += expr[++i];
                }
                current += expr[i];
            }
            tokens.push_back(current);
            current.clear();
        } else if (std::isalpha(c)) {
            // Идентификатор (функция или константа)
            current += c;
            while (i + 1 < expr.length() && std::isalnum(expr[i + 1])) {
                current += expr[++i];
            }
            tokens.push_back(current);
            current.clear();
        } else if (c == '+' || c == '-' || c == '*' || c == '/' || c == '^' || c == '(' || c == ')') {
            // Операторы и скобки
            if ((c == '+' || c == '-') && (tokens.empty() || tokens.back() == "(" || tokens.back() == "+" ||
                                           tokens.back() == "-" || tokens.back() == "*" || tokens.back() == "/")) {
                // Унарный плюс/минус → заменяем на специальный токен
                current = (c == '-') ? "u-" : "u+";
                tokens.push_back(current);
                current.clear();
            } else {
                current += c;
                tokens.push_back(current);
                current.clear();
            }
        } else {
            throw std::runtime_error("Недопустимый символ: " + std::string(1, c));
        }
    }

    if (!current.empty()) {
        tokens.push_back(current);
    }

    return tokens;
}
