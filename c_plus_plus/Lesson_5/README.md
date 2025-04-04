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
