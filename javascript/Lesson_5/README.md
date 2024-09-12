# Массивы и объекты

### 1. Создание и работа с массивами

**В C++ массивы** — это последовательности элементов одного типа, хранящиеся в непрерывной области памяти.

**Вот как можно создать и работать с массивами:**

**Объявление и инициализация массивов:**
```cpp
#include <iostream>

int main() {
    // Объявление массива целых чисел размером 5
    int numbers[5] = {1, 2, 3, 4, 5};

    // Доступ к элементам массива
    std::cout << "Первый элемент: " << numbers[0] << std::endl;
    std::cout << "Второй элемент: " << numbers[1] << std::endl;

    // Изменение элемента массива
    numbers[2] = 10;
    std::cout << "Измененный третий элемент: " << numbers[2] << std::endl;

    return 0;
}
```

**Массивы могут быть инициализированы частично:**
```cpp
int numbers[5] = {1, 2};  // Остальные элементы будут инициализированы нулями
```

**Определение размера массива:**
```cpp
int size = sizeof(numbers) / sizeof(numbers[0]);  // Размер массива
std::cout << "Размер массива: " << size << std::endl;
```

**Многомерные массивы:**
```cpp
int matrix[3][3] = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Доступ к элементам
std::cout << "Элемент в строке 2, столбце 3: " << matrix[1][2] << std::endl;
```

### 2. Объекты: ключи и значения

В C++ нет встроенной структуры данных для работы с объектами в стиле ассоциативных массивов (как в JavaScript или Python).

Однако можно использовать стандартные контейнеры, такие как `std::map` и `std::unordered_map`, для создания ассоциативных массивов.

**Использование `std::map`:**
```cpp
#include <iostream>
#include <map>

int main() {
    std::map<std::string, int> ages;

    // Добавление пар ключ-значение
    ages["Alice"] = 30;
    ages["Bob"] = 25;

    // Доступ к значению по ключу
    std::cout << "Возраст Alice: " << ages["Alice"] << std::endl;

    // Проверка наличия ключа
    if (ages.find("Charlie") == ages.end()) {
        std::cout << "Charlie не найден в карте." << std::endl;
    }

    return 0;
}
```

**Использование `std::unordered_map`:**

**`std::unordered_map` работает быстрее для поиска элементов, но не гарантирует порядок ключей:**
```cpp
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<std::string, int> ages;

    // Добавление пар ключ-значение
    ages["Alice"] = 30;
    ages["Bob"] = 25;

    // Доступ к значению по ключу
    std::cout << "Возраст Alice: " << ages["Alice"] << std::endl;

    // Проверка наличия ключа
    if (ages.find("Charlie") == ages.end()) {
        std::cout << "Charlie не найден в карте." << std::endl;
    }

    return 0;
}
```

### 3. Встроенные методы для работы с массивами и объектами

**Работа с массивами:**

**`std::fill`: Заполняет диапазон значениями.**

```cpp
#include <iostream>
#include <algorithm>  // Для std::fill

int main() {
    int arr[5];
    std::fill(arr, arr + 5, 0);  // Заполняет массив значениями 0

    for (int i : arr) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

**`std::copy`: Копирует диапазон элементов.**

```cpp
#include <iostream>
#include <algorithm>  // Для std::copy

int main() {
    int source[] = {1, 2, 3, 4, 5};
    int destination[5];

    std::copy(source, source + 5, destination);

    for (int i : destination) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

**Работа с `std::map` и `std::unordered_map`:**

- `find`: Поиск элемента по ключу.
- `insert`: Добавление новой пары ключ-значение.
- `erase`: Удаление элемента по ключу.
- `at`: Доступ к значению по ключу (с проверкой наличия ключа).
- `clear`: Очистка контейнера.


**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**