#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <string>
#include <vector>

using namespace std;

/**
 * @brief Класс для вычисления математических выражений.
 * 
 * Реализует инженерный калькулятор, котороый поддерживает:
 *  - арифметические операции (+, -, *, /, ^),
 *  - унарные операторы (+, -),
 *  - тригонометрические и логарифмические функции,
 *  - константы (pi, e),
 *  - скобки и приоритеты операций.
 * 
 * Внутренне использует алгоритм "сортировочной станции" (Shunting Yard) для преобразования инфиксной записи в постфиксную (обратную польскую запись, RPN), а затем вычисляет результат.
 * 
 * > Сортировочная станция (англ. Shunting Yard Algorithm) — это алгоритм, разработанный Эдсгером Дейкстрой в 1961 году для преобразования математических выражений из инфиксной записи в постфиксную (обратную польскую запись, RPN — Reverse Polish Notation).
 */

class Calculator {
public:
    static double evaluate(const std::vector<std::string>& tokens);
private:
    static std::vector<std::string> infixToPRN(const std::vector<std::string>& tokens);
    
    static double evaluateRPN(const std::vector<std::string>& rpn);
    
    /**
     * @brief Проверяет, является ли токен числом (включая экспоненциальную запись).
     * 
     * @param token Строка для проверки.
     * @return true Если строку можно преобразовать в число.
     * @return false Иначе.
     */
    static bool isNumber(const std::string& token);
    
    /**
     * @brief Проверяет, является ли токен бинарным или унарным оператором.
     * 
     * Поддерживаемые операторы: "+", "-", "*", "/", "^", "u+", "u-".
     * 
     * @param token Строка для проверки.
     * @return true Если токен — оператор.
     * @return false Иначе.
     */
    static bool isOperator(const std::string& token);
    
    /**
     * @brief Проверяет, является ли токен поддерживаемой математической функцией.
     * 
     * Поддерживаемые функции: sin, cos, tan, asin, acos, atan, ln, log, sqrt, exp.
     * 
     * @param token Строка для проверки.
     * @return true Если токен — функция.
     * @return false Иначе.
     */
    static bool isFunction(const std::string& token);
    
    /**
     * @brief Проверяет, является ли токен предопределённой константой.
     * 
     * Поддерживаемые константы: "pi", "e".
     * 
     * @param token Строка для проверки.
     * @return true Если токен — константа.
     * @return false Иначе.
     */
    static bool isConstant(const std::string& token);

    /**
     * @brief Возвращает числовое значение предопределённой константы.
     * 
     * @param token Имя константы ("pi" или "e").
     * @return double Числовое значение константы.
     * @throws std::runtime_error Если константа неизвестна.
     */
    static double getConstantValue(const std::string& token);

    /**
     * @brief Возвращает приоритет оператора для алгоритма сортировочной станции.
     * 
     * Приоритеты:
     * - унарные операторы ("u+", "u-"): 4
     * - возведение в степень ("^"): 3
     * - умножение/деление ("*", "/"): 2
     * - сложение/вычитание ("+", "-"): 1
     * 
     * @param op Оператор в виде строки.
     * @return int Целое число — приоритет оператора.
     */
    static int getPrecedence(const std::string& op);

    /**
     * @brief Возвращает арность токена (количество операндов).
     * 
     * - Функции и унарные операторы ("u+", "u-") имеют арность 1.
     * - Бинарные операторы имеют арность 2.
     * 
     * @param token Токен для анализа.
     * @return int Арность: 1 или 2. Возвращает 0 для чисел и констант.
     */
    static int getArity(const std::string& token); // 1 (для функций/унарных), 2 (для бинарных)
};

#endif