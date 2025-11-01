# ⚡ Прерывания (interrupts) и обработка событий в реальном времени

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Что такое прерывание?](#что-такое-прерывание)
3. [Типы прерываний](#типы-прерываний)
4. [Пины прерываний на Arduino](#пины-прерываний-на-arduino)
5. [Подключение прерываний](#подключение-прерываний)
6. [Функция attachInterrupt()](#функция-attachinterrupt)
7. [Режимы триггера](#режимы-триггера)
8. [Обработчики прерываний](#обработчики-прерываний)
9. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите прерывания (interrupts) — один из самых мощных инструментов Arduino для обработки событий в реальном времени. Прерывания позволяют программе мгновенно реагировать на внешние события, не проверяя их постоянно.

---

## Что такое прерывание?

### Концепция прерывания

Прерывание — это сигнал, который останавливает текущее выполнение программы и вызывает специальную функцию-обработчик.

### Визуализация работы

```
Без прерываний:                    С прерываниями:

┌─────────────────────────┐       ┌─────────────────────────┐
│ loop() - основная цикл  │       │ loop() - основная цикл  │
│ ├─ Линия 1              │       │ ├─ Линия 1              │
│ ├─ Линия 2              │       │ ├─ Линия 2              │
│ ├─ Линия 3              │       │ ├─ !ПРЕРЫВАНИЕ!         │
│ ├─ Линия 4 (долго)      │       │ │  ├─ Вызов handler()   │
│ │  (кнопка нажата, но   │       │ │  ├─ Выполнение       │
│ │   не заметим!)        │       │ │  └─ Возврат          │
│ ├─ Линия 5              │       │ ├─ Линия 4 (продолж.)   │
│ ├─ Линия 6              │       │ ├─ Линия 5              │
│ └─ Конец цикла          │       │ └─ Конец цикла          │
└─────────────────────────┘       └─────────────────────────┘

❌ Пропущим нажатие                ✅ Обработали мгновенно!
```

### Преимущества прерываний

```
✅ Мгновенная реакция на события
✅ Не нужно постоянно проверять состояние
✅ Экономит вычислительные ресурсы
✅ Идеально для критичных по времени задач
✅ Несколько независимых прерываний
```

### Недостатки прерываний

```
❌ Сложнее в отладке
❌ Могут вызвать race conditions (конфликты)
❌ Ограниченное количество пинов
❌ Требует знания асинхронного программирования
```

---

## Типы прерываний

### Прерывания по событиям (External Interrupts)

```
Уровень (Level triggered):
├─ HIGH - прерывание когда пин HIGH
├─ LOW - прерывание когда пин LOW
└─ Постоянные прерывания!

Фронт (Edge triggered):
├─ RISING - прерывание на переход LOW→HIGH
├─ FALLING - прерывание на переход HIGH→LOW
└─ CHANGE - прерывание на любой переход
```

### Прерывания по времени (Timer Interrupts)

```
Встроенные таймеры Arduino вызывают прерывания
с определённой частотой (требует усложненного кода)
```

### Прерывания по UART (Serial Interrupts)

```
Автоматические прерывания при получении данных
через Serial порт
```

---

## Пины прерываний на Arduino

### Arduino UNO

```
Arduino UNO имеет 2 пина прерываний:

┌────────────────────────────────────────┐
│ Пин 2 → Прерывание INT0 (interrupt 0) │
│ Пин 3 → Прерывание INT1 (interrupt 1) │
└────────────────────────────────────────┘

Пример:
attachInterrupt(0, handler0, RISING);  // Пин 2
attachInterrupt(1, handler1, RISING);  // Пин 3
```

### Arduino Mega

```
Arduino Mega имеет 6 пинов прерываний:

Пин  → Прерывание
───────────────────
2    → INT4
3    → INT5
21   → INT0
20   → INT1
19   → INT2
18   → INT3
```

### Arduino Leonardo

```
Arduino Leonardo имеет 4 пина прерываний:

Пин  → Прерывание
───────────────────
3    → INT0
2    → INT1
0    → INT2
1    → INT3
```

---

## Подключение прерываний

### Схема подключения кнопки

```
Arduino:          Кнопка:

Pin 2 (INT0) ←→ [Кнопка]
                   │
                  GND

С резистором pull-up:

5V
│
├─ 10kΩ резистор
│
├────→ Pin 2 (INT0)
│
[Кнопка]
│
GND
```

---

## Функция attachInterrupt()

### Синтаксис (старый способ - Arduino Uno/Mega)

```cpp
attachInterrupt(interrupt_number, handler_function, mode);

// Параметры:
// interrupt_number: 0 (пин 2) или 1 (пин 3) на UNO
// handler_function: функция-обработчик прерывания
// mode: RISING, FALLING, CHANGE, LOW, HIGH
```

### Синтаксис (новый способ - рекомендуется)

```cpp
attachInterrupt(digitalPinToInterrupt(pin), handler_function, mode);

// Параметры:
// pin: номер пина (2, 3 на UNO)
// handler_function: функция-обработчик
// mode: RISING, FALLING, CHANGE, LOW, HIGH
```

### Отключение прерывания

```cpp
detachInterrupt(interrupt_number);
// или
detachInterrupt(digitalPinToInterrupt(pin));
```

---

## Режимы триггера

### RISING - переход из LOW в HIGH

```
Сигнал:  LOW ─────┐
                  │ HIGH
                  └───────
                  ↑
            Прерывание здесь!
```

### FALLING - переход из HIGH в LOW

```
Сигнал:  HIGH ─────┐
                   │ LOW
                   └────
                   ↑
            Прерывание здесь!
```

### CHANGE - любой переход

```
Сигнал:  LOW ─┐ HIGH ┐ LOW ┐ HIGH
             └─────┘ └────┘ └────
             ↑     ↑      ↑      ↑
      Прерывания везде!
```

### LOW - пока сигнал LOW

```
Сигнал:  LOW ─────────┐
      ↑↑↑ ПРЕРЫВАНИЯ ↑↑↑
                     HIGH
                         └───
                         ↑ (прерывания прекратились)
```

### HIGH - пока сигнал HIGH

```
Сигнал:  LOW ────┐
               HIGH ──────┐
                    ↑↑↑ ПРЕРЫВАНИЯ ↑↑↑
                          LOW
                          ↑ (прерывания прекратились)
```

---

## Обработчики прерываний

### Важные правила

```
⚠️ ПРАВИЛА для функций-обработчиков:

1. НЕ используйте delay()
2. НЕ используйте Serial.print() (он медленный)
3. Сделайте функцию максимально короткой
4. Используйте volatile переменные для глобальных данных
5. Не передавайте параметры (функция не может принимать аргументы)
6. Возвращаемое значение void
```

### Простой обработчик

```cpp
volatile int counter = 0;  // volatile! Важно!

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(2), buttonPressed, FALLING);
}

void loop() {
  Serial.print("Counter: ");
  Serial.println(counter);
  delay(1000);
}

// ВАЖНО: функция обработчика
// - void (ничего не возвращает)
// - без параметров
// - максимально короткая
void buttonPressed() {
  counter++;  // Только необходимые действия!
}
```

### Volatile переменные

```cpp
// ❌ БЕЗ volatile - может быть ошибка!
int flag = 0;

void setup() {
  attachInterrupt(digitalPinToInterrupt(2), handler, RISING);
}

void handler() {
  flag = 1;  // Компилятор может оптимизировать неправильно
}

// ✅ С volatile - правильно!
volatile int flag = 0;

void setup() {
  attachInterrupt(digitalPinToInterrupt(2), handler, RISING);
}

void handler() {
  flag = 1;  // Компилятор не оптимизирует
}
```

---

## Практические примеры

### Пример 1: Счётчик нажатий кнопки

```cpp
volatile int click_count = 0;
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println("=== Счётчик нажатий ===");
  
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), 
                  onButtonPress, 
                  FALLING);
}

void loop() {
  Serial.print("Нажатий: ");
  Serial.println(click_count);
  
  // Включаем LED каждые 5 нажатий
  if (click_count % 5 == 0 && click_count > 0) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  
  delay(1000);
}

void onButtonPress() {
  // Дебоунс в обработчике
  static unsigned long last_press = 0;
  unsigned long current_time = millis();
  
  if (current_time - last_press > 50) {  // 50мс дебоунс
    click_count++;
    last_press = current_time;
  }
}
```

### Пример 2: Энкодер (поворотный переключатель)

```cpp
volatile int position = 0;
const int ENCODER_A = 2;
const int ENCODER_B = 3;

void setup() {
  Serial.begin(9600);
  
  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(ENCODER_A), 
                  encoderInterrupt, 
                  CHANGE);
}

void loop() {
  Serial.print("Позиция: ");
  Serial.println(position);
  delay(500);
}

void encoderInterrupt() {
  // Читаем оба пина
  int a = digitalRead(ENCODER_A);
  int b = digitalRead(ENCODER_B);
  
  // Определяем направление
  if (a == b) {
    position++;  // Вращение вправо
  } else {
    position--;  // Вращение влево
  }
}
```

### Пример 3: Система тревоги с датчиком движения

```cpp
volatile boolean motion_detected = false;
volatile unsigned long motion_time = 0;

const int MOTION_SENSOR = 2;  // PIR датчик
const int ALARM_PIN = 13;     // Сирена

void setup() {
  Serial.begin(9600);
  
  pinMode(MOTION_SENSOR, INPUT);
  pinMode(ALARM_PIN, OUTPUT);
  
  Serial.println("=== Система тревоги ===");
  
  // HIGH когда движение обнаружено
  attachInterrupt(digitalPinToInterrupt(MOTION_SENSOR), 
                  motionDetected, 
                  HIGH);
}

void loop() {
  if (motion_detected) {
    digitalWrite(ALARM_PIN, HIGH);
    Serial.println("⚠️ ДВИЖЕНИЕ ОБНАРУЖЕНО!");
    
    // Сирена звучит 2 секунды
    if (millis() - motion_time > 2000) {
      motion_detected = false;
      digitalWrite(ALARM_PIN, LOW);
    }
  }
  
  delay(100);
}

void motionDetected() {
  motion_detected = true;
  motion_time = millis();
}
```

### Пример 4: Система с двумя независимыми прерываниями

```cpp
volatile int button1_count = 0;
volatile int button2_count = 0;

const int BUTTON1 = 2;
const int BUTTON2 = 3;
const int LED1 = 9;
const int LED2 = 10;

void setup() {
  Serial.begin(9600);
  
  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  
  // Два независимых прерывания
  attachInterrupt(digitalPinToInterrupt(BUTTON1), 
                  button1Handler, 
                  FALLING);
  
  attachInterrupt(digitalPinToInterrupt(BUTTON2), 
                  button2Handler, 
                  FALLING);
  
  Serial.println("=== Система с двумя кнопками ===");
}

void loop() {
  // Управление LED1
  if (button1_count % 2 == 1) {
    digitalWrite(LED1, HIGH);
  } else {
    digitalWrite(LED1, LOW);
  }
  
  // Управление LED2
  analogWrite(LED2, map(button2_count % 256, 0, 255, 0, 255));
  
  // Вывод информации
  static unsigned long last_print = 0;
  if (millis() - last_print > 1000) {
    Serial.print("Кнопка 1: ");
    Serial.print(button1_count);
    Serial.print(" | Кнопка 2: ");
    Serial.println(button2_count);
    last_print = millis();
  }
}

void button1Handler() {
  static unsigned long last_time = 0;
  if (millis() - last_time > 50) {
    button1_count++;
    last_time = millis();
  }
}

void button2Handler() {
  static unsigned long last_time = 0;
  if (millis() - last_time > 50) {
    button2_count++;
    last_time = millis();
  }
}
```

### Пример 5: Обработка сложного события

```cpp
volatile unsigned long button_press_time = 0;
volatile boolean button_pressed = false;
volatile int press_type = 0;  // 0=none, 1=short, 2=long

const int BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), 
                  buttonChanged, 
                  CHANGE);
}

void loop() {
  if (press_type == 1) {
    Serial.println("✓ Короткое нажатие (< 500мс)");
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    press_type = 0;
  }
  else if (press_type == 2) {
    Serial.println("✓✓ Длинное нажатие (>= 500мс)");
    digitalWrite(LED_PIN, HIGH);
    delay(500);
    digitalWrite(LED_PIN, LOW);
    press_type = 0;
  }
  
  delay(50);
}

void buttonChanged() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    // Кнопка нажата
    button_press_time = millis();
    button_pressed = true;
  } else {
    // Кнопка отпущена
    if (button_pressed) {
      unsigned long press_duration = millis() - button_press_time;
      
      if (press_duration < 500) {
        press_type = 1;  // Короткое
      } else {
        press_type = 2;  // Длинное
      }
      
      button_pressed = false;
    }
  }
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Понимать концепцию прерываний

✅ Использовать attachInterrupt() для подключения прерываний

✅ Работать с различными режимами триггера

✅ Писать эффективные обработчики прерываний

✅ Использовать volatile переменные правильно

✅ Обрабатывать события в реальном времени

✅ Создавать сложные системы с прерываниями

✅ Избегать типичных ошибок

---

## 🎯 Домашнее задание

1. Создайте счётчик нажатий кнопки с использованием прерываний

2. Реализуйте обработчик для обнаружения коротких и длинных нажатий

3. Напишите программу с двумя независимыми кнопками (разные действия)

4. Создайте систему мониторинга датчика движения (PIR) с прерыванием

5. Реализуйте энкодер с обнаружением направления вращения

6. Дополнительно: Создайте систему с 3+ событиями, обрабатываемыми прерываниями

---

## 🔗 Полезные ссылки

- 📖 **attachInterrupt():** https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/
- 📖 **Interrupts:** https://www.arduino.cc/reference/en/language/functions/external-interrupts/
- 📖 **volatile:** https://www.arduino.cc/reference/en/language/variables/variable-scope-qualifiers/volatile/
- 📖 **Interrupt Tutorial:** https://www.arduino.cc/en/Tutorial/Interrupts
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Прерывание** | Сигнал, который прерывает выполнение программы |
| **Обработчик** | Функция, которая вызывается при прерывании |
| **INT0, INT1** | Номера прерываний на Arduino UNO |
| **RISING** | Переход из LOW в HIGH |
| **FALLING** | Переход из HIGH в LOW |
| **CHANGE** | Любой переход сигнала |
| **volatile** | Квалификатор для переменных в прерываниях |
| **attachInterrupt()** | Функция подключения обработчика прерывания |
| **detachInterrupt()** | Функция отключения обработчика прерывания |
| **Race condition** | Конфликт при одновременном доступе к данным |
| **Дебоунс** | Защита от дребезга контактов |
| **Асинхронность** | События происходят независимо друг от друга |

---

**Следующий урок:** 💾 [Работа с памятью: EEPROM и SRAM на Arduino](../Lesson_16/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
