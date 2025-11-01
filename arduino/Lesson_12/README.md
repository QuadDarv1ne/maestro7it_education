# 🌐 Протоколы коммуникации: I2C, SPI, UART

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [UART (Serial)](#uart-serial)
3. [I2C (TWI)](#i2c-twi)
4. [SPI](#spi)
5. [Сравнение протоколов](#сравнение-протоколов)
6. [Работа с I2C](#работа-с-i2c)
7. [Работа с SPI](#работа-с-spi)
8. [Диагностика проблем](#диагностика-проблем)
9. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите три основных протокола коммуникации для Arduino: UART (Serial), I2C и SPI. Эти протоколы используются для обмена данными между Arduino и различными датчиками, модулями и другими устройствами.

---

## UART (Serial)

### Что такое UART?

UART (Universal Asynchronous Receiver/Transmitter) — это протокол последовательной асинхронной передачи данных.

### Характеристики UART

```
┌─────────────────────────────────────┐
│        UART (Serial)                │
├─────────────────────────────────────┤
│                                     │
│ Количество проводов: 2-3            │
│ ├─ TX (передача)                   │
│ ├─ RX (приём)                      │
│ └─ GND (земля)                     │
│                                     │
│ Скорость: 9600, 115200, 230400 bps  │
│                                     │
│ Асинхронный: нет синхросигнала      │
│                                     │
│ Расстояние: до 15 метров            │
│                                     │
│ Использование: отладка, USB         │
│                                     │
└─────────────────────────────────────┘
```

### Примеры UART (уже изучены)

```cpp
void setup() {
  Serial.begin(9600);  // Инициализация UART
}

void loop() {
  Serial.print("Data: ");
  Serial.println(analogRead(A0));
  delay(1000);
}
```

---

## I2C (TWI)

### Что такое I2C?

I2C (Inter-Integrated Circuit) — это синхронный двухпроводный протокол коммуникации для связи нескольких устройств.

### Характеристики I2C

```
┌─────────────────────────────────────┐
│        I2C (TWI)                    │
├─────────────────────────────────────┤
│                                     │
│ Количество проводов: 2              │
│ ├─ SDA (Serial Data)               │
│ └─ SCL (Serial Clock)              │
│                                     │
│ Скорость: 100 kHz (Standard)        │
│          400 kHz (Fast)             │
│          1 MHz (Fast Plus)          │
│                                     │
│ Синхронный: есть часовой сигнал    │
│                                     │
│ Количество устройств: до 127        │
│                                     │
│ Расстояние: до 1 метра              │
│                                     │
│ Использование: датчики, модули     │
│                                     │
└─────────────────────────────────────┘
```

### Пины I2C на Arduino UNO

```
Arduino UNO:
├─ SDA: A4 (Pin 18)
└─ SCL: A5 (Pin 19)

Arduino Mega:
├─ SDA: 20
└─ SCL: 21

Arduino Leonardo:
├─ SDA: 2
└─ SCL: 3
```

### Схема подключения I2C

```
Arduino UNO:          I2C устройство:

A4 (SDA) ─────────→ SDA
A5 (SCL) ─────────→ SCL
GND ────────────→ GND

Примечание:
└─ Часто нужны pull-up резисторы 4.7kΩ
  между SDA и 5V
  между SCL и 5V
```

### Адресация в I2C

```
Каждое I2C устройство имеет адрес (7 бит):
├─ 0x00 - 0x7F (0 - 127 в десятичной)
├─ Некоторые адреса зарезервированы
└─ Прибор использует свой уникальный адрес

Типичные адреса:
├─ DS3231 (RTC): 0x68
├─ MPU6050 (Gyro): 0x68 или 0x69
├─ BMP280 (Pressure): 0x76 или 0x77
├─ DHT12 (Temp/Humidity): 0x5C
└─ LCD1602 (Display): 0x27 или 0x3F
```

### Работа с I2C

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Wire.begin();  // Инициализация I2C как Master
}

void loop() {
  // Начинаем передачу к устройству с адресом 0x68
  Wire.beginTransmission(0x68);
  
  // Отправляем адрес регистра
  Wire.write(0x3F);
  
  // Завершаем передачу
  Wire.endTransmission();
  
  // Запрашиваем 1 байт данных
  Wire.requestFrom(0x68, 1);
  
  // Проверяем, есть ли данные
  if (Wire.available()) {
    byte data = Wire.read();
    Serial.println(data);
  }
  
  delay(1000);
}
```

---

## SPI

### Что такое SPI?

SPI (Serial Peripheral Interface) — это синхронный четырёхпроводный протокол высокоскоростной коммуникации.

### Характеристики SPI

```
┌─────────────────────────────────────┐
│        SPI                          │
├─────────────────────────────────────┤
│                                     │
│ Количество проводов: 4 (минимум)    │
│ ├─ MOSI (Master Out Slave In)      │
│ ├─ MISO (Master In Slave Out)      │
│ ├─ SCK (Serial Clock)              │
│ └─ SS/CS (Chip Select)             │
│                                     │
│ Скорость: от 100 kHz до 10+ MHz     │
│                                     │
│ Синхронный: есть часовой сигнал    │
│                                     │
│ Количество устройств: теоретически  │
│          бесконечное (каждому свой CS)
│                                     │
│ Расстояние: до 1 метра              │
│                                     │
│ Использование: SD карты, датчики   │
│                                     │
└─────────────────────────────────────┘
```

### Пины SPI на Arduino UNO

```
Arduino UNO:
├─ MOSI: 11 (Pin 11)
├─ MISO: 12 (Pin 12)
├─ SCK:  13 (Pin 13)
└─ SS:   10 (Pin 10) - обычно для первого устройства

Arduino Mega:
├─ MOSI: 51
├─ MISO: 50
├─ SCK:  52
└─ SS:   53
```

### Схема подключения SPI

```
Arduino UNO:          SPI устройство:

11 (MOSI) ────────→ MOSI (DIN)
12 (MISO) ←──────── MISO (DOUT)
13 (SCK)  ────────→ SCK (CLK)
10 (SS)   ────────→ CS (Chip Select)
GND ──────────────→ GND
```

### Работа с SPI

```cpp
#include <SPI.h>

const int CS_PIN = 10;

void setup() {
  Serial.begin(9600);
  
  SPI.begin();  // Инициализация SPI
  SPI.setClockDivider(SPI_CLOCK_DIV4);  // Установка скорости
  SPI.setDataMode(SPI_MODE0);  // Режим работы
  
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);  // CS неактивна (HIGH)
}

void loop() {
  // Выбираем устройство (CS LOW)
  digitalWrite(CS_PIN, LOW);
  
  // Отправляем и получаем байт
  byte response = SPI.transfer(0xAA);  // Отправляем 0xAA
  
  // Отпускаем устройство (CS HIGH)
  digitalWrite(CS_PIN, HIGH);
  
  Serial.println(response, HEX);
  
  delay(1000);
}
```

---

## Сравнение протоколов

### Таблица сравнения

```
┌──────────────┬────────────┬────────────┬────────────┐
│ Параметр     │   UART     │    I2C     │    SPI     │
├──────────────┼────────────┼────────────┼────────────┤
│ Проводов     │ 2-3        │ 2          │ 4          │
│ Скорость     │ 115k бит/с │ 400k бит/с │ 10+ МБит/с │
│ Синхронный   │ Нет        │ Да         │ Да         │
│ Расстояние   │ 15м        │ 1м         │ 1м         │
│ Устройств    │ 1-2        │ До 127     │ Много      │
│ Сложность    │ Простая    │ Средняя    │ Сложная    │
│ Резистор     │ -          │ 4.7kΩ      │ -          │
└──────────────┴────────────┴────────────┴────────────┘
```

### Когда использовать

```
UART (Serial):
├─ Отладка программы
├─ Связь с компьютером через USB
├─ Простые проекты с одним устройством
└─ Когда нужна простота

I2C:
├─ Несколько датчиков на одной шине
├─ Когда провода ограничены (только 2)
├─ Датчики температуры, влажности, GPS
└─ Дисплеи LCD/OLED

SPI:
├─ Высокая скорость передачи
├─ SD карты, микросхемы памяти
├─ Беспроводные модули
└─ Когда нужна максимальная скорость
```

---

## Работа с I2C

### I2C Scanner (поиск устройств)

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  Serial.println("\nI2C Scanner");
  Serial.println("Scanning...\n");
  
  scanI2C();
}

void loop() {
  delay(5000);
  scanI2C();
}

void scanI2C() {
  int found = 0;
  
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      found++;
    }
  }
  
  if (found == 0) {
    Serial.println("No I2C devices found\n");
  } else {
    Serial.print("Total: ");
    Serial.print(found);
    Serial.println(" device(s)\n");
  }
}
```

### Работа с DS3231 (RTC модуль)

```cpp
#include <Wire.h>

const int DS3231_ADDRESS = 0x68;

struct Time {
  byte seconds;
  byte minutes;
  byte hours;
  byte day;
  byte month;
  byte year;
};

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  Serial.println("DS3231 RTC Module Test");
}

void loop() {
  Time t = readTime();
  
  Serial.print("20");
  Serial.print(t.year);
  Serial.print("-");
  printTwoDigits(t.month);
  Serial.print("-");
  printTwoDigits(t.day);
  Serial.print(" ");
  printTwoDigits(t.hours);
  Serial.print(":");
  printTwoDigits(t.minutes);
  Serial.print(":");
  printTwoDigits(t.seconds);
  Serial.println();
  
  delay(1000);
}

Time readTime() {
  Wire.beginTransmission(DS3231_ADDRESS);
  Wire.write(0x00);  // Регистр времени
  Wire.endTransmission();
  
  Wire.requestFrom(DS3231_ADDRESS, 7);
  
  Time t;
  t.seconds = bcdToDec(Wire.read());
  t.minutes = bcdToDec(Wire.read());
  t.hours = bcdToDec(Wire.read());
  Wire.read();  // День недели (пропускаем)
  t.day = bcdToDec(Wire.read());
  t.month = bcdToDec(Wire.read());
  t.year = bcdToDec(Wire.read());
  
  return t;
}

byte bcdToDec(byte val) {
  return (val / 16 * 10) + (val % 16);
}

void printTwoDigits(byte val) {
  if (val < 10) Serial.print("0");
  Serial.print(val);
}
```

---

## Работа с SPI

### Работа с SD картой

```cpp
#include <SPI.h>
#include <SD.h>

const int CS_PIN = 10;
File myFile;

void setup() {
  Serial.begin(9600);
  
  Serial.println("Initializing SD card...");
  
  if (!SD.begin(CS_PIN)) {
    Serial.println("initialization failed!");
    return;
  }
  
  Serial.println("initialization done.");
  
  // Создаём или открываем файл
  myFile = SD.open("test.txt", FILE_WRITE);
  
  if (myFile) {
    Serial.println("Writing to test.txt...");
    
    // Записываем данные
    myFile.println("This is a test");
    myFile.println("123,456,789");
    
    myFile.close();
    Serial.println("done.");
  } else {
    Serial.println("error opening test.txt");
  }
  
  // Читаем файл
  myFile = SD.open("test.txt");
  if (myFile) {
    Serial.println("test.txt:");
    
    while (myFile.available()) {
      Serial.write(myFile.read());
    }
    
    myFile.close();
  } else {
    Serial.println("error opening test.txt");
  }
}

void loop() {
  // ничего
}
```

### Работа с EEPROM через SPI

```cpp
#include <SPI.h>

const int CS_PIN = 10;
const int EEPROM_READ = 0x03;
const int EEPROM_WRITE = 0x02;

void setup() {
  Serial.begin(9600);
  
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV4);
  
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  
  Serial.println("SPI EEPROM Test");
}

void loop() {
  // Записываем данные
  writeEEPROM(0x00, 0x42);  // Адрес 0x00, значение 0x42
  delay(100);
  
  // Читаем данные
  byte data = readEEPROM(0x00);
  
  Serial.print("Data read: 0x");
  Serial.println(data, HEX);
  
  delay(5000);
}

byte readEEPROM(int address) {
  digitalWrite(CS_PIN, LOW);
  
  SPI.transfer(EEPROM_READ);
  SPI.transfer((address >> 8) & 0xFF);
  SPI.transfer(address & 0xFF);
  
  byte data = SPI.transfer(0x00);
  
  digitalWrite(CS_PIN, HIGH);
  
  return data;
}

void writeEEPROM(int address, byte data) {
  digitalWrite(CS_PIN, LOW);
  
  SPI.transfer(EEPROM_WRITE);
  SPI.transfer((address >> 8) & 0xFF);
  SPI.transfer(address & 0xFF);
  SPI.transfer(data);
  
  digitalWrite(CS_PIN, HIGH);
}
```

---

## Диагностика проблем

### Проблема 1: I2C устройство не найдено

```cpp
// Диагностика I2C проблем
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  Serial.println("=== I2C Diagnostics ===");
  
  // Проверяем напряжение
  Serial.println("\nChecking voltage...");
  Serial.print("Voltage: ");
  Serial.print(analogRead(A0) * 5.0 / 1023.0);
  Serial.println("V");
  
  // Проверяем SDA и SCL линии
  Serial.println("\nChecking I2C lines...");
  pinMode(A4, INPUT);  // SDA
  pinMode(A5, INPUT);  // SCL
  
  Serial.print("SDA level: ");
  Serial.println(digitalRead(A4) ? "HIGH" : "LOW");
  Serial.print("SCL level: ");
  Serial.println(digitalRead(A5) ? "HIGH" : "LOW");
  
  // Сканируем адреса
  Serial.println("\nScanning addresses...");
  scanI2C();
}

void loop() { }

void scanI2C() {
  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();
    
    Serial.print("Address 0x");
    if (address < 16) Serial.print("0");
    Serial.print(address, HEX);
    Serial.print(": ");
    
    switch (error) {
      case 0:
        Serial.println("Device found");
        break;
      case 1:
        Serial.println("Data too long");
        break;
      case 2:
        Serial.println("NACK on address");
        break;
      case 3:
        Serial.println("NACK on data");
        break;
      case 4:
        Serial.println("Other error");
        break;
      default:
        Serial.println("Unknown error");
    }
  }
}
```

### Проблема 2: SPI не работает

```cpp
#include <SPI.h>

void setup() {
  Serial.begin(9600);
  
  Serial.println("=== SPI Diagnostics ===");
  
  // Проверяем пины
  Serial.println("Checking SPI pins...");
  Serial.print("MOSI (11): ");
  Serial.println("OK");
  
  Serial.print("MISO (12): ");
  Serial.println("OK");
  
  Serial.print("SCK (13): ");
  Serial.println("OK");
  
  // Инициализируем SPI
  SPI.begin();
  Serial.println("SPI initialized");
  
  // Тестируем передачу
  Serial.println("Testing SPI transfer...");
  byte response = SPI.transfer(0x55);
  Serial.print("Sent: 0x55, Received: 0x");
  Serial.println(response, HEX);
}

void loop() { }
```

---

## Практические примеры

### Пример 1: Система с I2C датчиком температуры (BMP280)

```cpp
#include <Wire.h>

const int BMP280_ADDRESS = 0x76;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  initBMP280();
  Serial.println("BMP280 initialized");
}

void loop() {
  float temperature = readTemperature();
  float pressure = readPressure();
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C | Pressure: ");
  Serial.print(pressure);
  Serial.println(" hPa");
  
  delay(2000);
}

void initBMP280() {
  Wire.beginTransmission(BMP280_ADDRESS);
  Wire.write(0xF4);  // Control register
  Wire.write(0x27);  // Initialization value
  Wire.endTransmission();
}

float readTemperature() {
  Wire.beginTransmission(BMP280_ADDRESS);
  Wire.write(0xFA);  // Temperature MSB register
  Wire.endTransmission();
  
  Wire.requestFrom(BMP280_ADDRESS, 3);
  
  int t_raw = (Wire.read() << 12) | (Wire.read() << 4) | (Wire.read() >> 4);
  
  // Упрощённый расчёт
  float temperature = t_raw / 5120.0 - 50.0;
  
  return temperature;
}

float readPressure() {
  Wire.beginTransmission(BMP280_ADDRESS);
  Wire.write(0xF7);  // Pressure MSB register
  Wire.endTransmission();
  
  Wire.requestFrom(BMP280_ADDRESS, 3);
  
  int p_raw = (Wire.read() << 12) | (Wire.read() << 4) | (Wire.read() >> 4);
  
  // Упрощённый расчёт
  float pressure = p_raw / 256.0 / 100.0;
  
  return pressure;
}
```

### Пример 2: Система с множественными I2C устройствами

```cpp
#include <Wire.h>

// I2C адреса
const int RTC_ADDRESS = 0x68;      // DS3231
const int TEMP_ADDRESS = 0x48;     // LM75
const int LCD_ADDRESS = 0x27;      // LCD1602

void setup() {
  Serial.begin(9600);
  Wire.begin();
  
  Serial.println("Multi-device I2C system");
}

void loop() {
  // Читаем время
  byte hour = readRTCRegister(0x02);
  byte minute = readRTCRegister(0x01);
  
  // Читаем температуру
  float temp = readTemperature();
  
  // Выводим
  Serial.print("Time: ");
  Serial.print(hour);
  Serial.print(":");
  Serial.print(minute);
  Serial.print(" | Temp: ");
  Serial.println(temp);
  
  delay(2000);
}

byte readRTCRegister(byte reg) {
  Wire.beginTransmission(RTC_ADDRESS);
  Wire.write(reg);
  Wire.endTransmission();
  
  Wire.requestFrom(RTC_ADDRESS, 1);
  return Wire.read();
}

float readTemperature() {
  Wire.beginTransmission(TEMP_ADDRESS);
  Wire.write(0x00);  // Temperature register
  Wire.endTransmission();
  
  Wire.requestFrom(TEMP_ADDRESS, 2);
  
  byte temp_int = Wire.read();
  byte temp_frac = Wire.read();
  
  float temperature = temp_int + (temp_frac >> 4) * 0.0625;
  
  return temperature;
}
```

### Пример 3: Логирование на SD карту (SPI)

```cpp
#include <SPI.h>
#include <SD.h>

const int CS_PIN = 10;
const int TEMP_SENSOR = A0;

File logFile;

void setup() {
  Serial.begin(9600);
  
  if (!SD.begin(CS_PIN)) {
    Serial.println("SD init failed");
    return;
  }
  
  Serial.println("SD card initialized");
  
  // Открываем/создаём файл логирования
  logFile = SD.open("log.csv", FILE_WRITE);
  
  if (logFile) {
    logFile.println("Time(ms),Temperature(C)");
    logFile.close();
    Serial.println("Log file created");
  }
}

void loop() {
  float temp = analogRead(TEMP_SENSOR) * (5.0 / 1023.0) * 100.0;
  
  logFile = SD.open("log.csv", FILE_WRITE);
  
  if (logFile) {
    logFile.print(millis());
    logFile.print(",");
    logFile.println(temp);
    logFile.close();
    
    Serial.print(millis());
    Serial.print(" ms: ");
    Serial.print(temp);
    Serial.println("°C");
  } else {
    Serial.println("Error opening log file");
  }
  
  delay(5000);
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Понимать UART (Serial) протокол

✅ Работать с I2C протоколом

✅ Работать с SPI протоколом

✅ Сравнивать протоколы и выбирать нужный

✅ Сканировать I2C устройства

✅ Работать с I2C датчиками

✅ Использовать SPI для SD карт

✅ Диагностировать проблемы коммуникации

---

## 🎯 Домашнее задание

1. Напишите I2C scanner и найдите все подключённые устройства

2. Создайте программу чтения данных с I2C датчика (DS3231, BMP280 или другой)

3. Напишите программу логирования на SD карту через SPI

4. Создайте систему, читающую данные с нескольких I2C устройств одновременно

5. Напишите программу сравнения скорости UART, I2C и SPI

6. Дополнительно: Создайте систему с множественными SPI устройствами

---

## 🔗 Полезные ссылки

- 📖 **Wire Library:** https://www.arduino.cc/reference/en/language/functions/communication/wire/
- 📖 **SPI Library:** https://www.arduino.cc/reference/en/language/functions/communication/spi/
- 📖 **SD Library:** https://www.arduino.cc/reference/en/libraries/sd/
- 📖 **I2C Protocol:** https://en.wikipedia.org/wiki/I%C2%B2C
- 📖 **SPI Protocol:** https://en.wikipedia.org/wiki/Serial_Peripheral_Interface
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **UART** | Universal Asynchronous Receiver/Transmitter |
| **I2C** | Inter-Integrated Circuit (TWI - Two Wire Interface) |
| **SPI** | Serial Peripheral Interface |
| **Асинхронный** | Передача без синхросигнала |
| **Синхронный** | Передача с синхросигналом (Clock) |
| **SDA** | Serial Data (I2C) |
| **SCL** | Serial Clock (I2C) |
| **MOSI** | Master Out Slave In (SPI) |
| **MISO** | Master In Slave Out (SPI) |
| **SCK** | Serial Clock (SPI) |
| **CS/SS** | Chip Select (SPI) |
| **Master** | Устройство, управляющее коммуникацией |
| **Slave** | Устройство, управляемое master-ом |
| **Адрес** | Уникальный идентификатор устройства (I2C) |
| **Baud Rate** | Скорость передачи (бит в секунду) |

---

**Следующий урок:** 📺 [Работа с дисплеями: LCD, OLED, 7-сегментные индикаторы](../Lesson_13/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025