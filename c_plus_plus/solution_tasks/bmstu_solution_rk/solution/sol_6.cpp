/**
 * Задание №6: sol_6.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * Задача:
 * Реализуйте шифрование строки методом Цезаря.
 * Каждая буква сдвигается в алфавите на заданное пользователем число позиций.
 * Символы, не являющиеся буквами, не изменяются. Сдвиг циклический: после Z идёт A.
 * Для заглавных букв используйте диапазон 'A'–'Z', для строчных — 'a'–'z'.
 * Формула: символ = (символ - base + shift) % 26 + base.
 * 
 * Пример ввода:
 * Hello, World!
 * 3
 * 
 * Вывод:
 * Khoor, Zruog!
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_6.cpp -o sol_6
 */

#include <iostream>
#include <cctype>
#include <cstring>
#include <windows.h>

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    const int MAX = 1000;
    char s[MAX];
    int shift;
    std::cin.getline(s, MAX);
    std::cin >> shift;

    for (int i = 0; s[i]; ++i) {
        if (std::isupper(s[i])) {
            s[i] = 'A' + (s[i] - 'A' + shift % 26 + 26) % 26;
        } else if (std::islower(s[i])) {
            s[i] = 'a' + (s[i] - 'a' + shift % 26 + 26) % 26;
        }
    }
    std::cout << s << "\n";
}