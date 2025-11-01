# 🔧 Работа с модулями расширения: реле, RGB LED, звуковые модули

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Электромеханические реле](#электромеханические-реле)
3. [RGB светодиоды](#rgb-светодиоды)
4. [Звуковые модули](#звуковые-модули)
5. [Защита входов Arduino](#защита-входов-arduino)
6. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы научитесь работать с тремя основными типами модулей расширения:

- **Реле** — для управления мощными устройствами (220В, высокие токи)
- **RGB светодиоды** — для создания цветовых индикаторов и эффектов
- **Звуковые модули** — для генерации звуков и мелодий

---

## Электромеханические реле

### Что такое реле?

Реле — это электромеханический переключатель, который позволяет Arduino управлять высокими напряжениями и токами (220В, 10А и выше).

### Схема подключения реле

```
     Arduino
        │
        ├─ GND ─────────────┐
        │                   │
        ├─ D3 ──────┐       │
        │           │       │
        │         Резистор  │
        │         330 Ом    │
        │           │       │
        │          LED ●    │
        │           │       │
        │         Транзистор│
        │         2N2222    │
        │           │       │
        │ ┌─────────┴───────┤
        │ │                 │
        │ │ ┌──────────────┐│
        │ │ │ Реле         ││
        │ │ │  Катушка     ││
        │ │ │  ┌───┬───┐   ││
        │ │ │  │ 1 │ 2 │   ││
        │ │ └──┴───┴───┴───┘│
        │ │                 │
        │ └────────────┬────┘
        │              │
        │ ┌────────────┘
        │ │
    [Диод 1N4007]
        │
        ├─ COM (общий вывод)
        ├─ NO (нормально открытый)
        ├─ NC (нормально закрытый)
        │
    220В устройство
```

### Типы реле

```
┌──────────────────────────────────────┐
│ ТИПЫ РЕЛЕ                            │
├──────────────────────────────────────┤
│                                      │
│ 1. Электромеханические               │
│    ├─ Напряжение катушки: 5V-12V    │
│    ├─ Контакты: NO/NC               │
│    ├─ Мощность: до 250В/10А         │
│    └─ Задержка: ~10мс               │
│                                      │
│ 2. Твёрдотельные (SSR)               │
│    ├─ Нет движущихся частей         │
│    ├─ Быстрые (~мкс)                │
│    ├─ Бесшумные                     │
│    └─ Дороже                        │
│                                      │
│ 3. Модули реле (готовые)             │
│    ├─ С защитой                     │
│    ├─ С оптроизоляцией             │
│    ├─ С диодом защиты               │
│    └─ Просто подключить             │
│                                      │
└──────────────────────────────────────┘
```

### Базовый пример управления реле

```cpp
const int RELAY_PIN = 3;

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // Реле выключено
  
  Serial.println("=== Управление реле ===");
}

void loop() {
  // Включаем реле
  digitalWrite(RELAY_PIN, HIGH);
  Serial.println("Реле включено");
  delay(2000);
  
  // Выключаем реле
  digitalWrite(RELAY_PIN, LOW);
  Serial.println("Реле выключено");
  delay(2000);
}
```

### Управление реле через команды

```cpp
const int RELAY_PIN = 3;
boolean relay_state = false;

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  
  Serial.println("=== Система управления реле ===");
  Serial.println("Команды: ON, OFF, TOGGLE, STATUS");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.toUpperCase();
    cmd.trim();
    
    if (cmd == "ON") {
      digitalWrite(RELAY_PIN, HIGH);
      relay_state = true;
      Serial.println("✓ Реле ВКЛЮЧЕНО");
    }
    else if (cmd == "OFF") {
      digitalWrite(RELAY_PIN, LOW);
      relay_state = false;
      Serial.println("✓ Реле ВЫКЛЮЧЕНО");
    }
    else if (cmd == "TOGGLE") {
      relay_state = !relay_state;
      digitalWrite(RELAY_PIN, relay_state ? HIGH : LOW);
      Serial.print("✓ Реле переключено: ");
      Serial.println(relay_state ? "ВКЛ" : "ВЫКЛ");
    }
    else if (cmd == "STATUS") {
      Serial.print("Состояние: ");
      Serial.println(relay_state ? "ВКЛ" : "ВЫКЛ");
    }
  }
}
```

---

## RGB светодиоды

### Структура RGB LED

```
       RGB LED (4-ножка, общий катод)
       ┌──────────────┐
       │    ▲ ▲ ▲     │
       │   R G B      │
       │    │ │ │     │
       ├────┼─┼─┼────┐
       │    │ │ │    │
      (1)  (2)(3)(4) │
       │           GND│
       └──────────────┘

(1) - Красный (R)
(2) - Зелёный (G)
(3) - Синий (B)
(4) - Общий (-)

Подключение к Arduino:
R ──── Резистор 220Ω ──── PWM вывод
G ──── Резистор 220Ω ──── PWM вывод
B ──── Резистор 220Ω ──── PWM вывод
GND ── GND Arduino
```

### Управление RGB LED

```cpp
const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;

void setup() {
  Serial.begin(9600);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  
  // Все светодиоды выключены
  setColor(0, 0, 0);
}

void loop() {
  // Красный
  setColor(255, 0, 0);
  Serial.println("Красный");
  delay(1000);
  
  // Зелёный
  setColor(0, 255, 0);
  Serial.println("Зелёный");
  delay(1000);
  
  // Синий
  setColor(0, 0, 255);
  Serial.println("Синий");
  delay(1000);
  
  // Жёлтый (красный + зелёный)
  setColor(255, 255, 0);
  Serial.println("Жёлтый");
  delay(1000);
  
  // Голубой (зелёный + синий)
  setColor(0, 255, 255);
  Serial.println("Голубой");
  delay(1000);
  
  // Фиолетовый (красный + синий)
  setColor(255, 0, 255);
  Serial.println("Фиолетовый");
  delay(1000);
  
  // Белый (все вместе)
  setColor(255, 255, 255);
  Serial.println("Белый");
  delay(1000);
}

void setColor(int red, int green, int blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}
```

### Плавное изменение цвета (breathing effect)

```cpp
const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;

void setup() {
  Serial.begin(9600);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  // Красное дыхание
  breatheColor(255, 0, 0);
  
  // Зелёное дыхание
  breatheColor(0, 255, 0);
  
  // Синее дыхание
  breatheColor(0, 0, 255);
}

void breatheColor(int red, int green, int blue) {
  // Увеличение яркости
  for (int i = 0; i <= 255; i += 5) {
    analogWrite(RED_PIN, (red * i) / 255);
    analogWrite(GREEN_PIN, (green * i) / 255);
    analogWrite(BLUE_PIN, (blue * i) / 255);
    delay(30);
  }
  
  // Уменьшение яркости
  for (int i = 255; i >= 0; i -= 5) {
    analogWrite(RED_PIN, (red * i) / 255);
    analogWrite(GREEN_PIN, (green * i) / 255);
    analogWrite(BLUE_PIN, (blue * i) / 255);
    delay(30);
  }
}

void setColor(int red, int green, int blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}
```

### RGB LED цветовой индикатор статуса

```cpp
const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;

enum SystemStatus {
  IDLE,      // Голубой
  WORKING,   // Зелёный
  WARNING,   // Жёлтый
  ERROR      // Красный
};

SystemStatus current_status = IDLE;

void setup() {
  Serial.begin(9600);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  
  updateStatusLight();
}

void loop() {
  // Симуляция различных состояний
  static unsigned long last_change = millis();
  
  if (millis() - last_change > 3000) {
    current_status = (SystemStatus)((current_status + 1) % 4);
    updateStatusLight();
    last_change = millis();
    
    Serial.print("Статус: ");
    Serial.println(current_status);
  }
}

void updateStatusLight() {
  switch (current_status) {
    case IDLE:
      setColor(0, 255, 255);  // Голубой
      break;
    case WORKING:
      setColor(0, 255, 0);    // Зелёный
      break;
    case WARNING:
      setColor(255, 255, 0);  // Жёлтый
      break;
    case ERROR:
      setColor(255, 0, 0);    // Красный
      break;
  }
}

void setColor(int red, int green, int blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}
```

---

## Звуковые модули

### Типы звуковых модулей

```
┌────────────────────────────────────┐
│ ЗВУКОВЫЕ МОДУЛИ                    │
├────────────────────────────────────┤
│                                    │
│ 1. Пьезозвукоизлучатель (Buzzer)   │
│    ├─ Напряжение: 5V               │
│    ├─ Звук: 2-4 кГц                │
│    ├─ Простой, дешёвый             │
│    ├─ Два типа:                    │
│    │  ├─ Пассивный (требует PWM)  │
│    │  └─ Активный (просто +5V)    │
│    └─ Подходит для сигналов       │
│                                    │
│ 2. Музыкальный модуль (MP3)        │
│    ├─ Сложный                      │
│    ├─ Требует SD карту             │
│    ├─ UART интерфейс               │
│    └─ Для воспроизведения файлов  │
│                                    │
│ 3. Динамик + усилитель             │
│    ├─ Высокая мощность             │
│    ├─ Требует усилителя            │
│    └─ Для нормального звука        │
│                                    │
└────────────────────────────────────┘
```

### Пассивный пьезозвукоизлучатель

```cpp
const int BUZZER_PIN = 9;

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);
  
  Serial.println("=== Пьезозвукоизлучатель ===");
}

void loop() {
  // Один сигнал
  tone(BUZZER_PIN, 1000);  // 1000 Hz
  delay(500);
  noTone(BUZZER_PIN);
  delay(500);
  
  // Два сигнала
  tone(BUZZER_PIN, 1000);
  delay(200);
  noTone(BUZZER_PIN);
  delay(100);
  
  tone(BUZZER_PIN, 1000);
  delay(200);
  noTone(BUZZER_PIN);
  delay(2000);
}
```

### Проигрывание мелодии

```cpp
const int BUZZER_PIN = 9;

// Частоты нот (Герцы)
#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_D1  37
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_G1  49
#define NOTE_A1  55
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_D2  73
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_G2  98
#define NOTE_A2  110
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_D3  147
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_G3  196
#define NOTE_A3  220
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_D5  587
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_G5  784
#define NOTE_A5  880
#define NOTE_B5  988

// Длительность нот
#define WHOLE 4000
#define HALF  2000
#define QUARTER 1000
#define EIGHTH  500
#define SIXTEENTH 250

// Мелодия: первые ноты "Во поле берёза стояла"
int melody[] = {
  NOTE_E4, NOTE_G4, NOTE_A4, NOTE_B4,
  NOTE_C5, NOTE_B4, NOTE_A4, NOTE_G4,
  NOTE_A4, NOTE_B4, NOTE_C5, NOTE_D5,
  NOTE_C5, NOTE_B4, NOTE_A4, NOTE_G4
};

int durations[] = {
  QUARTER, QUARTER, QUARTER, QUARTER,
  HALF, QUARTER, QUARTER, QUARTER,
  QUARTER, QUARTER, QUARTER, QUARTER,
  HALF, QUARTER, QUARTER, QUARTER
};

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  playMelody();
  delay(3000);
}

void playMelody() {
  for (int i = 0; i < 16; i++) {
    tone(BUZZER_PIN, melody[i], durations[i]);
    delay(durations[i] + 50);  // Небольшая пауза между нотами
  }
}
```

### Алармовый сигнал

```cpp
const int BUZZER_PIN = 9;
boolean alarm_active = false;

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);
  
  Serial.println("=== Система сигнализации ===");
  Serial.println("Команды: ALARM_ON, ALARM_OFF");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.toUpperCase();
    cmd.trim();
    
    if (cmd == "ALARM_ON") {
      alarm_active = true;
      Serial.println("⚠️  СИГНАЛИЗАЦИЯ ВКЛЮЧЕНА!");
    }
    else if (cmd == "ALARM_OFF") {
      alarm_active = false;
      noTone(BUZZER_PIN);
      Serial.println("✓ Сигнализация выключена");
    }
  }
  
  if (alarm_active) {
    soundAlarm();
  }
}

void soundAlarm() {
  // Растущий звук
  for (int freq = 800; freq <= 2000; freq += 100) {
    tone(BUZZER_PIN, freq, 100);
    delay(100);
  }
  
  // Убывающий звук
  for (int freq = 2000; freq >= 800; freq -= 100) {
    tone(BUZZER_PIN, freq, 100);
    delay(100);
  }
}
```

---

## Защита входов Arduino

### Защитные компоненты

```
┌─────────────────────────────────┐
│ ЗАЩИТА ВХОДОВ ARDUINO           │
├─────────────────────────────────┤
│                                 │
│ 1. Резисторы токоограничивающие │
│    ├─ 220-1кОм между сигналом  │
│    ├─ Защита от перегрузки     │
│    └─ Уменьшает ток            │
│                                 │
│ 2. Конденсаторы (фильтр)        │
│    ├─ 0.1μF от сигнала к GND   │
│    ├─ Убирают помехи           │
│    └─ Сглаживают колебания     │
│                                 │
│ 3. Диоды Шоттки                 │
│    ├─ BAT54, 1N4148             │
│    ├─ Между сигналом и +5V/GND │
│    └─ Ограничивают напряжение   │
│                                 │
│ 4. Оптроизолятор                │
│    ├─ PC817, TLP291             │
│    ├─ Гальваническая развязка  │
│    └─ Для высоких напряжений   │
│                                 │
└─────────────────────────────────┘
```

### Схема защиты цифрового входа

```
    Внешний сигнал
         │
         ├──── Резистор 1кОм ────┐
         │                        │
         └──────────┐      ┌──────┴─────────── Цифровой вход
                    │      │
                   Диод    Конденсатор
                 Шоттки     100nF
                    │      │
                    └──────┴─────── GND
```

### Пример с защитой аналогового входа

```cpp
const int SENSOR_PIN = A0;

void setup() {
  Serial.begin(9600);
  pinMode(SENSOR_PIN, INPUT);
}

void loop() {
  // Снимаем несколько показаний
  int reading1 = analogRead(SENSOR_PIN);
  delay(10);
  int reading2 = analogRead(SENSOR_PIN);
  delay(10);
  int reading3 = analogRead(SENSOR_PIN);
  
  // Среднее значение (фильтр)
  int average = (reading1 + reading2 + reading3) / 3;
  
  Serial.print("Значение сенсора: ");
  Serial.println(average);
  
  delay(500);
}
```

---

## Практические примеры

### Пример 1: Система сигнализации с RGB LED и звуком

```cpp
const int RELAY_PIN = 2;
const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;
const int BUZZER_PIN = 9;
const int SENSOR_PIN = A0;

enum SystemMode {
  NORMAL,
  ALERT,
  ALARM
};

SystemMode current_mode = NORMAL;
unsigned long last_sensor_read = 0;

void setup() {
  Serial.begin(9600);
  
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  digitalWrite(RELAY_PIN, LOW);
  
  Serial.println("=== Система сигнализации ===");
}

void loop() {
  // Читаем датчик каждые 500ms
  if (millis() - last_sensor_read > 500) {
    int sensor_value = analogRead(SENSOR_PIN);
    last_sensor_read = millis();
    
    // Определяем режим
    if (sensor_value < 300) {
      current_mode = NORMAL;
    } else if (sensor_value < 600) {
      current_mode = ALERT;
    } else {
      current_mode = ALARM;
    }
    
    updateSystem();
    printStatus();
  }
  
  // Обработка команд
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    handleCommand(cmd);
  }
}

void updateSystem() {
  switch (current_mode) {
    case NORMAL:
      setColor(0, 255, 0);      // Зелёный
      digitalWrite(RELAY_PIN, LOW);
      noTone(BUZZER_PIN);
      break;
      
    case ALERT:
      setColor(255, 255, 0);    // Жёлтый
      digitalWrite(RELAY_PIN, LOW);
      tone(BUZZER_PIN, 1000, 100);
      delay(100);
      noTone(BUZZER_PIN);
      break;
      
    case ALARM:
      setColor(255, 0, 0);      // Красный
      digitalWrite(RELAY_PIN, HIGH);
      tone(BUZZER_PIN, 2000, 200);
      delay(200);
      tone(BUZZER_PIN, 1000, 200);
      delay(200);
      break;
  }
}

void setColor(int red, int green, int blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}

void printStatus() {
  Serial.print("Режим: ");
  switch (current_mode) {
    case NORMAL:
      Serial.print("НОРМАЛЬНЫЙ");
      break;
    case ALERT:
      Serial.print("ВНИМАНИЕ");
      break;
    case ALARM:
      Serial.print("ТРЕВОГА!!!");
      break;
  }
  Serial.print(" | Реле: ");
  Serial.println(digitalRead(RELAY_PIN) ? "ВКЛ" : "ВЫКЛ");
}

void handleCommand(String cmd) {
  if (cmd == "RESET") {
    current_mode = NORMAL;
    digitalWrite(RELAY_PIN, LOW);
    noTone(BUZZER_PIN);
    Serial.println("✓ Система сброшена");
  }
}
```

### Пример 2: RGB LED со звуковыми уведомлениями

```cpp
const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;
const int BUZZER_PIN = 9;

void setup() {
  Serial.begin(9600);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  Serial.println("=== Демонстрация LED и звука ===");
}

void loop() {
  // Уведомление "ОК"
  notificationOK();
  delay(1000);
  
  // Уведомление "ОШИБКА"
  notificationError();
  delay(1000);
  
  // Уведомление "УСПЕХ"
  notificationSuccess();
  delay(1000);
}

void notificationOK() {
  Serial.println("ℹ️  Уведомление ОК");
  
  // Голубой мигающий свет
  for (int i = 0; i < 2; i++) {
    setColor(0, 255, 255);
    tone(BUZZER_PIN, 1000, 100);
    delay(200);
    
    setColor(0, 0, 0);
    delay(100);
  }
}

void notificationError() {
  Serial.println("❌ Ошибка!");
  
  // Красный мигающий свет с звуком
  for (int i = 0; i < 3; i++) {
    setColor(255, 0, 0);
    tone(BUZZER_PIN, 500, 150);
    delay(250);
    
    setColor(0, 0, 0);
    delay(100);
  }
}

void notificationSuccess() {
  Serial.println("✓ Успех!");
  
  // Зелёный с мелодией
  setColor(0, 255, 0);
  tone(BUZZER_PIN, 1000, 100);
  delay(150);
  tone(BUZZER_PIN, 1500, 100);
  delay(150);
  tone(BUZZER_PIN, 2000, 100);
  delay(150);
  
  setColor(0, 0, 0);
}

void setColor(int red, int green, int blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Управлять электромеханическими реле

✅ Работать с RGB светодиодами

✅ Создавать цветовые индикаторы

✅ Генерировать звуки и мелодии

✅ Защищать входы Arduino

✅ Комбинировать модули для создания сложных систем

---

## 🎯 Домашнее задание

1. Создайте систему управления реле с обратной связью через RGB LED

2. Напишите программу проигрывания мелодии с 16 нотами

3. Реализуйте цветовой индикатор состояния системы (3+ состояния)

4. Создайте систему сигнализации с RGB LED и пьезозвукоизлучателем

5. Напишите функции различных типов уведомлений (успех, ошибка, предупреждение)

6. Дополнительно: Интегрируйте все три модуля в один проект

---

## 🔗 Полезные ссылки

- 📖 **Relay Module Guide:** https://www.arduino.cc/en/Tutorial/RelayModule
- 📖 **RGB LED Tutorial:** https://www.arduino.cc/en/Tutorial/RGBLED
- 📖 **Tone Function:** https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/
- 📖 **PWM Guide:** https://www.arduino.cc/en/Tutorial/PWM
- 💬 **Forum:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Реле** | Электромеханический переключатель |
| **RGB** | Red-Green-Blue (красный, зелёный, синий) |
| **PWM** | Pulse Width Modulation (широтно-импульсная модуляция) |
| **Buzzer** | Пьезозвукоизлучатель |
| **Tone** | Генерация звука определённой частоты |
| **Оптроизолятор** | Компонент для гальванической развязки |
| **Диод** | Компонент для защиты от обратного тока |
| **NO/NC** | Normally Open / Normally Closed (нормально открытый/закрытый) |
| **Транзистор** | Компонент для управления током |
| **Экранирование** | Защита от электромагнитных помех |

---

**Следующий урок:** 🌐 [Wi-Fi и IoT: Arduino с модулями ESP8266/ESP32](../Lesson_18/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
