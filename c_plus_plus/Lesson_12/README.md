# 1️⃣2️⃣ Работа с файлами и потоками

**Работа с файлами и потоками** — важная часть программирования, которая позволяет сохранять данные, читать их и обмениваться информацией между программами.

В C++ это реализовано через стандартные библиотеки потоков ввода-вывода (`<iostream>`, `<fstream>`, и `<sstream>`).

### 1. Работа с потоками ввода-вывода

Потоки ввода-вывода (I/O streams) позволяют взаимодействовать с данными.

**Основные классы для работы с потоками в C++:**

- `std::cin`: для ввода данных с клавиатуры.
- `std::cout`: для вывода данных на экран.
- `std::cerr`: для вывода ошибок.
- `std::clog`: для записи логов и сообщений.

**Пример использования стандартных потоков:**

```cpp
#include <iostream>

int main() {
    int number;
    std::cout << "Введите число: ";
    std::cin >> number;
    std::cout << "Вы ввели: " << number << std::endl;
    return 0;
}
```

### 2. Работа с файлами

**Для работы с файлами в C++ используются классы из заголовка `<fstream>`:**

- `std::ifstream`: для чтения данных из файла.
- `std::ofstream`: для записи данных в файл.
- `std::fstream`: для чтения и записи данных в файл.

**Пример записи в файл:**

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ofstream outfile("example.txt");

    if (outfile.is_open()) {
        outfile << "Hello, world!" << std::endl;
        outfile.close(); // Закрытие файла
    } else {
        std::cerr << "Не удалось открыть файл для записи" << std::endl;
    }

    return 0;
}
```

**Пример чтения из файла:**

```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ifstream infile("example.txt");
    std::string line;

    if (infile.is_open()) {
        while (std::getline(infile, line)) {
            std::cout << line << std::endl;
        }
        infile.close(); // Закрытие файла
    } else {
        std::cerr << "Не удалось открыть файл для чтения" << std::endl;
    }

    return 0;
}
```

**Пример чтения и записи в один файл с помощью `std::fstream`:**

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::fstream file("example.txt", std::ios::in | std::ios::out | std::ios::trunc);

    if (file.is_open()) {
        file << "Hello, world!" << std::endl;

        file.seekg(0); // Перемещение указателя чтения в начало файла

        std::string line;
        while (std::getline(file, line)) {
            std::cout << line << std::endl;
        }

        file.close(); // Закрытие файла
    } else {
        std::cerr << "Не удалось открыть файл" << std::endl;
    }

    return 0;
}
```

### 3. Работа с буферами и форматированным выводом

**Форматирование вывода**

Для форматирования вывода можно использовать манипуляторы, такие как `std::setw`, `std::setprecision`, и `std::fixed`.

**Пример:**

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double pi = 3.141592653589793;

    std::cout << "Не форматированный вывод: " << pi << std::endl;
    std::cout << "Форматированный вывод (4 знака после запятой): " << std::fixed << std::setprecision(4) << pi << std::endl;

    return 0;
}
```

**Буферизация ввода/вывода**

В C++ потоки буферизуются для оптимизации ввода/вывода.

Например, стандартный `std::cout` использует буфер, чтобы уменьшить количество операций вывода на экран.

- `std::flush`: принудительно сбрасывает буфер.
- `std::endl`: сбрасывает буфер и вставляет символ новой строки.

**Пример:**

```cpp
#include <iostream>

int main() {
    std::cout << "Привет" << std::flush; // Сброс буфера
    std::cout << "Мир" << std::endl; // Сброс буфера и новая строка

    return 0;
}
```

### 4. Строковые потоки

Строковые потоки (<sstream>) позволяют работать со строками как с потоками. Это удобно для парсинга строк и форматирования вывода.

**Пример использования `std::stringstream`:**

```cpp
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::stringstream ss;
    int number = 42;
    std::string text = "Hello, world!";

    ss << number << " - " << text;

    std::string result;
    ss >> result; // Чтение строки из потока

    std::cout << "Результат: " << result << std::endl;

    return 0;
}
```

### Заключение

Работа с файлами и потоками в C++ предоставляет мощные инструменты для ввода/вывода данных.

Использование стандартных потоков ввода/вывода, работы с файлами, буферизации и строковых потоков позволяет создавать гибкие и эффективные программы для обработки данных.



**Автор:** Дуплей Максим Игоревич

**Дата:** 07.09.2024

**Версия 1.0**