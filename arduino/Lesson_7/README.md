# ⚡ Указатели и работа с памятью

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Память в Arduino](#память-в-arduino)
3. [Что такое указатель?](#что-такое-указатель)
4. [Объявление указателей](#объявление-указателей)
5. [Операторы & и *](#операторы--и-)
6. [Указатели и массивы](#указатели-и-массивы)
7. [Указатели и функции](#указатели-и-функции)
8. [Динамическое выделение памяти](#динамическое-выделение-памяти)
9. [Типичные ошибки](#типичные-ошибки)
10. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите указатели — один из самых мощных и сложных инструментов программирования. Указатели позволяют работать с памятью напрямую и создавать более эффективный код.

⚠️ **Внимание:** Этот урок сложный! Будьте внимательны и не торопитесь.

---

## Память в Arduino

Прежде чем изучать указатели, нужно понять, как устроена память.

### Типы памяти в Arduino UNO

```
┌─────────────────────────────────────┐
│  ПАМЯТЬ ARDUINO UNO                 │
├─────────────────────────────────────┤
│                                     │
│  Flash (32 KB)                      │
│  ├─ Программный код                │
│  ├─ Константы                       │
│  └─ Постоянные данные               │
│                                     │
│  SRAM (2 KB)                        │
│  ├─ Глобальные переменные           │
│  ├─ Локальные переменные            │
│  ├─ Стек (Stack)                    │
│  └─ Кучаа (Heap)                    │
│                                     │
│  EEPROM (1 KB)                      │
│  ├─ Энергонезависимая память        │
│  └─ Данные сохраняются при выключ.  │
│                                     │
└─────────────────────────────────────┘
```

### Адреса памяти

```cpp
int value = 42;
// Переменная value занимает 2 байта (int = 2 байта)
// Адрес в памяти: например, 0x100

// Представление в памяти:
// Адрес:  0x100  0x101
// Значение: 42    0      (42 = 0x00 0x2A в маленьком формате)

// Мы можем узнать адрес переменной:
int* address = &value;  // & означает "адрес"
```

### SRAM исчисляется быстро!

```cpp
// ❌ ОПАСНО! Переполнение памяти
char large_array[1000];  // 1000 байт
String big_string = "очень длинная строка";
// SRAM только 2 KB! Программа может зависнуть!

// ✅ ПРАВИЛЬНО - экономим память
byte small_array[50];
char text[] = "текст";
```

---

## Что такое указатель?

Указатель — это переменная, которая хранит адрес другой переменной в памяти.

### Визуализация

```
Обычная переменная:
┌──────────────┐
│  value = 42  │
│ адрес: 0x100 │
└──────────────┘

Указатель на переменную:
┌────────────────────┐
│  ptr = 0x100       │
│ адрес: 0x200       │
│ (хранит адрес!)    │
└────────────────────┘
       ↓
       указывает на 0x100
```

### Аналогия

```
Переменная  = ящик с вещами (содержит значение)
Указатель   = стрелка на ящик (содержит адрес)
```

---

## Объявление указателей

### Синтаксис

```cpp
// тип* имя_указателя;
int* ptr;        // Указатель на int
float* fptr;     // Указатель на float
char* cptr;      // Указатель на char
```

### Примеры

```cpp
int value = 42;
int* ptr = &value;  // ptr хранит адрес переменной value

float temperature = 23.5;
float* temp_ptr = &temperature;

boolean flag = true;
boolean* flag_ptr = &flag;
```

### Типы указателей

```cpp
// Указатель на int
int* int_ptr;

// Указатель на char
char* char_ptr;

// Указатель на массив
int* array_ptr;

// NULL указатель (не указывает ни на что)
int* null_ptr = NULL;

// Указатель на указатель
int** ptr_to_ptr;
```

---

## Операторы & и *

### Оператор & (адрес)

Оператор `&` возвращает адрес переменной.

```cpp
int value = 42;

// Получить адрес переменной
int* ptr = &value;

// Вывести адрес
Serial.print("Адрес value: ");
Serial.println((int)ptr);  // Выведет что-то вроде 128

// Адреса обычно выводятся в шестнадцатеричной системе
Serial.println((int)ptr, HEX);
```

### Оператор * (разыменование)

Оператор `*` получает значение по адресу.

```cpp
int value = 42;
int* ptr = &value;

// Получить значение через указатель
int val = *ptr;  // val = 42

// Изменить значение через указатель
*ptr = 100;      // Теперь value = 100

Serial.println(value);  // 100
Serial.println(*ptr);   // 100 (то же самое)
```

### Практический пример

```cpp
void setup() {
  Serial.begin(9600);
  
  int x = 10;
  int y = 20;
  
  int* ptr_x = &x;
  int* ptr_y = &y;
  
  Serial.print("x = ");
  Serial.println(x);                    // 10
  
  Serial.print("*ptr_x = ");
  Serial.println(*ptr_x);               // 10 (то же значение)
  
  Serial.print("Адрес x: ");
  Serial.println((int)ptr_x, HEX);      // Адрес в hex
  
  // Изменяем через указатель
  *ptr_x = 50;
  Serial.print("x после изменения: ");
  Serial.println(x);                    // 50
  
  // Меняем, на что указывает ptr_x
  ptr_x = &y;
  Serial.print("*ptr_x теперь = ");
  Serial.println(*ptr_x);               // 20 (значение y)
}

void loop() { }
```

---

## Указатели и массивы

Массив — это просто указатель на первый элемент!

### Связь между массивом и указателем

```cpp
int array[] = {10, 20, 30, 40, 50};

// array — это указатель на первый элемент
// array == &array[0]

int* ptr = array;  // Указатель на начало массива
// или
int* ptr = &array[0];  // То же самое

// Доступ через указатель
Serial.println(*ptr);       // 10 (первый элемент)
Serial.println(*(ptr + 1)); // 20 (второй элемент)
Serial.println(*(ptr + 2)); // 30 (третий элемент)
```

### Арифметика указателей

```cpp
int array[] = {10, 20, 30, 40, 50};
int* ptr = array;

// ptr указывает на array[0]
Serial.println(*ptr);        // 10

// ptr + 1 указывает на array[1]
ptr = ptr + 1;
Serial.println(*ptr);        // 20

// ptr + 2 указывает на array[2]
ptr = ptr + 2;
Serial.println(*ptr);        // 30

// Можно использовать ++ и --
ptr++;  // Указатель переместился на следующий элемент
Serial.println(*ptr);        // 40

ptr--;  // Указатель переместился на предыдущий элемент
Serial.println(*ptr);        // 30
```

### Передача массива в функцию

```cpp
// Когда передаём массив в функцию, передаём указатель!
void printArray(int* array, int size) {
  for (int i = 0; i < size; i++) {
    Serial.print(array[i]);  // Можем использовать []
    Serial.print(" ");
    
    // Или через указатель:
    Serial.print(*(array + i));  // То же самое
    Serial.print(" ");
  }
  Serial.println();
}

void setup() {
  Serial.begin(9600);
  
  int values[] = {10, 20, 30, 40, 50};
  
  // Передаём массив (передаётся указатель!)
  printArray(values, 5);
  
  // Это то же самое:
  printArray(&values[0], 5);
}

void loop() { }
```

---

## Указатели и функции

Указатели позволяют функции изменять исходные переменные!

### Передача по ссылке через указатель

```cpp
// Функция БЕЗ указателя - не может изменить исходную переменную
void addOne_wrong(int value) {
  value++;  // Изменяется КОПИЯ, не оригинал
}

// Функция С указателем - может изменить исходную переменную
void addOne_correct(int* value) {
  (*value)++;  // Изменяется оригинал!
}

void setup() {
  Serial.begin(9600);
  
  int x = 10;
  
  addOne_wrong(x);
  Serial.println(x);  // 10 (не изменилось)
  
  addOne_correct(&x);
  Serial.println(x);  // 11 (изменилось!)
}

void loop() { }
```

### Функция возвращает указатель

```cpp
// Функция, возвращающая адрес локальной переменной (ОПАСНО!)
int* dangeronus_function() {
  int local_var = 42;
  return &local_var;  // ❌ ОПАСНО! После выхода из функции переменная удаляется
}

// Правильное использование указателей в функциях
void fillArray(int* array, int size, int value) {
  for (int i = 0; i < size; i++) {
    array[i] = value + i;
  }
}

int findMax(int* array, int size) {
  int max = array[0];
  for (int i = 1; i < size; i++) {
    if (array[i] > max) {
      max = array[i];
    }
  }
  return max;
}

void setup() {
  Serial.begin(9600);
  
  int values[5];
  fillArray(values, 5, 10);  // Заполняем массив
  
  int max_val = findMax(values, 5);
  Serial.print("Максимум: ");
  Serial.println(max_val);  // 14
}

void loop() { }
```

---

## Динамическое выделение памяти

⚠️ **Не рекомендуется для Arduino!** SRAM слишком мало.

### malloc и free

```cpp
// Выделить память
int* ptr = (int*)malloc(sizeof(int) * 5);

// Использовать
ptr[0] = 10;
ptr[1] = 20;

// Освободить память
free(ptr);
ptr = NULL;  // Всегда обнуляем после free!
```

### Пример (ОСТОРОЖНО!)

```cpp
void setup() {
  Serial.begin(9600);
  
  // Выделяем память для массива из 5 int
  int* array = (int*)malloc(sizeof(int) * 5);
  
  if (array == NULL) {
    Serial.println("Ошибка: не хватает памяти!");
    return;
  }
  
  // Заполняем
  for (int i = 0; i < 5; i++) {
    array[i] = i * 10;
  }
  
  // Выводим
  for (int i = 0; i < 5; i++) {
    Serial.println(array[i]);
  }
  
  // Освобождаем
  free(array);
  array = NULL;
}

void loop() { }
```

---

## Типичные ошибки

### Ошибка 1: Использование неинициализированного указателя

```cpp
// ❌ ОШИБКА
int* ptr;  // ptr указывает ниоткуда!
*ptr = 42; // КРАШ!

// ✅ ПРАВИЛЬНО
int value = 10;
int* ptr = &value;  // Теперь указывает на value
*ptr = 42;          // OK
```

### Ошибка 2: Выход за границы

```cpp
// ❌ ОШИБКА
int array[5] = {1, 2, 3, 4, 5};
int* ptr = array;
*(ptr + 10) = 99;  // Выход за границы массива!

// ✅ ПРАВИЛЬНО
if (index >= 0 && index < 5) {
  *(ptr + index) = value;
}
```

### Ошибка 3: Возврат адреса локальной переменной

```cpp
// ❌ ОШИБКА
int* getNumber() {
  int local = 42;
  return &local;  // После выхода из функции local удалится!
}

// ✅ ПРАВИЛЬНО
int getNumber() {
  int local = 42;
  return local;  // Возвращаем значение, не адрес
}
```

### Ошибка 4: Забыли скобки при разыменовании

```cpp
// ❌ НЕПРАВИЛЬНО (низкий приоритет *)
int* ptr = &value;
int x = *ptr + 5;  // Может быть непредсказуемо

// ✅ ПРАВИЛЬНО (используем скобки)
int x = (*ptr) + 5;  // Ясно и безопасно
```

---

## Практические примеры

### Пример 1: Обмен значений через указатели

```cpp
void swap(int* a, int* b) {
  int temp = *a;
  *a = *b;
  *b = temp;
  
  Serial.print("Обмен: ");
  Serial.print(*a);
  Serial.print(" и ");
  Serial.println(*b);
}

void setup() {
  Serial.begin(9600);
  
  int x = 10;
  int y = 20;
  
  Serial.print("До: x=");
  Serial.print(x);
  Serial.print(", y=");
  Serial.println(y);
  
  swap(&x, &y);
  
  Serial.print("После: x=");
  Serial.print(x);
  Serial.print(", y=");
  Serial.println(y);
}

void loop() { }
```

### Пример 2: Модификация массива через указатель

```cpp
void incrementAll(int* array, int size, int increment) {
  for (int i = 0; i < size; i++) {
    *(array + i) += increment;  // Изменяем исходный массив
  }
}

int findMaxIndex(int* array, int size) {
  int max_index = 0;
  
  for (int i = 1; i < size; i++) {
    if (*(array + i) > *(array + max_index)) {
      max_index = i;
    }
  }
  
  return max_index;
}

void setup() {
  Serial.begin(9600);
  
  int values[] = {10, 25, 15, 30, 20};
  
  Serial.println("Исходный массив:");
  for (int i = 0; i < 5; i++) {
    Serial.print(values[i]);
    Serial.print(" ");
  }
  Serial.println();
  
  incrementAll(values, 5, 5);
  
  Serial.println("После увеличения на 5:");
  for (int i = 0; i < 5; i++) {
    Serial.print(values[i]);
    Serial.print(" ");
  }
  Serial.println();
  
  int max_idx = findMaxIndex(values, 5);
  Serial.print("Максимум в индексе: ");
  Serial.println(max_idx);
}

void loop() { }
```

### Пример 3: Структура данных с указателями

```cpp
struct Sensor {
  int* values;      // Указатель на массив значений
  int size;         // Размер массива
  String name;      // Имя датчика
};

void initSensor(Sensor* sensor, int array_size, String sensor_name) {
  sensor->values = (int*)malloc(sizeof(int) * array_size);
  sensor->size = array_size;
  sensor->name = sensor_name;
  
  // Инициализируем нулями
  for (int i = 0; i < array_size; i++) {
    sensor->values[i] = 0;
  }
}

void readSensorData(Sensor* sensor) {
  for (int i = 0; i < sensor->size; i++) {
    sensor->values[i] = analogRead(A0 + i);
  }
}

void printSensorData(Sensor* sensor) {
  Serial.print("Датчик: ");
  Serial.println(sensor->name);
  
  for (int i = 0; i < sensor->size; i++) {
    Serial.print("Значение ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(sensor->values[i]);
  }
}

void freeSensor(Sensor* sensor) {
  if (sensor->values != NULL) {
    free(sensor->values);
    sensor->values = NULL;
  }
}

void setup() {
  Serial.begin(9600);
  
  Sensor temp_sensor;
  initSensor(&temp_sensor, 5, "Температура");
  
  readSensorData(&temp_sensor);
  printSensorData(&temp_sensor);
  
  freeSensor(&temp_sensor);
}

void loop() { }
```

### Пример 4: Массив указателей на строки

```cpp
const char* commands[] = {
  "LED_ON",
  "LED_OFF",
  "TEMP",
  "STATUS",
  "RESET"
};

const int NUM_COMMANDS = 5;

int findCommand(const char* cmd) {
  for (int i = 0; i < NUM_COMMANDS; i++) {
    if (strcmp(commands[i], cmd) == 0) {
      return i;
    }
  }
  return -1;  // Не найдено
}

void executeCommand(int command_index) {
  switch (command_index) {
    case 0:  // LED_ON
      digitalWrite(13, HIGH);
      Serial.println("LED включен");
      break;
    case 1:  // LED_OFF
      digitalWrite(13, LOW);
      Serial.println("LED выключен");
      break;
    case 2:  // TEMP
      Serial.print("Температура: ");
      Serial.println(analogRead(A0));
      break;
    case 3:  // STATUS
      Serial.println("Система в норме");
      break;
    case 4:  // RESET
      Serial.println("Перезагрузка...");
      break;
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  
  Serial.println("Доступные команды:");
  for (int i = 0; i < NUM_COMMANDS; i++) {
    Serial.println(commands[i]);
  }
}

void loop() {
  if (Serial.available() > 0) {
    char command[20];
    int i = 0;
    
    while (Serial.available() > 0 && i < 19) {
      char c = Serial.read();
      if (c != '\n') {
        command[i++] = c;
      }
    }
    command[i] = '\0';
    
    int cmd_index = findCommand(command);
    if (cmd_index != -1) {
      executeCommand(cmd_index);
    } else {
      Serial.print("Неизвестная команда: ");
      Serial.println(command);
    }
  }
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Понимать устройство памяти в Arduino

✅ Работать с указателями

✅ Использовать операторы & и *

✅ Связь между массивами и указателями

✅ Передавать указатели в функции

✅ Избегать типичных ошибок

✅ Применять указатели на практике

---

## 🎯 Домашнее задание

1. Напишите функцию `void swapValues(int* a, int* b)` для обмена значений

2. Создайте функцию `int* findValue(int* array, int size, int value)`, возвращающую указатель на найденный элемент

3. Напишите функцию `void reverseArray(int* array, int size)` для инвертирования массива через указатели

4. Создайте функцию `int sumArray(int* array, int size)` для подсчёта суммы через указатель

5. Напишите программу для работы с двумя массивами через указатели

6. Дополнительно: Создайте структуру для хранения данных датчика и работайте с ней через указатели

---

## 🔗 Полезные ссылки

- 📖 **Указатели в C:** https://www.cplusplus.com/reference/
- 📖 **Память Arduino:** https://www.arduino.cc/en/Guide/Memory
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Указатель** | Переменная, хранящая адрес другой переменной |
| **Адрес** | Местоположение переменной в памяти |
| **Оператор &** | Получить адрес переменной |
| **Оператор \*** | Разыменование (получить значение по адресу) |
| **NULL** | Указатель не указывает ни на что |
| **malloc** | Динамическое выделение памяти |
| **free** | Освобождение выделенной памяти |
| **Арифметика указателей** | Перемещение указателя по памяти |
| **Разыменование** | Доступ к значению через указатель |
| **SRAM** | Оперативная память (ограничена!) |

---

**Следующий урок:** 🏗️ [Структуры и объединения: пользовательские типы данных](../Lesson_8/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025