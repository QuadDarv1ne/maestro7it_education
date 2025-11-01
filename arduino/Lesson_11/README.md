# 🔄 Работа с серво-моторами и управление движением

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Что такое серво-мотор?](#что-такое-серво-мотор)
3. [Типы серво-моторов](#типы-серво-моторов)
4. [Принцип работы PWM](#принцип-работы-pwm)
5. [Подключение серво-мотора](#подключение-серво-мотора)
6. [Библиотека Servo](#библиотека-servo)
7. [Управление серво-мотором](#управление-серво-мотором)
8. [Несколько серво-моторов](#несколько-серво-моторов)
9. [Работа с DC моторами](#работа-с-dc-моторами)
10. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите работу с серво-моторами и другими двигателями. Серво-моторы используются для точного управления углом поворота, а DC моторы — для управления скоростью вращения.

---

## Что такое серво-мотор?

Серво-мотор — это специальный электромотор с встроенной системой управления, позволяющей точно устанавливать угол поворота вала.

### Основные характеристики

```
┌─────────────────────────────────────┐
│   СЕРВО-МОТОР (SG90)                │
├─────────────────────────────────────┤
│                                     │
│ Угол поворота: 0-180 градусов       │
│ Скорость: ~60° за 0.1 секунду       │
│ Момент (крутящий момент): 2.5 кг·см │
│ Питание: 4.8-6V                    │
│ Управление: PWM сигнал             │
│                                     │
└─────────────────────────────────────┘
```

### Устройство серво-мотора

```
┌──────────────────────────┐
│   Серво-мотор SG90       │
├──────────────────────────┤
│                          │
│  ┌────────────────────┐  │
│  │  DC Мотор          │  │
│  │  (движение)        │  │
│  └────────────────────┘  │
│           ↓              │
│  ┌────────────────────┐  │
│  │  Редуктор          │  │
│  │  (замедление)      │  │
│  └────────────────────┘  │
│           ↓              │
│  ┌────────────────────┐  │
│  │  Датчик положения  │  │
│  │  (обратная связь)  │  │
│  └────────────────────┘  │
│           ↓              │
│  ┌────────────────────┐  │
│  │  Контроллер        │  │
│  │  (электроника)     │  │
│  └────────────────────┘  │
│                          │
└──────────────────────────┘
```

---

## Типы серво-моторов

### По диапазону поворота

```
Стандартный серво (0-180°)
├─ SG90, MG996R
├─ Диапазон: 0-180 градусов
└─ Самый распространённый

Микро-серво (0-180°)
├─ Tiny, Micro servo
├─ Маленький размер
└─ Слабый момент

Цифровой серво
├─ Более точное управление
├─ Быстрее работает
└─ Дороже

Бесконечный серво (Continuous)
├─ Вращается полностью (360°)
├─ Управление скоростью и направлением
└─ Используется как обычный мотор
```

### По характеристикам

```
SG90 (Популярный, дешёвый)
├─ Напряжение: 4.8-6V
├─ Момент: 2.5 кг·см
├─ Скорость: 0.1s / 60°
└─ Цена: низкая

MG996R (Мощный, быстрый)
├─ Напряжение: 4.8-7.2V
├─ Момент: 11 кг·см
├─ Скорость: 0.2s / 60°
└─ Цена: средняя

LTD-311HV (Профессиональный)
├─ Напряжение: 7.4-11V
├─ Момент: 30+ кг·см
├─ Скорость: быстрый
└─ Цена: высокая
```

---

## Принцип работы PWM

### Что такое PWM?

PWM (Pulse Width Modulation) — это способ управления серво-мотором через модуляцию ширины импульса.

```
PWM сигнал (на примере серво):

Период: 20 миллисекунд (50 Гц)

┌─────────────────────────────┐
│ Угол 0° (полностью влево)   │
├─────────────────────────────┤
│ ┌──┐                        │
│ │  │                        │
└─┘  └────────────────────────┘
│  │
Импульс 1мс

┌─────────────────────────────┐
│ Угол 90° (центр)            │
├─────────────────────────────┤
│ ┌────┐                      │
│ │    │                      │
└─┘    └──────────────────────┘
│    │
Импульс 1.5мс

┌─────────────────────────────┐
│ Угол 180° (полностью вправо)│
├─────────────────────────────┤
│ ┌──────┐                    │
│ │      │                    │
└─┘      └────────────────────┘
│      │
Импульс 2мс
```

### Соответствие импульса углу

```
Длительность импульса    →    Угол поворота

1.0 мс    →  0°    (полностью влево)
1.25 мс   →  45°   (влево от центра)
1.5 мс    →  90°   (центр)
1.75 мс   →  135°  (вправо от центра)
2.0 мс    →  180°  (полностью вправо)
```

---

## Подключение серво-мотора

### Схема подключения

```
Серво-мотор:         Arduino UNO:

[Коричневый] GND  ──→  GND
[Красный]    +5V  ──→  5V (или внешнее питание)
[Жёлтый]     PWM  ──→  Pin 9 (или другой PWM пин)

Важно: 
└─ Пины PWM на Arduino: 3, 5, 6, 9, 10, 11
└─ Можно использовать только эти пины для Servo!
```

### Важные замечания

```
⚠️ ПИТАНИЕ
├─ Используйте отдельное питание для сервомотора!
├─ USB от Arduino может быть недостаточно
└─ Используйте блок питания 5V, 2A+

⚠️ ПРОВОДА
├─ Используйте качественные провода
├─ Проверяйте полярность (красный - +5V, коричневый - GND)
└─ Длинные провода могут вызвать помехи

⚠️ КОНТРОЛИРУЙТЕ
├─ Проверяйте напряжение питания
├─ Не перегружайте сервомотор
└─ Используйте конденсатор 100µF между питанием и GND
```

---

## Библиотека Servo

### Установка библиотеки

Servo библиотека встроена в Arduino IDE, не нужно устанавливать!

```cpp
#include <Servo.h>

Servo myservo;  // Создаём объект сервомотора
```

### Основные функции

```cpp
Servo servo;

// Инициализация
servo.attach(pin);           // Подключить к пину (3, 5, 6, 9, 10, 11)

// Управление
servo.write(angle);          // Установить угол (0-180)
servo.read();                // Получить текущий угол

// Отключение
servo.detach();              // Отключить сервомотор

// Дополнительно
servo.writeMicroseconds(us); // Написать в микросекундах (1000-2000)
```

---

## Управление серво-мотором

### Простое управление

```cpp
#include <Servo.h>

Servo myservo;
int angle = 90;  // Начальный угол

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // Подключаем к пину 9
  myservo.write(angle);  // Устанавливаем начальный угол
  Serial.println("Сервомотор инициализирован");
}

void loop() {
  // Вращаем от 0 до 180 градусов
  for (angle = 0; angle <= 180; angle++) {
    myservo.write(angle);
    Serial.print("Угол: ");
    Serial.println(angle);
    delay(15);  // Небольшая задержка для плавного движения
  }
  
  delay(1000);
  
  // Вращаем обратно от 180 к 0
  for (angle = 180; angle >= 0; angle--) {
    myservo.write(angle);
    Serial.print("Угол: ");
    Serial.println(angle);
    delay(15);
  }
  
  delay(1000);
}
```

### Управление с кнопками

```cpp
#include <Servo.h>

Servo myservo;
const int BUTTON_LEFT = 2;
const int BUTTON_RIGHT = 3;
const int BUTTON_CENTER = 4;

int angle = 90;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  
  pinMode(BUTTON_LEFT, INPUT_PULLUP);
  pinMode(BUTTON_RIGHT, INPUT_PULLUP);
  pinMode(BUTTON_CENTER, INPUT_PULLUP);
  
  myservo.write(angle);
}

void loop() {
  // Кнопка влево
  if (digitalRead(BUTTON_LEFT) == LOW) {
    angle = max(0, angle - 10);  // Уменьшаем на 10, но не ниже 0
    myservo.write(angle);
    Serial.print("Влево. Угол: ");
    Serial.println(angle);
    delay(300);  // Защита от дребезга
  }
  
  // Кнопка вправо
  if (digitalRead(BUTTON_RIGHT) == LOW) {
    angle = min(180, angle + 10);  // Увеличиваем на 10, но не выше 180
    myservo.write(angle);
    Serial.print("Вправо. Угол: ");
    Serial.println(angle);
    delay(300);
  }
  
  // Кнопка центр
  if (digitalRead(BUTTON_CENTER) == LOW) {
    angle = 90;
    myservo.write(angle);
    Serial.println("Центр. Угол: 90");
    delay(300);
  }
  
  delay(50);
}
```

### Управление через Serial

```cpp
#include <Servo.h>

Servo myservo;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  myservo.write(90);
  
  Serial.println("=== УПРАВЛЕНИЕ СЕРВОМОТОРОМ ===");
  Serial.println("Введите угол (0-180) или команду:");
  Serial.println("LEFT - 0°, CENTER - 90°, RIGHT - 180°");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    input.toUpperCase();
    
    if (input == "LEFT") {
      myservo.write(0);
      Serial.println("Угол: 0°");
    }
    else if (input == "CENTER") {
      myservo.write(90);
      Serial.println("Угол: 90°");
    }
    else if (input == "RIGHT") {
      myservo.write(180);
      Serial.println("Угол: 180°");
    }
    else {
      int angle = input.toInt();
      if (angle >= 0 && angle <= 180) {
        myservo.write(angle);
        Serial.print("Угол: ");
        Serial.println(angle);
      } else {
        Serial.println("Ошибка! Угол должен быть 0-180");
      }
    }
  }
}
```

---

## Несколько серво-моторов

### Управление двумя сервомоторами

```cpp
#include <Servo.h>

Servo servo1;  // Горизонтальное движение
Servo servo2;  // Вертикальное движение

int angle_h = 90;  // Горизонтальный угол
int angle_v = 90;  // Вертикальный угол

void setup() {
  Serial.begin(9600);
  
  servo1.attach(9);   // Горизонтальный на пин 9
  servo2.attach(10);  // Вертикальный на пин 10
  
  servo1.write(angle_h);
  servo2.write(angle_v);
  
  Serial.println("Два сервомотора инициализированы");
}

void loop() {
  // Движение - рисуем квадрат
  moveServos(0, 0);     delay(500);
  moveServos(180, 0);   delay(500);
  moveServos(180, 180); delay(500);
  moveServos(0, 180);   delay(500);
  
  delay(1000);
}

void moveServos(int h, int v) {
  // Плавное движение от текущей позиции к целевой
  while (angle_h != h || angle_v != v) {
    if (angle_h < h) angle_h++;
    if (angle_h > h) angle_h--;
    if (angle_v < v) angle_v++;
    if (angle_v > v) angle_v--;
    
    servo1.write(angle_h);
    servo2.write(angle_v);
    
    delay(15);
  }
  
  Serial.print("H:");
  Serial.print(angle_h);
  Serial.print(" V:");
  Serial.println(angle_v);
}
```

### Массив сервомоторов

```cpp
#include <Servo.h>

const int NUM_SERVOS = 4;
Servo servos[NUM_SERVOS];
const int SERVO_PINS[NUM_SERVOS] = {3, 5, 6, 9};

void setup() {
  Serial.begin(9600);
  
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(SERVO_PINS[i]);
    servos[i].write(90);
  }
  
  Serial.println("4 сервомотора инициализированы");
}

void loop() {
  // Поднимаем каждый серво по очереди
  for (int i = 0; i < NUM_SERVOS; i++) {
    for (int angle = 90; angle <= 180; angle += 5) {
      servos[i].write(angle);
      delay(50);
    }
    for (int angle = 180; angle >= 90; angle -= 5) {
      servos[i].write(angle);
      delay(50);
    }
  }
}
```

---

## Работа с DC моторами

### DC мотор (обычный мотор)

```
Отличия от серво-мотора:
├─ Вращается постоянно (на 360°)
├─ Управление скоростью через PWM
├─ Управление направлением через L298N модуль
└─ Дешевле, но менее точный контроль
```

### Управление DC мотором через L298N

```cpp
// Пины для L298N модуля
const int MOTOR_IN1 = 8;   // Direction 1
const int MOTOR_IN2 = 9;   // Direction 2
const int MOTOR_ENA = 10;  // Speed control (PWM)

void setup() {
  Serial.begin(9600);
  
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  pinMode(MOTOR_ENA, OUTPUT);
}

void loop() {
  // Вращение вперёд с полной скоростью
  moveMotor(255, "Forward");
  delay(2000);
  
  // Вращение вперёд с половинной скоростью
  moveMotor(128, "Slow Forward");
  delay(2000);
  
  // Остановка
  moveMotor(0, "Stop");
  delay(1000);
  
  // Вращение назад с полной скоростью
  moveMotor(-255, "Backward");
  delay(2000);
}

void moveMotor(int speed, String direction) {
  if (speed > 0) {
    // Вращение вперёд
    digitalWrite(MOTOR_IN1, HIGH);
    digitalWrite(MOTOR_IN2, LOW);
  } else if (speed < 0) {
    // Вращение назад
    digitalWrite(MOTOR_IN1, LOW);
    digitalWrite(MOTOR_IN2, HIGH);
    speed = -speed;  // Делаем положительным
  } else {
    // Остановка
    digitalWrite(MOTOR_IN1, LOW);
    digitalWrite(MOTOR_IN2, LOW);
  }
  
  analogWrite(MOTOR_ENA, speed);  // 0-255
  
  Serial.print("Motor: ");
  Serial.print(direction);
  Serial.print(" (");
  Serial.print(speed);
  Serial.println(")");
}
```

---

## Практические примеры

### Пример 1: Робот с двумя сервомоторами (панорамная камера)

```cpp
#include <Servo.h>

Servo servo_h;  // Горизонтальный (левый-правый)
Servo servo_v;  // Вертикальный (вверх-вниз)

const int POT_H = A0;  // Потенциометр для горизонтального
const int POT_V = A1;  // Потенциометр для вертикального

void setup() {
  Serial.begin(9600);
  servo_h.attach(9);
  servo_v.attach(10);
  
  servo_h.write(90);
  servo_v.write(90);
  
  Serial.println("Pan-Tilt система инициализирована");
}

void loop() {
  // Читаем потенциометры
  int pot_h = analogRead(POT_H);
  int pot_v = analogRead(POT_V);
  
  // Преобразуем 0-1023 в 0-180
  int angle_h = map(pot_h, 0, 1023, 0, 180);
  int angle_v = map(pot_v, 0, 1023, 0, 180);
  
  // Устанавливаем углы
  servo_h.write(angle_h);
  servo_v.write(angle_v);
  
  // Выводим в Serial
  Serial.print("H:");
  Serial.print(angle_h);
  Serial.print(" V:");
  Serial.println(angle_v);
  
  delay(50);
}
```

### Пример 2: Захват робота (2 сервомотора для клешни)

```cpp
#include <Servo.h>

Servo servo_left;   // Левая часть клешни
Servo servo_right;  // Правая часть клешни

const int BUTTON_OPEN = 2;
const int BUTTON_CLOSE = 3;

void setup() {
  Serial.begin(9600);
  
  servo_left.attach(9);
  servo_right.attach(10);
  
  pinMode(BUTTON_OPEN, INPUT_PULLUP);
  pinMode(BUTTON_CLOSE, INPUT_PULLUP);
  
  openGripper();
  Serial.println("Захват инициализирован");
}

void loop() {
  if (digitalRead(BUTTON_OPEN) == LOW) {
    openGripper();
    Serial.println("Клешня открыта");
    delay(500);
  }
  
  if (digitalRead(BUTTON_CLOSE) == LOW) {
    closeGripper();
    Serial.println("Клешня закрыта");
    delay(500);
  }
}

void openGripper() {
  servo_left.write(0);    // Левая раскрывается
  servo_right.write(180); // Правая раскрывается
}

void closeGripper() {
  servo_left.write(90);   // Левая закрывается
  servo_right.write(90);  // Правая закрывается
}
```

### Пример 3: Маятник (плавное качание)

```cpp
#include <Servo.h>

Servo myservo;
int angle = 90;
int direction = 1;  // 1 = вправо, -1 = влево

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  myservo.write(angle);
  
  Serial.println("Маятник инициализирован");
}

void loop() {
  // Плавное маятниковое движение
  angle += direction * 2;  // Увеличиваем/уменьшаем на 2°
  
  // Меняем направление на концах
  if (angle >= 160) {
    direction = -1;
  } else if (angle <= 20) {
    direction = 1;
  }
  
  myservo.write(angle);
  delay(30);
  
  // Выводим каждый 10-й раз для экономии
  static int counter = 0;
  if (counter++ % 10 == 0) {
    Serial.println(angle);
  }
}
```

### Пример 4: Система слежения (следит за потенциометром)

```cpp
#include <Servo.h>

Servo myservo;
const int SENSOR_PIN = A0;
const int SMOOTHING = 5;  // Количество образцов для сглаживания

int angle = 90;
int readings[SMOOTHING];

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  
  // Инициализируем массив нулями
  for (int i = 0; i < SMOOTHING; i++) {
    readings[i] = 0;
  }
  
  Serial.println("Система слежения инициализирована");
}

void loop() {
  // Смещаем значения массива
  for (int i = SMOOTHING - 1; i > 0; i--) {
    readings[i] = readings[i - 1];
  }
  
  // Читаем новое значение
  readings[0] = analogRead(SENSOR_PIN);
  
  // Вычисляем среднее значение
  int sum = 0;
  for (int i = 0; i < SMOOTHING; i++) {
    sum += readings[i];
  }
  
  int average = sum / SMOOTHING;
  
  // Преобразуем в угол
  angle = map(average, 0, 1023, 0, 180);
  
  // Устанавливаем угол с ограничением скорости
  // (чтобы движение было плавнее)
  static int last_angle = 90;
  if (abs(angle - last_angle) > 5) {
    // Движемся на максимум на 5° за раз
    if (angle > last_angle) {
      last_angle += 5;
    } else {
      last_angle -= 5;
    }
  } else {
    last_angle = angle;
  }
  
  myservo.write(last_angle);
  
  Serial.print("Sensor: ");
  Serial.print(average);
  Serial.print(" | Angle: ");
  Serial.println(last_angle);
  
  delay(50);
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Понимать принцип работы серво-моторов

✅ Разбираться в типах сервомоторов и DC моторов

✅ Знать принцип работы PWM сигнала

✅ Подключать сервомотор к Arduino

✅ Использовать библиотеку Servo

✅ Управлять сервомотором (угол, скорость)

✅ Работать с несколькими сервомоторами

✅ Управлять DC моторами через L298N

✅ Создавать системы с движением

---

## 🎯 Домашнее задание

1. Напишите программу плавного поворота сервомотора от 0° к 180° и обратно

2. Создайте систему управления сервомотором с тремя кнопками (лево/центр/право)

3. Напишите программу управления сервомотором через Serial (ввод угла)

4. Создайте систему с двумя сервомоторами, рисующую квадрат

5. Напишите программу следящей системы (сервомотор следит за потенциометром)

6. Дополнительно: Создайте систему панорамной камеры с двумя сервомоторами

---

## 🔗 Полезные ссылки

- 📖 **Servo Library:** https://www.arduino.cc/reference/en/libraries/servo/
- 📖 **servo.write():** https://www.arduino.cc/reference/en/libraries/servo/write/
- 📖 **PWM:** https://www.arduino.cc/en/Tutorial/PWM
- 📖 **L298N Module:** https://components101.com/modules/l298n-motor-driver-module
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Серво-мотор** | Мотор с системой управления углом |
| **DC мотор** | Обычный мотор (вращается на 360°) |
| **PWM** | Pulse Width Modulation (модуляция ширины импульса) |
| **Угол поворота** | Положение вала сервомотора (0-180°) |
| **Крутящий момент** | Сила вращения (кг·см) |
| **Импульс** | Электрический сигнал определённой длительности |
| **Редуктор** | Механизм замедления и увеличения момента |
| **Обратная связь** | Датчик, контролирующий положение |
| **L298N** | Модуль для управления DC моторами |
| **Направление** | Сторона вращения мотора |
| **Скорость** | Величина PWM сигнала (0-255) |
| **attach()** | Подключение сервомотора к пину |
| **write()** | Установка угла поворота |

---

**Следующий урок:** 🌐 [Протоколы коммуникации: I2C, SPI, UART](../Lesson_12/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025