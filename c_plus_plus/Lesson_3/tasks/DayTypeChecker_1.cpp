#include <iostream>
#include <string>

using namespace std;

/** DocString
 * @brief Определяет тип дня недели.
 *
 * Эта функция принимает строку, представляющую день недели,
 * и определяет, является ли этот день рабочим днем или выходным.
 *
 * @param day Строка, представляющая день недели.
 */

void determineDayType(const string& day) {
    if (day == "Понедельник" || day == "Вторник" || day == "Среда" ||
        day == "Четверг" || day == "Пятница") {
        cout << "Рабочий день" << endl;
    } else if (day == "Суббота" || day == "Воскресенье") {
        cout << "Выходной день" << endl;
    } else {
        cout << "Такого дня недели не существует ..." << endl;
    }
}

int main() {
    string day = "Гамбургер";
    determineDayType(day);
    return 0;
}
