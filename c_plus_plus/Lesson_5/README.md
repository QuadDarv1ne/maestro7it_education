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
constexpr size_t ARRAY_SIZE = 10;
using NumberType = double;

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

// --- Работа с основными функциями ---

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
        150.0f, 2.6f, 31.3f, 44.5f, 5.757f, 303.0f, 567.0f, -190.0f, -30.0f, -56.758765454f
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

### 4. Сравнение с векторами (vector)

**🔍 Основные различия**

| Аспект | C-style (`int arr[5]`, `char str[]`) | Современный C++ (`std::array`, `std::vector`, `std::string`) |
|-------|--------------------------------------|---------------------------------------------------------------|
| **Размер** | Фиксированный (компиляция) | `std::array` — фиксированный, `std::vector`/`std::string` — динамический |
| **Память** | Ручное управление или стек | Полностью автоматическое |
| **Безопасность** | Низкая (риск переполнения, утечек) | Высокая (проверки границ, RAII) |
| **Интерфейс** | Минимальный (указатели, `strlen`, `strcpy`) | Богатый (`.size()`, `.push_back()`, `.substr()`, итераторы, алгоритмы STL) |
| **Читаемость** | Низкая | Высокая |

---

**📊 Сравнительная таблица**

| Характеристика            | `int arr[N]` / `char[]` | `std::array` | `std::vector` | `std::string` |
|--------------------------|-------------------------|--------------|---------------|---------------|
| Размер известен на этапе компиляции | ✅ | ✅ | ❌ | ❌ |
| Автоматическое управление памятью | ❌ | ✅ | ✅ | ✅ |
| Поддержка `.size()` | ❌ | ✅ | ✅ | ✅ |
| Динамическое изменение размера | ❌ | ❌ | ✅ | ✅ |
| Безопасность | ❌ | ✅ | ✅ | ✅ |
| Совместимость с STL | ⚠️ (через указатели) | ✅ | ✅ | ✅ |

---

**Наглядное сравнение в коде**

```cpp
/**
 * @file comparison_demo.cpp
 * @brief Наглядное сравнение C-style массивов/строк, std::array, std::vector и std::string.
 * 
 * Образовательный материал школы Maestro7IT: https://school-maestro7it.ru/
 * Автор: Дуплей М.И. — старший преподаватель, аналитик, философ, музыкант, DevOps-инженер
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * Лицензия: CC0 (public domain)
 */

#include <iostream>
#include <array>
#include <vector>
#include <string>
#include <iomanip>

void print_separator(const std::string& title) {
    std::cout << "\n" << std::string(60, '=') << "\n";
    std::cout << "📌 " << title << "\n";
    std::cout << std::string(60, '=') << "\n";
}

// === 1. C-style массив и строка (традиционный C) ===
void demo_c_style() {
    print_separator("C-style: int arr[5] и char str[]");

    // Массив целых
    int c_array[5] = {10, 20, 30, 40, 50};
    std::cout << "Массив (C-style): ";
    for (int i = 0; i < 5; ++i) std::cout << c_array[i] << " ";
    std::cout << "\nРазмер: 5 (жёстко задан, нет .size())\n";

    // Строка в стиле C
    char c_string[] = "Hello, C!";
    std::cout << "Строка (C-style): " << c_string << "\n";
    std::cout << "Длина: " << std::strlen(c_string) << " (вычисляется каждый раз!)\n";
    std::cout << "⚠️  Риск переполнения, нет методов, завершается \\0\n";
}

// === 2. std::array ===
void demo_std_array() {
    print_separator("std::array<int, 5> — безопасный фиксированный массив");

    std::array<int, 5> arr = {10, 20, 30, 40, 50};
    std::cout << "Содержимое: ";
    for (const auto& x : arr) std::cout << x << " ";
    std::cout << "\nРазмер: " << arr.size() << " (известен на этапе компиляции)\n";
    std::cout << "✅ Безопасен, поддерживает итераторы, STL, .size(), .empty()\n";
}

// === 3. std::vector ===
void demo_std_vector() {
    print_separator("std::vector<int> — динамический массив");

    std::vector<int> vec = {10, 20, 30};
    std::cout << "Исходный: ";
    for (const auto& x : vec) std::cout << x << " ";
    std::cout << " | Размер: " << vec.size() << "\n";

    vec.push_back(40);
    vec.push_back(50);
    std::cout << "После push_back: ";
    for (const auto& x : vec) std::cout << x << " ";
    std::cout << " | Размер: " << vec.size() << "\n";

    std::cout << "✅ Размер меняется динамически, память управляется автоматически\n";
}

// === 4. std::string ===
void demo_std_string() {
    print_separator("std::string — современная строка");

    std::string s = "Hello, C++!";
    std::cout << "Строка: " << s << "\n";
    std::cout << "Длина: " << s.length() << " (мгновенно, O(1))\n";
    std::cout << "Подстрока: " << s.substr(7) << "\n";

    s += " 🎉";
    std::cout << "После добавления: " << s << "\n";
    std::cout << "✅ Автоматическое управление памятью, методы, безопасность\n";
}

// === 5. Сравнение возможностей ===
void demo_comparison() {
    print_separator("Сравнение: что можно и нельзя?");

    std::cout << std::left << std::setw(20) << "Операция"
              << std::setw(12) << "C-style"
              << std::setw(12) << "std::array"
              << std::setw(12) << "std::vector"
              << "std::string" << "\n";
    std::cout << std::string(80, '-') << "\n";

    std::cout << std::setw(20) << "Изменить размер"     << "❌" << "  " << "❌" << "  " << "✅" << "  " << "✅" << "\n";
    std::cout << std::setw(20) << ".size()"             << "❌" << "  " << "✅" << "  " << "✅" << "  " << "✅" << "\n";
    std::cout << std::setw(20) << "Безопасность"        << "❌" << "  " << "✅" << "  " << "✅" << "  " << "✅" << "\n";
    std::cout << std::setw(20) << "STL-алгоритмы"       << "⚠️" << "  " << "✅" << "  " << "✅" << "  " << "✅" << "\n";
    std::cout << std::setw(20) << "Автоматическая память" << "❌" << "  " << "✅" << "  " << "✅" << "  " << "✅" << "\n";
}

// === Основная функция ===
int main() {
    std::cout << "🎓 Наглядное сравнение: C-style vs современные контейнеры C++\n";
    std::cout << "Школа программирования Maestro7IT — https://school-maestro7it.ru/\n\n";

    demo_c_style();
    demo_std_array();
    demo_std_vector();
    demo_std_string();
    demo_comparison();

    std::cout << "\n💡 Совет Maestro7IT:\n";
    std::cout << "В 99% случаев используйте std::array, std::vector и std::string.\n";
    std::cout << "C-style — только при работе с legacy API или в embedded-системах.\n\n";

    return 0;
}
```

**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**
