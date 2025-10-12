#include "Calculator.h"
#include <stack>
#include <cmath>
#include <stdexcept>
#include <sstream>

bool Calculator::isNumber(const std::string& token) {
    try {
        std::stod(token);
        return true;
    } catch (...) {
        return false;
    }
}

bool Calculator::isConstant(const std::string& token) {
    return token == "pi" || token == "e";
}

double Calculator::getConstantValue(const std::string& token) {
    if (token == "pi") return M_PI;
    if (token == "e") return M_E;
    throw std::runtime_error("Неизвестная константа: " + token);
}

bool Calculator::isFunction(const std::string& token) {
    return token == "sin" || token == "cos" || token == "tan" ||
           token == "asin" || token == "acos" || token == "atan" ||
           token == "ln" || token == "log" || token == "sqrt" ||
           token == "exp";
}

bool Calculator::isOperator(const std::string& token) {
    return token == "+" || token == "-" || token == "*" || token == "/" || token == "^" ||
           token == "u+" || token == "u-";
}

int Calculator::getArity(const std::string& token) {
    if (isFunction(token) || token == "u+" || token == "u-") return 1;
    if (isOperator(token)) return 2;
    return 0;
}

int Calculator::getPrecedence(const std::string& op) {
    if (op == "u+" || op == "u-") return 4;
    if (op == "^") return 3;
    if (op == "*" || op == "/") return 2;
    if (op == "+" || op == "-") return 1;
    return 0;
}

std::vector<std::string> Calculator::infixToRPN(const std::vector<std::string>& tokens) {
    std::vector<std::string> output;
    std::stack<std::string> ops;

    for (const auto& token : tokens) {
        if (isNumber(token)) {
            output.push_back(token);
        } else if (isConstant(token)) {
            output.push_back(std::to_string(getConstantValue(token)));
        } else if (isFunction(token)) {
            ops.push(token);
        } else if (token == "(") {
            ops.push(token);
        } else if (token == ")") {
            while (!ops.empty() && ops.top() != "(") {
                output.push_back(ops.top());
                ops.pop();
            }
            if (ops.empty()) throw std::runtime_error("Несбалансированные скобки");
            ops.pop(); // убрать "("
            if (!ops.empty() && isFunction(ops.top())) {
                output.push_back(ops.top());
                ops.pop();
            }
        } else if (isOperator(token)) {
            int prec = getPrecedence(token);
            while (!ops.empty() && ops.top() != "(" &&
                   ((isOperator(ops.top()) && getPrecedence(ops.top()) >= prec) ||
                    isFunction(ops.top()))) {
                output.push_back(ops.top());
                ops.pop();
            }
            ops.push(token);
        } else {
            throw std::runtime_error("Неизвестный токен: " + token);
        }
    }

    while (!ops.empty()) {
        if (ops.top() == "(" || ops.top() == ")")
            throw std::runtime_error("Несбалансированные скобки");
        output.push_back(ops.top());
        ops.pop();
    }

    return output;
}

double Calculator::evaluateRPN(const std::vector<std::string>& rpn) {
    std::stack<double> stack;
    for (const auto& token : rpn) {
        if (isNumber(token)) {
            stack.push(std::stod(token));
        } else if (isFunction(token)) {
            if (stack.size() < 1) throw std::runtime_error("Недостаточно операндов для функции");
            double a = stack.top(); stack.pop();
            if (token == "sin") stack.push(sin(a));
            else if (token == "cos") stack.push(cos(a));
            else if (token == "tan") stack.push(tan(a));
            else if (token == "asin") stack.push(asin(a));
            else if (token == "acos") stack.push(acos(a));
            else if (token == "atan") stack.push(atan(a));
            else if (token == "ln") stack.push(log(a));
            else if (token == "log") stack.push(log10(a));
            else if (token == "sqrt") stack.push(sqrt(a));
            else if (token == "exp") stack.push(exp(a));
            else throw std::runtime_error("Неизвестная функция: " + token);
        } else if (token == "u-") {
            if (stack.size() < 1) throw std::runtime_error("Недостаточно операндов для унарного минуса");
            double a = stack.top(); stack.pop();
            stack.push(-a);
        } else if (token == "u+") {
            // ничего не делаем
        } else if (token == "+") {
            if (stack.size() < 2) throw std::runtime_error("Недостаточно операндов для +");
            double b = stack.top(); stack.pop();
            double a = stack.top(); stack.pop();
            stack.push(a + b);
        } else if (token == "-") {
            if (stack.size() < 2) throw std::runtime_error("Недостаточно операндов для -");
            double b = stack.top(); stack.pop();
            double a = stack.top(); stack.pop();
            stack.push(a - b);
        } else if (token == "*") {
            if (stack.size() < 2) throw std::runtime_error("Недостаточно операндов для *");
            double b = stack.top(); stack.pop();
            double a = stack.top(); stack.pop();
            stack.push(a * b);
        } else if (token == "/") {
            if (stack.size() < 2) throw std::runtime_error("Недостаточно операндов для /");
            double b = stack.top(); stack.pop();
            double a = stack.top(); stack.pop();
            if (b == 0) throw std::runtime_error("Деление на ноль");
            stack.push(a / b);
        } else if (token == "^") {
            if (stack.size() < 2) throw std::runtime_error("Недостаточно операндов для ^");
            double b = stack.top(); stack.pop();
            double a = stack.top(); stack.pop();
            stack.push(pow(a, b));
        } else {
            throw std::runtime_error("Неизвестный оператор в RPN: " + token);
        }
    }

    if (stack.size() != 1)
        throw std::runtime_error("Некорректное выражение");
    return stack.top();
}

double Calculator::evaluate(const std::vector<std::string>& tokens) {
    auto rpn = infixToRPN(tokens);
    return evaluateRPN(rpn);
}
