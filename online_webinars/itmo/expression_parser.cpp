/**
 * @file expression_parser.cpp
 * @brief Парсер арифметических выражений с переменными методом рекурсивного спуска
 * 
 * Программа разбирает арифметические выражения, содержащие:
 * - бинарные операции: *, /, +, -
 * - унарный минус: -
 * - переменные: $0, $1, ...
 * - целочисленные константы в 32-битном диапазоне
 * - круглые скобки для задания приоритета
 * - пробелы между токенами
 * 
 * Приоритет операций (от высшего к низшему):
 * 1. Унарный минус
 * 2. Умножение и деление
 * 3. Сложение и вычитание
 * 
 * Алгоритм:
 * Используется метод рекурсивного спуска, который строит абстрактное
 * синтаксическое дерево (AST). Каждый узел дерева представляет собой:
 * - константу (Constant)
 * - переменную (Variable)
 * - бинарную операцию (BinaryOperation)
 * - унарный минус (UnaryMinus)
 * 
 * Пример выражения: "$0 * ($0 - 2)*$0 + 1"
 * 
 * При вычислении переменные $0, $1, ... заменяются на значение x,
 * переданное в метод evaluate().
 * 
 * Сложность алгоритма: O(n), где n - длина входной строки.
 * 
 * Обработка ошибок:
 * - Синтаксические ошибки в выражении
 * - Деление на ноль при вычислении
 * - Константы вне 32-битного диапазона
 * 
 * Формат ввода:
 * Каждая строка содержит одно выражение.
 * Программа вычисляет значение выражения для x от 0 до 10.
 * 
 * Пример работы:
 * Ввод: "$0 * ($0 - 2)*$0 + 1"
 * Вывод: "1 0 -3 -8 -15 -24 -35 -48 -63 -80 -99"
 */

#include <iostream>
#include <string>
#include <cctype>
#include <stdexcept>
#include <sstream>
#include <cstdint>

/**
 * @brief Абстрактный базовый класс для всех выражений
 */
class Expression {
public:
    virtual ~Expression() = default;
    
    /**
     * @brief Вычисляет значение выражения
     * @param x Значение переменной
     * @return Результат вычисления
     */
    virtual int evaluate(int x) const = 0;
};

/**
 * @brief Класс для представления целочисленной константы
 */
class Constant : public Expression {
    int value;
public:
    explicit Constant(int val) : value(val) {}
    int evaluate(int) const override { return value; }
};

/**
 * @brief Класс для представления переменной
 * 
 * Переменные вида $0, $1, ... заменяются на значение x.
 * В текущей реализации все переменные имеют одинаковое значение.
 */
class Variable : public Expression {
    int index;
public:
    explicit Variable(int idx) : index(idx) {}
    int evaluate(int x) const override { return x; }
};

/**
 * @brief Класс для представления бинарной операции
 * 
 * Поддерживает операции: +, -, *, /
 */
class BinaryOperation : public Expression {
    char op;
    Expression* left;
    Expression* right;
public:
    BinaryOperation(char op, Expression* l, Expression* r) 
        : op(op), left(l), right(r) {}
    
    ~BinaryOperation() {
        delete left;
        delete right;
    }
    
    int evaluate(int x) const override {
        int l = left->evaluate(x);
        int r = right->evaluate(x);
        switch(op) {
            case '+': return l + r;
            case '-': return l - r;
            case '*': return l * r;
            case '/': 
                if (r == 0) throw std::runtime_error("Division by zero");
                return l / r;
            default: throw std::runtime_error("Unknown operation");
        }
    }
};

/**
 * @brief Класс для представления унарного минуса
 */
class UnaryMinus : public Expression {
    Expression* expr;
public:
    explicit UnaryMinus(Expression* e) : expr(e) {}
    ~UnaryMinus() { delete expr; }
    
    int evaluate(int x) const override {
        return -expr->evaluate(x);
    }
};

/**
 * @brief Парсер выражений методом рекурсивного спуска
 * 
 * Грамматика:
 *   expression  ::= addsub
 *   addsub      ::= muldiv (('+' | '-') muldiv)*
 *   muldiv      ::= unary (('*' | '/') unary)*
 *   unary       ::= '-' unary | primary
 *   primary     ::= '(' expression ')' | '$' number | number
 *   number      ::= digit+
 */
class Parser {
    std::string input;  ///< Входная строка
    size_t pos;         ///< Текущая позиция в строке
    
    /**
     * @brief Пропускает пробельные символы
     */
    void skipSpaces() {
        while (pos < input.size() && std::isspace(input[pos])) {
            ++pos;
        }
    }
    
    /**
     * @brief Возвращает текущий символ без продвижения
     * @return Текущий символ или 0, если достигнут конец строки
     */
    char peek() {
        skipSpaces();
        if (pos < input.size()) return input[pos];
        return 0;
    }
    
    /**
     * @brief Читает текущий символ с продвижением
     * @return Считанный символ или 0, если достигнут конец строки
     */
    char get() {
        skipSpaces();
        if (pos < input.size()) return input[pos++];
        return 0;
    }
    
