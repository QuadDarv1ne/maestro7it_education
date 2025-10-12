# 5️⃣ Массивы и строки: основы работы с последовательностями данных

Массивы и строки являются основными структурами данных для хранения последовательностей элементов.

В C++ существуют разные способы работы с массивами и строками, как стандартные, так и предоставляемые библиотеками.

### 1. Массивы

**Массивы в C++** — это набор элементов одного типа, хранящийся в непрерывной области памяти.

Размер массива должен быть известен на момент компиляции.

**Объявление и инициализация массива**

▶️ **Пример объявления и инициализации массива:**

```cpp
#include <iostream>

int main() {
    int numbers[5] = {1, 2, 3, 4, 5}; // Объявление и инициализация массива целых чисел

    for (int i = 0; i < 5; ++i) {
        std::cout << "Element " << i << ": " << numbers[i] << std::endl;
    }

    return 0;
}
```

**Доступ к элементам массива**

Элементы массива индексируются, начиная с 0.

Доступ к элементу массива осуществляется через индекс.

▶️ **Пример доступа к элементам массива:**

```cpp
#include <iostream>

int main() {
    int values[3] = {10, 20, 30};

    std::cout << "Первый элемент: " << values[0] << std::endl;
    std::cout << "Второй элемент: " << values[1] << std::endl;
    std::cout << "Третий элемент: " << values[2] << std::endl;

    return 0;
}
```

**Массивы и функции**

Массивы могут передаваться в функции как параметры.

Внутри функции массив передаётся, как указатель.

> В C++ указатели — это переменные, которые хранят адреса других переменных в памяти. 
> Указатель может "указывать" на значение, которое хранится по этому адресу.

📖 Основные моменты:

1. **Объявление указателя:** Чтобы объявить указатель, нужно поставить символ * после типа переменной.

**Например:**
```cpp
int* ptr;  // Указатель на целое число
```

2. **Инициализация указателя:** Указатель можно инициализировать адресом переменной с помощью оператора & (адресная операция).

**Например:**

```cpp
int x = 10;
int* ptr = &x;  // ptr указывает на переменную x
```

3. **Разыменовывание указателя:** Операция разыменовывания позволяет получить значение, на которое указывает указатель. Это делается с помощью оператора `*`, но уже в контексте указателя:

```cpp
int x = 10;
int* ptr = &x;
int y = *ptr;  // Разыменовывание указателя, y = 10
```

4. **Передача массива в функцию:** Массивы в `C++` фактически передаются в функции как указатели на первый элемент массива. Это значит, что внутри функции можно работать с оригинальными данными массива, а не с их копией.

**Пример:**

```cpp
void modifyArray(int* arr, int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = arr[i] * 2;  // Изменяем значения массива
    }
}

int main() {
    int arr[] = {1, 2, 3, 4};
    modifyArray(arr, 4);
    // После вызова функции arr = {2, 4, 6, 8}
}
```

▶️ **Пример функции, работающей с массивами:**

```cpp
#include <iostream>

void printArray(int arr[], int size) {
    for (int i = 0; i < size; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

int main() {
    int data[4] = {1, 2, 3, 4};
    printArray(data, 4); // Передача массива в функцию
    return 0;
}
```

---

