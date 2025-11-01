# 📦 Массивы и строки: основы работы с последовательностями данных

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Что такое массив?](#что-такое-массив)
3. [Объявление массивов](#объявление-массивов)
4. [Индексирование массивов](#индексирование-массивов)
5. [Итерация по массивам](#итерация-по-массивам)
6. [Двумерные массивы](#двумерные-массивы)
7. [Строки (String)](#строки-string)
8. [Массивы символов (char)](#массивы-символов-char)
9. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите массивы и строки — способы хранения нескольких значений одного типа. Это очень важно для работы с датчиками, хранения данных и обработки текста.

---

## Что такое массив?

Массив — это коллекция элементов одного типа, расположенных в памяти рядом друг с другом.

### Представление массива в памяти

```
Массив: [10, 20, 30, 40, 50]
         
Индекс:  0   1   2   3   4
         ↓   ↓   ↓   ↓   ↓
Адрес: 1000 1002 1004 1006 1008
         
Значение: 10  20  30  40  50
```

### Преимущества массивов

```
✓ Хранение множества значений в одной переменной
✓ Удобство обработки однотипных данных
✓ Возможность использования циклов
✓ Экономия имён переменных
✓ Упрощение кода
```

### Пример: без массива vs с массивом

```cpp
// ❌ БЕЗ МАССИВА - много переменных
int sensor1 = 100;
int sensor2 = 200;
int sensor3 = 300;
int sensor4 = 400;
int sensor5 = 500;

// Сложно обрабатывать!
Serial.println(sensor1);
Serial.println(sensor2);
Serial.println(sensor3);
// ... и так 5 раз

// ✅ С МАССИВОМ - одна переменная
int sensors[5] = {100, 200, 300, 400, 500};

// Легко обрабатывать!
for (int i = 0; i < 5; i++) {
  Serial.println(sensors[i]);
}
```

---

## Объявление массивов

### Синтаксис

```cpp
// Объявление пустого массива
тип_данных имя_массива[размер];

// Объявление с инициализацией
тип_данных имя_массива[размер] = {значение1, значение2, ...};
```

### Примеры

```cpp
// Массив целых чисел (размер 5)
int numbers[5];

// Массив целых чисел с инициализацией
int values[5] = {10, 20, 30, 40, 50};

// Массив дробных чисел
float temperatures[10] = {22.5, 23.1, 21.8, 24.3, 25.0, 20.2, 19.5, 22.8, 23.4, 24.1};

// Массив логических значений
boolean states[8] = {true, false, true, true, false};

// Автоматическое определение размера
int data[] = {1, 2, 3, 4, 5};  // Размер = 5 автоматически

// Массив строк
String names[3] = {"Arduino", "Raspberry", "STM32"};

// Массив символов
char letters[5] = {'A', 'B', 'C', 'D', 'E'};
```

### Размер массива

```cpp
int values[10];  // Размер ВСЕГДА должен быть известен при объявлении!

// ❌ ОШИБКА - размер неизвестен!
// int array[n];  // n - переменная (не компилируется!)

// ✓ ПРАВИЛЬНО - размер известен
int array[10];  // Размер = 10
```

---

## Индексирование массивов

Индекс — это номер элемента в массиве (начиная с 0).

### Синтаксис

```cpp
// Чтение элемента
int value = array[индекс];

// Запись элемента
array[индекс] = значение;
```

### Примеры

```cpp
// Объявление массива
int values[5] = {10, 20, 30, 40, 50};

// Чтение элементов
int first = values[0];      // 10
int third = values[2];      // 30
int last = values[4];       // 50

// Запись элементов
values[0] = 100;            // Теперь values[0] = 100
values[2] = 300;            // Теперь values[2] = 300

// ⚠️ ОПАСНО! Выход за границы массива
// int wrong = values[10];  // ❌ ОШИБКА! Индекс 10 не существует
// values[5] = 999;         // ❌ ОШИБКА! Переполнение!
```

### Практический пример

```cpp
const int NUM_SENSORS = 5;
int sensor_readings[NUM_SENSORS];

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Читаем значения с 5 датчиков
  sensor_readings[0] = analogRead(A0);
  sensor_readings[1] = analogRead(A1);
  sensor_readings[2] = analogRead(A2);
  sensor_readings[3] = analogRead(A3);
  sensor_readings[4] = analogRead(A4);
  
  // Выводим первый датчик
  Serial.print("Датчик 1: ");
  Serial.println(sensor_readings[0]);
  
  // Выводим третий датчик
  Serial.print("Датчик 3: ");
  Serial.println(sensor_readings[2]);
  
  delay(1000);
}
```

---

## Итерация по массивам

### Цикл for

```cpp
int values[5] = {10, 20, 30, 40, 50};

// Перебор всех элементов
for (int i = 0; i < 5; i++) {
  Serial.println(values[i]);
}

// Вывод: 10, 20, 30, 40, 50
```

### Цикл for-each

```cpp
int values[] = {10, 20, 30, 40, 50};

// Проще и понятнее
for (int value : values) {
  Serial.println(value);
}
```

### Практические примеры

```cpp
// Пример 1: Сумма всех элементов
int values[] = {10, 20, 30, 40, 50};
int sum = 0;

for (int i = 0; i < 5; i++) {
  sum += values[i];
}

Serial.print("Сумма: ");
Serial.println(sum);  // 150

// Пример 2: Поиск максимума
int numbers[] = {45, 12, 89, 34, 56, 23};
int max_value = numbers[0];

for (int i = 1; i < 6; i++) {
  if (numbers[i] > max_value) {
    max_value = numbers[i];
  }
}

Serial.print("Максимум: ");
Serial.println(max_value);  // 89

// Пример 3: Средний результат датчиков
int sensor_values[] = {100, 105, 98, 102, 101};
int sum_sensors = 0;

for (int sensor : sensor_values) {
  sum_sensors += sensor;
}

float average = (float)sum_sensors / 5;
Serial.print("Среднее: ");
Serial.println(average);  // 101.2

// Пример 4: Инвертирование массива
int original[] = {1, 2, 3, 4, 5};
int reversed[5];

for (int i = 0; i < 5; i++) {
  reversed[i] = original[4 - i];
}

// reversed = {5, 4, 3, 2, 1}
```

### Функция для работы с массивом

```cpp
// Функция: вывести все элементы массива
void printArray(int array[], int size) {
  for (int i = 0; i < size; i++) {
    Serial.print(array[i]);
    Serial.print(" ");
  }
  Serial.println();
}

// Функция: найти максимальное значение
int findMax(int array[], int size) {
  int max_val = array[0];
  
  for (int i = 1; i < size; i++) {
    if (array[i] > max_val) {
      max_val = array[i];
    }
  }
  
  return max_val;
}

// Функция: вычислить среднее значение
float calculateAverage(int array[], int size) {
  int sum = 0;
  
  for (int i = 0; i < size; i++) {
    sum += array[i];
  }
  
  return (float)sum / size;
}

void setup() {
  Serial.begin(9600);
  
  int values[] = {10, 25, 15, 30, 20};
  
  Serial.print("Массив: ");
  printArray(values, 5);
  
  Serial.print("Максимум: ");
  Serial.println(findMax(values, 5));
  
  Serial.print("Среднее: ");
  Serial.println(calculateAverage(values, 5));
}

void loop() { }
```

---

## Двумерные массивы

Двумерный массив — это таблица с строками и столбцами.

### Синтаксис

```cpp
// Объявление двумерного массива
тип_данных имя[строки][столбцы];

// С инициализацией
тип_данных имя[строки][столбцы] = {
  {значение, значение, ...},
  {значение, значение, ...},
  ...
};
```

### Примеры

```cpp
// Матрица 3x3
int matrix[3][3] = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9}
};

// Таблица 4x2
float data[4][2] = {
  {10.5, 20.3},
  {15.2, 25.8},
  {12.1, 22.4},
  {18.3, 28.1}
};
```

### Доступ к элементам

```cpp
int matrix[3][3] = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9}
};

// Чтение элемента
int value = matrix[0][1];  // Строка 0, столбец 1 = 2
int value = matrix[2][2];  // Строка 2, столбец 2 = 9

// Запись элемента
matrix[1][1] = 50;         // Центральный элемент = 50
```

### Итерация по двумерному массиву

```cpp
int matrix[3][3] = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9}
};

// Вложенные циклы
for (int row = 0; row < 3; row++) {
  for (int col = 0; col < 3; col++) {
    Serial.print(matrix[row][col]);
    Serial.print("\t");  // Табуляция
  }
  Serial.println();       // Новая строка
}

// Вывод:
// 1  2  3
// 4  5  6
// 7  8  9
```

### Практический пример: таблица умножения

```cpp
int multiplication[10][10];

void setup() {
  Serial.begin(9600);
  
  // Заполняем таблицу умножения
  for (int i = 1; i <= 10; i++) {
    for (int j = 1; j <= 10; j++) {
      multiplication[i-1][j-1] = i * j;
    }
  }
  
  // Выводим таблицу
  for (int i = 1; i <= 10; i++) {
    for (int j = 1; j <= 10; j++) {
      Serial.print(multiplication[i-1][j-1]);
      Serial.print("\t");
    }
    Serial.println();
  }
}

void loop() { }
```

---

## Строки (String)

String в Arduino — это объект для работы со строками (не рекомендуется для микроконтроллеров с малой памятью).

### Синтаксис

```cpp
// Объявление строки
String text = "Hello Arduino";

// Конкатенация (объединение)
String greeting = "Hello" + " " + "World";

// Преобразование чисел в строку
String number_str = String(42);
String float_str = String(3.14, 2);  // 2 знака после запятой
```

### Методы String

```cpp
String text = "Arduino";

// Длина строки
int length = text.length();           // 7

// Преобразование в верхний регистр
String upper = text.toUpperCase();    // "ARDUINO"

// Преобразование в нижний регистр
String lower = text.toLowerCase();    // "arduino"

// Получить символ по индексу
char first_char = text.charAt(0);     // 'A'

// Поиск подстроки
int index = text.indexOf("dui");      // 3

// Получить подстроку
String sub = text.substring(2, 5);    // "dui"

// Удалить пробелы
String trimmed = "  Hello  ".trim(); // "Hello"

// Замена
String replaced = text.replace("A", "X");  // "Xrduino"
```

### Примеры работы со String

```cpp
void setup() {
  Serial.begin(9600);
  
  String name = "Arduino";
  int value = 42;
  float temperature = 23.5;
  
  // Конкатенация с числами
  String message = "Название: " + name + ", Значение: " + String(value);
  Serial.println(message);  // Название: Arduino, Значение: 42
  
  // Конкатенация температуры
  String temp_msg = "Температура: " + String(temperature, 1) + "°C";
  Serial.println(temp_msg);  // Температура: 23.5°C
  
  // Условная проверка
  if (name == "Arduino") {
    Serial.println("Это Arduino!");
  }
  
  // Работа с частями строки
  String command = "LED_ON";
  if (command.startsWith("LED")) {
    Serial.println("Это команда для LED");
  }
}

void loop() { }
```

---

## Массивы символов (char)

Массив символов — это более эффективный способ работы со строками (экономит память).

### Синтаксис

```cpp
// Массив символов (C-строка)
char text[20] = "Hello";  // Размер должен быть на 1 больше!

// Без инициализации размера
char text[] = "Arduino";  // Размер определяется автоматически
```

### Важное: null-терминатор

```cpp
// Каждая C-строка должна заканчиваться '\0'
char text[6] = "Hello";
//            = {'H', 'e', 'l', 'l', 'o', '\0'}
//               0    1    2    3    4    5
```

### Примеры

```cpp
void setup() {
  Serial.begin(9600);
  
  // Объявление C-строки
  char message[20] = "Hello Arduino!";
  
  // Вывод строки
  Serial.println(message);
  
  // Доступ к отдельным символам
  char first = message[0];   // 'H'
  char last = message[5];    // 'A'
  
  // Изменение символов
  message[0] = 'J';          // "Jello Arduino!"
  Serial.println(message);
}

void loop() { }
```

### Функции для работы с char массивами

```cpp
// Функция: длина строки
int string_length(char str[]) {
  int length = 0;
  while (str[length] != '\0') {
    length++;
  }
  return length;
}

// Функция: сравнение строк
boolean strings_equal(char str1[], char str2[]) {
  int i = 0;
  while (str1[i] != '\0' && str2[i] != '\0') {
    if (str1[i] != str2[i]) {
      return false;
    }
    i++;
  }
  return (str1[i] == '\0' && str2[i] == '\0');
}

// Функция: копирование строки
void string_copy(char source[], char destination[]) {
  int i = 0;
  while (source[i] != '\0') {
    destination[i] = source[i];
    i++;
  }
  destination[i] = '\0';
}

void setup() {
  Serial.begin(9600);
  
  char text1[20] = "Arduino";
  char text2[20] = "Arduino";
  char text3[20];
  
  Serial.print("Длина: ");
  Serial.println(string_length(text1));  // 7
  
  Serial.print("Равны? ");
  Serial.println(strings_equal(text1, text2) ? "Да" : "Нет");  // Да
  
  string_copy(text1, text3);
  Serial.println(text3);  // Arduino
}

void loop() { }
```

---

## Практические примеры

### Пример 1: Система записи данных датчиков

```cpp
const int NUM_READINGS = 10;
const int NUM_SENSORS = 3;

int readings[NUM_READINGS][NUM_SENSORS];
int read_index = 0;

const int SENSOR_PINS[NUM_SENSORS] = {A0, A1, A2};
const String SENSOR_NAMES[NUM_SENSORS] = {"Температура", "Влажность", "Свет"};

void setup() {
  Serial.begin(9600);
  
  // Инициализируем массив нулями
  for (int i = 0; i < NUM_READINGS; i++) {
    for (int j = 0; j < NUM_SENSORS; j++) {
      readings[i][j] = 0;
    }
  }
  
  Serial.println("=== Система записи данных ===");
}

void recordSensorData() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    readings[read_index][i] = analogRead(SENSOR_PINS[i]);
  }
  
  read_index = (read_index + 1) % NUM_READINGS;
}

void displayAllData() {
  Serial.println("\n=== Записанные данные ===");
  
  for (int i = 0; i < NUM_READINGS; i++) {
    Serial.print("Запись ");
    Serial.print(i + 1);
    Serial.print(": ");
    
    for (int j = 0; j < NUM_SENSORS; j++) {
      Serial.print(SENSOR_NAMES[j]);
      Serial.print("=");
      Serial.print(readings[i][j]);
      
      if (j < NUM_SENSORS - 1) {
        Serial.print(", ");
      }
    }
    
    Serial.println();
  }
}

float getAverageSensor(int sensor_index) {
  int sum = 0;
  
  for (int i = 0; i < NUM_READINGS; i++) {
    sum += readings[i][sensor_index];
  }
  
  return (float)sum / NUM_READINGS;
}

void loop() {
  recordSensorData();
  displayAllData();
  
  Serial.println("\n=== Средние значения ===");
  for (int i = 0; i < NUM_SENSORS; i++) {
    Serial.print(SENSOR_NAMES[i]);
    Serial.print(": ");
    Serial.println(getAverageSensor(i), 1);
  }
  
  delay(10000);
}
```

### Пример 2: Управление массивом светодиодов

```cpp
const int NUM_LEDS = 5;
const int LED_PINS[NUM_LEDS] = {5, 6, 7, 8, 9};
boolean led_states[NUM_LEDS] = {false, false, false, false, false};

void setup() {
  Serial.begin(9600);
  
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }
  
  Serial.println("Система управления LED инициализирована");
}

void turnOnLED(int led_index) {
  if (led_index >= 0 && led_index < NUM_LEDS) {
    digitalWrite(LED_PINS[led_index], HIGH);
    led_states[led_index] = true;
    Serial.print("LED ");
    Serial.print(led_index + 1);
    Serial.println(" включен");
  }
}

void turnOffLED(int led_index) {
  if (led_index >= 0 && led_index < NUM_LEDS) {
    digitalWrite(LED_PINS[led_index], LOW);
    led_states[led_index] = false;
    Serial.print("LED ");
    Serial.print(led_index + 1);
    Serial.println(" выключен");
  }
}

void blinkAllLEDs(int times, int delay_ms) {
  for (int i = 0; i < times; i++) {
    for (int j = 0; j < NUM_LEDS; j++) {
      turnOnLED(j);
    }
    delay(delay_ms);
    
    for (int j = 0; j < NUM_LEDS; j++) {
      turnOffLED(j);
    }
    delay(delay_ms);
  }
}

void sequentialBlink(int delay_ms) {
  for (int i = 0; i < NUM_LEDS; i++) {
    turnOnLED(i);
    delay(delay_ms);
    turnOffLED(i);
  }
}

void displayStatus() {
  Serial.print("Статус: ");
  for (int i = 0; i < NUM_LEDS; i++) {
    Serial.print(led_states[i] ? "1" : "0");
  }
  Serial.println();
}

void loop() {
  // Все включаем
  for (int i = 0; i < NUM_LEDS; i++) {
    turnOnLED(i);
  }
  displayStatus();
  delay(2000);
  
  // Все выключаем
  for (int i = 0; i < NUM_LEDS; i++) {
    turnOffLED(i);
  }
  displayStatus();
  delay(2000);
  
  // Последовательное мигание
  sequentialBlink(500);
  delay(1000);
  
  // Все мигают вместе
  blinkAllLEDs(3, 300);
  delay(2000);
}
```

### Пример 3: Обработка команд из Serial

```cpp
const int MAX_COMMAND_LENGTH = 50;
char command[MAX_COMMAND_LENGTH];
int command_index = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("=== Система команд ===");
  Serial.println("Команды: LED_ON, LED_OFF, TEMP, STATUS");
}

void processCommand(char cmd[]) {
  if (strcmp(cmd, "LED_ON") == 0) {
    digitalWrite(13, HIGH);
    Serial.println("LED включен");
  } 
  else if (strcmp(cmd, "LED_OFF") == 0) {
    digitalWrite(13, LOW);
    Serial.println("LED выключен");
  } 
  else if (strcmp(cmd, "TEMP") == 0) {
    int temp = analogRead(A0);
    Serial.print("Температура: ");
    Serial.println(temp);
  } 
  else if (strcmp(cmd, "STATUS") == 0) {
    Serial.println("Система в норме");
  } 
  else {
    Serial.print("Неизвестная команда: ");
    Serial.println(cmd);
  }
}

void loop() {
  if (Serial.available() > 0) {
    char received = Serial.read();
    
    if (received == '\n') {
      command[command_index] = '\0';
      
      if (command_index > 0) {
        Serial.print("Получена команда: ");
        Serial.println(command);
        
        processCommand(command);
      }
      
      command_index = 0;
    } 
    else if (command_index < MAX_COMMAND_LENGTH - 1) {
      command[command_index] = received;
      command_index++;
    }
  }
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Создавать и использовать одномерные массивы

✅ Работать с индексированием массивов

✅ Перебирать массивы циклами

✅ Создавать двумерные массивы (матрицы)

✅ Работать со строками (String объекты)

✅ Работать с массивами символов (C-строки)

✅ Применять функции для работы с массивами

✅ Применять массивы на практических примерах

---

## 🎯 Домашнее задание

1. Создайте массив из 8 значений датчиков и найдите максимум и минимум

2. Напишите функцию, которая выводит весь массив в Serial Monitor

3. Создайте матрицу 4x4 и найдите сумму всех элементов

4. Напишите программу для работы с 4 светодиодами с помощью массива

5. Создайте систему для сохранения истории 10 последних показаний датчика

6. Дополнительно: Напишите функцию сортировки массива по возрастанию

---

## 🔗 Полезные ссылки

- 📖 **Массивы:** https://www.arduino.cc/reference/en/language/variables/data-types/array/
- 📖 **String:** https://www.arduino.cc/reference/en/language/variables/data-types/stringobject/
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Массив** | Коллекция элементов одного типа |
| **Индекс** | Номер элемента (начиная с 0) |
| **Элемент** | Одно значение в массиве |
| **Размер** | Количество элементов в массиве |
| **Двумерный массив** | Таблица (массив массивов) |
| **String** | Объект для работы со строками |
| **Char массив** | C-строка (массив символов) |
| **Null-терминатор** | Символ '\0' в конце C-строки |
| **Индексирование** | Доступ к элементу по индексу |
| **Итерация** | Перебор всех элементов |

---

**Следующий урок:** ⚡ [Указатели и работа с памятью](../Lesson_7/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025