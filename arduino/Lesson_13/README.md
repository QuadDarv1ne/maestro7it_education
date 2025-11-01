# 📺 Работа с дисплеями: LCD, OLED, 7-сегментные индикаторы

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [LCD дисплеи (16x2, 20x4)](#lcd-дисплеи-16x2-20x4)
3. [OLED дисплеи (128x64, 128x32)](#oled-дисплеи-128x64-128x32)
4. [7-сегментные индикаторы](#7-сегментные-индикаторы)
5. [Подключение дисплеев](#подключение-дисплеев)
6. [Библиотеки для дисплеев](#библиотеки-для-дисплеев)
7. [Работа с LCD](#работа-с-lcd)
8. [Работа с OLED](#работа-с-oled)
9. [Работа с 7-сегментом](#работа-с-7-сегментом)
10. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите различные типы дисплеев для Arduino и научитесь выводить информацию, включая текст, числа и графику. Дисплеи используются для отображения информации от датчиков, статуса системы и взаимодействия с пользователем.

---

## LCD дисплеи (16x2, 20x4)

### Что такое LCD?

LCD (Liquid Crystal Display) — это жидкокристаллический дисплей, который использует параллельный или последовательный интерфейс для передачи данных.

### Характеристики LCD

```
┌─────────────────────────────────────┐
│        LCD Дисплей (16x2)           │
├─────────────────────────────────────┤
│                                     │
│ Разрешение: 16 символов x 2 строки │
│            (или 20x4)               │
│                                     │
│ Тип подключения:                    │
│ ├─ Параллельный (8-бит или 4-бит)  │
│ ├─ I2C (через модуль расширения)    │
│ └─ SPI                              │
│                                     │
│ Питание: 5V                         │
│                                     │
│ Контрастность: регулируемая         │
│                                     │
│ Подсветка: светодиод (LED)          │
│                                     │
│ Цена: дешёвые                       │
│                                     │
└─────────────────────────────────────┘
```

### Типы LCD подключения

```
1. Параллельное подключение (4-бит режим)
   ├─ RS - Register Select
   ├─ E - Enable
   ├─ D4-D7 - Data линии
   ├─ RW - Read/Write (обычно к GND)
   └─ 11 проводов всего

2. I2C подключение (через PCF8574)
   ├─ SDA - Serial Data
   ├─ SCL - Serial Clock
   ├─ 5V - питание
   └─ GND - земля
   └─ Всего 4 провода!

3. SPI подключение
   ├─ MOSI, MISO, SCK
   ├─ CS - Chip Select
   └─ Редко используется
```

---

## OLED дисплеи (128x64, 128x32)

### Что такое OLED?

OLED (Organic Light Emitting Diode) — это органический светоизлучающий диод. Каждый пиксель светит самостоятельно.

### Характеристики OLED

```
┌─────────────────────────────────────┐
│        OLED Дисплей (128x64)        │
├─────────────────────────────────────┤
│                                     │
│ Разрешение: 128x64 пиксели          │
│           (или 128x32)               │
│                                     │
│ Типы:                               │
│ ├─ Монохромные (белые/синие)        │
│ ├─ Цветные (очень редко)            │
│                                     │
│ Интерфейс: I2C или SPI              │
│                                     │
│ Питание: 3.3V или 5V                │
│                                     │
│ Яркость: отличная                   │
│                                     │
│ Контрастность: отличная (100%)      │
│                                     │
│ Видеоугол: 160° (очень хороший)    │
│                                     │
│ Цена: средние                       │
│                                     │
│ Преимущества:                       │
│ ├─ Графика, пиксели                │
│ ├─ Меньше энергии                  │
│ └─ Лучше контрастность             │
│                                     │
└─────────────────────────────────────┘
```

---

## 7-сегментные индикаторы

### Что такое 7-сегментный индикатор?

7-сегментный индикатор — это устройство из семи светодиодных сегментов для отображения цифр и букв.

### Структура 7-сегмента

```
     aaa
    f   b
    ggg
    e   c
     ddd   dp (точка)

Пины:
├─ Общий катод (GND)
├─ a, b, c, d, e, f, g - сегменты
└─ dp - десятичная точка
```

### Коды для отображения цифр

```
Цифра  | a b c d e f g | Hex код
───────┼──────────────┼────────
  0    | 1 1 1 1 1 1 0 | 0x3F
  1    | 0 1 1 0 0 0 0 | 0x06
  2    | 1 1 0 1 1 0 1 | 0x5B
  3    | 1 1 1 1 0 0 1 | 0x4F
  4    | 0 1 1 0 0 1 1 | 0x66
  5    | 1 0 1 1 0 1 1 | 0x6D
  6    | 1 0 1 1 1 1 1 | 0x7D
  7    | 1 1 1 0 0 0 0 | 0x07
  8    | 1 1 1 1 1 1 1 | 0x7F
  9    | 1 1 1 1 0 1 1 | 0x6F
```

---

## Подключение дисплеев

### LCD 16x2 через I2C

```
LCD 16x2 (с модулем I2C):

GND ──→ GND (Arduino)
5V  ──→ 5V (Arduino)
SDA ──→ A4 (Arduino UNO)
SCL ──→ A5 (Arduino UNO)
```

### OLED 128x64 через I2C

```
OLED SSD1306:

GND ──→ GND (Arduino)
VCC ──→ 5V или 3.3V (Arduino)
SDA ──→ A4 (Arduino UNO)
SCL ──→ A5 (Arduino UNO)
```

### 7-сегментный индикатор

```
Общий катод (GCC):

A   ──→ Pin 2
B   ──→ Pin 3
C   ──→ Pin 4
D   ──→ Pin 5
E   ──→ Pin 6
F   ──→ Pin 7
G   ──→ Pin 8
DP  ──→ Pin 9
GND ──→ GND (через резисторы 220Ω)

Примечание:
└─ Нужны резисторы 220Ω для защиты каждого сегмента
```

---

## Библиотеки для дисплеев

### Установка библиотек

```
Для LCD (I2C):
├─ LiquidCrystal_I2C (most common)
├─ Sketch > Include Library > Manage Libraries
└─ Поиск "LiquidCrystal I2C" и установка

Для OLED:
├─ Adafruit SSD1306
├─ Adafruit GFX Library (зависимость)
└─ Sketch > Include Library > Manage Libraries
```

---

## Работа с LCD

### Простой вывод на LCD (I2C)

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Адрес LCD (0x27 или 0x3F), столбцы, строки
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  
  // Инициализация LCD
  lcd.init();
  lcd.backlight();  // Включить подсветку
  
  // Выводим текст
  lcd.print("Hello Arduino!");
}

void loop() {
  // Выводим число
  lcd.setCursor(0, 1);  // Позиция: столбец 0, строка 1
  lcd.print("Time: ");
  lcd.print(millis() / 1000);
  
  delay(1000);
}
```

### Функции работы с LCD

```cpp
lcd.init();                    // Инициализация
lcd.backlight();               // Включить подсветку
lcd.noBacklight();             // Выключить подсветку
lcd.print("text");             // Вывести текст
lcd.println("text");           // Вывести текст с переводом строки
lcd.setCursor(col, row);       // Установить позицию курсора
lcd.clear();                   // Очистить дисплей
lcd.home();                    // Переместить курсор в начало
lcd.cursor();                  // Показать курсор
lcd.noCursor();                // Спрятать курсор
lcd.blink();                   // Мигание курсора
lcd.noBlink();                 // Отключить мигание
lcd.createChar(num, data);     // Создать пользовательский символ
lcd.write(character);          // Вывести символ
```

### Практический пример LCD

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
  
  showWelcome();
}

void loop() {
  displaySensorData();
  delay(1000);
}

void showWelcome() {
  lcd.print("Arduino System");
  lcd.setCursor(0, 1);
  lcd.print("v1.0");
  
  delay(2000);
  lcd.clear();
}

void displaySensorData() {
  int temp = 23;
  int humidity = 65;
  
  // Первая строка
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temp);
  lcd.print("C H:");
  lcd.print(humidity);
  lcd.print("%");
  
  // Вторая строка - время
  lcd.setCursor(0, 1);
  lcd.print("Time: ");
  lcd.print(millis() / 1000);
  lcd.print("s   ");
}
```

---

## Работа с OLED

### Простой вывод на OLED

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED разрешение (128x64)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// I2C адрес (0x3C или 0x3D)
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(9600);
  
  // Инициализация OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("SSD1306 allocation failed");
    while (1);
  }
  
  // Очищаем дисплей
  display.clearDisplay();
  
  // Выводим текст
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Hello OLED!");
  display.println("128x64 Display");
  
  // Отправляем на дисплей
  display.display();
}

void loop() {
  // Обновляем дисплей
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Time:");
  display.println(millis() / 1000);
  display.display();
  
  delay(1000);
}
```

### Функции работы с OLED

```cpp
display.clearDisplay();                    // Очистить дисплей
display.setTextSize(size);                 // Размер текста (1-3)
display.setTextColor(color);               // Цвет (SSD1306_WHITE, SSD1306_BLACK)
display.setCursor(x, y);                   // Позиция
display.println("text");                   // Вывести строку
display.print("text");                     // Вывести текст
display.display();                         // Обновить дисплей
display.drawPixel(x, y, color);            // Рисовать пиксель
display.drawLine(x1, y1, x2, y2, color);  // Рисовать линию
display.drawRect(x, y, w, h, color);      // Рисовать прямоугольник
display.fillRect(x, y, w, h, color);      // Заполненный прямоугольник
display.drawCircle(x, y, r, color);       // Рисовать круг
display.fillCircle(x, y, r, color);       // Заполненный круг
```

### Практический пример OLED

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();
}

void loop() {
  display.clearDisplay();
  
  // Рисуем графику
  drawSystemStatus();
  
  display.display();
  delay(1000);
}

void drawSystemStatus() {
  int temp = 23;
  int humidity = 65;
  float battery = 4.8;
  
  // Заголовок
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("SYSTEM STATUS");
  display.drawLine(0, 10, 128, 10, SSD1306_WHITE);
  
  // Температура
  display.setCursor(0, 15);
  display.print("Temp: ");
  display.print(temp);
  display.println("C");
  
  // Влажность
  display.setCursor(0, 25);
  display.print("Humidity: ");
  display.print(humidity);
  display.println("%");
  
  // Батарея
  display.setCursor(0, 35);
  display.print("Battery: ");
  display.print(battery);
  display.println("V");
  
  // Полоса прогресса
  int progress = map(humidity, 0, 100, 0, 128);
  display.drawRect(0, 50, 128, 14, SSD1306_WHITE);
  display.fillRect(0, 50, progress, 14, SSD1306_WHITE);
}
```

---

## Работа с 7-сегментом

### Управление 7-сегментным индикатором

```cpp
// Коды для цифр (общий катод)
const byte DIGITS[] = {
  0x3F,  // 0
  0x06,  // 1
  0x5B,  // 2
  0x4F,  // 3
  0x66,  // 4
  0x6D,  // 5
  0x7D,  // 6
  0x07,  // 7
  0x7F,  // 8
  0x6F   // 9
};

// Пины сегментов
const int SEGMENTS[] = {2, 3, 4, 5, 6, 7, 8, 9};  // a-g, dp

void setup() {
  // Устанавливаем пины как выводы
  for (int i = 0; i < 8; i++) {
    pinMode(SEGMENTS[i], OUTPUT);
  }
}

void loop() {
  // Выводим числа от 0 до 9
  for (int i = 0; i < 10; i++) {
    displayDigit(i);
    delay(500);
  }
}

void displayDigit(int digit) {
  byte pattern = DIGITS[digit];
  
  // Включаем нужные сегменты
  for (int i = 0; i < 7; i++) {
    int bit = (pattern >> i) & 1;
    digitalWrite(SEGMENTS[i], bit);
  }
}
```

### Многозначный 7-сегментный индикатор

```cpp
const byte DIGITS[] = {
  0x3F, 0x06, 0x5B, 0x4F, 0x66, 
  0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

// Пины двух индикаторов
const int DIGIT1_PINS[] = {2, 3, 4, 5, 6, 7, 8, 9};
const int DIGIT2_PINS[] = {10, 11, 12, 13, A0, A1, A2, A3};

void setup() {
  for (int i = 0; i < 8; i++) {
    pinMode(DIGIT1_PINS[i], OUTPUT);
    pinMode(DIGIT2_PINS[i], OUTPUT);
  }
}

void loop() {
  // Выводим число 42
  displayNumber(42);
}

void displayNumber(int num) {
  int tens = num / 10;
  int ones = num % 10;
  
  displayDigitOnPin1(tens);
  delay(5);
  displayDigitOnPin2(ones);
  delay(5);
}

void displayDigitOnPin1(int digit) {
  byte pattern = DIGITS[digit];
  for (int i = 0; i < 7; i++) {
    int bit = (pattern >> i) & 1;
    digitalWrite(DIGIT1_PINS[i], bit);
  }
}

void displayDigitOnPin2(int digit) {
  byte pattern = DIGITS[digit];
  for (int i = 0; i < 7; i++) {
    int bit = (pattern >> i) & 1;
    digitalWrite(DIGIT2_PINS[i], bit);
  }
}
```

---

## Практические примеры

### Пример 1: Метеостанция на LCD

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int TEMP_SENSOR = A0;
const int HUMIDITY_SENSOR = A1;

void setup() {
  lcd.init();
  lcd.backlight();
  
  lcd.print("Weather Station");
  lcd.setCursor(0, 1);
  lcd.print("v1.0");
  delay(2000);
  lcd.clear();
}

void loop() {
  int temp_raw = analogRead(TEMP_SENSOR);
  int humidity_raw = analogRead(HUMIDITY_SENSOR);
  
  float temperature = map(temp_raw, 0, 1023, -40, 85);
  float humidity = map(humidity_raw, 0, 1023, 0, 100);
  
  // Первая строка - температура
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temperature, 1);
  lcd.print("C ");
  
  // Вторая строка - влажность
  lcd.setCursor(0, 1);
  lcd.print("H:");
  lcd.print(humidity, 0);
  lcd.print("% ");
  
  delay(1000);
}
```

### Пример 2: Часы на OLED

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

unsigned long start_time = 0;

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  start_time = millis();
}

void loop() {
  unsigned long elapsed = millis() - start_time;
  
  int hours = (elapsed / 3600000) % 24;
  int minutes = (elapsed / 60000) % 60;
  int seconds = (elapsed / 1000) % 60;
  
  display.clearDisplay();
  
  // Выводим время большим шрифтом
  display.setTextSize(3);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(20, 20);
  
  if (hours < 10) display.print("0");
  display.print(hours);
  display.print(":");
  if (minutes < 10) display.print("0");
  display.print(minutes);
  display.print(":");
  if (seconds < 10) display.print("0");
  display.print(seconds);
  
  display.display();
  delay(1000);
}
```

### Пример 3: Счётчик на 7-сегменте

```cpp
const byte DIGITS[] = {
  0x3F, 0x06, 0x5B, 0x4F, 0x66,
  0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

const int SEG_PINS[] = {2, 3, 4, 5, 6, 7, 8, 9};

int counter = 0;

void setup() {
  for (int i = 0; i < 8; i++) {
    pinMode(SEG_PINS[i], OUTPUT);
  }
}

void loop() {
  displayDigit(counter % 10);
  
  delay(1000);
  counter++;
  
  if (counter > 9) {
    counter = 0;
  }
}

void displayDigit(int digit) {
  byte pattern = DIGITS[digit];
  
  for (int i = 0; i < 7; i++) {
    int bit = (pattern >> i) & 1;
    digitalWrite(SEG_PINS[i], bit);
  }
}
```

### Пример 4: Система мониторинга (LCD + датчики)

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int TEMP = A0;
const int LIGHT = A1;
const int BUTTON = 2;

int display_mode = 0;

void setup() {
  lcd.init();
  lcd.backlight();
  
  pinMode(BUTTON, INPUT_PULLUP);
}

void loop() {
  // Проверяем кнопку для смены режима
  if (digitalRead(BUTTON) == LOW) {
    display_mode = (display_mode + 1) % 3;
    delay(300);
  }
  
  lcd.clear();
  
  switch (display_mode) {
    case 0:
      showTemperature();
      break;
    case 1:
      showLight();
      break;
    case 2:
      showBoth();
      break;
  }
  
  delay(500);
}

void showTemperature() {
  int temp_raw = analogRead(TEMP);
  float temp = map(temp_raw, 0, 1023, -40, 85);
  
  lcd.setCursor(0, 0);
  lcd.print("Temperature");
  lcd.setCursor(0, 1);
  lcd.print(temp, 1);
  lcd.print("C");
}

void showLight() {
  int light = analogRead(LIGHT);
  
  lcd.setCursor(0, 0);
  lcd.print("Light Level");
  lcd.setCursor(0, 1);
  lcd.print(light);
  lcd.print("/1023");
}

void showBoth() {
  int temp_raw = analogRead(TEMP);
  int light = analogRead(LIGHT);
  float temp = map(temp_raw, 0, 1023, -40, 85);
  
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(temp, 0);
  lcd.print("C L:");
  lcd.print(map(light, 0, 1023, 0, 100));
  lcd.print("%");
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Работать с LCD дисплеями (16x2, 20x4)

✅ Подключать LCD через I2C

✅ Использовать библиотеку LiquidCrystal_I2C

✅ Работать с OLED дисплеями (128x64)

✅ Рисовать графику на OLED

✅ Использовать 7-сегментные индикаторы

✅ Выводить текст и числа на различные дисплеи

✅ Создавать информационные системы

---

## 🎯 Домашнее задание

1. Напишите программу вывода информации датчика на LCD дисплей

2. Создайте приложение часов на OLED дисплее

3. Реализуйте счётчик нажатий на 7-сегментном индикаторе

4. Напишите программу метеостанции на LCD (температура, влажность, давление)

5. Создайте систему меню на LCD (переключение между экранами)

6. Дополнительно: Создайте графический эквалайзер на OLED

---

## 🔗 Полезные ссылки

- 📖 **LiquidCrystal_I2C:** https://github.com/johnwasser/LiquidCrystal_I2C
- 📖 **Adafruit SSD1306:** https://github.com/adafruit/Adafruit_SSD1306
- 📖 **Adafruit GFX:** https://github.com/adafruit/Adafruit-GFX-Library
- 📖 **LCD Guide:** https://www.arduino.cc/en/Tutorial/LiquidCrystal
- 📖 **OLED Guide:** https://randomnerdtutorials.com/arduino-oled-display-tutorial/
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **LCD** | Liquid Crystal Display (жидкокристаллический дисплей) |
| **OLED** | Organic Light Emitting Diode (органический светодиод) |
| **Пиксель** | Минимальный элемент изображения |
| **Резолюция** | Разрешение экрана (количество пикселей) |
| **Контрастность** | Разница между яркостью светлых и тёмных элементов |
| **Подсветка** | Источник света за дисплеем (LCD) |
| **I2C модуль** | PCF8574 - расширитель портов для LCD |
| **Сегмент** | Отдельная часть 7-сегментного индикатора |
| **Общий катод** | Конфигурация 7-сегмента с общим GND |
| **Общий анод** | Конфигурация 7-сегмента с общим 5V |
| **Курсор** | Указатель позиции на дисплее |
| **Символ** | Буква, цифра или специальный знак |
| **Графика** | Изображения, линии, фигуры (OLED) |

---

**Следующий урок:** ⏱️ [Встроенные функции Arduino: millis(), delay(), micros()](../Lesson_14/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
