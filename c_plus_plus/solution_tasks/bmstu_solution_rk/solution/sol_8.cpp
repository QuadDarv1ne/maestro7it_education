/**
 * Задание №8: sol_8.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * Задача:
 * Напишите программу, которая корректирует регистр символов в тексте так, чтобы:
 * — первая буква каждого предложения была заглавной,
 * — остальные — строчные.
 * Границы предложений определяются по символам '.', '!', '?'.
 * 
 * Пример ввода:
 * это пример. а вот второе предложение! третье?
 * 
 * Вывод:
 * Это пример. А вот второе предложение! Третье?
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_8.cpp -o sol_8
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
    std::cin.getline(s, MAX);

    bool newSentence = true;
    for (int i = 0; s[i]; ++i) {
        if (s[i] == '.' || s[i] == '!' || s[i] == '?') {
            newSentence = true;
        } else if (std::isalpha(s[i])) {
            if (newSentence) {
                s[i] = std::toupper(s[i]);
                newSentence = false;
            } else {
                s[i] = std::tolower(s[i]);
            }
        }
    }
    std::cout << s << "\n";
}