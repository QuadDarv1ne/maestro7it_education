/**
 * Задание №11: sol_11.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * Задача:
 * Дана строка и число k. Выведите все подстроки длины k, в которых все символы различны.
 * Работайте с массивом символов (char[]).
 * Для каждой подстроки длины k проверяйте уникальность символов двойным циклом.
 * Сдвигайте окно на один символ и повторяйте проверку до конца строки.
 * 
 * Пример ввода:
 * abcabc
 * 3
 * 
 * Вывод:
 * abc bca cab
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_11.cpp -o sol_11
 */

#include <iostream>
#include <cstring>
#include <windows.h>

bool allUnique(char s[], int start, int k) {
    for (int i = start; i < start + k; ++i)
        for (int j = i + 1; j < start + k; ++j)
            if (s[i] == s[j]) return false;
    return true;
}

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    const int MAX = 1000;
    char s[MAX];
    int k;
    std::cin.getline(s, MAX);
    std::cin >> k;

    int n = std::strlen(s);
    bool first = true;
    for (int i = 0; i <= n - k; ++i) {
        if (allUnique(s, i, k)) {
            if (!first) std::cout << " ";
            for (int j = 0; j < k; ++j) std::cout << s[i + j];
            first = false;
        }
    }
    if (!first) std::cout << "\n";
}