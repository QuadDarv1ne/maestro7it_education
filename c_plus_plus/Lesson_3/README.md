# 3️⃣ Условные операторы и циклы

Условные операторы и циклы позволяют управлять выполнением кода в зависимости от условий и выполнять повторяющиеся задачи.

Они являются основными инструментами для создания логики в программе.

### 1. Условные операторы

Условные операторы позволяют выполнять разные участки кода в зависимости от выполнения или невыполнения определенного условия.

**Оператор if**

Основной условный оператор в `C++` — if.

Он выполняет блок кода, если условие истинно.

```cpp
#include <iostream>

using namespace std; // упрощаем дальнейшую запись кода

int main() {
    int number = 10;
    
    if (number > 0) {
        // std::cout << "Число положительное." << std::endl;
        cout << "Число положительное." << endl;
    }
    
    return 0;
}
```

**Оператор if-else**

Если условие в `if` ложно, то выполняется блок кода после `else`

```cpp
#include <iostream>

using namespace std; // упрощаем дальнейшую запись кода

int main() {
    int number = -5;
    
    if (number >= 0) {
        // std::cout << "Число неотрицательное." << std::endl;
        cout << "Число неотрицательное." << endl;
    } else {
        // std::cout << "Число отрицательное." << std::endl;
        cout << "Число отрицательное." << endl;
    }
    
    return 0;
}
```

**Оператор if-else if-else**

Используется для проверки нескольких условий.

```cpp
#include <iostream>

using namespace std; // упрощаем дальнейшую запись кода

int main() {
    int number = 0;
    
    if (number > 0) {
        // std::cout << "Число положительное." << std::endl;
        cout << "Число положительное." << endl;
    } else if (number < 0) {
        cout << "Число отрицательное." << endl;
    } else {
        cout << "Число равно нулю." << endl;
    }
    
    return 0;
}
```

---

```cpp
#include <iostream>
#include <cmath> // для round()
using namespace std;

int main() {
    double number;
    
    cout << "Введите число: ";
    cin >> number;
    
    // Округляем число до ближайшего целого
    int rounded = round(number);
    
    if (rounded > 0) {
        cout << "Округленное число: " << rounded << " (положительное";
        if (rounded % 2 == 0) {
            cout << " четное)." << endl;
        } else {
            cout << " нечетное)." << endl;
        }
    } else if (rounded < 0) {
        cout << "Округленное число " << rounded << " (отрицательное";
        if (rounded % 2 == 0) {
            cout << " четное)." << endl;
        } else {
            cout << " нечетное)." << endl;
        }
    } else {
        cout << "Округленное число: 0 (ноль)." << endl;
    }
    
    return 0;
}
```

---

**Оператор switch**

Оператор `switch` используется для выбора одного из нескольких блоков кода в зависимости от значения переменной.

```cpp
#include <iostream>

int main() {
    int day = 3;
    
    switch (day) {
        case 1:
            std::cout << "Понедельник" << std::endl;
            break;
        case 2:
            std::cout << "Вторник" << std::endl;
            break;
        case 3:
            std::cout << "Среда" << std::endl;
            break;
        default:
            std::cout << "Другой день недели" << std::endl;
            break;
    }
    
    return 0;
}
```

### 2. Циклы

Циклы позволяют выполнять один и тот же блок кода несколько раз.

**В C++ существуют следующие типы циклов:**

**Цикл for**

Цикл for используется, когда известно количество выполняемых итераций.

```cpp
#include <iostream>

int main() {
    for (int i = 0; i < 5; ++i) {
        std::cout << "Итерация: " << i << std::endl;
    }
    
    return 0;
}
```

**Цикл while**

Цикл `while` выполняется, пока условие истинно.

Он используется, когда количество итераций заранее неизвестно.

```cpp
#include <iostream>

int main() {
    int i = 0;
    while (i < 5) {
        std::cout << "Итерация: " << i << std::endl;
        ++i;
    }
    
    return 0;
}
```

**Цикл do-while**

Цикл `do-while` выполняется хотя бы один раз, а затем продолжает выполняться, пока условие истинно.

```cpp
#include <iostream>

int main() {
    int i = 0;
    do {
        std::cout << "Итерация: " << i << std::endl;
        ++i;
    } while (i < 5);
    
    return 0;
}
```

### 3. Примеры использования

**Пример программы, которая использует условные операторы и циклы для решения задачи:**

```cpp
#include <iostream>

int main() {
    int number;
    
    std::cout << "Введите число: ";
    std::cin >> number;

    // Условный оператор
    if (number % 2 == 0) {
        std::cout << "Число четное." << std::endl;
    } else {
        std::cout << "Число нечетное." << std::endl;
    }

    // Цикл for
    std::cout << "Числа от 1 до 5:" << std::endl;
    for (int i = 1; i <= 5; ++i) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    // Цикл while
    std::cout << "Числа от 5 до 1:" << std::endl;
    int count = 5;
    while (count > 0) {
        std::cout << count << " ";
        --count;
    }
    std::cout << std::endl;

    return 0;
}
```

