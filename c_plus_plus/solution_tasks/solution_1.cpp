/*
    Задача №1: Перевод температуры
    Описание: Напишите программу, которая переводит температуру из Цельсия в Фаренгейты и наоборот.
*/

#include <iostream>

void celsiusToFahrenheit(double celsius) {
    double fahrenheit = (celsius * 9 / 5) + 32;
    std::cout << celsius << " градусов Цельсия = " << fahrenheit << " градусов Фаренгейта" << std::endl;
}

void fahrenheitToCelsius(double fahrenheit) {
    double celsius = (fahrenheit - 32) * 5 / 9;
    std::cout << fahrenheit << " градусов Фаренгейта = " << celsius << " градусов Цельсия" << std::endl;
}

int main() {
    int choice;
    double temperature;

    std::cout << "Выберите направление перевода:" << std::endl;
    std::cout << "1. Цельсий в Фаренгейт" << std::endl;
    std::cout << "2. Фаренгейт в Цельсий" << std::endl;
    std::cin >> choice;

    std::cout << "Введите температуру: ";
    std::cin >> temperature;

    if (choice == 1) {
        celsiusToFahrenheit(temperature);
    } else if (choice == 2) {
        fahrenheitToCelsius(temperature);
    } else {
        std::cout << "Неверный выбор!" << std::endl;
    }

    return 0;
}
