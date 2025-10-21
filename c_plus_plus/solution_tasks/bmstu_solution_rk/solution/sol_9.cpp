/**
 * Задание №9: sol_9.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * Задача:
 * Даны две строки. Найдите самую длинную подстроку, которая встречается в обеих строках.
 * Используйте двумерный массив dp[i][j], где dp[i][j] — длина совпадающей подстроки,
 * заканчивающейся на str1[i-1] и str2[j-1].
 * 
 * Пример ввода:sol_10.cpp
 * information
 * formation
 * 
 * Вывод:
 * formation
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_9.cpp -o sol_9
 */

#include <iostream>
#include <cstring>
#include <windows.h>

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    const int MAX = 1000;
    char A[MAX], B[MAX];
    std::cin.getline(A, MAX);
    std::cin.getline(B, MAX);

    int lenA = std::strlen(A), lenB = std::strlen(B);
    int dp[MAX + 1][MAX + 1] = {};
    int maxLength = 0, endIndex = 0;

    for (int i = 1; i <= lenA; ++i) {
        for (int j = 1; j <= lenB; ++j) {
            if (A[i - 1] == B[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > maxLength) {
                    maxLength = dp[i][j];
                    endIndex = i;
                }
            }
        }
    }

    if (maxLength > 0) {
        for (int i = endIndex - maxLength; i < endIndex; ++i)
            std::cout << A[i];
    }
    std::cout << "\n";
}