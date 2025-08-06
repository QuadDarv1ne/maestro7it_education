#include <iostream>
#include <string>
#include <map>

using namespace std;

/**
 * Определяет тип дня недели.
 *
 * @param day Строка, представляющая день недели.
 */
void determineDayType(const string& day) {
    // Создаем отображение для дней недели и их числовых представлений
    map<string, int> dayMap = {
        {"Понедельник", 1},
        {"Вторник", 2},
        {"Среда", 3},
        {"Четверг", 4},
        {"Пятница", 5},
        {"Суббота", 6},
        {"Воскресенье", 7}
    };

    // Проверяем, есть ли такой день в нашем отображении
    if (dayMap.find(day) != dayMap.end()) {
        int dayNumber = dayMap[day];
        switch (dayNumber) {
            case 1: // Понедельник
            case 2: // Вторник
            case 3: // Среда
            case 4: // Четверг
            case 5: // Пятница
                cout << "Рабочий день" << endl;
                break;
            case 6: // Суббота
            case 7: // Воскресенье
                cout << "Выходной день" << endl;
                break;
        }
    } else {
        cout << "Такого дня недели не существует ..." << endl;
    }
}

int main() {
    // Пример использования
    string day = "Гамбургер";
    determineDayType(day);
    return 0;
}
