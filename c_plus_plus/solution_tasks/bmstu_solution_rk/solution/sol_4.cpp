/**
 * Задание №4: sol_4.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * 
 * Задача:
 * Даны две строки A и B. Определить, содержатся ли все символы из B в A (порядок не важен).
 * Для каждого символа из B выполняется поиск в A посимвольно.
 * Если хотя бы один символ из B не найден в A — выводится "Нет", иначе — "Да".
 * 
 * Пример ввода:
 * A = information
 * B = train
 * 
 * Вывод:
 * Да
 * 
 * Примечание:
 * Программа работает с однобайтовыми символами (ASCII). Регистр учитывается.
 * 
 * Сборка:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_4.cpp -o sol_4
 */

#include <iostream>
#include <cctype>
#include <windows.h> // Для работы с кодовыми страницами

// Проверяет, содержится ли символ c в строке str
bool contains(const char str[], int len, char c) {
    for (int i = 0; i < len; ++i) {
        if (str[i] == c) {
            return true;
        }
    }
    return false;
}

// Проверяет, содержатся ли все символы B в A
bool allCharsInA(const char A[], int lenA, const char B[], int lenB) {
    for (int i = 0; i < lenB; ++i) {
        if (!contains(A, lenA, B[i])) {
            return false;
        }
    }
    return true;
}

int main() {
    // Для версий Windows 10 и выше можно использовать UTF-8 для работы с Кириллицей
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    const int MAX = 255;
    char A[MAX], B[MAX];
    
    std::cout << "Введите строку A: ";
    std::cin.getline(A, MAX);
    std::cout << "Введите строку B: ";
    std::cin.getline(B, MAX);

    // Вычисляем длины строк A и B
    int lenA = 0, lenB = 0;
    while (A[lenA] != '\0') ++lenA;
    while (B[lenB] != '\0') ++lenB;

    if (allCharsInA(A, lenA, B, lenB)) {
        std::cout << "Да" << std::endl;
    } else {
        std::cout << "Нет" << std::endl;
    }

    return 0;
}
