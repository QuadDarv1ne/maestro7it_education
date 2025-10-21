/**
 * Задание №3: sol_3.cpp
 * 
 * Автор: Дуплей Максим Игоревич
 * Студент: Кузнецов Юрий Андреевич
 * 
 * Задача:
 * Удалить все цифры из введённой строки, оставив все остальные символы без изменений.
 * Работа должна выполняться исключительно с использованием символьного массива (char[]),
 * без применения std::string и стандартных контейнеров.
 * Рекомендуется использовать два индекса:
 * один — для чтения исходной строки, второй — для записи результата.
 * Если текущий символ не является цифрой, он копируется в позицию записи.
 * 
 * Пример ввода:
 * C++17 is better than C89
 * 
 * Вывод:
 * C++ is better than C
 * 
 * Сборка проекта:
 * g++ -std=c++17 -Wall -Wextra -O2 sol_3.cpp -o sol_3
 */

#include <iostream>
#include <cctype>
#include <windows.h> // Для работы с кодовыми страницами

void removeDigits(char str[]) {
    int readIndex = 0;  // Индекс для чтения исходной строки
    int writeIndex = 0; // Индекс для записи результата

    while (str[readIndex] != '\0') {
        if (!std::isdigit(str[readIndex])) {
            str[writeIndex] = str[readIndex];
            writeIndex++;
        }
        readIndex++;
    }
    str[writeIndex] = '\0'; // Завершаем результирующую строку нулевым символом   
}

int main() {
    // Для версий Windows 10 и выше можно использовать UTF-8 для работы с Кириллицей
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    const int MAX = 255;
    char str[MAX];
    std::cout << "Введите строку: ";
    std::cin.getline(str, MAX);
    removeDigits(str);
    std::cout << "Результат: " << str << std::endl;
    return 0;
}
