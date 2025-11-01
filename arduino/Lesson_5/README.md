# 🔌 Функции в Arduino: объявление, параметры, возвращаемые значения

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Что такое функция?](#что-такое-функция)
3. [Объявление функций](#объявление-функций)
4. [Вызов функций](#вызов-функций)
5. [Функции без параметров](#функции-без-параметров)
6. [Функции с параметрами](#функции-с-параметрами)
7. [Функции с возвращаемым значением](#функции-с-возвращаемым-значением)
8. [Встроенные функции Arduino](#встроенные-функции-arduino)
9. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите функции — один из самых важных инструментов программирования. Функции позволяют организовать код, избежать повторений и сделать программу более понятной и модульной.

---

## Что такое функция?

Функция — это блок кода, который выполняет определённую задачу и может быть вызван несколько раз.

### Преимущества использования функций

```
✓ Переиспользование кода
✓ Легче читать и понимать программу
✓ Легче искать и исправлять ошибки
✓ Упрощает отладку
✓ Делает код модульным
✓ Экономит память (код не дублируется)
```

### Пример: без функций vs с функциями

```cpp
// ❌ БЕЗ ФУНКЦИЙ - код повторяется везде
void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}

// ✅ С ФУНКЦИЯМИ - чистый код
void blinkLED() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}

void loop() {
  blinkLED();
}
```

---

## Объявление функций

### Синтаксис

```cpp
тип_возврата имя_функции(параметры) {
  // Тело функции
  if (тип_возврата != void) {
    return значение;
  }
}
```

### Типы возвращаемых значений

```cpp
void function1() { }           // Ничего не возвращает
int function2() { return 42; } // Возвращает int
float function3() { return 3.14; }  // Возвращает float
boolean function4() { return true; }  // Возвращает boolean
String function5() { return "Hello"; }  // Возвращает строку
```

---

## Вызов функций

```cpp
void greet() {
  Serial.println("Привет!");
}

void loop() {
  greet();  // Вызов функции
  delay(1000);
}
```

---

## Функции без параметров

```cpp
void initializeSensors() {
  pinMode(SENSOR_PIN_1, INPUT);
  pinMode(SENSOR_PIN_2, INPUT);
  Serial.println("Датчики инициализированы");
}

void printStatus() {
  Serial.println("=== Статус системы ===");
  Serial.print("Время: ");
  Serial.println(millis());
}

void setup() {
  Serial.begin(9600);
  initializeSensors();
}

void loop() {
  printStatus();
  delay(1000);
}
```

---

## Функции с параметрами

Параметры — это входные данные функции.

### Синтаксис

```cpp
void printNumber(int number) {
  Serial.println(number);
}

void printCoordinates(int x, int y) {
  Serial.print("X: ");
  Serial.print(x);
  Serial.print(", Y: ");
  Serial.println(y);
}

void loop() {
  printNumber(42);
  printCoordinates(10, 20);
}
```

### Различные типы параметров

```cpp
void setSpeed(int speed) {
  analogWrite(PWM_PIN, speed);
}

void setTemperature(float temp) {
  target_temperature = temp;
}

void setLED(boolean state) {
  digitalWrite(LED_PIN, state ? HIGH : LOW);
}

void printMessage(String message) {
  Serial.println(message);
}

void delay_and_print(int ms, String text) {
  delay(ms);
  Serial.println(text);
}
```

---

## Функции с возвращаемым значением

```cpp
int add(int a, int b) {
  return a + b;
}

float calculateAverage(float a, float b) {
  return (a + b) / 2.0;
}

boolean isEven(int number) {
  return (number % 2 == 0);
}

void loop() {
  int result = add(5, 3);
  Serial.println(result);  // 8
  
  boolean even = isEven(4);
  Serial.println(even);    // 1 (true)
}
```

---

## Встроенные функции Arduino

### GPIO функции

```cpp
pinMode(pin, OUTPUT);              // Установить режим
digitalWrite(pin, HIGH);           // Установить выход
int state = digitalRead(pin);      // Прочитать вход
int value = analogRead(A0);        // Прочитать аналог
analogWrite(pin, 255);             // ШИМ выход
```

### Функции времени

```cpp
delay(1000);                       // Задержка в мс
unsigned long ms = millis();       // Миллисекунды с включения
int random_num = random(100);      // Случайное число
```

### Математические функции

```cpp
int abs_val = abs(-5);             // 5
int max_val = max(10, 5);          // 10
int limited = constrain(150, 0, 100);  // 100
int mapped = map(512, 0, 1023, 0, 255);  // Преобразование
```

---

## Практические примеры

### Пример 1: Модульная система LED

```cpp
const int LED_PIN = 9;

void setupLED() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void turnOnLED() {
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED включен");
}

void turnOffLED() {
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED выключен");
}

void blinkLED(int times, int delay_ms) {
  for (int i = 0; i < times; i++) {
    turnOnLED();
    delay(delay_ms);
    turnOffLED();
    delay(delay_ms);
  }
}

void setLEDBrightness(int brightness) {
  brightness = constrain(brightness, 0, 255);
  analogWrite(LED_PIN, brightness);
}

void setup() {
  Serial.begin(9600);
  setupLED();
}

void loop() {
  turnOnLED();
  delay(2000);
  blinkLED(5, 300);
  delay(2000);
  
  for (int i = 0; i <= 255; i += 10) {
    setLEDBrightness(i);
    delay(100);
  }
  
  turnOffLED();
  delay(2000);
}
```

### Пример 2: Система обработки датчиков

```cpp
const int TEMP_SENSOR = A0;
const int LIGHT_SENSOR = A1;

int readSensorFiltered(int sensor_pin, int samples) {
  long sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += analogRead(sensor_pin);
    delay(5);
  }
  return sum / samples;
}

float rawToTemperature(int raw_value) {
  float voltage = raw_value * (5.0 / 1023.0);
  return (voltage - 0.5) * 100.0;
}

int rawToPercent(int raw_value) {
  return map(raw_value, 0, 1023, 0, 100);
}

void displaySensorData(float temp, int light) {
  Serial.print("Температура: ");
  Serial.print(temp);
  Serial.print("°C, Освещённость: ");
  Serial.print(light);
  Serial.println("%");
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  int temp_raw = readSensorFiltered(TEMP_SENSOR, 10);
  float temperature = rawToTemperature(temp_raw);
  
  int light_raw = readSensorFiltered(LIGHT_SENSOR, 10);
  int light_percent = rawToPercent(light_raw);
  
  displaySensorData(temperature, light_percent);
  delay(2000);
}
```

### Пример 3: Светофор с функциями

```cpp
const int RED_LED = 9;
const int YELLOW_LED = 10;
const int GREEN_LED = 11;

void turnOffAll() {
  digitalWrite(RED_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
}

void showRed(int duration) {
  turnOffAll();
  digitalWrite(RED_LED, HIGH);
  Serial.println("КРАСНЫЙ - СТОП!");
  delay(duration);
}

void showYellow(int duration) {
  turnOffAll();
  digitalWrite(YELLOW_LED, HIGH);
  Serial.println("ЖЁЛТЫЙ - ПОДГОТОВКА");
  delay(duration);
}

void showGreen(int duration) {
  turnOffAll();
  digitalWrite(GREEN_LED, HIGH);
  Serial.println("ЗЕЛЁНЫЙ - ПРОЕЗД");
  delay(duration);
}

void setup() {
  Serial.begin(9600);
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
}

void loop() {
  for (int i = 0; i < 3; i++) {
    showRed(3000);
    showYellow(1000);
    showGreen(3000);
    showYellow(1000);
  }
  
  turnOffAll();
  delay(2000);
}
```

### Пример 4: Производственный мониторинг

```cpp
// Система контроля температуры и влажности для производства

const float TEMP_MIN = 15.0;
const float TEMP_MAX = 30.0;
const float HUMIDITY_MIN = 30.0;
const float HUMIDITY_MAX = 70.0;

const int ALARM_LED = 9;
const int WARNING_LED = 10;
const int NORMAL_LED = 11;

enum Status {
  STATUS_NORMAL,
  STATUS_WARNING,
  STATUS_CRITICAL
};

// Структура для хранения данных
struct SensorData {
  float temperature;
  float humidity;
  unsigned long timestamp;
  boolean is_valid;
};

SensorData readSensor(int temp_pin, int humidity_pin) {
  SensorData data;
  data.timestamp = millis();
  data.temperature = analogRead(temp_pin) * (5.0 / 1023.0) * 20.0;
  data.humidity = analogRead(humidity_pin) * (100.0 / 1023.0);
  data.is_valid = true;
  return data;
}

Status analyzeConditions(SensorData data) {
  if (data.temperature < TEMP_MIN - 5 || data.temperature > TEMP_MAX + 5 ||
      data.humidity < HUMIDITY_MIN - 10 || data.humidity > HUMIDITY_MAX + 10) {
    return STATUS_CRITICAL;
  }
  
  if (data.temperature < TEMP_MIN || data.temperature > TEMP_MAX ||
      data.humidity < HUMIDITY_MIN || data.humidity > HUMIDITY_MAX) {
    return STATUS_WARNING;
  }
  
  return STATUS_NORMAL;
}

void updateIndicators(Status status) {
  digitalWrite(NORMAL_LED, LOW);
  digitalWrite(WARNING_LED, LOW);
  digitalWrite(ALARM_LED, LOW);
  
  switch (status) {
    case STATUS_NORMAL:
      digitalWrite(NORMAL_LED, HIGH);
      break;
    case STATUS_WARNING:
      digitalWrite(WARNING_LED, HIGH);
      break;
    case STATUS_CRITICAL:
      digitalWrite(ALARM_LED, HIGH);
      break;
  }
}

void displayStatus(SensorData data, Status status) {
  Serial.print("Температура: ");
  Serial.print(data.temperature, 1);
  Serial.print("°C (");
  Serial.print(TEMP_MIN);
  Serial.print("-");
  Serial.print(TEMP_MAX);
  Serial.println("°C)");
  
  Serial.print("Влажность: ");
  Serial.print(data.humidity, 1);
  Serial.print("% (");
  Serial.print(HUMIDITY_MIN);
  Serial.print("-");
  Serial.print(HUMIDITY_MAX);
  Serial.println("%)");
  
  Serial.print("Статус: ");
  if (status == STATUS_NORMAL) {
    Serial.println("✓ НОРМАЛЬНО");
  } else if (status == STATUS_WARNING) {
    Serial.println("⚠ ВНИМАНИЕ");
  } else {
    Serial.println("✗ КРИТИЧНО");
  }
  
  Serial.println("-----");
}

void setup() {
  Serial.begin(9600);
  pinMode(NORMAL_LED, OUTPUT);
  pinMode(WARNING_LED, OUTPUT);
  pinMode(ALARM_LED, OUTPUT);
  Serial.println("=== ПРОИЗВОДСТВЕННЫЙ МОНИТОРИНГ ===\n");
}

void loop() {
  SensorData data = readSensor(A0, A1);
  Status status = analyzeConditions(data);
  updateIndicators(status);
  displayStatus(data, status);
  
  delay(5000);
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Понимать концепцию функций и их преимущества

✅ Объявлять функции без параметров и с параметрами

✅ Вызывать функции и передавать аргументы

✅ Создавать функции с возвращаемыми значениями

✅ Использовать встроенные функции Arduino

✅ Писать модульный и переиспользуемый код

✅ Применять функции на практических примерах

---

## 🎯 Домашнее задание

1. Напишите функцию `void setLED(int pin, boolean state)` для управления светодиодом

2. Создайте функцию `int getAverageValue(int pin, int samples)` для среднего значения

3. Напишите функцию `boolean isInRange(int value, int min, int max)` для проверки диапазона

4. Создайте функцию `void blink(int pin, int times, int delay_ms)` для мигания

5. Напишите систему из 3 функций: включение, выключение и переключение светодиода

6. Дополнительно: Создайте функцию для преобразования температуры в Фаренгейт

---

## 🔗 Полезные ссылки

- 📖 **Справка по функциям:** https://www.arduino.cc/reference/en/language/functions/
- 📖 **Встроенные функции:** https://www.arduino.cc/reference/en/
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Функция** | Блок кода, выполняющий определённую задачу |
| **Параметр** | Входные данные функции |
| **Аргумент** | Значение, передаваемое при вызове |
| **Возвращаемое значение** | Результат функции |
| **void** | Отсутствие возвращаемого значения |
| **return** | Оператор для возврата значения |
| **Прототип** | Предварительное объявление функции |

---

**Следующий урок:** 📦 [Массивы и строки: основы работы с последовательностями данных](../Lesson_6/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025