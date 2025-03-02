/*
    Задача №2: Генератор случайного пароля
    Описание: Напишите программу, которая генерирует случайный пароль заданной длины.
*/

#include <iostream>
#include <cstdlib>
#include <ctime>

std::string generatePassword(int length) {
    const std::string characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
    std::string password;

    for (int i = 0; i < length; ++i) {
        int index = std::rand() % characters.size();
        password += characters[index];
    }

    return password;
}

int main() {
    std::srand(std::time(0)); // Инициализация генератора случайных чисел
    int length;

    std::cout << "Введите длину пароля: ";
    std::cin >> length;

    std::string password = generatePassword(length);
    std::cout << "Сгенерированный пароль: " << password << std::endl;

    return 0;
}
