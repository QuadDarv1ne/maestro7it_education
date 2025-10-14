/*
 * ПОМОЩЬ ДЛЯ СТУДЕНТОВ В РЕШЕНИИ ЛАБОРАТОРНЫХ РАБОТ *
 * @file Файл: matrix_diagonals.cpp
 *
 * @brief Лабораторная работа №5, Задача 1
 * Описание: Ввод матрицы 4x4, вывод диагоналей и транспонированной матрицы.
 *
 * Программа запрашивает у пользователя матрицу 4×4 целых чисел,
 * проверяет корректность ввода и выводит:
 * - элементы главной диагонали,
 * - элементы побочной диагонали,
 * - элементы под главной диагональю,
 * - элементы над побочной диагональю,
 * - транспонированную матрицу.
 * 
 * Все операции выполняются с защитой от некорректного ввода.
 * 
 * @note Для компиляции: g++ -std=c++17 matrix_diagonals.cpp -o matrix_diagonals
 * 
 * @author Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
*/

#include <iostream>
#include <limits>

using namespace std;

// Вспомогательная функция для безопасного ввода целого числа
bool getValidInt(int &value) {
    while (!(cin >> value)) {
        cout << "Ошибка ввода! Введите целое число: ";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
    return true;
}

int main() {
    const int N = 4;
    int matrix[N][N];

    cout << "Введите элементы матрицы 4x4 (целые числа):\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            cout << "Элемент [" << i+1 << "][" << j+1 << "]: ";
            getValidInt(matrix[i][j]);
        }
    }

    cout << "\n=== Результаты ===\n";

    // Главная диагональ
    cout << "Элементы главной диагонали: ";
    for (int i = 0; i < N; ++i) {
        cout << matrix[i][i] << " ";
    }
    cout << endl;

    // Побочная диагональ
    cout << "Элементы побочной диагонали: ";
    for (int i = 0; i < N; ++i) {
        cout << matrix[i][N-1-i] << " ";
    }
    cout << endl;

    // Под главной диагональю
    cout << "Элементы под главной диагональю: ";
    bool found = false;
    for (int i = 1; i < N; ++i) {
        for (int j = 0; j < i; ++j) {
            cout << matrix[i][j] << " ";
            found = true;
        }
    }
    if (!found) cout << "(нет)";
    cout << endl;

    // Над побочной диагональю
    cout << "Элементы над побочной диагональю: ";
    found = false;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            if (i + j < N - 1) {
                cout << matrix[i][j] << " ";
                found = true;
            }
        }
    }
    if (!found) cout << "(нет)";
    cout << endl;

    // Транспонирование
    cout << "\nТранспонированная матрица:\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            cout << matrix[j][i] << " ";
        }
        cout << endl;
    }

    return 0;
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/