# ⚡ Условные операторы и циклы

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Оператор if](#оператор-if)
3. [Оператор if-else](#оператор-if-else)
4. [Оператор if-else if-else](#оператор-if-else-if-else)
5. [Оператор switch-case](#оператор-switch-case)
6. [Тернарный оператор](#тернарный-оператор)
7. [Цикл for](#цикл-for)
8. [Цикл while](#цикл-while)
9. [Цикл do-while](#цикл-do-while)
10. [Вложенные циклы](#вложенные-циклы)
11. [Управление циклами (break, continue)](#управление-циклами)
12. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке мы подробно изучим условные операторы и циклы — ключевые инструменты для создания логики программ. Вы научитесь создавать программы, которые принимают решения и повторяют действия.

---

## Оператор if

Оператор `if` выполняет код только если условие истинно.

### Синтаксис

```cpp
if (условие) {
  // Код здесь выполняется, если условие true
}
```

### Простые примеры

```cpp
// Пример 1: Проверка температуры
int temperature = 28;

if (temperature > 25) {
  Serial.println("Жарко!");
}

// Пример 2: Проверка света
int light = analogRead(A0);

if (light < 200) {
  digitalWrite(LED_PIN, HIGH);  // Включить светодиод в темноте
}

// Пример 3: Проверка срабатывания датчика движения
int motion = digitalRead(2);

if (motion == HIGH) {
  Serial.println("Движение обнаружено!");
}
```

### Блок-схема if

```
           ┌──────────────┐
           │ Начало       │
           └──────┬───────┘
                  │
           ┌──────▼───────┐
           │  Условие?    │
           └──┬───────┬───┘
            ДА│       │НЕТ
              │       │
       ┌──────▼──┐  ┌─▼────────┐
       │Выполнить│  │Пропустить│
       │  код    │  │   код    │
       └──────┬──┘  └─┬────────┘
              │       │
              └───┬───┘
                  │
           ┌──────▼───────┐
           │ Конец        │
           └──────────────┘
```

---

## Оператор if-else

Оператор `if-else` выполняет один код если условие истинно, или другой код если ложно.

### Синтаксис

```cpp
if (условие) {
  // Выполняется, если условие true
} else {
  // Выполняется, если условие false
}
```

### Практические примеры

```cpp
// Пример 1: Классификация уровня освещённости
int light = analogRead(A0);

if (light > 500) {
  Serial.println("Светло");
  digitalWrite(LED_PIN, LOW);
} else {
  Serial.println("Темно");
  digitalWrite(LED_PIN, HIGH);
}

// Пример 2: Проверка диапазона напряжения
float voltage = analogRead(A1) * (5.0 / 1023.0);

if (voltage >= 4.5) {
  Serial.println("Батарея полностью заряжена");
} else {
  Serial.println("Батарея разряжена");
}

// Пример 3: Управление двигателем
int speed = 150;

if (speed > 0) {
  digitalWrite(MOTOR_DIR, HIGH);  // Прямое направление
  analogWrite(MOTOR_PWM, speed);
} else {
  digitalWrite(MOTOR_DIR, LOW);   // Обратное направление
  analogWrite(MOTOR_PWM, -speed);
}
```

### Блок-схема if-else

```
           ┌──────────────┐
           │ Начало       │
           └──────┬───────┘
                  │
           ┌──────▼───────┐
           │  Условие?    │
           └──┬───────┬───┘
            ДА│       │НЕТ
              │       │
       ┌──────▼──┐ ┌──▼─────┐
       │  Код    │ │ Код    │
       │  если   │ │ если   │
       │  true   │ │ false  │
       └──────┬──┘ └──┬─────┘
              │       │
              └───┬───┘
                  │
           ┌──────▼───────┐
           │ Конец        │
           └──────────────┘
```

---

## Оператор if-else if-else

Для проверки нескольких условий используется `if-else if-else`.

### Синтаксис

```cpp
if (условие1) {
  // Код для условия1
} else if (условие2) {
  // Код для условия2
} else if (условие3) {
  // Код для условия3
} else {
  // Код по умолчанию (если все условия false)
}
```

### Примеры классификации

```cpp
// Пример 1: Классификация температуры
float temperature = 22.5;

if (temperature < 0) {
  Serial.println("Холодно (< 0°C) - ЗАМЁРЗНЕТ!");
} else if (temperature < 10) {
  Serial.println("Холодно (0-10°C)");
} else if (temperature < 20) {
  Serial.println("Прохладно (10-20°C)");
} else if (temperature < 25) {
  Serial.println("Комфортно (20-25°C)");
} else if (temperature < 35) {
  Serial.println("Тепло (25-35°C)");
} else {
  Serial.println("Жарко (> 35°C) - ОПАСНО!");
}

// Пример 2: Классификация значения датчика влажности
int humidity = 65;

if (humidity < 20) {
  Serial.println("Очень сухо - опасно для здоровья");
} else if (humidity < 30) {
  Serial.println("Сухо");
} else if (humidity < 50) {
  Serial.println("Нормально");
} else if (humidity < 70) {
  Serial.println("Влажно");
} else {
  Serial.println("Очень влажно - может привести к конденсации");
}

// Пример 3: Определение режима работы по времени суток
int hour = 14;  // Время в часах (0-23)

if (hour >= 6 && hour < 12) {
  Serial.println("Утро");
} else if (hour >= 12 && hour < 17) {
  Serial.println("День");
} else if (hour >= 17 && hour < 21) {
  Serial.println("Вечер");
} else {
  Serial.println("Ночь");
}
```

### Порядок проверки условий

```cpp
// ⚠️ ВАЖНО: Условия проверяются ПО ПОРЯДКУ!
int value = 50;

if (value > 40) {
  Serial.println("Больше 40");       // ← Выполнится это
} else if (value > 30) {
  Serial.println("Больше 30");       // ← Это не выполнится
} else if (value > 0) {
  Serial.println("Больше 0");        // ← Это не выполнится
}

// Правильный порядок - от узкого к широкому
int value = 50;

if (value > 80) {
  Serial.println("Очень высокое");
} else if (value > 50) {
  Serial.println("Высокое");
} else if (value > 20) {
  Serial.println("Среднее");
} else {
  Serial.println("Низкое");
}
```

---

## Оператор switch-case

Оператор `switch-case` используется когда нужно проверить множество конкретных значений.

### Синтаксис

```cpp
switch (переменная) {
  case значение1:
    // Код для значения1
    break;
  case значение2:
    // Код для значения2
    break;
  case значение3:
  case значение4:
    // Код для значения3 или значения4
    break;
  default:
    // Код, если ничего не совпало
}
```

### Важные моменты

```cpp
// ВАЖНО: обязательно используйте break!
int mode = 2;

switch (mode) {
  case 1:
    Serial.println("Режим 1");
    break;  // ← Выходим из switch
  case 2:
    Serial.println("Режим 2");
    break;  // ← Выходим из switch
  default:
    Serial.println("Неизвестный режим");
}

// ❌ БЕЗ break - "падение сквозь" (fall-through)
int mode = 1;

switch (mode) {
  case 1:
    Serial.println("Режим 1");
    // БЕЗ break!
  case 2:
    Serial.println("Режим 2");  // ← Это ТАКЖЕ выполнится!
    break;
}
// Результат: будет выведено "Режим 1" и "Режим 2"

// ✅ Можно объединить несколько случаев
int day = 3;

switch (day) {
  case 1:
  case 2:
  case 3:
  case 4:
  case 5:
    Serial.println("Рабочий день");
    break;
  case 6:
  case 7:
    Serial.println("Выходной");
    break;
}
```

### Примеры

```cpp
// Пример 1: Выбор режима работы
int mode = 2;

switch (mode) {
  case 1:
    Serial.println("Автоматический режим");
    autoMode();
    break;
  case 2:
    Serial.println("Ручной режим");
    manualMode();
    break;
  case 3:
    Serial.println("Режим тестирования");
    testMode();
    break;
  default:
    Serial.println("Неизвестный режим!");
}

// Пример 2: Перевод номера в день недели
int day = 3;
String dayName;

switch (day) {
  case 1:
    dayName = "Понедельник";
    break;
  case 2:
    dayName = "Вторник";
    break;
  case 3:
    dayName = "Среда";
    break;
  case 4:
    dayName = "Четверг";
    break;
  case 5:
    dayName = "Пятница";
    break;
  case 6:
    dayName = "Суббота";
    break;
  case 7:
    dayName = "Воскресенье";
    break;
  default:
    dayName = "Неизвестный день";
}

Serial.println(dayName);
```

### switch vs if-else

```
┌─────────────────────────────────────────────────────────┐
│ Когда использовать switch-case?                         │
├─────────────────────────────────────────────────────────┤
│ ✓ Проверка конкретных значений переменной              │
│ ✓ Много вариантов выбора (4 и более)                   │
│ ✓ Один и тот же результат для нескольких значений      │
│ ✗ Сложные условия (операторы сравнения, логика)       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Когда использовать if-else?                             │
├─────────────────────────────────────────────────────────┤
│ ✓ Сложные условия (>, <, &&, ||)                       │
│ ✓ Диапазоны значений                                   │
│ ✓ Мало вариантов (2-3)                                 │
│ ✗ Проверка одной переменной на множество значений      │
└─────────────────────────────────────────────────────────┘
```

---

## Тернарный оператор

Тернарный оператор — сокращённая форма if-else для одной строки.

### Синтаксис

```cpp
переменная = (условие) ? значение_если_true : значение_если_false;
```

### Примеры

```cpp
// Пример 1: Простое присваивание
int value = (temperature > 25) ? 100 : 50;

// Эквивалент:
int value;
if (temperature > 25) {
  value = 100;
} else {
  value = 50;
}

// Пример 2: Вывод текста
String status = (motion == HIGH) ? "Движение!" : "Спокойно";
Serial.println(status);

// Пример 3: Вложенные тернарные операторы (не рекомендуется!)
String temperature_status = (temp < 0) ? "Холодно" : (temp < 20) ? "Нормально" : "Жарко";

// ЛУЧШЕ использовать if-else if-else для читаемости:
String temperature_status;
if (temp < 0) {
  temperature_status = "Холодно";
} else if (temp < 20) {
  temperature_status = "Нормально";
} else {
  temperature_status = "Жарко";
}

// Пример 4: Управление PWM яркостью
int brightness = (sensor_value > 500) ? 255 : 0;
analogWrite(LED_PIN, brightness);
```

---

## Цикл for

Цикл `for` повторяет код определённое количество раз.

### Синтаксис

```cpp
for (инициализация; условие; изменение) {
  // Код повторяется
}
```

### Разбор синтаксиса

```cpp
for (int i = 0; i < 10; i++) {
//   │────┬────│ ───┬──  │ ──┬──
//   │    │    │    │    │  │
//   │    │    │    │    │  └─ Изменение (после каждой итерации)
//   │    │    │    │    └──── Условие выхода (проверяется каждый раз)
//   │    │    │    └───────── 
//   │    │    └────────────── Начальное значение
//   │    └───────────────────── Объявление переменной цикла
//   └────────────────────────── 

  Serial.println(i);            // Выведет 0, 1, 2, ..., 9
}
```

### Различные варианты циклов for

```cpp
// Цикл от 0 до 9
for (int i = 0; i < 10; i++) {
  Serial.println(i);            // 0, 1, 2, ..., 9
}

// Цикл от 1 до 10
for (int i = 1; i <= 10; i++) {
  Serial.println(i);            // 1, 2, 3, ..., 10
}

// Цикл в обратном порядке от 10 до 1
for (int i = 10; i > 0; i--) {
  Serial.println(i);            // 10, 9, 8, ..., 1
}

// Цикл с шагом 2
for (int i = 0; i < 20; i += 2) {
  Serial.println(i);            // 0, 2, 4, 6, 8, 10, 12, 14, 16, 18
}

// Цикл с шагом 5
for (int i = 0; i <= 100; i += 5) {
  Serial.println(i);            // 0, 5, 10, 15, ..., 100
}

// Бесконечный цикл (осторожно!)
for (;;) {
  Serial.println("Бесконечный цикл");
  // Нужен break для выхода
}
```

### Практические примеры for

```cpp
// Пример 1: Мигание светодиодом 5 раз
const int LED_PIN = 13;

for (int i = 0; i < 5; i++) {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
  Serial.print("Мигание №");
  Serial.println(i + 1);
}

// Пример 2: Увеличение яркости (PWM)
const int LED_PIN = 9;

for (int brightness = 0; brightness <= 255; brightness += 10) {
  analogWrite(LED_PIN, brightness);
  Serial.print("Яркость: ");
  Serial.println(brightness);
  delay(200);
}

// Пример 3: Работа с массивом
int values[] = {10, 20, 30, 40, 50};

for (int i = 0; i < 5; i++) {
  Serial.print("Элемент ");
  Serial.print(i);
  Serial.print(": ");
  Serial.println(values[i]);
}

// Пример 4: Сумма чисел от 1 до 100
int sum = 0;

for (int i = 1; i <= 100; i++) {
  sum += i;
}

Serial.print("Сумма: ");
Serial.println(sum);  // 5050
```

### Цикл for-each (для массивов)

```cpp
// Синтаксис: for (тип элемента : массив)

int values[] = {10, 20, 30, 40, 50};

// Перебор всех элементов
for (int value : values) {
  Serial.println(value);
}

// Со String массивом
String colors[] = {"красный", "зелёный", "синий"};

for (String color : colors) {
  Serial.println(color);
}
```

---

## Цикл while

Цикл `while` повторяется пока условие истинно.

### Синтаксис

```cpp
while (условие) {
  // Код повторяется
  // Должно быть что-то, что изменит условие!
}
```

### Примеры while

```cpp
// Пример 1: Счёт от 1 до 10
int i = 1;
while (i <= 10) {
  Serial.println(i);
  i++;
}

// Пример 2: Ожидание события
boolean button_pressed = false;
int attempts = 0;

while (!button_pressed && attempts < 100) {
  button_pressed = (digitalRead(BUTTON_PIN) == HIGH);
  attempts++;
  delay(100);  // Проверяем каждые 100мс
}

if (button_pressed) {
  Serial.println("Кнопка нажата!");
} else {
  Serial.println("Кнопка не была нажата");
}

// Пример 3: Чтение данных по Serial
while (Serial.available() > 0) {
  char data = Serial.read();
  Serial.print("Получено: ");
  Serial.println(data);
}

// Пример 4: Ожидание стабильного значения
int prev_value = 0;
int current_value = 0;
int stable_count = 0;

while (stable_count < 5) {
  current_value = analogRead(A0);
  
  if (current_value == prev_value) {
    stable_count++;
  } else {
    stable_count = 0;
    prev_value = current_value;
  }
  
  delay(100);
}

Serial.print("Стабильное значение: ");
Serial.println(current_value);
```

### ⚠️ Опасность бесконечного цикла

```cpp
// ❌ ОПАСНО! Бесконечный цикл - Arduino зависнет!
int i = 0;
while (i < 10) {
  Serial.println("Привет");
  // i никогда не увеличивается!
  // Цикл никогда не закончится!
}

// ✅ Правильно - нужно изменить условие
int i = 0;
while (i < 10) {
  Serial.println("Привет");
  i++;  // ← Важно!
}
```

---

## Цикл do-while

Цикл `do-while` выполняется минимум один раз, потом проверяет условие.

### Синтаксис

```cpp
do {
  // Код выполняется минимум один раз
} while (условие);
```

### Разница между while и do-while

```cpp
// while - может не выполниться вообще
int i = 10;
while (i < 5) {
  Serial.println(i);  // Это не выполнится!
}

// do-while - выполнится минимум один раз
int i = 10;
do {
  Serial.println(i);  // Это выполнится один раз!
} while (i < 5);

// Результат: будет выведено 10
```

### Практические примеры do-while

```cpp
// Пример 1: Меню с повторным выбором
int choice = 0;

do {
  Serial.println("1 - Включить");
  Serial.println("2 - Выключить");
  Serial.println("3 - Выход");
  Serial.println("Выберите действие: ");
  
  // Ждём ввода...
  // choice = readChoice();
  
  switch (choice) {
    case 1:
      turnOn();
      break;
    case 2:
      turnOff();
      break;
    case 3:
      Serial.println("До свидания!");
      break;
  }
} while (choice != 3);

// Пример 2: Повторная отправка данных пока не будет подтверждение
boolean confirmed = false;
int attempts = 0;

do {
  sendData();
  delay(1000);
  confirmed = checkAcknowledge();  // Проверяем подтверждение
  attempts++;
} while (!confirmed && attempts < 5);

if (confirmed) {
  Serial.println("Данные отправлены");
} else {
  Serial.println("Ошибка отправки");
}
```

---

## Вложенные циклы

Циклы могут содержать другие циклы внутри.

### Примеры вложенных циклов

```cpp
// Пример 1: Таблица умножения
for (int i = 1; i <= 10; i++) {
  for (int j = 1; j <= 10; j++) {
    int result = i * j;
    Serial.print(result);
    Serial.print("\t");  // Табуляция
  }
  Serial.println();       // Новая строка
}

// Вывод:
// 1  2  3  4  5  6  7  8  9  10
// 2  4  6  8  10 12 14 16 18 20
// ...

// Пример 2: Работа с двумерным массивом
int matrix[3][3] = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9}
};

for (int row = 0; row < 3; row++) {
  for (int col = 0; col < 3; col++) {
    Serial.print(matrix[row][col]);
    Serial.print("\t");
  }
  Serial.println();
}

// Пример 3: Мигание с двойной частотой
for (int i = 0; i < 3; i++) {        // Внешний цикл: 3 раза
  for (int j = 0; j < 2; j++) {      // Внутренний цикл: 2 раза
    digitalWrite(LED_PIN, HIGH);
    delay(250);
    digitalWrite(LED_PIN, LOW);
    delay(250);
  }
  delay(1000);                         // Пауза между группами
}
```

---

## Управление циклами

### Оператор break

Оператор `break` прерывает цикл (выходит из него).

```cpp
// Пример 1: Поиск значения в массиве
int values[] = {10, 20, 30, 40, 50};
int target = 30;
int index = -1;

for (int i = 0; i < 5; i++) {
  if (values[i] == target) {
    index = i;
    break;  // Выходим из цикла
  }
}

Serial.print("Найденный индекс: ");
Serial.println(index);  // 2

// Пример 2: Выход при нажатии кнопки
for (int i = 0; i < 1000; i++) {
  Serial.print("Отправляю данные ");
  Serial.println(i);
  
  if (digitalRead(BUTTON_PIN) == HIGH) {
    Serial.println("Отправка прервана!");
    break;  // Выходим из цикла
  }
  
  delay(100);
}
```

### Оператор continue

Оператор `continue` пропускает оставшуюся часть текущей итерации.

```cpp
// Пример 1: Вывод только чётных чисел
for (int i = 0; i < 10; i++) {
  if (i % 2 == 0) {
    continue;  // Пропускаем нечётные числа
  }
  Serial.println(i);  // Выведет 1, 3, 5, 7, 9
}

// Пример 2: Пропуск нулевых значений
int values[] = {10, 0, 20, 0, 30};

for (int i = 0; i < 5; i++) {
  if (values[i] == 0) {
    continue;  // Пропускаем нулевые значения
  }
  Serial.println(values[i]);  // Выведет 10, 20, 30
}

// Эквивалент со скобками и continue:
for (int i = 0; i < 10; i++) {
  if (i % 2 != 0) {  // Если нечётное
    // Действия...
  }
}

// vs с continue:
for (int i = 0; i < 10; i++) {
  if (i % 2 == 0) {  // Если чётное
    continue;        // Пропускаем
  }
  // Действия...
}
```

---

## Практические примеры

### Пример 1: Система климат-контроля

```cpp
const int TEMP_SENSOR = A0;
const int HEATER_PIN = 5;
const int COOLER_PIN = 6;

float target_temperature = 22.0;

void setup() {
  Serial.begin(9600);
  pinMode(HEATER_PIN, OUTPUT);
  pinMode(COOLER_PIN, OUTPUT);
}

void loop() {
  float current_temp = readTemperature();
  
  Serial.print("Текущая температура: ");
  Serial.println(current_temp);
  
  if (current_temp < target_temperature - 1) {
    // Слишком холодно - включаем обогреватель
    digitalWrite(HEATER_PIN, HIGH);
    digitalWrite(COOLER_PIN, LOW);
    Serial.println("Нагревание...");
  } else if (current_temp > target_temperature + 1) {
    // Слишком жарко - включаем охлаждение
    digitalWrite(HEATER_PIN, LOW);
    digitalWrite(COOLER_PIN, HIGH);
    Serial.println("Охлаждение...");
  } else {
    // Температура в норме
    digitalWrite(HEATER_PIN, LOW);
    digitalWrite(COOLER_PIN, LOW);
    Serial.println("Норма");
  }
  
  delay(2000);
}

float readTemperature() {
  int raw_value = analogRead(TEMP_SENSOR);
  // Преобразование в градусы Цельсия
  float voltage = raw_value * (5.0 / 1023.0);
  float temperature = (voltage - 0.5) * 100.0;
  return temperature;
}
```

### Пример 2: Игра "Угадай число"

```cpp
void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A5));  // Инициализация генератора случайных чисел
}

void loop() {
  Serial.println("=== Игра 'Угадай число' ===");
  Serial.println("Загадаю число от 1 до 100");
  
  int secret_number = random(1, 101);
  int guess = 0;
  int attempts = 0;
  
  while (guess != secret_number) {
    Serial.println("Введите число: ");
    
    // Имитация ввода (в реальной программе это будет Serial.read)
    guess = readNumber();
    attempts++;
    
    if (guess < secret_number) {
      Serial.println("Моё число больше!");
    } else if (guess > secret_number) {
      Serial.println("Моё число меньше!");
    } else {
      Serial.print("Угадали! Число: ");
      Serial.println(secret_number);
      Serial.print("Попыток: ");
      Serial.println(attempts);
    }
  }
  
  delay(5000);
}

int readNumber() {
  // Простая имитация ввода числа
  // В реальной программе здесь будет чтение Serial
  return random(1, 101);
}
```

### Пример 3: Светофор с циклом

```cpp
const int RED_LED = 9;
const int YELLOW_LED = 10;
const int GREEN_LED = 11;

void setup() {
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
}

void loop() {
  for (int i = 0; i < 5; i++) {  // 5 циклов светофора
    // Красный свет
    digitalWrite(RED_LED, HIGH);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(GREEN_LED, LOW);
    delay(3000);
    
    // Жёлтый свет
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    delay(1000);
    
    // Зелёный свет
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
    delay(3000);
    
    // Жёлтый свет (перед красным)
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    delay(1000);
  }
  
  // Выключаем все светодиоды
  digitalWrite(RED_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
  delay(2000);
}
```

### Пример 4: Контроль диапазона значений

```cpp
const int SENSOR_PIN = A0;
const int WARNING_LED = 6;
const int DANGER_LED = 7;

void setup() {
  Serial.begin(9600);
  pinMode(WARNING_LED, OUTPUT);
  pinMode(DANGER_LED, OUTPUT);
}

void loop() {
  int sensor_value = analogRead(SENSOR_PIN);
  
  // Преобразование в проценты (0-100%)
  int percentage = map(sensor_value, 0, 1023, 0, 100);
  
  Serial.print("Значение: ");
  Serial.print(percentage);
  Serial.println("%");
  
  if (percentage < 20) {
    // Нормально
    digitalWrite(WARNING_LED, LOW);
    digitalWrite(DANGER_LED, LOW);
    Serial.println("Статус: ОК");
  } else if (percentage < 70) {
    // Предупреждение
    digitalWrite(WARNING_LED, HIGH);
    digitalWrite(DANGER_LED, LOW);
    Serial.println("Статус: ВНИМАНИЕ");
    
    // Мигаем светодиодом
    for (int i = 0; i < 2; i++) {
      digitalWrite(WARNING_LED, LOW);
      delay(200);
      digitalWrite(WARNING_LED, HIGH);
      delay(200);
    }
  } else {
    // Опасность
    digitalWrite(WARNING_LED, LOW);
    digitalWrite(DANGER_LED, HIGH);
    Serial.println("Статус: ОПАСНОСТЬ!");
    
    // Быстрое мигание
    for (int i = 0; i < 5; i++) {
      digitalWrite(DANGER_LED, LOW);
      delay(100);
      digitalWrite(DANGER_LED, HIGH);
      delay(100);
    }
  }
  
  delay(1000);
}
```

### Пример 5: Обработка нажатия кнопки с debounce

```cpp
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Проверяем состояние кнопки (с защитой от дребезга)
  if (digitalRead(BUTTON_PIN) == HIGH) {
    // Дополнительная проверка
    delay(20);
    
    if (digitalRead(BUTTON_PIN) == HIGH) {
      Serial.println("Кнопка нажата!");
      toggleLED();
      
      // Ждём, пока кнопка будет отпущена
      while (digitalRead(BUTTON_PIN) == HIGH) {
        delay(10);
      }
      
      // Дополнительная задержка для стабилизации
      delay(50);
    }
  }
}

void toggleLED() {
  static boolean led_state = false;
  led_state = !led_state;
  digitalWrite(LED_PIN, led_state ? HIGH : LOW);
  
  Serial.print("Светодиод: ");
  Serial.println(led_state ? "включен" : "выключен");
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Использовать оператор if для простых условий

✅ Использовать if-else для выбора между двумя вариантами

✅ Использовать if-else if-else для множественных условий

✅ Использовать switch-case для проверки конкретных значений

✅ Применять тернарный оператор для сокращённого кода

✅ Писать циклы for для повторения кода

✅ Использовать циклы while и do-while

✅ Писать вложенные циклы

✅ Управлять циклами с помощью break и continue

✅ Применять всё на практических примерах

---

## 🎯 Домашнее задание

1. **Напишите программу**, которая выводит все числа от 1 до 50, но пропускает кратные 5

2. **Создайте систему контроля**, которая проверяет значение датчика:
   - Если < 200 — вывести "Низко"
   - Если 200-600 — вывести "Нормально"
   - Если > 600 — вывести "Высоко"

3. **Напишите программу светофора** с циклом for (красный 3сек, жёлтый 1сек, зелёный 3сек)

4. **Создайте таблицу умножения** с использованием вложенных циклов (матрица 5x5)

5. **Напишите счётчик**, который увеличивается при нажатии кнопки и выводит значение в Serial

6. **Дополнительно:** Создайте игру "Угадай число" с ограничением на количество попыток

---

## 🔗 Полезные ссылки

- 📖 **Arduino if-else:** https://www.arduino.cc/reference/en/language/structure/control-structure/if/
- 📖 **Arduino switch:** https://www.arduino.cc/reference/en/language/structure/control-structure/switchcase/
- 📖 **Arduino for loop:** https://www.arduino.cc/reference/en/language/structure/control-structure/for/
- 📖 **Arduino while loop:** https://www.arduino.cc/reference/en/language/structure/control-structure/while/
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **if** | Условный оператор для проверки условия |
| **else** | Альтернативный блок кода |
| **else if** | Дополнительное условие |
| **switch-case** | Множественный выбор на основе значения |
| **break** | Выход из цикла или switch |
| **continue** | Пропуск текущей итерации |
| **for** | Цикл с известным количеством итераций |
| **while** | Цикл с условием |
| **do-while** | Цикл, выполняющийся минимум один раз |
| **Тернарный оператор** | Сокращённая форма if-else |
| **Вложенные циклы** | Цикл внутри другого цикла |
| **Падение сквозь** | Выполнение нескольких case без break |
| **Дебоунс** | Защита от дребезга кнопки |

---

**Следующий урок:** 🔌 [Функции в Arduino: объявление, параметры, возвращаемые значения](../Lesson_5/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025