/*
    Программа для вывода таблицы умножения.

    Описание:
    Программа запрашивает у пользователя число и выводит таблицу умножения для этого числа от 1 до 10.

    Пример работы программы:
    Введите число для вывода таблицы умножения: 7
    
    Таблица умножения для числа 7:
    7 * 1 = 7
    7 * 2 = 14
    7 * 3 = 21
    7 * 4 = 28
    7 * 5 = 35
    7 * 6 = 42
    7 * 7 = 49
    7 * 8 = 56
    7 * 9 = 63
    7 * 10 = 70
*/

#include <iostream>
using namespace std;

int main() {
    int number;

    // Запрос числа у пользователя
    cout << "Введите число для вывода таблицы умножения: ";
    cin >> number;

    // Вывод таблицы умножения
    cout << "Таблица умножения для числа " << number << ":" << endl;
    for (int i = 1; i <= 10; i++) {
        cout << number << " * " << i << " = " << number * i << endl;
    }

    return 0;
}
