/**
 * @file euclid_gcd.cpp
 * @brief Реализация алгоритма Евклида для вычисления НОД
 * 
 * Программа запрашивает у пользователя два положительных целых числа,
 * вычисляет их наибольший общий делитель (НОД) с помощью алгоритма Евклида
 * и выводит результат. Обрабатывает некорректный ввод и случай (0, 0).
 */

#include <iostream>
#include <optional>
#include <limits>

/**
 * @brief Вычисляет НОД двух чисел по алгоритму Евклида
 * 
 * @param a Первое число (неотрицательное)
 * @param b Второе число (неотрицательное)
 * @return std::optional<unsigned long> НОД или std::nullopt для (0,0)
 */
std::optional<unsigned long> gcd(unsigned long a, unsigned long b) {
    if (a == 0 && b == 0) return std::nullopt;
    while (b != 0) {
        unsigned long temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    unsigned long num1, num2;
    std::cout << "Введите два положительных целых числа: ";
    
    // Обработка некорректного ввода
    while (!(std::cin >> num1 >> num2) || num1 < 0 || num2 < 0) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cout << "Ошибка! Введите положительные целые числа: ";
    }

    // Вычисление и вывод результата
    auto result = gcd(num1, num2);
    if (result) {
        std::cout << "НОД(" << num1 << ", " << num2 << ") = " << *result << std::endl;
    } else {
        std::cout << "НОД(0, 0) не определён" << std::endl;
    }
    
    return 0;
}
