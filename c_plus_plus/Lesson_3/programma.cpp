// Пример программы, которая использует условные операторы и циклы для решения задачи

#include <iostream>

int main() {
    int number;
    
    std::cout << "Введите число: ";
    std::cin >> number;

    // Условный оператор
    if (number % 2 == 0) {
        std::cout << "Число четное." << std::endl;
    } else {
        std::cout << "Число нечетное." << std::endl;
    }

    // Цикл for
    std::cout << "Числа от 1 до 5:" << std::endl;
    for (int i = 1; i <= 5; ++i) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // Цикл while
    std::cout << "Числа от 5 до 1:" << std::endl;
    int count = 5;
    while (count > 0) {
        std::cout << count << " ";
        --count;
    }
    std::cout << std::endl;

    return 0;
}