# 📡 Серийная коммуникация (Serial): отладка и обмен данными

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Что такое Serial?](#что-такое-serial)
3. [Инициализация Serial](#инициализация-serial)
4. [Вывод данных](#вывод-данных)
5. [Чтение данных](#чтение-данных)
6. [Serial Monitor](#serial-monitor)
7. [Передача текстовых команд](#передача-текстовых-команд)
8. [Форматированный вывод](#форматированный-вывод)
9. [Двусторонняя коммуникация](#двусторонняя-коммуникация)
10. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите серийную коммуникацию — способ обмена данными между Arduino и компьютером через USB кабель. Это основной инструмент для отладки и взаимодействия с программой.

---

## Что такое Serial?

Serial (последовательная передача) — это протокол для отправки данных по одному биту за раз через один провод.

### Как работает Serial?

```
Arduino          USB кабель          Компьютер
│                                    │
├─ TX (передача)────────────────→  COM порт
├─ RX (приём)←────────────────────  COM порт
└─ GND (земля)───────────────────→  GND
```

### Параметры Serial

```
Скорость (Baud Rate):
├─ 9600   - Стандартная (медленная, надёжная)
├─ 115200 - Быстрая (требует хорошего кабеля)
├─ 57600  - Среднее значение
└─ другие значения...

Биты:
├─ 8 бит данных (стандарт)
├─ 1 стоп-бит
└─ Нет проверки чётности
```

---

## Инициализация Serial

### Начало работы

```cpp
void setup() {
  // Инициализировать Serial с скоростью 9600 бод
  Serial.begin(9600);
  
  // Опционально: подождать подключения (для некоторых платформ)
  while (!Serial) {
    ;  // Ждём подключения
  }
  
  Serial.println("Serial коммуникация начата!");
}

void loop() {
  // ...
}
```

### Разные скорости

```cpp
// Медленная (надёжная)
Serial.begin(9600);

// Быстрая (для больших объёмов данных)
Serial.begin(115200);

// Среднее значение
Serial.begin(57600);
```

⚠️ **Важно:** Скорость в коде должна совпадать со скоростью в Serial Monitor!

---

## Вывод данных

### Функции вывода

```cpp
Serial.print(data);        // Вывести БЕЗ перевода строки
Serial.println(data);      // Вывести С переводом строки
Serial.write(byte);        // Отправить один байт
Serial.flush();            // Очистить буфер
```

### Примеры вывода

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  // Вывод целого числа
  int number = 42;
  Serial.println(number);           // 42
  
  // Вывод дробного числа
  float pi = 3.14159;
  Serial.println(pi);               // 3.14
  Serial.println(pi, 2);            // 3.14 (2 знака после запятой)
  
  // Вывод строки
  Serial.println("Hello Arduino!");
  
  // Вывод логического значения
  boolean flag = true;
  Serial.println(flag);             // 1 (true) или 0 (false)
  
  // Вывод символа
  Serial.println('A');              // A
  
  // Вывод в разных системах счисления
  Serial.println(255, DEC);         // 255 (десятичная)
  Serial.println(255, HEX);         // FF (шестнадцатеричная)
  Serial.println(255, OCT);         // 377 (восьмеричная)
  Serial.println(255, BIN);         // 11111111 (двоичная)
  
  delay(1000);
}
```

### Вывод БЕЗ перевода строки

```cpp
void loop() {
  Serial.print("Температура: ");
  Serial.print(23.5);
  Serial.print("°C, Влажность: ");
  Serial.print(65);
  Serial.println("%");
  
  // Результат: Температура: 23.5°C, Влажность: 65%
  
  delay(1000);
}
```

---

## Чтение данных

### Функции чтения

```cpp
Serial.available();       // Сколько байт доступно для чтения
Serial.read();            // Прочитать один байт
Serial.readString();      // Прочитать строку
Serial.readStringUntil(); // Прочитать строку до символа
Serial.peek();            // Посмотреть байт БЕЗ удаления
```

### Простой пример чтения

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  // Проверяем, есть ли данные
  if (Serial.available() > 0) {
    // Читаем один байт
    int data = Serial.read();
    
    // Выводим полученный байт
    Serial.print("Получено: ");
    Serial.println(data);
  }
}
```

### Чтение одного символа

```cpp
void setup() {
  Serial.begin(9600);
  Serial.println("Введите символ:");
}

void loop() {
  if (Serial.available() > 0) {
    char symbol = Serial.read();
    
    Serial.print("Вы ввели: ");
    Serial.println(symbol);
  }
}
```

---

## Serial Monitor

### Как открыть Serial Monitor

```
Arduino IDE:
├─ Tools > Serial Monitor
├─ Или нажмите Ctrl+Shift+M
└─ Выберите правильный COM порт и скорость (9600)
```

### Примеры вывода в Serial Monitor

```cpp
void setup() {
  Serial.begin(9600);
  
  Serial.println("=== СИСТЕМА МОНИТОРИНГА ===");
  Serial.print("Напряжение: ");
  Serial.print(5.0);
  Serial.println("V");
  Serial.println("Система готова");
}

void loop() {
  // Имитация показаний датчика
  float temp = 20.0 + random(-10, 10) / 10.0;
  int humidity = random(40, 80);
  
  Serial.print("Время: ");
  Serial.print(millis());
  Serial.print("мс | Температура: ");
  Serial.print(temp, 1);
  Serial.print("°C | Влажность: ");
  Serial.print(humidity);
  Serial.println("%");
  
  delay(1000);
}

// Вывод в Serial Monitor:
// === СИСТЕМА МОНИТОРИНГА ===
// Напряжение: 5.0V
// Система готова
// Время: 1000мс | Температура: 20.5°C | Влажность: 62%
// Время: 2000мс | Температура: 21.2°C | Влажность: 58%
// ...
```

---

## Передача текстовых команд

### Простая обработка команд

```cpp
void setup() {
  Serial.begin(9600);
  Serial.println("Введите команду: LED_ON или LED_OFF");
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    // Удаляем пробелы
    command.trim();
    
    Serial.print("Получена команда: ");
    Serial.println(command);
    
    if (command == "LED_ON") {
      digitalWrite(13, HIGH);
      Serial.println("LED включен");
    } 
    else if (command == "LED_OFF") {
      digitalWrite(13, LOW);
      Serial.println("LED выключен");
    } 
    else {
      Serial.println("Неизвестная команда!");
    }
  }
}
```

### Обработка команд с параметрами

```cpp
void setup() {
  Serial.begin(9600);
  Serial.println("Команды: BLINK [times] [delay]");
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    
    if (line.startsWith("BLINK")) {
      // Парсим параметры
      int times = 3;      // Значения по умолчанию
      int delay_ms = 500;
      
      // Простой парсинг (для демонстрации)
      int space1 = line.indexOf(' ');
      int space2 = line.indexOf(' ', space1 + 1);
      
      if (space1 > 0) {
        times = line.substring(space1 + 1).toInt();
      }
      if (space2 > 0) {
        delay_ms = line.substring(space2 + 1).toInt();
      }
      
      Serial.print("Мигаю ");
      Serial.print(times);
      Serial.print(" раз с задержкой ");
      Serial.print(delay_ms);
      Serial.println("мс");
      
      for (int i = 0; i < times; i++) {
        digitalWrite(13, HIGH);
        delay(delay_ms);
        digitalWrite(13, LOW);
        delay(delay_ms);
      }
    }
  }
}

// Примеры команд:
// BLINK         → Мигает 3 раза, 500мс
// BLINK 5       → Мигает 5 раз, 500мс
// BLINK 5 200   → Мигает 5 раз, 200мс
```

---

## Форматированный вывод

### Вывод таблицы

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("=== ТАБЛИЦА ДАННЫХ ===");
  Serial.println("Время(мс)\tТемп(°C)\tВлажность(%)");
  Serial.println("─────────────────────────────────");
  
  for (int i = 0; i < 5; i++) {
    float temp = 20.0 + random(-50, 50) / 10.0;
    int humidity = random(40, 80);
    
    Serial.print(millis());
    Serial.print("\t");
    Serial.print(temp, 1);
    Serial.print("\t");
    Serial.println(humidity);
    
    delay(1000);
  }
  
  Serial.println();
  delay(5000);
}

// Вывод:
// === ТАБЛИЦА ДАННЫХ ===
// Время(мс)	Темп(°C)	Влажность(%)
// ─────────────────────────────────
// 1000	    20.5	    62
// 2000	    21.2	    58
// 3000	    19.8	    71
// 4000	    22.1	    55
// 5000	    20.3	    68
```

### Вывод JSON формата

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  float temp = 23.5;
  int humidity = 65;
  int pressure = 1013;
  
  // JSON формат (полезен для интеграции с системами)
  Serial.print("{\"temperature\":");
  Serial.print(temp);
  Serial.print(",\"humidity\":");
  Serial.print(humidity);
  Serial.print(",\"pressure\":");
  Serial.print(pressure);
  Serial.println("}");
  
  delay(2000);
}

// Вывод:
// {"temperature":23.5,"humidity":65,"pressure":1013}
// {"temperature":23.7,"humidity":64,"pressure":1013}
```

---

## Двусторонняя коммуникация

### Полный диалог Arduino ↔ Компьютер

```cpp
void setup() {
  Serial.begin(9600);
  Serial.println("Добро пожаловать в Arduino!");
  Serial.println("Доступные команды:");
  Serial.println("1 - Включить LED");
  Serial.println("2 - Выключить LED");
  Serial.println("3 - Показать статус");
  Serial.println("4 - Сброс");
  
  pinMode(13, OUTPUT);
}

boolean led_status = false;
unsigned long led_on_time = 0;

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    processCommand(input);
  }
}

void processCommand(String cmd) {
  if (cmd == "1") {
    digitalWrite(13, HIGH);
    led_status = true;
    led_on_time = millis();
    Serial.println("✓ LED включен");
  }
  else if (cmd == "2") {
    digitalWrite(13, LOW);
    led_status = false;
    Serial.println("✓ LED выключен");
  }
  else if (cmd == "3") {
    showStatus();
  }
  else if (cmd == "4") {
    digitalWrite(13, LOW);
    led_status = false;
    Serial.println("✓ Система сброшена");
  }
  else {
    Serial.print("? Неизвестная команда: ");
    Serial.println(cmd);
  }
}

void showStatus() {
  Serial.println("=== СТАТУС СИСТЕМЫ ===");
  Serial.print("LED: ");
  Serial.println(led_status ? "ВКЛ" : "ВЫКЛ");
  
  if (led_status) {
    unsigned long uptime = millis() - led_on_time;
    Serial.print("Время работы: ");
    Serial.print(uptime / 1000);
    Serial.println("сек");
  }
  
  Serial.print("Время работы Arduino: ");
  Serial.print(millis() / 1000);
  Serial.println("сек");
}
```

---

## Практические примеры

### Пример 1: Мониторинг датчиков в реальном времени

```cpp
const int TEMP_SENSOR = A0;
const int HUMIDITY_SENSOR = A1;

void setup() {
  Serial.begin(115200);  // Более быстрая скорость
  Serial.println("=== СИСТЕМА МОНИТОРИНГА ===");
}

void loop() {
  int temp_raw = analogRead(TEMP_SENSOR);
  int humidity_raw = analogRead(HUMIDITY_SENSOR);
  
  float temperature = map(temp_raw, 0, 1023, -40, 85);
  float humidity = map(humidity_raw, 0, 1023, 0, 100);
  
  // Вывод с форматированием
  Serial.print("[");
  Serial.print(millis() / 1000);
  Serial.print("s] ");
  Serial.print("T=");
  Serial.print(temperature, 1);
  Serial.print("°C ");
  Serial.print("H=");
  Serial.print(humidity, 1);
  Serial.println("%");
  
  delay(1000);
}
```

### Пример 2: Система управления через Serial

```cpp
const int LED1 = 9;
const int LED2 = 10;
const int LED3 = 11;

void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  
  Serial.println("=== КОНТРОЛЬНАЯ ПАНЕЛЬ ===");
  Serial.println("LED1, LED2, LED3, STATUS, HELP");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toUpperCase();
    
    if (command == "LED1") {
      toggleLED(LED1, "LED1");
    }
    else if (command == "LED2") {
      toggleLED(LED2, "LED2");
    }
    else if (command == "LED3") {
      toggleLED(LED3, "LED3");
    }
    else if (command == "STATUS") {
      showStatus();
    }
    else if (command == "HELP") {
      showHelp();
    }
    else {
      Serial.print("? Неизвестно: ");
      Serial.println(command);
    }
  }
}

void toggleLED(int pin, String name) {
  int state = digitalRead(pin);
  digitalWrite(pin, !state);
  
  Serial.print(name);
  Serial.println(state == LOW ? " - ВКЛ" : " - ВЫКЛ");
}

void showStatus() {
  Serial.println("=== СТАТУС ===");
  Serial.print("LED1: ");
  Serial.println(digitalRead(LED1) ? "ВКЛ" : "ВЫКЛ");
  Serial.print("LED2: ");
  Serial.println(digitalRead(LED2) ? "ВКЛ" : "ВЫКЛ");
  Serial.print("LED3: ");
  Serial.println(digitalRead(LED3) ? "ВКЛ" : "ВЫКЛ");
}

void showHelp() {
  Serial.println("=== СПРАВКА ===");
  Serial.println("LED1 - Переключить LED1");
  Serial.println("LED2 - Переключить LED2");
  Serial.println("LED3 - Переключить LED3");
  Serial.println("STATUS - Показать статус");
  Serial.println("HELP - Показать эту справку");
}
```

### Пример 3: Логирование с датчиком

```cpp
const int SENSOR_PIN = A0;
const int LOG_INTERVAL = 5000;  // 5 секунд

unsigned long last_log = 0;
int log_count = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("=== ЛОГИРОВАНИЕ ДАТЧИКА ===");
  Serial.println("Формат: [Номер] [Время] [Значение]");
  Serial.println("─────────────────────────────────");
}

void loop() {
  if (millis() - last_log >= LOG_INTERVAL) {
    log_count++;
    int value = analogRead(SENSOR_PIN);
    
    // Форматированный вывод
    Serial.print("[");
    Serial.print(log_count);
    Serial.print("] ");
    
    Serial.print(millis() / 1000);
    Serial.print("s ");
    
    Serial.print("Val=");
    Serial.println(value);
    
    last_log = millis();
  }
}

// Вывод:
// === ЛОГИРОВАНИЕ ДАТЧИКА ===
// Формат: [Номер] [Время] [Значение]
// ─────────────────────────────────
// [1] 5s Val=512
// [2] 10s Val=523
// [3] 15s Val=518
// [4] 20s Val=531
```

### Пример 4: Интерактивная система калибровки

```cpp
void setup() {
  Serial.begin(9600);
  Serial.println("=== СИСТЕМА КАЛИБРОВКИ ===");
  Serial.println("Команды: ZERO, SPAN, READ, STATUS");
}

float zero_offset = 0;
float span_factor = 1.0;

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();
    
    if (cmd == "ZERO") {
      zero_offset = analogRead(A0);
      Serial.print("Zero offset установлен: ");
      Serial.println(zero_offset);
    }
    else if (cmd == "SPAN") {
      Serial.println("Введите значение span:");
      while (!Serial.available());
      span_factor = Serial.parseFloat();
      Serial.print("Span factor установлен: ");
      Serial.println(span_factor, 3);
    }
    else if (cmd == "READ") {
      float raw = analogRead(A0);
      float calibrated = (raw - zero_offset) * span_factor;
      Serial.print("Raw: ");
      Serial.print(raw);
      Serial.print(" | Calibrated: ");
      Serial.println(calibrated, 2);
    }
    else if (cmd == "STATUS") {
      Serial.println("=== СТАТУС КАЛИБРОВКИ ===");
      Serial.print("Zero offset: ");
      Serial.println(zero_offset);
      Serial.print("Span factor: ");
      Serial.println(span_factor, 3);
    }
  }
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Инициализировать Serial коммуникацию

✅ Выводить данные в Serial Monitor

✅ Читать данные от пользователя

✅ Обрабатывать текстовые команды

✅ Форматировать вывод данных

✅ Создавать двусторонний диалог

✅ Использовать Serial для отладки

✅ Логировать данные датчиков

---

## 🎯 Домашнее задание

1. Напишите программу, которая выводит показания датчика в Serial Monitor каждую секунду

2. Создайте простую систему команд: вкл/выкл LED через Serial

3. Напишите программу, которая считает слова, отправленные через Serial

4. Создайте систему меню (вверх/вниз/выбор) через Serial

5. Напишите логгер, который записывает время и значения в формате таблицы

6. Дополнительно: Создайте систему с калибровкой датчика через Serial команды

---

## 🔗 Полезные ссылки

- 📖 **Serial Reference:** https://www.arduino.cc/reference/en/language/functions/communication/serial/
- 📖 **Serial.begin:** https://www.arduino.cc/reference/en/language/functions/communication/serial/begin/
- 📖 **Serial.print:** https://www.arduino.cc/reference/en/language/functions/communication/serial/print/
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Serial** | Последовательная передача данных |
| **Baud Rate** | Скорость передачи (бит в секунду) |
| **TX** | Передача (отправка) |
| **RX** | Приём (получение) |
| **COM порт** | Последовательный порт на компьютере |
| **Serial Monitor** | Окно для просмотра Serial данных |
| **print()** | Вывести без перевода строки |
| **println()** | Вывести с переводом строки |
| **read()** | Прочитать данные |
| **available()** | Проверить наличие данных |
| **Буфер** | Временное хранилище данных |
| **Форматирование** | Специальное представление данных |

---

**Следующий урок:** 🔄 [Работа с серво-моторами и управление движением](../Lesson_11/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025