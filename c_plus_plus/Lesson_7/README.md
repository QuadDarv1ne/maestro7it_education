# 7️⃣ Структуры и объединения: пользовательские типы данных

Структуры и объединения в C++ позволяют создавать собственные типы данных, которые могут содержать несколько различных данных.

Эти пользовательские типы данных помогают организовать код и управлять сложными структурами данных.

### 1. Структуры

Структуры `(struct)` позволяют объединять несколько переменных (членов) разных типов под одним именем.

Это удобно для создания более сложных типов данных.

**Объявление и определение структуры**

```cpp
#include <iostream>
#include <string>

using namespace std;

struct Person {
    std::string name;
    int age;
    double height;

    // Конструктор для инициализации
    Person(const std::string& n, int a, double h) : name(n), age(a), height(h) {}
};

int main() {
    // Использование конструктора
    Person person1("Иван", 30, 1.80);

    std::cout << "Имя: " << person1.name << std::endl;
    std::cout << "Возраст: " << person1.age << std::endl;
    std::cout << "Рост: " << person1.height << " м" << std::endl;

    return 0;
}
```

**Инициализация структуры**

Структуру можно инициализировать при объявлении.

```cpp
#include <iostream>

struct Rectangle {
    int width;
    int height;
};

int main() {
    Rectangle rect = {10, 20}; // Инициализация структуры

    std::cout << "Ширина: " << rect.width << std::endl;
    std::cout << "Высота: " << rect.height << std::endl;

    return 0;
}
```

```cpp
#include <iostream>
#include <string>
#include <iomanip> // Для форматирования вывода

// Структура для представления человека
struct Person {
    std::string name;   // Имя
    int age;            // Возраст
    double height;      // Рост в метрах

    // Конструктор для инициализации
    Person(const std::string& n, int a, double h) : name(n), age(a), height(h) {
        if (age < 0) {
            throw std::invalid_argument("Возраст не может быть отрицательным!");
        }
        if (height < 0) {
            throw std::invalid_argument("Рост не может быть отрицательным!");
        }
    }

    // Метод для вывода информации
    void printInfo() const {
        std::cout << "Имя: " << name << std::endl;
        std::cout << "Возраст: " << age << std::endl;
        std::cout << std::fixed << std::setprecision(2)
                  << "Рост: " << height << " м" << std::endl;
    }
};

int main() {
    try {
        // Создание объекта Person
        Person person1("Иван", 30, 1.80);

        // Вывод информации о человеке
        person1.printInfo();
    } catch (const std::exception& e) {
        // Обработка исключений
        std::cerr << "Ошибка: " << e.what() << std::endl;
    }

    return 0;
}
```

**Функции, работающие со структурами**

Функции могут принимать структуры в качестве параметров и возвращать их.

```cpp
#include <iostream>

struct Point {
    int x;
    int y;
};

void printPoint(const Point &p) {
    std::cout << "Точка: (" << p.x << ", " << p.y << ")" << std::endl;
}

Point createPoint(int x, int y) {
    Point p;
    p.x = x;
    p.y = y;
    return p;
}

int main() {
    Point p1 = createPoint(5, 10);
    printPoint(p1);

    return 0;
}
```

### 2. Объединения

Объединения `(union)` позволяют хранить различные типы данных в одной и той же области памяти.

В отличие от структур, объединения используют одну и ту же память для всех своих членов, что делает их более экономичными по памяти, но только один член может быть активен в любой момент времени.

**Объявление и определение объединения**

```cpp
#include <iostream>

union Data {
    int i;
    float f;
    char c;
};

int main() {
    Data data;

    data.i = 10;
    std::cout << "Data.i: " << data.i << std::endl;

    data.f = 220.5;
    std::cout << "Data.f: " << data.f << std::endl; // Перепишет данные

    data.c = 'A';
    std::cout << "Data.c: " << data.c << std::endl; // Перепишет данные

    return 0;
}
```

**Доступ к членам объединения**

При использовании объединения нужно учитывать, что при присвоении значения одному члену, другие члены могут быть изменены или невалидны.

```cpp
#include <iostream>

union Value {
    int intValue;
    double doubleValue;
};

int main() {
    Value v;
    v.intValue = 42;
    std::cout << "intValue: " << v.intValue << std::endl;

    v.doubleValue = 3.14;
    std::cout << "doubleValue: " << v.doubleValue << std::endl; // intValue теперь не определён

    return 0;
}
```

**Использование объединений в структурах**

Объединения можно использовать в структурах, чтобы создавать сложные типы данных.

```cpp
#include <iostream>

struct Data {
    int type;
    union {
        int intValue;
        float floatValue;
        char charValue;
    } value;
};

int main() {
    Data d;
    d.type = 1; // Тип данных
    d.value.intValue = 100;

    if (d.type == 1) {
        std::cout << "intValue: " << d.value.intValue << std::endl;
    }

    d.type = 2;
    d.value.floatValue = 99.9;

    if (d.type == 2) {
        std::cout << "floatValue: " << d.value.floatValue << std::endl;
    }

    return 0;
}
```

### Заключение

Структуры позволяют объединять переменные различных типов и использовать их как единое целое.

Они полезны для организации данных и группировки связанных данных.

Объединения позволяют экономить память, храня разные типы данных в одной и той же области памяти, но только один из них может быть активен в любой момент времени.

Они удобны для ситуаций, когда нужно работать с различными типами данных, но не одновременно.

Оба этих типа данных являются мощными инструментами для создания сложных и эффективных программ в C++.


**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