Этот код демонстрирует использование условных операторов для проверки четности числа и использование циклов `for` и `while` для вывода чисел.

```cpp
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
```

```cpp
#include <iostream>
#include <string>
#include <map>

using namespace std;

/* 
 * Карта или std::map представляет контейнер, где каждое значение ассоциировано с определенным ключом.
 * И по этому ключу можно получить элемент. Причем ключи могут иметь только уникальные значения. 
 * Примером такого контейнера может служить словарь, где каждому слову сопоставляется его перевод или объяснение.
 * Поэтому такие структуры еще называют словарями.
 * Стандартная библиотека C++ предоставляет два типа словарей: std::map<Key, Value> и std::unordered_map<Key, Value>.
 * Эти типы представляют шаблоны, которые типизируются двумя типами.
 * Первый тип - Key задает тип для ключей, а второй тип - Value устанавливает тип для значений.
 */

void determineDayType(const string& day) {
    // Создаем отображение для дней недели
    map<string, string> dayTypes = {
        {"Понедельник", "Рабочий день"},
        {"Вторник", "Рабочий день"},
        {"Среда", "Рабочий день"},
        {"Четверг", "Рабочий день"},
        {"Пятница", "Рабочий день"},
        {"Суббота", "Выходной день"},
        {"Воскресенье", "Выходной день"}
    };

    // Проверяем, есть ли такой день в нашем отображении
    if (dayTypes.find(day) != dayTypes.end()) {
        cout << dayTypes[day] << endl;
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
```

```cpp
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
    string day;
    cout << "Введите день недели: ";
    getline(cin, day); // читаем всю строку, чтобы пользователь мог писать, например, 'Воскресенье'
    determineDayType(day);
    return 0;
}
```

---

```cpp
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
```

---

**Программа на С++ для вывода первых 10 - 15 - 20 чисел последовательности Фиббоначи**

```cpp
#include <bits/stdc++.h>
#include <iostream>
#include <vector>

using namespace std;

/**
 * @brief Генерация последовательности Фибоначчи.
 *
 * Функция создает последовательность Фибоначчи длиной n.
 * Последовательность начинается с 0 и 1, каждый следующий элемент
 * равен сумме двух предыдущих.
 *
 * @param n Количество элементов последовательности.
 * @return vector<long long> Вектор с n элементами последовательности Фибоначчи.
 */
vector<long long> fibonacci(int n) {
    vector<long long> seq;
    if (n <= 0) return seq;

    seq.push_back(0); // F0
    if (n == 1) return seq;

    seq.push_back(1); // F1
    for (int i = 2; i < n; ++i) {
        seq.push_back(seq[i - 1] + seq[i - 2]);
    }
    return seq;
}

/**
 * @brief Вывод последовательности Фибоначчи на экран.
 *
 * Функция генерирует последовательность Фибоначчи длиной n и выводит
 * её в консоль в удобном формате.
 *
 * @param n Количество элементов для вывода.
 */
void printFibonacci(int n) {
    vector<long long> seq = fibonacci(n);
    cout << "Первые " << n << " чисел Фибоначчи: ";
    for (long long num : seq) {
        cout << num << " ";
    }
    cout << endl;
}

/**
 * @brief Главная функция программы.
 *
 * Выводит на экран первые 10, 15 и 20 чисел последовательности Фибоначчи.
 */
int main() {
    printFibonacci(10);  // первые 10 чисел
    printFibonacci(15);  // первые 15 чисел
    printFibonacci(20);  // первые 20 чисел

    return 0;
}
```

---

```cpp
#include <bits/stdc++.h>
#include <iostream>
#include <iomanip> // Для форматирования вывода

using namespace std;

/**
 * @brief Программа для генерации таблицы умножения
 * 
 * Данная программа выводит на экран таблицу умножения чисел от 1 до 10
 * в отформатированном виде с использованием вложенных циклов.
 * 
 * Основные особенности:
 * - Использование манипуляторов вывода для форматирования
 * - Заголовок с номерами столбцов
 * - Разделительная линия для улучшения читаемости
 * - Выравнивание чисел по правому краю в столбцах
 * 
 * @return int Код возврата (0 в случае успешного выполнения)
 */

int main() {
    std::cout << "Таблица умножения:\n\n";
    
    // Заголовок с номерами столбцов
    std::cout << "     ";
    for (int col = 1; col <= 10; ++col) {
        std::cout << std::setw(4) << col;
    }
    std::cout << "\n";

    // Разделительная линия
    std::cout << "     ";
    for (int col = 1; col <= 10; ++col) {
        std::cout << "─ ─ "; // ----
    }
    std::cout << "\n";
    
    // Генерация строк таблицы
    for (int row = 1; row <= 10; ++row) {
        std::cout << std::setw(2) << row << " |"; // Номер строки
        for (int col = 1; col <= 10; ++col) {
            std::cout << std::setw(4) << row * col;
        }
        std::cout << "\n";
    }
    
    return 0;
}
```

---

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
