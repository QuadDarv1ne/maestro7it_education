/*
    Задача №3: Проверка на простое число
    Описание: Напишите программу, которая проверяет, является ли введенное пользователем число простым.
*/

#include <iostream>
#include <cmath>

bool isPrime(int num) {
    if (num <= 1) return false;
    if (num == 2) return true;
    if (num % 2 == 0) return false;
    
    for (int i = 3; i <= std::sqrt(num); i += 2) {
        if (num % i == 0) return false;
    }
    return true;
}

int main() {
    int number;
    std::cout << "Введите число: ";
    std::cin >> number;
    
    if (isPrime(number)) {
        std::cout << number << " является простым числом." << std::endl;
    } else {
        std::cout << number << " не является простым числом." << std::endl;
    }

    return 0;
}
