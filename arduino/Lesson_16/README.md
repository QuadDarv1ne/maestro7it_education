# 💾 Работа с памятью: EEPROM и SRAM на Arduino

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Типы памяти в Arduino](#типы-памяти-в-arduino)
3. [SRAM (оперативная память)](#sram-оперативная-память)
4. [FLASH память](#flash-память)
5. [EEPROM (энергонезависимая память)](#eeprom-энергонезависимая-память)
6. [Работа с EEPROM](#работа-с-eeprom)
7. [Сохранение структур](#сохранение-структур)
8. [Оптимизация памяти](#оптимизация-памяти)
9. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите различные типы памяти в Arduino и научитесь работать с ними эффективно. Понимание памяти критически важно для создания сложных и надёжных приложений.

---

## Типы памяти в Arduino

### Трёхуровневая система памяти

```
┌───────────────────────────────────────────────────┐
│         ПАМЯТЬ ARDUINO UNO                        │
├───────────────────────────────────────────────────┤
│                                                   │
│ FLASH (32 KB) - Программная память               │
│ ├─ Хранит вашу программу                        │
│ ├─ Энергонезависимая (сохраняется при выключ.)  │
│ ├─ Перезаписывается при загрузке                │
│ └─ Оптимизирована для чтения                     │
│                                                   │
│ SRAM (2 KB) - Оперативная память                 │
│ ├─ Глобальные и локальные переменные            │
│ ├─ Стек (stack) и куча (heap)                   │
│ ├─ Очень быстрая                                │
│ ├─ Теряется при выключении                      │
│ └─ ОГРАНИЧЕНА! (самая критичная)                │
│                                                   │
│ EEPROM (1 KB) - Энергонезависимая память        │
│ ├─ Для сохранения данных между сеансами         │
│ ├─ Очень медленная                              │
│ ├─ Ограниченное количество записей (~100000)    │
│ └─ Используется редко                           │
│                                                   │
└───────────────────────────────────────────────────┘
```

### Сравнение памяти

```
┌──────────┬───────┬──────────────┬────────────────┐
│ Тип      │ Размер│ Скорость     │ Энергонезав.   │
├──────────┼───────┼──────────────┼────────────────┤
│ FLASH    │ 32 KB │ Быстро       │ Да             │
│ SRAM     │ 2 KB  │ Очень быстро │ Нет            │
│ EEPROM   │ 1 KB  │ Медленно     │ Да             │
└──────────┴───────┴──────────────┴────────────────┘
```

---

## SRAM (оперативная память)

### Структура SRAM

```
SRAM (2 KB):

┌─────────────────────────────────┐
│ Стек (Stack)                    │
│ └─ Растёт вниз → ← растёт вверх│
│   (локальные переменные, адреса)│
│          ↓       ↑              │
│     [пустое место]              │
│          ↑       ↓              │
│ Куча (Heap)                     │
│ └─ Динамическая память          │
├─────────────────────────────────┤
│ Глобальные переменные           │
│ Инициализированные данные       │
│ BSS (неинициализированные)      │
└─────────────────────────────────┘
```

### Проблема нехватки памяти

```cpp
// ❌ ПРОБЛЕМА - недостаточно SRAM!
void setup() {
  Serial.begin(9600);
  
  // Это займет много памяти!
  String text1 = "Длинная строка текста для хранения";
  String text2 = "Ещё одна длинная строка";
  String text3 = "И ещё одна строка";
  
  // Создали большой массив
  int data[200];
  
  // Результат: программа начинает работать неправильно!
}
```

### Проверка использования памяти

```cpp
// Функция для проверки свободной памяти
int freeRam() {
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? 
          (int) &__heap_start : (int) __brkval);
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("Свободная SRAM: ");
  Serial.print(freeRam());
  Serial.println(" байт");
  
  delay(1000);
}
```

### Оптимизация использования SRAM

```cpp
// ❌ Неправильно - строки в SRAM
void setup() {
  Serial.begin(9600);
  Serial.println("Это строка занимает SRAM!");
}

// ✅ Правильно - строки в FLASH
void setup() {
  Serial.begin(9600);
  Serial.println(F("Это строка в FLASH памяти!"));
}
```

---

## FLASH память

### Использование FLASH для данных

```cpp
// Сохраняем данные в FLASH (не в SRAM)
const byte DIGITS[] PROGMEM = {
  0x3F, 0x06, 0x5B, 0x4F, 0x66,
  0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

const char MESSAGE[] PROGMEM = "Привет из FLASH!";

void setup() {
  Serial.begin(9600);
  
  // Чтение из FLASH
  byte digit = pgm_read_byte(&DIGITS[0]);
  Serial.println(digit);
}
```

### Макросы для работы с FLASH

```cpp
// PROGMEM - сохранить в FLASH
const char text[] PROGMEM = "Текст в FLASH";

// F() макрос - удобнее
Serial.println(F("Текст в FLASH"));

// pgm_read_byte - чтение байта из FLASH
byte value = pgm_read_byte(&array[0]);

// pgm_read_word - чтение слова из FLASH
word value = pgm_read_word(&array[0]);
```

---

## EEPROM (энергонезависимая память)

### Что такое EEPROM?

EEPROM (Electrically Erasable Programmable Read-Only Memory) — это память, которая сохраняет данные при отключении питания.

### Характеристики EEPROM

```
┌─────────────────────────────────┐
│ EEPROM (Arduino UNO)            │
├─────────────────────────────────┤
│                                 │
│ Размер: 1024 байта              │
│                                 │
│ Адреса: 0 - 1023                │
│                                 │
│ Циклы записи: ~100,000          │
│ (после этого может быть ошибка) │
│                                 │
│ Время записи: ~3.3 мс за байт   │
│ (МЕДЛЕННО!)                     │
│                                 │
│ Назначение:                     │
│ ├─ Сохранение настроек          │
│ ├─ Логирование данных           │
│ └─ Конфигурация устройства      │
│                                 │
└─────────────────────────────────┘
```

### Работа с EEPROM

```cpp
#include <EEPROM.h>

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Чтение одного байта
  byte value = EEPROM.read(0);
  
  // Запись одного байта
  EEPROM.write(0, 42);
  
  // Запись завершена? Может быть 3.3мс задержка
}
```

### Основные функции EEPROM

```cpp
#include <EEPROM.h>

// Чтение байта по адресу
byte value = EEPROM.read(address);

// Запись байта по адресу
EEPROM.write(address, value);

// Обновление (только если значение другое)
EEPROM.update(address, value);

// Получить доступ к байту через operator[]
byte val = EEPROM[0];
EEPROM[0] = 42;

// Получить размер
int size = EEPROM.length();  // 1024 на UNO
```

---

## Сохранение структур

### Сохранение простых типов

```cpp
#include <EEPROM.h>

const int ADDR_INT = 0;
const int ADDR_FLOAT = 2;
const int ADDR_LONG = 6;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Сохранение
  saveInt(100);
  saveFloat(3.14);
  saveLong(1234567);
  
  // Чтение
  int i = readInt();
  float f = readFloat();
  long l = readLong();
  
  Serial.print("Int: ");
  Serial.println(i);
  
  delay(5000);
}

void saveInt(int value) {
  EEPROM.write(ADDR_INT, (value >> 8) & 0xFF);
  EEPROM.write(ADDR_INT + 1, value & 0xFF);
}

int readInt() {
  int value = EEPROM.read(ADDR_INT) << 8;
  value |= EEPROM.read(ADDR_INT + 1);
  return value;
}

void saveFloat(float value) {
  byte* p = (byte*)&value;
  for (int i = 0; i < 4; i++) {
    EEPROM.write(ADDR_FLOAT + i, p[i]);
  }
}

float readFloat() {
  float value;
  byte* p = (byte*)&value;
  for (int i = 0; i < 4; i++) {
    p[i] = EEPROM.read(ADDR_FLOAT + i);
  }
  return value;
}

void saveLong(long value) {
  for (int i = 0; i < 4; i++) {
    EEPROM.write(ADDR_LONG + i, (value >> (8 * i)) & 0xFF);
  }
}

long readLong() {
  long value = 0;
  for (int i = 0; i < 4; i++) {
    value |= ((long)EEPROM.read(ADDR_LONG + i)) << (8 * i);
  }
  return value;
}
```

### Сохранение структур

```cpp
#include <EEPROM.h>

struct Settings {
  int brightness;
  float temperature_target;
  boolean enabled;
};

const int ADDR_SETTINGS = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Создаём структуру
  Settings settings;
  settings.brightness = 200;
  settings.temperature_target = 25.5;
  settings.enabled = true;
  
  // Сохраняем
  saveSettings(settings);
  
  // Читаем обратно
  Settings loaded = loadSettings();
  
  Serial.print("Brightness: ");
  Serial.println(loaded.brightness);
  
  delay(5000);
}

void saveSettings(Settings s) {
  byte* p = (byte*)&s;
  for (int i = 0; i < sizeof(Settings); i++) {
    EEPROM.write(ADDR_SETTINGS + i, p[i]);
  }
}

Settings loadSettings() {
  Settings s;
  byte* p = (byte*)&s;
  for (int i = 0; i < sizeof(Settings); i++) {
    p[i] = EEPROM.read(ADDR_SETTINGS + i);
  }
  return s;
}
```

---

## Оптимизация памяти

### Техники оптимизации

```cpp
// ❌ Неправильно - много памяти
void setup() {
  Serial.begin(9600);
  String message = "Это занимает много памяти!";
  Serial.println(message);
}

// ✅ Правильно - экономно
void setup() {
  Serial.begin(9600);
  Serial.println(F("Это экономит память!"));
}

// ❌ Много массивов
byte array1[100];
byte array2[100];
byte array3[100];

// ✅ Переиспользование
byte temp_array[100];
// использование...
// очистка...
// переиспользование...
```

### Использование битовых полей

```cpp
// ❌ Неправильно - 4 байта на 4 boolean
struct Config1 {
  boolean enabled;
  boolean debug;
  boolean logging;
  boolean alarm;
};

// ✅ Правильно - 1 байт на 4 boolean
struct Config2 {
  boolean enabled : 1;
  boolean debug : 1;
  boolean logging : 1;
  boolean alarm : 1;
};

void setup() {
  Serial.begin(9600);
  
  Serial.print("Config1 размер: ");
  Serial.println(sizeof(Config1));  // 4 байта
  
  Serial.print("Config2 размер: ");
  Serial.println(sizeof(Config2));  // 1 байт
}

void loop() { }
```

---

## Практические примеры

### Пример 1: Сохранение параметров системы

```cpp
#include <EEPROM.h>

const int ADDR_MODE = 0;
const int ADDR_SPEED = 1;
const int ADDR_CHECKSUM = 2;

int current_mode = 0;
int current_speed = 100;

void setup() {
  Serial.begin(9600);
  
  // Загружаем сохранённые параметры
  loadSettings();
  
  Serial.println("=== Система сохранения ===");
  Serial.print("Режим: ");
  Serial.println(current_mode);
  Serial.print("Скорость: ");
  Serial.println(current_speed);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd.startsWith("MODE")) {
      current_mode = cmd.substring(5).toInt();
      saveSettings();
      Serial.print("Режим установлен: ");
      Serial.println(current_mode);
    }
    else if (cmd.startsWith("SPEED")) {
      current_speed = cmd.substring(6).toInt();
      saveSettings();
      Serial.print("Скорость установлена: ");
      Serial.println(current_speed);
    }
    else if (cmd == "STATUS") {
      Serial.print("Режим: ");
      Serial.print(current_mode);
      Serial.print(", Скорость: ");
      Serial.println(current_speed);
    }
  }
}

void saveSettings() {
  EEPROM.write(ADDR_MODE, current_mode);
  EEPROM.write(ADDR_SPEED, current_speed);
  
  // Простая контрольная сумма
  byte checksum = (current_mode + current_speed) % 256;
  EEPROM.write(ADDR_CHECKSUM, checksum);
  
  Serial.println("Параметры сохранены в EEPROM");
}

void loadSettings() {
  byte checksum = (EEPROM.read(ADDR_MODE) + 
                   EEPROM.read(ADDR_SPEED)) % 256;
  
  if (checksum == EEPROM.read(ADDR_CHECKSUM)) {
    current_mode = EEPROM.read(ADDR_MODE);
    current_speed = EEPROM.read(ADDR_SPEED);
    Serial.println("Параметры загружены из EEPROM");
  } else {
    Serial.println("Контрольная сумма ошибка! Используются значения по умолчанию");
  }
}
```

### Пример 2: Счётчик числа включений

```cpp
#include <EEPROM.h>

const int ADDR_POWERUPS = 0;

void setup() {
  Serial.begin(9600);
  
  // Читаем счётчик
  unsigned long powerups = readCounter();
  powerups++;
  
  // Записываем обновленное значение
  writeCounter(powerups);
  
  Serial.print("Включений: ");
  Serial.println(powerups);
  
  Serial.print("Свободная память: ");
  Serial.print(freeRam());
  Serial.println(" байт");
}

void loop() { }

unsigned long readCounter() {
  unsigned long value = 0;
  for (int i = 0; i < 4; i++) {
    value |= ((unsigned long)EEPROM.read(ADDR_POWERUPS + i)) << (8 * i);
  }
  return value;
}

void writeCounter(unsigned long value) {
  for (int i = 0; i < 4; i++) {
    EEPROM.write(ADDR_POWERUPS + i, (value >> (8 * i)) & 0xFF);
  }
}

int freeRam() {
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? 
          (int) &__heap_start : (int) __brkval);
}
```

### Пример 3: Логирование данных в EEPROM

```cpp
#include <EEPROM.h>

const int LOG_START = 0;
const int LOG_SIZE = 100;  // Место для 100 записей
const int RECORD_SIZE = 10;  // Размер одной записи (байт)

int current_record = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("=== Логирование в EEPROM ===");
}

void loop() {
  // Записываем данные
  int temp = 20 + random(-5, 5);
  int humidity = 60 + random(-10, 10);
  
  logData(temp, humidity);
  
  delay(5000);
}

void logData(int temp, int humidity) {
  // Рассчитываем адрес для новой записи
  int addr = LOG_START + (current_record * RECORD_SIZE);
  
  if (addr + RECORD_SIZE <= LOG_START + (LOG_SIZE * RECORD_SIZE)) {
    // Записываем температуру (2 байта)
    EEPROM.write(addr, (temp >> 8) & 0xFF);
    EEPROM.write(addr + 1, temp & 0xFF);
    
    // Записываем влажность (2 байта)
    EEPROM.write(addr + 2, (humidity >> 8) & 0xFF);
    EEPROM.write(addr + 3, humidity & 0xFF);
    
    // Записываем время (4 байта)
    unsigned long time_val = millis();
    for (int i = 0; i < 4; i++) {
      EEPROM.write(addr + 4 + i, (time_val >> (8 * i)) & 0xFF);
    }
    
    current_record++;
    
    Serial.print("Записано: T=");
    Serial.print(temp);
    Serial.print("°C H=");
    Serial.print(humidity);
    Serial.print("% Запись #");
    Serial.println(current_record);
  } else {
    Serial.println("EEPROM переполнен!");
  }
}

void readAllLogs() {
  Serial.println("\n=== Все логи ===");
  
  for (int i = 0; i < current_record; i++) {
    int addr = LOG_START + (i * RECORD_SIZE);
    
    // Читаем температуру
    int temp = (EEPROM.read(addr) << 8) | EEPROM.read(addr + 1);
    
    // Читаем влажность
    int humidity = (EEPROM.read(addr + 2) << 8) | EEPROM.read(addr + 3);
    
    // Читаем время
    unsigned long time_val = 0;
    for (int j = 0; j < 4; j++) {
      time_val |= ((unsigned long)EEPROM.read(addr + 4 + j)) << (8 * j);
    }
    
    Serial.print("Запись ");
    Serial.print(i + 1);
    Serial.print(": T=");
    Serial.print(temp);
    Serial.print("°C H=");
    Serial.print(humidity);
    Serial.print("% Time=");
    Serial.print(time_val);
    Serial.println("ms");
  }
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Понимать разные типы памяти в Arduino

✅ Работать с ограниченной SRAM памятью

✅ Использовать FLASH память для хранения данных

✅ Читать и писать в EEPROM

✅ Сохранять структуры в EEPROM

✅ Оптимизировать использование памяти

✅ Создавать системы с сохранением данных

---

## 🎯 Домашнее задание

1. Создайте программу сохранения параметров в EEPROM

2. Напишите счётчик включений, сохраняемый в EEPROM

3. Создайте систему логирования температуры в EEPROM

4. Напишите функции для работы со структурами в EEPROM

5. Создайте приложение с восстановлением параметров при включении

6. Дополнительно: Реализуйте систему контрольных сумм для защиты данных

---

## 🔗 Полезные ссылки

- 📖 **EEPROM Library:** https://www.arduino.cc/reference/en/libraries/eeprom/
- 📖 **Memory Guide:** https://www.arduino.cc/en/Guide/Memory
- 📖 **PROGMEM:** https://www.arduino.cc/reference/en/language/variables/utilities/progmem/
- 📖 **AVR Memory:** https://www.nongnu.org/avr-libc/user-manual/
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **SRAM** | Static Random Access Memory (оперативная память) |
| **FLASH** | Памь для хранения программы |
| **EEPROM** | Electrically Erasable Programmable ROM |
| **Энергонезависимая** | Память, которая не теряется при отключении питания |
| **Адрес** | Номер ячейки памяти (0-1023 для EEPROM) |
| **PROGMEM** | Макрос для сохранения данных в FLASH |
| **Контрольная сумма** | Сумма для проверки целостности данных |
| **Битовое поле** | Использование отдельных битов для хранения флагов |
| **Цикл записи** | Одна операция записи в EEPROM |
| **Стек (Stack)** | Область памяти для локальных переменных |
| **Куча (Heap)** | Область динамической памяти |

---

**Следующий урок:** 🔧 [Работа с модулями расширения: реле, RGB LED, звуковые модули](../Lesson_17/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
