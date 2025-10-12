#include "Tokenizer.h"
#include <cctype>
#include <unordered_map>
#include <algorithm>
#include <stdexcept>

std::vector<std::string> tokenizeExpression(const std::string& expr) {
    static const std::unordered_map<std::string, std::string> russianToEnglish = {
        {"синус", "sin"}, {"косинус", "cos"}, {"тангенс", "tan"},
        {"арксинус", "asin"}, {"арккосинус", "acos"}, {"арктангенс", "atan"},
        {"логарифм", "log"}, {"натуральный_лог", "ln"}, {"корень", "sqrt"},
        {"экспонента", "exp"}, {"пи", "pi"}, {"э", "e"}
    };

    std::vector<std::string> tokens;
    size_t i = 0;

    while (i < expr.size()) {
        if (std::isspace(expr[i])) {
            i++;
            continue;
        }

        // Числа
        if (std::isdigit(expr[i]) || expr[i] == '.') {
            size_t start = i;
            i++;
            while (i < expr.size() && (std::isdigit(expr[i]) || expr[i] == '.')) i++;
            if (i < expr.size() && (expr[i] == 'e' || expr[i] == 'E')) {
                i++;
                if (i < expr.size() && (expr[i] == '+' || expr[i] == '-')) i++;
                while (i < expr.size() && std::isdigit(expr[i])) i++;
            }
            tokens.push_back(expr.substr(start, i - start));
            continue;
        }

        // Идентификаторы
        if (std::isalpha(expr[i])) {
            size_t start = i;
            i++;
            while (i < expr.size() && std::isalnum(expr[i])) i++;
            std::string ident = expr.substr(start, i - start);
            std::transform(ident.begin(), ident.end(), ident.begin(), ::tolower);

            // Преобразуем русские имена в английские
            auto it = russianToEnglish.find(ident);
            if (it != russianToEnglish.end()) {
                ident = it->second;
            }
            tokens.push_back(ident);
            continue;
        }

        // Операторы и скобки
        if (expr[i] == '(' || expr[i] == ')') {
            tokens.push_back(std::string(1, expr[i]));
            i++;
            continue;
        }

        if (expr[i] == '+' || expr[i] == '-' || expr[i] == '*' || expr[i] == '/' || expr[i] == '^') {
            // Обрабатываем унарные операторы
            bool isUnary = false;
            if ((expr[i] == '+' || expr[i] == '-') &&
                (tokens.empty() ||
                 tokens.back() == "(" ||
                 tokens.back() == "+" ||
                 tokens.back() == "-" ||
                 tokens.back() == "*" ||
                 tokens.back() == "/")) {
                isUnary = true;
            }

            if (isUnary) {
                tokens.push_back((expr[i] == '-') ? "u-" : "u+");
            } else {
                tokens.push_back(std::string(1, expr[i]));
            }
            i++;
            continue;
        }

        throw std::runtime_error("Неожиданный символ: " + std::string(1, expr[i]));
    }

    return tokens;
}
