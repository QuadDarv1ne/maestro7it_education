/**
 * @file calculator.h
 * @brief Заголовочный файл класса Calculator
 * 
 * Содержит объявление класса Calculator с методами для выполнения
 * основных арифметических операций.
 */

#ifndef CALCULATOR_H
#define CALCULATOR_H

/**
 * @class Calculator
 * @brief Класс для выполнения арифметических операций
 * 
 * Предоставляет методы для сложения, вычитания, умножения и деления чисел.
 * Включает проверку ошибок при делении на ноль.
 */
class Calculator {
public:
    /**
     * @brief Сложение двух чисел
     * @param a Первое слагаемое
     * @param b Второе слагаемое
     * @return double Результат сложения a + b
     */
    double add(double a, double b);
    
    /**
     * @brief Вычитание двух чисел
     * @param a Уменьшаемое
     * @param b Вычитаемое
     * @return double Результат вычитания a - b
     */
    double subtract(double a, double b);
    
    /**
     * @brief Умножение двух чисел
     * @param a Первый множитель
     * @param b Второй множитель
     * @return double Результат умножения a * b
     */
    double multiply(double a, double b);
    
    /**
     * @brief Деление двух чисел
     * @param a Делимое
     * @param b Делитель
     * @return double Результат деления a / b
     * @throws std::runtime_error если b равно 0 (деление на ноль)
     */
    double divide(double a, double b);
};

#endif