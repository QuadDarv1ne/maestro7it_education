# ⏱️ Встроенные функции Arduino: millis(), delay(), micros()

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Функция delay()](#функция-delay)
3. [Функция millis()](#функция-millis)
4. [Функция micros()](#функция-micros)
5. [Функция delayMicroseconds()](#функция-delaymicroseconds)
6. [Проблема переполнения](#проблема-переполнения)
7. [Неблокирующие задержки](#неблокирующие-задержки)
8. [Таймеры и счётчики](#таймеры-и-счётчики)
9. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите встроенные функции Arduino для работы со временем. Эти функции критически важны для создания приложений, которые должны выполняться в определённые моменты времени или с определёнными интервалами.

---

## Функция delay()

### Что такое delay()?

Функция `delay()` приостанавливает выполнение программы на указанное количество миллисекунд.

### Синтаксис

```cpp
delay(milliseconds);  // Задержка в миллисекундах
```

### Характеристики delay()

```
┌─────────────────────────────────────┐
│        Функция delay()              │
├─────────────────────────────────────┤
│                                     │
│ Параметр: миллисекунды (0-4294967) │
│                                     │
│ Точность: ±1 мс (примерно)         │
│                                     │
│ Тип: БЛОКИРУЮЩАЯ функция           │
│  └─ Процессор ничего не делает!    │
│                                     │
│ Использование:                      │
│ ├─ Простые проекты                 │
│ ├─ Отладка                         │
│ └─ Когда ничего не нужно делать    │
│                                     │
│ Недостатки:                         │
│ ├─ Блокирует весь код               │
│ ├─ Невозможно прерывать             │
│ └─ Нельзя выполнять другие задачи   │
│                                     │
└─────────────────────────────────────┘
```

### Примеры delay()

```cpp
// Простое мигание
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);  // 1 секунда
  
  digitalWrite(13, LOW);
  delay(1000);  // 1 секунда
}
```

### Проблема с delay()

```cpp
// ❌ ПРОБЛЕМА - во время delay() ничего не происходит!
void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  Serial.println("Проверяю кнопку...");
  delay(5000);  // 5 секунд ничего не происходит
  
  // Если нажать кнопку во время delay(), это не заметит!
  int button = digitalRead(2);
  Serial.println(button);
}
```

---

## Функция millis()

### Что такое millis()?

Функция `millis()` возвращает количество миллисекунд, прошедших с момента включения Arduino.

### Синтаксис

```cpp
unsigned long time_ms = millis();  // Получить время в миллисекундах
```

### Характеристики millis()

```
┌─────────────────────────────────────┐
│        Функция millis()             │
├─────────────────────────────────────┤
│                                     │
│ Возвращаемое значение:              │
│ ├─ unsigned long (0-4294967295)    │
│ └─ Переполняется каждые 49.7 дней  │
│                                     │
│ Точность: примерно ±1 мс            │
│                                     │
│ Тип: НЕ БЛОКИРУЮЩАЯ функция        │
│  └─ Программа продолжает работать!  │
│                                     │
│ Использование:                      │
│ ├─ Неблокирующие задержки          │
│ ├─ Измерение времени                │
│ ├─ Таймеры и счётчики              │
│ └─ Сложные проекты                 │
│                                     │
└─────────────────────────────────────┘
```

### Примеры millis()

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  // Получаем текущее время
  unsigned long current_time = millis();
  
  Serial.print("Время работы: ");
  Serial.print(current_time);
  Serial.println(" мс");
  
  delay(1000);
}

// Вывод:
// Время работы: 1000 мс
// Время работы: 2000 мс
// Время работы: 3000 мс
// ...
```

### Неблокирующая задержка с millis()

```cpp
unsigned long last_time = 0;
const int INTERVAL = 1000;  // 1 секунда

void setup() {
  Serial.begin(9600);
}

void loop() {
  unsigned long current_time = millis();
  
  // Проверяем, прошло ли нужное количество времени
  if (current_time - last_time >= INTERVAL) {
    Serial.println("1 секунда прошла!");
    last_time = current_time;
  }
  
  // Код продолжает выполняться, не блокируется!
  Serial.println("Я выполняюсь постоянно!");
  delay(100);
}
```

---

## Функция micros()

### Что такое micros()?

Функция `micros()` возвращает количество микросекунд, прошедших с момента включения Arduino. Микросекунда в 1000 раз меньше миллисекунды!

### Синтаксис

```cpp
unsigned long time_us = micros();  // Получить время в микросекундах
```

### Характеристики micros()

```
┌─────────────────────────────────────┐
│        Функция micros()             │
├─────────────────────────────────────┤
│                                     │
│ Возвращаемое значение:              │
│ ├─ unsigned long                    │
│ └─ Переполняется каждые 71 минуту  │
│                                     │
│ Точность: примерно ±4 микросекунды │
│                                     │
│ Тип: НЕ БЛОКИРУЮЩАЯ функция        │
│                                     │
│ Использование:                      │
│ ├─ Измерение очень коротких времён │
│ ├─ Высокоточные таймеры            │
│ ├─ Измерение частоты сигналов      │
│ └─ Профилирование кода             │
│                                     │
│ Примечание:                         │
│ └─ Переполняется чаще чем millis()! │
│                                     │
└─────────────────────────────────────┘
```

### Примеры micros()

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  unsigned long start_time = micros();
  
  // Какой-то код
  for (int i = 0; i < 1000; i++) {
    analogRead(A0);
  }
  
  unsigned long end_time = micros();
  unsigned long duration = end_time - start_time;
  
  Serial.print("Время выполнения: ");
  Serial.print(duration);
  Serial.println(" микросекунд");
  
  delay(1000);
}
```

---

## Функция delayMicroseconds()

### Что такое delayMicroseconds()?

Функция `delayMicroseconds()` приостанавливает выполнение на указанное количество микросекунд.

### Синтаксис

```cpp
delayMicroseconds(microseconds);  // Задержка в микросекундах
```

### Характеристики

```
┌─────────────────────────────────────┐
│  Функция delayMicroseconds()        │
├─────────────────────────────────────┤
│                                     │
│ Параметр: микросекунды (1-16383)   │
│                                     │
│ Точность: примерно ±1 микросекунда │
│                                     │
│ Тип: БЛОКИРУЮЩАЯ функция           │
│                                     │
│ Максимум: ~16 миллисекунд          │
│                                     │
│ Использование:                      │
│ ├─ Генерирование сигналов          │
│ ├─ Точные временные интервалы      │
│ └─ Протоколы с жёсткими сроками    │
│                                     │
│ Осторожно:                          │
│ └─ Очень точная, блокирует код!    │
│                                     │
└─────────────────────────────────────┘
```

### Примеры delayMicroseconds()

```cpp
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  // Генерируем импульс 10 микросекунд
  digitalWrite(13, HIGH);
  delayMicroseconds(10);
  digitalWrite(13, LOW);
  delayMicroseconds(990);  // ~1000 микросекунд всего
}
```

---

## Проблема переполнения

### Когда происходит переполнение?

```
millis(): переполняется каждые 49.7 дня
├─ Максимальное значение: 4,294,967,295 мс
└─ После этого возвращается к 0

micros(): переполняется каждые 71 минуту
├─ Максимальное значение: 4,294,967,295 мкс
└─ После этого возвращается к 0
```

### Безопасное сравнение времени

```cpp
// ❌ НЕПРАВИЛЬНО - может сбиться при переполнении
unsigned long last_time = 0;

void loop() {
  if (millis() > last_time + 1000) {
    // Проблема, если произойдёт переполнение!
    last_time = millis();
  }
}

// ✅ ПРАВИЛЬНО - безопасное сравнение
unsigned long last_time = 0;

void loop() {
  if (millis() - last_time >= 1000) {
    // Безопасно! Работает даже при переполнении
    last_time = millis();
  }
}
```

### Проверка переполнения

```cpp
unsigned long start_time = millis();

void setup() {
  Serial.begin(9600);
}

void loop() {
  unsigned long current_time = millis();
  unsigned long elapsed = current_time - start_time;
  
  // Конвертируем в дни
  unsigned long days = elapsed / (24 * 60 * 60 * 1000);
  
  Serial.print("Дней работы: ");
  Serial.println(days);
  
  delay(1000);
}
```

---

## Неблокирующие задержки

### Шаблон неблокирующей задержки

```cpp
// Глобальные переменные
unsigned long last_action_time = 0;
const unsigned long ACTION_INTERVAL = 1000;  // мс

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Проверяем, пора ли выполнять действие
  if (millis() - last_action_time >= ACTION_INTERVAL) {
    // Выполняем действие
    Serial.println("Действие!");
    
    // Обновляем время
    last_action_time = millis();
  }
  
  // Остальной код выполняется всегда!
  Serial.println("Я работаю постоянно!");
}
```

### Множественные таймеры

```cpp
// Таймер 1: каждые 500мс
unsigned long timer1_last = 0;
const unsigned long TIMER1_INTERVAL = 500;

// Таймер 2: каждые 2000мс
unsigned long timer2_last = 0;
const unsigned long TIMER2_INTERVAL = 2000;

// Таймер 3: каждые 100мс
unsigned long timer3_last = 0;
const unsigned long TIMER3_INTERVAL = 100;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  unsigned long current_time = millis();
  
  // Таймер 1
  if (current_time - timer1_last >= TIMER1_INTERVAL) {
    Serial.println("Таймер 1!");
    timer1_last = current_time;
  }
  
  // Таймер 2
  if (current_time - timer2_last >= TIMER2_INTERVAL) {
    Serial.println("Таймер 2!");
    digitalWrite(13, !digitalRead(13));  // Переключаем LED
    timer2_last = current_time;
  }
  
  // Таймер 3
  if (current_time - timer3_last >= TIMER3_INTERVAL) {
    // Быстрый таймер
    timer3_last = current_time;
  }
}
```

---

## Таймеры и счётчики

### Простой таймер обратного отсчёта

```cpp
unsigned long countdown_end = 0;
boolean counting = false;

void setup() {
  Serial.begin(9600);
}

void startCountdown(unsigned long seconds) {
  countdown_end = millis() + (seconds * 1000);
  counting = true;
  Serial.print("Отсчёт: ");
  Serial.print(seconds);
  Serial.println(" секунд");
}

void loop() {
  if (counting) {
    unsigned long remaining = countdown_end - millis();
    
    if (remaining > 0) {
      static unsigned long last_update = 0;
      
      if (millis() - last_update >= 1000) {
        Serial.print("Осталось: ");
        Serial.print(remaining / 1000);
        Serial.println(" сек");
        last_update = millis();
      }
    } else {
      Serial.println("Время закончилось!");
      counting = false;
    }
  } else {
    // Ждём команды
    if (Serial.available()) {
      String cmd = Serial.readStringUntil('\n');
      if (cmd.startsWith("TIMER")) {
        int seconds = cmd.substring(6).toInt();
        startCountdown(seconds);
      }
    }
  }
}
```

### Счётчик прошедшего времени

```cpp
unsigned long start_time = 0;
boolean timer_running = false;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (timer_running) {
    unsigned long elapsed = millis() - start_time;
    
    unsigned long hours = elapsed / 3600000;
    unsigned long minutes = (elapsed % 3600000) / 60000;
    unsigned long seconds = (elapsed % 60000) / 1000;
    
    Serial.print("Прошло: ");
    if (hours < 10) Serial.print("0");
    Serial.print(hours);
    Serial.print(":");
    if (minutes < 10) Serial.print("0");
    Serial.print(minutes);
    Serial.print(":");
    if (seconds < 10) Serial.print("0");
    Serial.println(seconds);
    
    delay(1000);
  } else {
    if (Serial.available()) {
      String cmd = Serial.readStringUntil('\n');
      cmd.trim();
      
      if (cmd == "START") {
        start_time = millis();
        timer_running = true;
        Serial.println("Таймер запущен");
      }
    }
  }
}
```

---

## Практические примеры

### Пример 1: Система мониторинга с неблокирующими задержками

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Таймеры
unsigned long sensor_timer = 0;
unsigned long display_timer = 0;
unsigned long log_timer = 0;

const unsigned long SENSOR_INTERVAL = 500;    // 500мс
const unsigned long DISPLAY_INTERVAL = 1000;  // 1 сек
const unsigned long LOG_INTERVAL = 10000;     // 10 сек

// Данные
float temperature = 0;
int humidity = 0;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  
  Serial.println("=== Система мониторинга ===");
}

void loop() {
  unsigned long current_time = millis();
  
  // Читаем датчики
  if (current_time - sensor_timer >= SENSOR_INTERVAL) {
    readSensors();
    sensor_timer = current_time;
  }
  
  // Обновляем LCD
  if (current_time - display_timer >= DISPLAY_INTERVAL) {
    updateDisplay();
    display_timer = current_time;
  }
  
  // Логируем данные
  if (current_time - log_timer >= LOG_INTERVAL) {
    logData();
    log_timer = current_time;
  }
  
  // Проверяем Serial команды
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    processCommand(cmd);
  }
}

void readSensors() {
  temperature = 20.0 + (analogRead(A0) - 512) / 100.0;
  humidity = map(analogRead(A1), 0, 1023, 0, 100);
}

void updateDisplay() {
  lcd.clear();
  lcd.print("T:");
  lcd.print(temperature, 1);
  lcd.print("C H:");
  lcd.print(humidity);
  lcd.print("%");
}

void logData() {
  Serial.print(millis() / 1000);
  Serial.print("s - T:");
  Serial.print(temperature, 1);
  Serial.print("C H:");
  Serial.print(humidity);
  Serial.println("%");
}

void processCommand(String cmd) {
  if (cmd == "STATUS") {
    Serial.println("System OK");
  } else if (cmd == "TIME") {
    Serial.print("Uptime: ");
    Serial.print(millis() / 1000);
    Serial.println("s");
  }
}
```

### Пример 2: Многофункциональный таймер

```cpp
enum TimerMode {
  MODE_IDLE,
  MODE_COUNTDOWN,
  MODE_STOPWATCH
};

TimerMode mode = MODE_IDLE;
unsigned long timer_value = 0;
boolean timer_running = false;

void setup() {
  Serial.begin(9600);
  Serial.println("=== Таймер ===");
  Serial.println("TIMER <сек> - отсчёт");
  Serial.println("START/STOP/RESET - управление");
}

void loop() {
  unsigned long current_time = millis();
  
  switch (mode) {
    case MODE_COUNTDOWN:
      handleCountdown(current_time);
      break;
    case MODE_STOPWATCH:
      handleStopwatch(current_time);
      break;
    case MODE_IDLE:
      // Ничего не делаем
      break;
  }
  
  // Обрабатываем команды
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    processTimerCommand(cmd);
  }
}

void handleCountdown(unsigned long current_time) {
  if (timer_running) {
    if (timer_value > current_time) {
      unsigned long remaining = timer_value - current_time;
      if (remaining % 1000 < 100) {  // Выводим раз в секунду примерно
        Serial.print("Осталось: ");
        Serial.print(remaining / 1000);
        Serial.println("s");
      }
    } else {
      Serial.println("ВРЕМЯ ВЫШЛО!");
      timer_running = false;
      mode = MODE_IDLE;
    }
  }
}

void handleStopwatch(unsigned long current_time) {
  if (timer_running) {
    unsigned long elapsed = current_time - timer_value;
    
    static unsigned long last_display = 0;
    if (current_time - last_display >= 1000) {
      Serial.print("Прошло: ");
      Serial.print(elapsed / 1000);
      Serial.println("s");
      last_display = current_time;
    }
  }
}

void processTimerCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();
  
  if (cmd.startsWith("TIMER")) {
    int seconds = cmd.substring(6).toInt();
    mode = MODE_COUNTDOWN;
    timer_value = millis() + (seconds * 1000);
    timer_running = true;
    Serial.print("Отсчёт начался: ");
    Serial.print(seconds);
    Serial.println("s");
  }
  else if (cmd == "START") {
    if (mode == MODE_IDLE) {
      mode = MODE_STOPWATCH;
      timer_value = millis();
    }
    timer_running = true;
    Serial.println("Запущено");
  }
  else if (cmd == "STOP") {
    timer_running = false;
    Serial.println("Остановлено");
  }
  else if (cmd == "RESET") {
    timer_running = false;
    mode = MODE_IDLE;
    Serial.println("Сброс");
  }
}
```

### Пример 3: Профилирование производительности кода

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("=== Профилирование ===");
  
  // Тест 1: analogRead
  benchmarkAnalogRead();
  
  // Тест 2: digitalRead
  benchmarkDigitalRead();
  
  // Тест 3: Цикл
  benchmarkLoop();
  
  delay(5000);
}

void benchmarkAnalogRead() {
  unsigned long start = micros();
  
  for (int i = 0; i < 1000; i++) {
    analogRead(A0);
  }
  
  unsigned long duration = micros() - start;
  
  Serial.print("analogRead (1000x): ");
  Serial.print(duration);
  Serial.print(" микросек (");
  Serial.print(duration / 1000.0);
  Serial.println(" мс)");
}

void benchmarkDigitalRead() {
  unsigned long start = micros();
  
  for (int i = 0; i < 10000; i++) {
    digitalRead(2);
  }
  
  unsigned long duration = micros() - start;
  
  Serial.print("digitalRead (10000x): ");
  Serial.print(duration);
  Serial.print(" микросек (");
  Serial.print(duration / 1000.0);
  Serial.println(" мс)");
}

void benchmarkLoop() {
  unsigned long start = micros();
  
  int sum = 0;
  for (int i = 0; i < 10000; i++) {
    sum += i;
  }
  
  unsigned long duration = micros() - start;
  
  Serial.print("Цикл 10000 итераций: ");
  Serial.print(duration);
  Serial.print(" микросек (");
  Serial.print(duration / 1000.0);
  Serial.println(" мс)");
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Использовать функцию delay() для блокирующих задержек

✅ Использовать millis() для неблокирующих задержек

✅ Использовать micros() для микросекундных измерений

✅ Использовать delayMicroseconds() для точных интервалов

✅ Избегать проблемы переполнения временных счётчиков

✅ Создавать множественные таймеры одновременно

✅ Профилировать производительность кода

✅ Создавать сложные системы с управлением временем

---

## 🎯 Домашнее задание

1. Напишите программу с тремя независимыми таймерами (каждый со своим интервалом)

2. Создайте систему обратного отсчёта (вводимое время через Serial)

3. Напишите программу профилирования (измеряйте время выполнения разных операций)

4. Создайте приложение секундомера (START/STOP/RESET)

5. Напишите программу с множественными задачами без блокирования (LED, датчики, вывод)

6. Дополнительно: Создайте систему планировщика задач (выполнение в определённые времена)

---

## 🔗 Полезные ссылки

- 📖 **millis():** https://www.arduino.cc/reference/en/language/functions/time/millis/
- 📖 **delay():** https://www.arduino.cc/reference/en/language/functions/time/delay/
- 📖 **micros():** https://www.arduino.cc/reference/en/language/functions/time/micros/
- 📖 **delayMicroseconds():** https://www.arduino.cc/reference/en/language/functions/time/delaymicroseconds/
- 📖 **Timing:** https://www.arduino.cc/en/Tutorial/TimingSecrets
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **delay()** | Блокирующая задержка в миллисекундах |
| **millis()** | Возвращает миллисекунды с включения |
| **micros()** | Возвращает микросекунды с включения |
| **delayMicroseconds()** | Блокирующая задержка в микросекундах |
| **unsigned long** | Тип данных (0 - 4,294,967,295) |
| **Переполнение** | Превышение максимального значения переменной |
| **Неблокирующая задержка** | Проверка времени без остановки программы |
| **Таймер** | Устройство для отсчёта или измерения времени |
| **Интервал** | Промежуток времени между событиями |
| **Профилирование** | Измерение производительности кода |
| **Микросекунда** | 1/1,000,000 часть секунды |
| **Миллисекунда** | 1/1,000 часть секунды |

---

**Следующий урок:** ⚡ [Прерывания (interrupts) и обработка событий в реальном времени](../Lesson_15/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
