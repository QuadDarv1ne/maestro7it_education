# 1️⃣1️⃣ Шаблоны и обобщённое программирование

**Шаблоны в C++** — это мощный инструмент для создания обобщённого кода, который может работать с различными типами данных.

Они позволяют создавать функции и классы, которые могут работать с любым типом данных, обеспечивая гибкость и повторное использование кода.

### 1. Функциональные шаблоны

Функциональные шаблоны позволяют создавать функции, которые могут принимать параметры различных типов.

**Определение шаблона функции**

```cpp
#include <iostream>

// Определение шаблона функции
template <typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    std::cout << "Максимум из 10 и 20: " << max(10, 20) << std::endl; // int
    std::cout << "Максимум из 10.5 и 20.5: " << max(10.5, 20.5) << std::endl; // double

    return 0;
}
```

В этом примере template `<typename T>` определяет шаблон функции `max`, который работает с любым типом `T`.

**Шаблоны с несколькими параметрами**

Функциональные шаблоны могут иметь несколько параметров.

```cpp
#include <iostream>

template <typename T1, typename T2>
void print(T1 a, T2 b) {
    std::cout << "a: " << a << ", b: " << b << std::endl;
}

int main() {
    print(10, 3.14); // int и double
    print("Hello", 42); // const char* и int

    return 0;
}
```

### 2. Класс-шаблоны

Шаблоны классов позволяют создавать классы, которые могут работать с различными типами данных.

Это особенно полезно для создания обобщённых контейнеров, таких как векторы, списки и очереди.

**Определение шаблона класса**

```cpp
#include <iostream>

template <typename T>
class Box {
private:
    T value;
public:
    Box(T v) : value(v) {}

    void setValue(T v) {
        value = v;
    }

    T getValue() const {
        return value;
    }
};

int main() {
    Box<int> intBox(123);
    Box<double> doubleBox(456.78);

    std::cout << "Значение intBox: " << intBox.getValue() << std::endl;
    std::cout << "Значение doubleBox: " << doubleBox.getValue() << std::endl;

    return 0;
}
```

**Шаблоны с несколькими параметрами**

Шаблоны классов могут иметь несколько параметров.

```cpp
#include <iostream>

template <typename T1, typename T2>
class Pair {
private:
    T1 first;
    T2 second;
public:
    Pair(T1 f, T2 s) : first(f), second(s) {}

    T1 getFirst() const {
        return first;
    }

    T2 getSecond() const {
        return second;
    }
};

int main() {
    Pair<int, std::string> myPair(1, "Hello");

    std::cout << "Первый элемент: " << myPair.getFirst() << std::endl;
    std::cout << "Второй элемент: " << myPair.getSecond() << std::endl;

    return 0;
}
```

### 3. Шаблоны методов и классов

Методы в шаблонах классов также могут быть шаблонными.

Это позволяет создавать методы, которые работают с различными типами данных.

**Шаблоны методов класса**

```cpp
#include <iostream>

template <typename T>
class Calculator {
public:
    T add(T a, T b) {
        return a + b;
    }

    T multiply(T a, T b) {
        return a * b;
    }
};

int main() {
    Calculator<int> intCalc;
    Calculator<double> doubleCalc;

    std::cout << "Сумма int: " << intCalc.add(2, 3) << std::endl;
    std::cout << "Произведение double: " << doubleCalc.multiply(2.5, 4.0) << std::endl;

    return 0;
}
```

### 4. Частичные специализации шаблонов

Частичная специализация позволяет создавать специализации шаблонов для определённых типов данных.

**Пример частичной специализации**

```cpp
#include <iostream>

// Шаблон класса
template <typename T>
class Storage {
public:
    void info() {
        std::cout << "Общий Storage" << std::endl;
    }
};

// Частичная специализация для указателей
template <typename T>
class Storage<T*> {
public:
    void info() {
        std::cout << "Storage для указателей" << std::endl;
    }
};

int main() {
    Storage<int> intStorage;
    Storage<int*> pointerStorage;

    intStorage.info(); // Общий Storage
    pointerStorage.info(); // Storage для указателей

    return 0;
}
```

### 5. Полная специализация шаблонов

Полная специализация позволяет создавать специальную реализацию для конкретного типа данных.

```cpp
#include <iostream>

// Полный шаблон
template <typename T>
class Data {
public:
    void print() {
        std::cout << "Общий шаблон" << std::endl;
    }
};

// Полная специализация для типа int
template <>
class Data<int> {
public:
    void print() {
        std::cout << "Специализация для int" << std::endl;
    }
};

int main() {
    Data<double> doubleData;
    Data<int> intData;

    doubleData.print(); // Общий шаблон
    intData.print();    // Специализация для int

    return 0;
}
```

### Заключение

Шаблоны и обобщённое программирование позволяют создавать гибкие и расширяемые программы в C++.

Они обеспечивают возможность написания универсального кода, который может работать с любыми типами данных, что упрощает разработку и поддержку программного обеспечения.

Шаблоны помогают создать эффективные и легко поддерживаемые приложения, обеспечивая высокую степень повторного использования кода.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**