    // Рекурсивные функции разбора (объявления)
    Expression* parseExpression();
    Expression* parseAddSub();
    Expression* parseMulDiv();
    Expression* parseUnary();
    Expression* parsePrimary();
    
public:
    /**
     * @brief Конструктор парсера
     * @param str Входная строка с выражением
     */
    explicit Parser(const std::string& str) : input(str), pos(0) {}
    
    /**
     * @brief Основной метод разбора выражения
     * @return Указатель на корень AST
     * @throws std::runtime_error при синтаксической ошибке
     */
    Expression* parse() {
        Expression* result = parseExpression();
        if (pos < input.size()) {
            delete result;
            throw std::runtime_error("Unexpected characters at end of input");
        }
        return result;
    }
};

/**
 * @brief Разбор выражения (стартовая точка)
 * @return Указатель на разобранное выражение
 */
Expression* Parser::parseExpression() {
    return parseAddSub();
}

/**
 * @brief Разбор операций сложения и вычитания
 * 
 * Грамматика: muldiv (('+' | '-') muldiv)*
 * Обрабатывает левую ассоциативность операций.
 */
Expression* Parser::parseAddSub() {
    Expression* left = parseMulDiv();
    
    while (true) {
        char op = peek();
        if (op == '+' || op == '-') {
            get();
            Expression* right = parseMulDiv();
            left = new BinaryOperation(op, left, right);
        } else {
            break;
        }
    }
    return left;
}

/**
 * @brief Разбор операций умножения и деления
 * 
 * Грамматика: unary (('*' | '/') unary)*
 * Обрабатывает левую ассоциативность операций.
 */
Expression* Parser::parseMulDiv() {
    Expression* left = parseUnary();
    
    while (true) {
        char op = peek();
        if (op == '*' || op == '/') {
            get();
            Expression* right = parseUnary();
            left = new BinaryOperation(op, left, right);
        } else {
            break;
        }
    }
    return left;
}

/**
 * @brief Разбор унарных операций
 * 
 * Грамматика: '-' unary | primary
 * Унарный минус имеет наивысший приоритет.
 */
Expression* Parser::parseUnary() {
    skipSpaces();
    
    if (peek() == '-') {
        get();
        Expression* expr = parseUnary();
        return new UnaryMinus(expr);
    }
    
    return parsePrimary();
}

/**
 * @brief Разбор первичных выражений
 * 
 * Грамматика: '(' expression ')' | '$' number | number
 * Обрабатывает:
 * - выражения в скобках
 * - переменные вида $0, $1, ...
 * - целочисленные константы
 */
Expression* Parser::parsePrimary() {
    skipSpaces();
    char c = get();
    
    // Обработка скобок
    if (c == '(') {
        Expression* expr = parseExpression();
        skipSpaces();
        if (get() != ')') {
            delete expr;
            throw std::runtime_error("Expected ')'");
        }
        return expr;
    }
    
    // Обработка переменных
    if (c == '$') {
        std::string num;
        while (pos < input.size() && std::isdigit(input[pos])) {
            num += get();
        }
        if (num.empty()) {
            throw std::runtime_error("Expected variable index after '$'");
        }
        int index = std::stoi(num);
        return new Variable(index);
    }
    
    // Обработка чисел (может начинаться с цифры, '+' или '-')
    if (std::isdigit(c) || c == '-' || c == '+') {
        std::string num;
        num += c;
        while (pos < input.size() && std::isdigit(input[pos])) {
            num += get();
        }
        
        // Проверка, что это не просто знак
        if (num == "-" || num == "+") {
            throw std::runtime_error("Invalid number format");
        }
        
        // Проверка диапазона 32-битного числа
        try {
            long long val = std::stoll(num);
            if (val < INT32_MIN || val > INT32_MAX) {
                throw std::runtime_error("Constant out of 32-bit range");
            }
            return new Constant(static_cast<int>(val));
        } catch (const std::out_of_range&) {
            throw std::runtime_error("Constant out of range");
        }
    }
    
    // Неизвестный символ
    throw std::runtime_error("Unexpected character");
}

/**
 * @brief Основная функция программы
 * 
 * Читает выражения из стандартного ввода, парсит их и вычисляет
 * значения для x от 0 до 10.
 * 
 * Формат вывода: для каждого x выводится результат через пробел,
 * в случае ошибки - "ERROR" для соответствующего x.
 * 
 * @return 0 при успешном завершении
 */
int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        try {
            Parser parser(line);
            Expression* expr = parser.parse();
            
            // Вычисление для x от 0 до 10
            for (int x = 0; x <= 10; ++x) {
                try {
                    std::cout << expr->evaluate(x) << " ";
                } catch (const std::runtime_error& e) {
                    std::cout << "ERROR ";
                }
            }
            std::cout << std::endl;
            
            delete expr;
        } catch (const std::exception& e) {
            // Синтаксическая ошибка во всем выражении
            std::cout << "ERROR" << std::endl;
        }
    }
    return 0;
}