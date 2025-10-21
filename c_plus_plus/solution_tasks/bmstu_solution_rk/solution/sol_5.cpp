/**
 * Задание №5: sol_5.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * 
 * Задача:
 * Считайте строку с клавиатуры и определите, сколько в ней гласных и согласных букв.
 * Учитывайте только английский алфавит. Все остальные символы (пробелы, знаки, цифры) не учитываются.
 * Считайте символы без учёта регистра (через tolower или toupper) и проверяйте принадлежность
 * к множеству гласных: A, E, I, O, U, Y.
 * 
 * Пример ввода:
 * Hello, world!
 * 
 * Вывод:
 * Гласных: 3 Согласных: 7
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_5.cpp -o sol_5
 */

#include <iostream>
#include <cctype>
#include <cstring>

bool isVowel(char c) {
    c = std::tolower(c);
    return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'y';
}

int main() {
    const int MAX = 1000;
    char s[MAX];
    std::cin.getline(s, MAX);
    int vowels = 0, consonants = 0;
    for (int i = 0; s[i]; ++i) {
        if (std::isalpha(s[i])) {
            if (isVowel(s[i])) ++vowels;
            else ++consonants;
        }
    }
    std::cout << "Гласных: " << vowels << " Согласных: " << consonants << "\n";
}