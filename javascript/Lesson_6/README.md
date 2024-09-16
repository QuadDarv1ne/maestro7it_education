# Работа со строками

В C++ работа со строками может быть выполнена с использованием стандартной библиотеки `<string>`.

**Основные методы для работы со строками, конкатенация, интерполяция и шаблонные строки описаны ниже:**

### 1. Основные методы для работы со строками

**Создание строк:**
```cpp
#include <iostream>
#include <string>

int main() {
    std::string str1 = "Hello";
    std::string str2("World");
    std::string str3 = str1 + " " + str2; // Конкатенация

    std::cout << str3 << std::endl; // Вывод: Hello World

    return 0;
}
```

**Основные методы класса `std::string`:**

- `size()` или `length()`: Возвращает длину строки.
```cpp
std::string s = "example";
std::cout << "Length: " << s.size() << std::endl; // Вывод: 7
```

- `empty()`: Проверяет, пуста ли строка.
```cpp
if (s.empty()) {
    std::cout << "String is empty" << std::endl;
}
```

- `substr()`: Возвращает подстроку.
```cpp
std::string sub = s.substr(0, 4); // Возвращает "exam"
std::cout << sub << std::endl;
````

- `find()`: Ищет подстроку и возвращает индекс первого вхождения.
```cpp
ssize_t found = s.find("ple");
if (found != std::string::npos) {
    std::cout << "Found at: " << found << std::endl;
}
```

- `replace()`: Заменяет часть строки.
```cpp
s.replace(0, 7, "sample"); // Заменяет "example" на "sample"
std::cout << s << std::endl; // Вывод: sample
```

- `erase()`: Удаляет часть строки.
```cpp
s.erase(5, 3); // Удаляет 3 символа, начиная с позиции 5
std::cout << s << std::endl;
```

# 2. Конкатенация и интерполяция строк

**Конкатенация строк:**
```cpp
std::string firstName = "John";
std::string lastName = "Doe";
std::string fullName = firstName + " " + lastName;
std::cout << fullName << std::endl; // Вывод: John Doe
```

**Интерполяция строк:**

В C++ нет встроенной поддержки интерполяции строк, как в Python, но можно использовать потоковый вывод `std::ostringstream` для форматирования строк.

**Пример с `std::ostringstream`:**
```cpp
#include <iostream>
#include <sstream>

int main() {
    std::string name = "Alice";
    int age = 30;

    std::ostringstream oss;
    oss << "Name: " << name << ", Age: " << age;

    std::string result = oss.str();
    std::cout << result << std::endl; // Вывод: Name: Alice, Age: 30

    return 0;
}
```

### 3. Шаблонные строки

Шаблонные строки в C++ можно создать с использованием литералов строк и потоков для подстановки значений.

**Пример с `std::format` (начиная с C++20):**

**Если ваша компилятор поддерживает C++20, вы можете использовать `std::format` для удобного создания строк:**
```cpp
#include <iostream>
#include <format> // Для std::format

int main() {
    std::string name = "Bob";
    int age = 25;

    std::string result = std::format("Name: {}, Age: {}", name, age);
    std::cout << result << std::endl; // Вывод: Name: Bob, Age: 25

    return 0;
}
```

Пример с `boost::format` (если C++20 недоступен):

**Если ваш компилятор не поддерживает C++20, вы можете использовать библиотеку Boost:**

```cpp
#include <iostream>
#include <boost/format.hpp>

int main() {
    std::string name = "Charlie";
    int age = 40;

    std::string result = boost::str(boost::format("Name: %s, Age: %d") % name % age);
    std::cout << result << std::endl; // Вывод: Name: Charlie, Age: 40

    return 0;
}
```



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**