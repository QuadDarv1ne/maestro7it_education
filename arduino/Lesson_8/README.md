# 🏗️ Структуры и объединения: пользовательские типы данных

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Что такое структура?](#что-такое-структура)
3. [Объявление структур](#объявление-структур)
4. [Создание и инициализация](#создание-и-инициализация)
5. [Доступ к членам структуры](#доступ-к-членам-структуры)
6. [Структуры в функциях](#структуры-в-функциях)
7. [Массивы структур](#массивы-структур)
8. [Вложенные структуры](#вложенные-структуры)
9. [Объединения (union)](#объединения-union)
10. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите структуры — один из самых полезных инструментов для организации сложных данных. Структуры позволяют объединить переменные разных типов в один пользовательский тип.

---

## Что такое структура?

Структура — это пользовательский тип данных, который объединяет несколько переменных разных типов в одну группу.

### Зачем нужны структуры?

```
❌ БЕЗ СТРУКТУР - беспорядок
int sensor_id;
float sensor_temp;
int sensor_humidity;
boolean sensor_active;
String sensor_name;

// Сложно организовать и использовать!

✅ СО СТРУКТУРАМИ - порядок
struct Sensor {
  int id;
  float temperature;
  int humidity;
  boolean active;
  String name;
};

// Всё организовано в одной структуре!
```

### Аналогия

```
Структура = Контейнер для хранения разных типов данных
Класс      = Структура + методы + управление доступом
```

---

## Объявление структур

### Синтаксис

```cpp
struct НазваниеСтруктуры {
  тип1 член1;
  тип2 член2;
  тип3 член3;
  // ...
};  // ← ВАЖНО: точка с запятой!
```

### Примеры структур

```cpp
// Структура для датчика температуры
struct TemperatureSensor {
  int pin;
  float temperature;
  float min_value;
  float max_value;
  boolean is_active;
};

// Структура для LED
struct LED {
  int pin;
  int brightness;
  boolean is_on;
};

// Структура для кнопки
struct Button {
  int pin;
  boolean pressed;
  unsigned long last_press_time;
};

// Структура для координат
struct Point {
  int x;
  int y;
};

// Структура для времени
struct Time {
  int hours;
  int minutes;
  int seconds;
};

// Структура для устройства с несколькими датчиками
struct Device {
  String name;
  int id;
  float temperature;
  int humidity;
  int light_level;
  boolean online;
};
```

---

## Создание и инициализация

### Создание переменной структурного типа

```cpp
struct Sensor {
  int id;
  float temperature;
  int humidity;
};

// Создание переменной
Sensor sensor1;

// Инициализация (способ 1)
sensor1.id = 1;
sensor1.temperature = 23.5;
sensor1.humidity = 65;

// Инициализация (способ 2) - при создании
Sensor sensor2 = {2, 25.1, 70};

// Инициализация (способ 3) - с именами членов
Sensor sensor3 = {
  .id = 3,
  .temperature = 22.3,
  .humidity = 68
};
```

### Типографские инициализации

```cpp
struct LED {
  int pin;
  int brightness;
};

void setup() {
  // Способ 1: Пустая инициализация
  LED led1;  // Члены имеют случайные значения!
  
  // Способ 2: Инициализация нулями
  LED led2 = {};  // Все члены = 0
  
  // Способ 3: Полная инициализация
  LED led3 = {9, 255};
  
  // Способ 4: Частичная инициализация (остальные = 0)
  LED led4 = {10};  // brightness = 0
}
```

---

## Доступ к членам структуры

### Оператор точка (.)

```cpp
struct Point {
  int x;
  int y;
};

void setup() {
  Point p1;
  
  // Запись
  p1.x = 10;
  p1.y = 20;
  
  // Чтение
  Serial.print("X: ");
  Serial.println(p1.x);
  
  Serial.print("Y: ");
  Serial.println(p1.y);
}
```

### Оператор стрелка (->) для указателей

```cpp
struct Point {
  int x;
  int y;
};

void setup() {
  Point p1 = {10, 20};
  Point* ptr = &p1;
  
  // Способ 1: разыменование + точка
  Serial.println((*ptr).x);      // 10
  
  // Способ 2: стрелка (удобнее)
  Serial.println(ptr->x);        // 10
  Serial.println(ptr->y);        // 20
  
  // Изменение через указатель
  ptr->x = 50;
  Serial.println(p1.x);          // 50
}
```

### Практический пример

```cpp
struct Sensor {
  String name;
  int pin;
  float value;
  float min_threshold;
  float max_threshold;
};

void displaySensorInfo(Sensor sensor) {
  Serial.print("Датчик: ");
  Serial.println(sensor.name);
  
  Serial.print("Pin: ");
  Serial.println(sensor.pin);
  
  Serial.print("Значение: ");
  Serial.println(sensor.value);
  
  Serial.print("Диапазон: ");
  Serial.print(sensor.min_threshold);
  Serial.print(" - ");
  Serial.println(sensor.max_threshold);
}

void setup() {
  Serial.begin(9600);
  
  Sensor temp = {
    "Температура",
    A0,
    23.5,
    15.0,
    30.0
  };
  
  displaySensorInfo(temp);
}

void loop() { }
```

---

## Структуры в функциях

### Передача структуры по значению

```cpp
struct Rectangle {
  int width;
  int height;
};

int calculateArea(Rectangle rect) {
  return rect.width * rect.height;
}

int calculatePerimeter(Rectangle rect) {
  return 2 * (rect.width + rect.height);
}

void displayRectangle(Rectangle rect) {
  Serial.print("Ширина: ");
  Serial.println(rect.width);
  
  Serial.print("Высота: ");
  Serial.println(rect.height);
  
  Serial.print("Площадь: ");
  Serial.println(calculateArea(rect));
  
  Serial.print("Периметр: ");
  Serial.println(calculatePerimeter(rect));
}

void setup() {
  Serial.begin(9600);
  
  Rectangle rect = {10, 5};
  displayRectangle(rect);
}

void loop() { }
```

### Передача структуры по указателю

```cpp
struct LED {
  int pin;
  int brightness;
  boolean is_on;
};

// Функция изменяет структуру
void turnOn(LED* led) {
  digitalWrite(led->pin, HIGH);
  led->is_on = true;
  Serial.println("LED включен");
}

void turnOff(LED* led) {
  digitalWrite(led->pin, LOW);
  led->is_on = false;
  Serial.println("LED выключен");
}

void setBrightness(LED* led, int brightness) {
  led->brightness = constrain(brightness, 0, 255);
  analogWrite(led->pin, led->brightness);
  Serial.print("Яркость: ");
  Serial.println(led->brightness);
}

void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
  
  LED led = {9, 255, false};
  
  turnOn(&led);
  setBrightness(&led, 150);
  turnOff(&led);
}

void loop() { }
```

### Возврат структуры из функции

```cpp
struct SensorReading {
  float temperature;
  int humidity;
  unsigned long timestamp;
};

SensorReading readSensors() {
  SensorReading reading;
  
  reading.temperature = analogRead(A0) * (5.0 / 1023.0) * 20;
  reading.humidity = analogRead(A1) * (100.0 / 1023.0);
  reading.timestamp = millis();
  
  return reading;
}

void setup() {
  Serial.begin(9600);
  
  SensorReading data = readSensors();
  
  Serial.print("Температура: ");
  Serial.println(data.temperature);
  
  Serial.print("Влажность: ");
  Serial.println(data.humidity);
  
  Serial.print("Время: ");
  Serial.println(data.timestamp);
}

void loop() { }
```

---

## Массивы структур

### Создание массива структур

```cpp
struct Student {
  String name;
  int id;
  float gpa;
};

void setup() {
  Serial.begin(9600);
  
  // Массив из 3 студентов
  Student students[3] = {
    {"Alice", 1, 4.5},
    {"Bob", 2, 3.8},
    {"Charlie", 3, 4.2}
  };
  
  // Доступ к элементам
  Serial.println(students[0].name);      // Alice
  Serial.println(students[1].gpa);       // 3.8
  
  // Итерация по массиву
  for (int i = 0; i < 3; i++) {
    Serial.print("Студент: ");
    Serial.print(students[i].name);
    Serial.print(", GPA: ");
    Serial.println(students[i].gpa);
  }
}

void loop() { }
```

### Практический пример: контроль множества датчиков

```cpp
struct Sensor {
  String name;
  int pin;
  float value;
  float threshold;
};

const int NUM_SENSORS = 4;
Sensor sensors[NUM_SENSORS] = {
  {"Температура", A0, 0, 25.0},
  {"Влажность", A1, 0, 70.0},
  {"Свет", A2, 0, 500.0},
  {"Давление", A3, 0, 1013.0}
};

void readAllSensors() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    sensors[i].value = analogRead(sensors[i].pin);
  }
}

void displayAllSensors() {
  Serial.println("=== Показания датчиков ===");
  
  for (int i = 0; i < NUM_SENSORS; i++) {
    Serial.print(sensors[i].name);
    Serial.print(": ");
    Serial.print(sensors[i].value);
    
    if (sensors[i].value > sensors[i].threshold) {
      Serial.print(" ⚠️ ПРЕВЫШЕНО");
    }
    
    Serial.println();
  }
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  readAllSensors();
  displayAllSensors();
  delay(5000);
}
```

---

## Вложенные структуры

Структура может содержать другую структуру!

### Объявление вложенной структуры

```cpp
struct Time {
  int hours;
  int minutes;
  int seconds;
};

struct Event {
  String name;
  Time start_time;
  Time end_time;
  boolean is_active;
};

void setup() {
  Serial.begin(9600);
  
  Event meeting = {
    "Совещание",
    {10, 30, 0},      // start_time
    {11, 15, 0},      // end_time
    true
  };
  
  Serial.print("Событие: ");
  Serial.println(meeting.name);
  
  Serial.print("Начало: ");
  Serial.print(meeting.start_time.hours);
  Serial.print(":");
  Serial.println(meeting.start_time.minutes);
  
  Serial.print("Конец: ");
  Serial.print(meeting.end_time.hours);
  Serial.print(":");
  Serial.println(meeting.end_time.minutes);
}

void loop() { }
```

### Сложный пример: GPS координаты

```cpp
struct Location {
  float latitude;
  float longitude;
};

struct GPSData {
  Location position;
  float altitude;
  float speed;
  unsigned long timestamp;
};

float calculateDistance(Location loc1, Location loc2) {
  // Упрощённый расчёт
  float lat_diff = loc1.latitude - loc2.latitude;
  float lon_diff = loc1.longitude - loc2.longitude;
  return sqrt(lat_diff * lat_diff + lon_diff * lon_diff);
}

void displayGPSData(GPSData gps) {
  Serial.print("Широта: ");
  Serial.println(gps.position.latitude, 6);
  
  Serial.print("Долгота: ");
  Serial.println(gps.position.longitude, 6);
  
  Serial.print("Высота: ");
  Serial.println(gps.altitude);
  
  Serial.print("Скорость: ");
  Serial.println(gps.speed);
}

void setup() {
  Serial.begin(9600);
  
  GPSData current_position = {
    {55.7558, 37.6173},  // Москва
    156.0,
    0.0,
    millis()
  };
  
  displayGPSData(current_position);
}

void loop() { }
```

---

## Объединения (union)

Объединение — это тип данных, где все члены РАЗДЕЛЯЮТ одну и ту же память!

### Различие между struct и union

```cpp
struct MyStruct {
  int a;      // 2 байта
  int b;      // 2 байта
  int c;      // 2 байта
};
// Размер: 6 байт

union MyUnion {
  int a;      // 2 байта ┐
  int b;      // 2 байта ├─ ВСЕ РАЗДЕЛЯЮТ 2 БАЙТА!
  int c;      // 2 байта ┘
};
// Размер: 2 байта (только!!)
```

### Синтаксис union

```cpp
union Data {
  int intValue;
  float floatValue;
  char charValue;
};

void setup() {
  Serial.begin(9600);
  
  Data data;
  
  // Записываем int
  data.intValue = 42;
  Serial.print("int: ");
  Serial.println(data.intValue);
  
  // Записываем float - перезаписывает int!
  data.floatValue = 3.14;
  Serial.print("float: ");
  Serial.println(data.floatValue);
  
  // int теперь имеет другое значение!
  Serial.print("int теперь: ");
  Serial.println(data.intValue);  // Измениться!
}

void loop() { }
```

### Когда использовать union?

```
✓ Когда нужно экономить память
✓ Когда нужно работать с данными в разных форматах
✗ Когда нужны все значения одновременно

Пример: экономия памяти на Arduino UNO
```

### Практический пример с union

```cpp
union SensorValue {
  int int_value;
  float float_value;
  byte byte_value;
};

struct FlexibleSensor {
  String name;
  int type;  // 0 = int, 1 = float, 2 = byte
  SensorValue value;
};

void displaySensorValue(FlexibleSensor sensor) {
  Serial.print(sensor.name);
  Serial.print(": ");
  
  switch (sensor.type) {
    case 0:
      Serial.println(sensor.value.int_value);
      break;
    case 1:
      Serial.println(sensor.value.float_value);
      break;
    case 2:
      Serial.println(sensor.value.byte_value);
      break;
  }
}

void setup() {
  Serial.begin(9600);
  
  FlexibleSensor sensor1 = {"Температура", 1, {0}};
  sensor1.value.float_value = 23.5;
  displaySensorValue(sensor1);
  
  FlexibleSensor sensor2 = {"Счётчик", 0, {0}};
  sensor2.value.int_value = 1000;
  displaySensorValue(sensor2);
}

void loop() { }
```

---

## Практические примеры

### Пример 1: Система управления устройствами

```cpp
struct Device {
  String name;
  int id;
  int pin;
  boolean is_on;
  unsigned long turn_on_time;
};

const int NUM_DEVICES = 3;
Device devices[NUM_DEVICES] = {
  {"LED", 1, 13, false, 0},
  {"Моtor", 2, 9, false, 0},
  {"Buzzer", 3, 8, false, 0}
};

void turnOnDevice(int device_index) {
  if (device_index >= 0 && device_index < NUM_DEVICES) {
    digitalWrite(devices[device_index].pin, HIGH);
    devices[device_index].is_on = true;
    devices[device_index].turn_on_time = millis();
    
    Serial.print("Включен: ");
    Serial.println(devices[device_index].name);
  }
}

void turnOffDevice(int device_index) {
  if (device_index >= 0 && device_index < NUM_DEVICES) {
    digitalWrite(devices[device_index].pin, LOW);
    devices[device_index].is_on = false;
    
    Serial.print("Выключен: ");
    Serial.println(devices[device_index].name);
  }
}

void displayAllDevices() {
  Serial.println("=== Состояние устройств ===");
  
  for (int i = 0; i < NUM_DEVICES; i++) {
    Serial.print(devices[i].name);
    Serial.print(": ");
    Serial.print(devices[i].is_on ? "ВКЛ" : "ВЫКЛ");
    
    if (devices[i].is_on) {
      unsigned long uptime = millis() - devices[i].turn_on_time;
      Serial.print(" (");
      Serial.print(uptime / 1000);
      Serial.print("сек)");
    }
    
    Serial.println();
  }
}

void setup() {
  Serial.begin(9600);
  
  for (int i = 0; i < NUM_DEVICES; i++) {
    pinMode(devices[i].pin, OUTPUT);
    digitalWrite(devices[i].pin, LOW);
  }
}

void loop() {
  // Включаем все устройства
  for (int i = 0; i < NUM_DEVICES; i++) {
    turnOnDevice(i);
  }
  
  displayAllDevices();
  delay(3000);
  
  // Выключаем все устройства
  for (int i = 0; i < NUM_DEVICES; i++) {
    turnOffDevice(i);
  }
  
  displayAllDevices();
  delay(3000);
}
```

### Пример 2: Логирование данных с временными метками

```cpp
struct LogEntry {
  unsigned long timestamp;
  String message;
  int sensor_value;
  float temperature;
};

const int MAX_LOGS = 10;
LogEntry logs[MAX_LOGS];
int log_count = 0;
int log_index = 0;

void addLog(String message, int value, float temp) {
  logs[log_index].timestamp = millis();
  logs[log_index].message = message;
  logs[log_index].sensor_value = value;
  logs[log_index].temperature = temp;
  
  log_index = (log_index + 1) % MAX_LOGS;
  
  if (log_count < MAX_LOGS) {
    log_count++;
  }
}

void displayLogs() {
  Serial.println("=== Лог событий ===");
  
  for (int i = 0; i < log_count; i++) {
    Serial.print("[");
    Serial.print(logs[i].timestamp);
    Serial.print("] ");
    Serial.print(logs[i].message);
    Serial.print(" - Значение: ");
    Serial.print(logs[i].sensor_value);
    Serial.print(", Температура: ");
    Serial.println(logs[i].temperature);
  }
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Имитация событий
  int sensor_val = random(0, 1023);
  float temp = 20.0 + random(-50, 50) / 10.0;
  
  addLog("Сенсор", sensor_val, temp);
  
  displayLogs();
  
  delay(5000);
}
```

### Пример 3: Конфигурация системы в структуре

```cpp
struct Config {
  String device_name;
  int device_id;
  float max_temperature;
  float min_temperature;
  int update_interval;
  boolean debug_mode;
};

struct SystemState {
  Config config;
  float current_temperature;
  int sensor_readings;
  unsigned long last_update;
  boolean alarm_active;
};

SystemState system_state = {
  {
    "Temperature Monitor",
    1,
    30.0,
    15.0,
    5000,
    true
  },
  0,
  0,
  0,
  false
};

void updateSystem() {
  system_state.current_temperature = analogRead(A0) * (5.0 / 1023.0) * 20;
  system_state.sensor_readings++;
  system_state.last_update = millis();
  
  // Проверяем пороги
  if (system_state.current_temperature > system_state.config.max_temperature) {
    system_state.alarm_active = true;
  } else if (system_state.current_temperature < system_state.config.min_temperature) {
    system_state.alarm_active = true;
  } else {
    system_state.alarm_active = false;
  }
}

void displaySystemStatus() {
  if (system_state.config.debug_mode) {
    Serial.print("Устройство: ");
    Serial.println(system_state.config.device_name);
    
    Serial.print("Температура: ");
    Serial.println(system_state.current_temperature);
    
    Serial.print("Диапазон: ");
    Serial.print(system_state.config.min_temperature);
    Serial.print(" - ");
    Serial.println(system_state.config.max_temperature);
    
    Serial.print("Сигнал тревоги: ");
    Serial.println(system_state.alarm_active ? "АКТИВНА" : "отключена");
    
    Serial.print("Показаний: ");
    Serial.println(system_state.sensor_readings);
    
    Serial.println("---");
  }
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  updateSystem();
  displaySystemStatus();
  
  delay(system_state.config.update_interval);
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Создавать пользовательские типы данных со структурами

✅ Объявлять и инициализировать структуры

✅ Получать доступ к членам структур

✅ Передавать структуры в функции

✅ Работать с массивами структур

✅ Использовать вложенные структуры

✅ Понимать различие между struct и union

✅ Применять структуры на практике

---

## 🎯 Домашнее задание

1. Создайте структуру `Student` с полями: имя, id, три оценки

2. Напишите функцию для вычисления среднего балла студента

3. Создайте массив из 5 студентов и выведите информацию о каждом

4. Напишите функцию, принимающую указатель на структуру и изменяющую её

5. Создайте структуру для автомобиля (марка, год, скорость) и функции для управления

6. Дополнительно: Создайте вложенную структуру для хранения адреса внутри структуры Person

---

## 🔗 Полезные ссылки

- 📖 **Структуры в C:** https://www.cplusplus.com/doc/tutorial/structures/
- 📖 **Arduino Tips:** https://www.arduino.cc/en/Reference/Struct
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Структура** | Пользовательский тип данных (группа переменных) |
| **Член структуры** | Отдельная переменная в структуре |
| **Инициализация** | Присвоение начальных значений членам |
| **Точка (.)** | Оператор доступа к членам структуры |
| **Стрелка (-\>)** | Оператор доступа через указатель |
| **Вложенная структура** | Структура внутри другой структуры |
| **Объединение (union)** | Тип данных с разделённой памятью |
| **sizeof** | Размер структуры в байтах |
| **Массив структур** | Несколько структур в одном массиве |
| **Разыменование** | Доступ через указатель (*ptr) |

---

**Следующий урок:** 🎓 [Классы и объекты: введение в ООП](../Lesson_9/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025