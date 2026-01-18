/**
 * @file laba_6.cpp
 * @brief Лабораторная работа 6 - Работа со строками
 * @details Программа демонстрирует операции со строками:
 *          - Удаление пробелов и знаков препинания
 *          - Преобразование символов в верхний регистр
 *          - Проверка строки на палиндром
 * @author Студент
 * @date 2026
 */

#include <iostream>
#include <string>
using namespace std;

/**
 * @brief Преобразует символ в верхний регистр
 * @param a Входной символ для преобразования
 * @return Символ в верхнем регистре, если это буква a-z, иначе исходный символ
 * @details Функция использует ASCII коды для преобразования.
 *          Разница между строчной и заглавной буквой = 32
 */
char toUpper(char a) {
    if (a >= 'a' && a <= 'z') {
        return char(a - 32);
    }
    return a;
}

/**
 * @brief Главная функция программы
 * @return 0 при успешном завершении
 * @details Выполняет следующие операции:
 *          1. Удаляет пробелы и знаки препинания из строки
 *          2. Преобразует массив строк в верхний регистр
 *          3. Проверяет строку на палиндром
 */
int main()
{
    string door = "Henlo wreld";
    
    // Удаление пробелов и знаков препинания
    for (int i = 0; i < door.length(); i++) {
        if (door[i] == ' ' || door[i] == '!' || door[i] == '?' || door[i] == '.') {
            door.erase(i, 1);
            i--;
        }
    }
    cout << door << endl;
    
    // Массив строк для преобразования в верхний регистр
    string doors[5] = {
        "one",
        "Uuu",
        "Door",
        "Two  notebook",
        "Kot Shotland"
    };
    
    int arrLen = 5;
    
    // Преобразование в верхний регистр и вывод
    for (int i = 0; i < arrLen; i++) {
        for (int j = 0; j < doors[i].length(); j++) {
            doors[i][j] = toUpper(doors[i][j]);
            cout << doors[i][j];
        }
        cout << endl;
    }
    
    // Проверка на палиндром
    bool isPalindrome = true;
    for (int i = 0; i < door.length() / 2; i++) {
        if (door[i] != door[door.length() - 1 - i]) {
            isPalindrome = false;
            break;
        }
    }
    
    if (isPalindrome) {
        cout << "palindrome" << endl;
    } else {
        cout << "not palindrome" << endl;
    }
    
    return 0;
}