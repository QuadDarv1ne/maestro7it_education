/**
 * Задание №10: sol_10.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * Задача:
 * Напишите программу, которая переворачивает каждое слово в строке,
 * но сохраняет порядок слов.
 * Слова разделяются пробелами и знаками препинания.
 * 
 * Пример ввода:
 * C++ strings are powerful
 * 
 * Вывод:
 * ++C sgnirts era lufrewop
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_10.cpp -o sol_10
 */

#include <iostream>
#include <cstring>
#include <windows.h>

void reverseRange(char s[], int l, int r) {
    while (l < r) {
        char tmp = s[l];
        s[l] = s[r];
        s[r] = tmp;
        ++l; --r;
    }
}

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    const int MAX = 1000;
    char s[MAX];
    std::cin.getline(s, MAX);

    int start = 0;
    for (int i = 0; s[i] || (i > 0 && s[i - 1]); ++i) {
        if (s[i] == ' ' || s[i] == '\0') {
            reverseRange(s, start, i - 1);
            start = i + 1;
        }
    }
    std::cout << s << "\n";
}