```cpp
#include <iostream>
#include <array>
#include <vector>
#include <iomanip>
#include <numeric>
#include <algorithm>
#include <string>

// === Конфигурация ===
constexpr size_t DEFAULT_PRECISION = 3;
constexpr size_t ARRAY_SIZE = 5;
using NumberType = float;

// === Информация об авторе ===
const std::string AUTHOR_NAME = "Дуплей М.И.";
const std::string ORCID_ID = "0009-0007-7605-539X";
const std::string SCHOOL_NAME = "Maestro7IT";
const std::string SCHOOL_URL = "https://school-maestro7it.ru/";

/**
 * @brief Выводит информационный баннер об авторе и проекте.
 */
void print_author_info() {
    std::cout << "===============================================\n";
    std::cout << "🎓 Автор: " << AUTHOR_NAME << "\n";
    std::cout << "🆔 ORCID: https://orcid.org/" << ORCID_ID << "\n";
    std::cout << "🏫 Школа программирования: " << SCHOOL_NAME << "\n";
    std::cout << "🌐 Сайт: " << SCHOOL_URL << "\n";
    std::cout << "© " << AUTHOR_NAME << ", " << SCHOOL_NAME << " — " 
              << __DATE__ << "\n"; // Автоматическая дата компиляции
    std::cout << "===============================================\n\n";
}

// --- Остальные функции (без изменений) ---

template <typename Container>
void print_array(const Container& arr, size_t precision = DEFAULT_PRECISION) {
    std::cout << std::fixed << std::setprecision(static_cast<int>(precision));
    for (size_t i = 0; i < arr.size(); ++i) {
        std::cout << "Element [" << i << "] = " << arr[i] << '\n';
    }
    std::cout << '\n';
}

template <typename Container>
NumberType compute_sum(const Container& arr) {
    return std::accumulate(arr.begin(), arr.end(), static_cast<NumberType>(0));
}

template <typename Container>
NumberType find_min(const Container& arr) {
    return *std::min_element(arr.begin(), arr.end());
}

template <typename Container>
NumberType find_max(const Container& arr) {
    return *std::max_element(arr.begin(), arr.end());
}

template <typename Container>
NumberType compute_mean(const Container& arr) {
    if (arr.empty()) return 0;
    return compute_sum(arr) / static_cast<NumberType>(arr.size());
}

template <typename Container>
bool is_sorted_ascending(const Container& arr) {
    return std::is_sorted(arr.begin(), arr.end());
}

template <typename Container>
Container sorted_copy(const Container& arr) {
    Container copy = arr;
    std::sort(copy.begin(), copy.end());
    return copy;
}

template <typename Container>
void print_statistics(const Container& arr) {
    std::cout << "📊 Статистика:\n";
    std::cout << "  Сумма:        " << compute_sum(arr) << '\n';
    std::cout << "  Минимум:      " << find_min(arr) << '\n';
    std::cout << "  Максимум:     " << find_max(arr) << '\n';
    std::cout << "  Среднее:      " << compute_mean(arr) << '\n';
    std::cout << "  Отсортирован: " << (is_sorted_ascending(arr) ? "Да" : "Нет") << '\n';
    std::cout << '\n';
}

template <typename Container>
void demonstrate_sorting(const Container& arr) {
    auto sorted = sorted_copy(arr);
    std::cout << "🔁 Исходный массив:\n";
    print_array(arr, 3);
    std::cout << "✅ Отсортированный массив:\n";
    print_array(sorted, 3);
}

// --- Основная функция ---
int main() {
    // Вывод информации об авторе
    print_author_info();

    const std::array<NumberType, ARRAY_SIZE> numbers = {
        150.0f, 2.6f, 31.3f, 44.5f, 5.757f
    };

    std::cout << "📦 Исходные данные:\n";
    print_array(numbers);

    print_statistics(numbers);
    demonstrate_sorting(numbers);

    // Пример с vector
    std::cout << "🧩 Пример с std::vector:\n";
    std::vector<NumberType> dynamic_numbers = {1.1f, 3.3f, 2.2f, 5.5f};
    print_array(dynamic_numbers);
    print_statistics(dynamic_numbers);

    std::cout.flush();
    return 0;
}
```

### 2. Строки

**В C++ строки могут быть представлены двумя способами:** как массивы символов или с помощью класса `std::string` из стандартной библиотеки.

**Строки как массивы символов**

Строки в `C++` могут быть представлены массивом символов, заканчивающимся нулевым символом `('\0')`.

▶️ **Пример строки как массива символов:**

```cpp
#include <iostream>

int main() {
    char str[] = "Мороз и солнце; день чудесный!\nЕще ты дремлешь, друг прелестный —\nПора, красавица, проснись:\nОткрой сомкнуты негой взоры\nНавстречу северной Авроры,\nЗвездою севера явись!";

    std::cout << "Строка: " << str << std::endl;

    return 0;
}
```

**Работа со строками**

Для работы с массивами символов можно использовать функции из библиотеки `<cstring>`.

▶️ **Пример использования функций для работы со строками:**

```cpp
#include <iostream>
#include <cstring> // Для работы со строками C-style

int main() {
    char str1[] = "Мороз и солнце; день чудесный!\nЕще ты дремлешь, друг прелестный —\nПора, красавица, проснись:\nОткрой сомкнуты негой взоры\nНавстречу северной Авроры,\nЗвездою севера явись!";
    char str2[] = "Hello World";
    char result[1000];

    std::strcpy(result, str1); // Копирование строки
    std::strcat(result, " ");  // Конкатенация строк
    std::strcat(result, str2);

    std::cout << "Результат: " << result << std::endl;

    std::cout << "Длина строки: " << std::strlen(result) << std::endl;

    return 0;
}
```

**Строки с использованием std::string**

Класс `std::string` из стандартной библиотеки предоставляет удобные методы для работы со строками.

▶️ **Пример использования std::string:**

```cpp
#include <iostream>
#include <string> // Для работы с классом std::string

int main() {
    std::string str1 = "Hello";
    std::string str2 = "World";

    std::string result = str1 + " " + str2; // Конкатенация строк
    std::cout << "Результат: " << result << std::endl;

    std::cout << "Длина строки: " << result.length() << std::endl;

    result[0] = 'h'; // Изменение первого символа
    std::cout << "Изменённая строка: " << result << std::endl;

    return 0;
}
```

`std::string` обеспечивает удобный интерфейс для работы со строками и избавляет от необходимости управлять памятью вручную, как это делается с массивами символов.

### 3. Сравнение массивов и строк

Массивы имеют фиксированный размер, который определяется во время компиляции.

Они требуют явного управления памятью и ограничены фиксированными размерами.

`std::string` предоставляет гибкий и мощный интерфейс для работы со строками, управляет памятью автоматически и включает в себя множество полезных методов для обработки текста.

Эти основы помогут вам эффективно работать с последовательностями данных в C++ и выбирать подходящий метод для ваших задач.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
