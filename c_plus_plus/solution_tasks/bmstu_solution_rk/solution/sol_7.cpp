/**
 * Задание №7: sol_7.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * Задача:
 * Реализуйте алгоритм RLE (Run-Length Encoding) — сжатие строк путём замены
 * последовательностей одинаковых символов на символ и количество повторений.
 * 
 * Пример ввода:
 * aaabbcddddd
 * 
 * Вывод:
 * a3b2c1d5
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_7.cpp -o sol_7
 */

#include <iostream>
#include <cstring>
#include <windows.h>

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    const int MAX = 1000;
    char s[MAX];
    std::cin.getline(s, MAX);

    for (int i = 0; s[i]; ) {
        char c = s[i];
        int count = 0;
        int j = i;
        while (s[j] == c) { ++count; ++j; }
        std::cout << c << count;
        i = j;
    }
    std::cout << "\n";
}