/**
 * @file calculator.cpp
 * @brief Реализация методов класса Calculator
 * 
 * Содержит определения методов для выполнения арифметических операций
 * и обработки ошибок.
 */

#include "calculator.h"
#include <stdexcept>

/**
 * @brief Реализация метода сложения
 */
double Calculator::add(double a, double b) {
    return a + b;
}

/**
 * @brief Реализация метода вычитания
 */
double Calculator::subtract(double a, double b) {
    return a - b;
}

/**
 * @brief Реализация метода умножения
 */
double Calculator::multiply(double a, double b) {
    return a * b;
}

/**
 * @brief Реализация метода деления с проверкой деления на ноль
 * @throws std::runtime_error если делитель равен нулю
 */
double Calculator::divide(double a, double b) {
    if (b == 0) {
        throw std::runtime_error("Деление на ноль невозможно");
    }
    return a / b;
}