# 🔘 Кнопки и интерактивные элементы управления

---

## 📋 Содержание урока

1. [Введение](#введение)
2. [Что такое кнопка?](#что-такое-кнопка)
3. [Принцип работы кнопки](#принцип-работы-кнопки)
4. [Подключение кнопки к Arduino](#подключение-кнопки-к-arduino)
5. [Чтение состояния кнопки](#чтение-состояния-кнопки)
6. [Проблема дребезга (debounce)](#проблема-дребезга-debounce)
7. [Обнаружение нажатия](#обнаружение-нажатия)
8. [Множественные кнопки](#множественные-кнопки)
9. [Другие интерактивные элементы](#другие-интерактивные-элементы)
10. [Практические примеры](#практические-примеры)

---

## Введение

На этом уроке вы изучите работу с кнопками и интерактивными элементами управления. Кнопки — один из самых простых способов взаимодействия пользователя с Arduino.

---

## Что такое кнопка?

Кнопка — это простой электрический переключатель, который замыкает или размыкает электрическую цепь при нажатии.

### Типы кнопок

```
┌────────────────────────────────────────┐
│        ТИПЫ КНОПОК                     │
├────────────────────────────────────────┤
│                                        │
│ Кнопка "Нормально открыта" (NO)       │
│ ├─ Не нажата: РАЗОМКНУТА (нет сигнала)│
│ └─ Нажата: ЗАМКНУТА (есть сигнал)     │
│                                        │
│ Кнопка "Нормально закрыта" (NC)       │
│ ├─ Не нажата: ЗАМКНУТА (есть сигнал)  │
│ └─ Нажата: РАЗОМКНУТА (нет сигнала)   │
│                                        │
│ Переключатель (Toggle switch)         │
│ ├─ Механический переключатель         │
│ └─ Может быть NO или NC               │
│                                        │
└────────────────────────────────────────┘
```

### Устройство кнопки

```
┌─────────────────┐
│   Кнопка (NO)   │
├─────────────────┤
│                 │
│  Не нажата:     │
│  ┌─┐   ┌─┐      │
│  │ │   │ │ ✕     │ (не соединены)
│  └─┘   └─┘      │
│                 │
│  Нажата:        │
│  ┌─────────┐    │
│  │ ─ ─ ─ ─ │    │ (соединены)
│  └─────────┘    │
│                 │
└─────────────────┘
```

---

## Принцип работы кнопки

### Логические уровни

```
HIGH (5V) ─────  Кнопка НЕ нажата
           │
           │ (нажатие)
           ↓
LOW (0V)  ─────  Кнопка НАЖАТА
```

### Схема подключения с pull-up резистором

```
        5V
        │
        ├─ 10kΩ резистор
        │
        ├──────→ Arduino Pin (читаем здесь)
        │
      Кнопка
        │
        GND
```

**Логика:**
- Кнопка не нажата → PIN = HIGH (5V через резистор)
- Кнопка нажата → PIN = LOW (0V через кнопку)

---

## Подключение кнопки к Arduino

### Схема подключения

```
Arduino UNO:

       Pin 2 (INPUT)
           │
           ├────────→ [Кнопка] → GND
           │
         10kΩ резистор
           │
           ├────────→ 5V
           │
           
Результат:
- Не нажата: Pin 2 = HIGH (5V)
- Нажата: Pin 2 = LOW (0V)
```

### Альтернативный способ: INPUT_PULLUP

Arduino имеет встроенный pull-up резистор!

```cpp
void setup() {
  pinMode(2, INPUT_PULLUP);  // Используем встроенный резистор
  // Теперь не нужен внешний резистор!
}
```

**Логика инвертирована:**
- Кнопка не нажата → HIGH
- Кнопка нажата → LOW

---

## Чтение состояния кнопки

### Простое чтение

```cpp
const int BUTTON_PIN = 2;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int button_state = digitalRead(BUTTON_PIN);
  
  Serial.print("Состояние кнопки: ");
  Serial.println(button_state);  // 1 (не нажата) или 0 (нажата)
  
  delay(100);
}
```

### С логикой "если нажата"

```cpp
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int button_state = digitalRead(BUTTON_PIN);
  
  if (button_state == LOW) {  // Кнопка НАЖАТА
    digitalWrite(LED_PIN, HIGH);
    Serial.println("Кнопка нажата! LED включен");
  } else {  // Кнопка НЕ НАЖАТА
    digitalWrite(LED_PIN, LOW);
    Serial.println("Кнопка отпущена");
  }
  
  delay(100);
}
```

---

## Проблема дребезга (debounce)

### Что такое дребезг?

Из-за механических колебаний контактов, кнопка может быть зарегистрирована как нажатая несколько раз!

```
Идеальное нажатие:        Реальное нажатие (дребезг):
│                         │
HIGH  ────────            HIGH  ──┐
      │                         │ ├──┬──┬───
LOW   │ (нажатие)               │ │  │  │
      │                         │ │  │  │
      └────────                 └─┘  └──┘
      
      1 нажатие                 Несколько "нажатий"!
```

### Решение 1: Задержка (delay)

```cpp
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    delay(20);  // Ждём 20мс - дребезг прекратится
    
    if (digitalRead(BUTTON_PIN) == LOW) {  // Второй раз проверяем
      Serial.println("Кнопка точно нажата!");
      digitalWrite(LED_PIN, HIGH);
      delay(500);
      digitalWrite(LED_PIN, LOW);
    }
  }
}
```

### Решение 2: Software debounce (профессиональный способ)

```cpp
const int BUTTON_PIN = 2;
const int LED_PIN = 13;
const int DEBOUNCE_DELAY = 50;  // миллисекунды

int last_button_state = HIGH;
int button_state = HIGH;
unsigned long last_debounce_time = 0;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int reading = digitalRead(BUTTON_PIN);
  
  // Если состояние изменилось - начинаем отсчёт
  if (reading != last_button_state) {
    last_debounce_time = millis();
  }
  
  // Если прошло достаточно времени - принимаем новое состояние
  if ((millis() - last_debounce_time) > DEBOUNCE_DELAY) {
    if (reading != button_state) {
      button_state = reading;
      
      // Обрабатываем ТОЛЬКО нажатие
      if (button_state == LOW) {
        Serial.println("Кнопка нажата!");
        digitalWrite(LED_PIN, HIGH);
        delay(500);
        digitalWrite(LED_PIN, LOW);
      }
    }
  }
  
  last_button_state = reading;
}
```

---

## Обнаружение нажатия

### Обнаружение "фронта" (переход из HIGH в LOW)

```cpp
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

int previous_state = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int current_state = digitalRead(BUTTON_PIN);
  
  // Обнаруживаем переход: было HIGH, стало LOW
  if (previous_state == HIGH && current_state == LOW) {
    Serial.println("Кнопка ТО ЧТО БЫЛА НАЖАТА!");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));  // Переключаем LED
  }
  
  previous_state = current_state;
  delay(20);
}
```

### Счёт нажатий

```cpp
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

int press_count = 0;
int previous_state = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int current_state = digitalRead(BUTTON_PIN);
  
  // Обнаруживаем нажатие
  if (previous_state == HIGH && current_state == LOW) {
    press_count++;
    Serial.print("Нажатий: ");
    Serial.println(press_count);
    
    // Каждое третье нажатие - переключаем LED
    if (press_count % 3 == 0) {
      digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    }
  }
  
  previous_state = current_state;
  delay(20);
}
```

---

## Множественные кнопки

### Работа с несколькими кнопками

```cpp
const int BUTTON1_PIN = 2;
const int BUTTON2_PIN = 3;
const int BUTTON3_PIN = 4;

const int LED1_PIN = 9;
const int LED2_PIN = 10;
const int LED3_PIN = 11;

void setup() {
  Serial.begin(9600);
  
  // Кнопки
  pinMode(BUTTON1_PIN, INPUT_PULLUP);
  pinMode(BUTTON2_PIN, INPUT_PULLUP);
  pinMode(BUTTON3_PIN, INPUT_PULLUP);
  
  // LED
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);
}

void loop() {
  // Проверяем первую кнопку
  if (digitalRead(BUTTON1_PIN) == LOW) {
    digitalWrite(LED1_PIN, HIGH);
    Serial.println("Кнопка 1 нажата");
  } else {
    digitalWrite(LED1_PIN, LOW);
  }
  
  // Проверяем вторую кнопку
  if (digitalRead(BUTTON2_PIN) == LOW) {
    digitalWrite(LED2_PIN, HIGH);
    Serial.println("Кнопка 2 нажата");
  } else {
    digitalWrite(LED2_PIN, LOW);
  }
  
  // Проверяем третью кнопку
  if (digitalRead(BUTTON3_PIN) == LOW) {
    digitalWrite(LED3_PIN, HIGH);
    Serial.println("Кнопка 3 нажата");
  } else {
    digitalWrite(LED3_PIN, LOW);
  }
  
  delay(50);
}
```

### С массивом кнопок

```cpp
const int NUM_BUTTONS = 4;
const int BUTTON_PINS[NUM_BUTTONS] = {2, 3, 4, 5};
const int LED_PINS[NUM_BUTTONS] = {9, 10, 11, 12};

int button_states[NUM_BUTTONS] = {HIGH, HIGH, HIGH, HIGH};
int previous_states[NUM_BUTTONS] = {HIGH, HIGH, HIGH, HIGH};

void setup() {
  Serial.begin(9600);
  
  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(BUTTON_PINS[i], INPUT_PULLUP);
    pinMode(LED_PINS[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < NUM_BUTTONS; i++) {
    button_states[i] = digitalRead(BUTTON_PINS[i]);
    
    // Обнаруживаем нажатие
    if (previous_states[i] == HIGH && button_states[i] == LOW) {
      Serial.print("Кнопка ");
      Serial.print(i + 1);
      Serial.println(" нажата");
      
      digitalWrite(LED_PINS[i], HIGH);
    } else {
      digitalWrite(LED_PINS[i], LOW);
    }
    
    previous_states[i] = button_states[i];
  }
  
  delay(20);
}
```

---

## Другие интерактивные элементы

### Переключатель (Switch)

```cpp
const int SWITCH_PIN = 6;
const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(SWITCH_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int switch_state = digitalRead(SWITCH_PIN);
  
  if (switch_state == LOW) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("Переключатель: ON");
  } else {
    digitalWrite(LED_PIN, LOW);
    Serial.println("Переключатель: OFF");
  }
  
  delay(100);
}
```

### Сенсор движения (PIR)

```cpp
const int PIR_PIN = 7;
const int ALARM_PIN = 13;

void setup() {
  Serial.begin(9600);
  pinMode(PIR_PIN, INPUT);
  pinMode(ALARM_PIN, OUTPUT);
  
  delay(30000);  // Калибровка PIR (30 сек)
}

void loop() {
  int motion = digitalRead(PIR_PIN);
  
  if (motion == HIGH) {
    digitalWrite(ALARM_PIN, HIGH);
    Serial.println("ДВИЖЕНИЕ ОБНАРУЖЕНО!");
  } else {
    digitalWrite(ALARM_PIN, LOW);
  }
  
  delay(100);
}
```

### Система с реле

```cpp
const int BUTTON_PIN = 2;
const int RELAY_PIN = 8;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // Реле изначально выключено
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    digitalWrite(RELAY_PIN, HIGH);  // Включаем реле
    Serial.println("Реле включено - подключение высокого тока");
    
    while (digitalRead(BUTTON_PIN) == LOW) {
      delay(10);  // Ждём отпускания кнопки
    }
    
    delay(2000);
    digitalWrite(RELAY_PIN, LOW);  // Выключаем реле
    Serial.println("Реле выключено");
  }
  
  delay(100);
}
```

---

## Практические примеры

### Пример 1: Система управления LED (вкл/выкл/яркость)

```cpp
const int BUTTON1_PIN = 2;  // Включение/выключение
const int BUTTON2_PIN = 3;  // Яркость
const int LED_PIN = 9;

boolean led_on = false;
int brightness = 0;
int previous_btn2 = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON1_PIN, INPUT_PULLUP);
  pinMode(BUTTON2_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Кнопка 1: Включение/выключение
  if (digitalRead(BUTTON1_PIN) == LOW) {
    delay(50);
    if (digitalRead(BUTTON1_PIN) == LOW) {
      led_on = !led_on;
      Serial.print("LED: ");
      Serial.println(led_on ? "ВКЛ" : "ВЫКЛ");
      
      while (digitalRead(BUTTON1_PIN) == LOW) {
        delay(10);
      }
      delay(200);
    }
  }
  
  // Кнопка 2: Регулировка яркости
  if (digitalRead(BUTTON2_PIN) == LOW && previous_btn2 == HIGH) {
    if (led_on) {
      brightness += 50;
      if (brightness > 255) brightness = 0;
      
      Serial.print("Яркость: ");
      Serial.println(brightness);
    }
  }
  
  previous_btn2 = digitalRead(BUTTON2_PIN);
  
  // Установка яркости
  if (led_on) {
    analogWrite(LED_PIN, brightness);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  
  delay(10);
}
```

### Пример 2: Калькулятор с кнопками

```cpp
const int BUTTON_UP = 2;     // Увеличить
const int BUTTON_DOWN = 3;   // Уменьшить
const int BUTTON_RESET = 4;  // Сброс

int value = 0;
int previous_up = HIGH;
int previous_down = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_UP, INPUT_PULLUP);
  pinMode(BUTTON_DOWN, INPUT_PULLUP);
  pinMode(BUTTON_RESET, INPUT_PULLUP);
  
  displayValue();
}

void loop() {
  // Увеличить
  if (digitalRead(BUTTON_UP) == LOW && previous_up == HIGH) {
    value++;
    displayValue();
  }
  previous_up = digitalRead(BUTTON_UP);
  
  // Уменьшить
  if (digitalRead(BUTTON_DOWN) == LOW && previous_down == HIGH) {
    value--;
    displayValue();
  }
  previous_down = digitalRead(BUTTON_DOWN);
  
  // Сброс
  if (digitalRead(BUTTON_RESET) == LOW) {
    value = 0;
    Serial.println("СБРОС!");
    displayValue();
    
    while (digitalRead(BUTTON_RESET) == LOW) {
      delay(10);
    }
    delay(200);
  }
  
  delay(20);
}

void displayValue() {
  Serial.print("Значение: ");
  Serial.println(value);
}
```

### Пример 3: Система меню с кнопками

```cpp
const int BUTTON_UP = 2;
const int BUTTON_DOWN = 3;
const int BUTTON_SELECT = 4;

const String MENU_ITEMS[] = {"Режим 1", "Режим 2", "Режим 3", "Выход"};
const int MENU_SIZE = 4;

int current_menu = 0;
int previous_up = HIGH;
int previous_down = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(BUTTON_UP, INPUT_PULLUP);
  pinMode(BUTTON_DOWN, INPUT_PULLUP);
  pinMode(BUTTON_SELECT, INPUT_PULLUP);
  
  displayMenu();
}

void loop() {
  // Вверх по меню
  if (digitalRead(BUTTON_UP) == LOW && previous_up == HIGH) {
    current_menu--;
    if (current_menu < 0) current_menu = MENU_SIZE - 1;
    displayMenu();
  }
  previous_up = digitalRead(BUTTON_UP);
  
  // Вниз по меню
  if (digitalRead(BUTTON_DOWN) == LOW && previous_down == HIGH) {
    current_menu++;
    if (current_menu >= MENU_SIZE) current_menu = 0;
    displayMenu();
  }
  previous_down = digitalRead(BUTTON_DOWN);
  
  // Выбор
  if (digitalRead(BUTTON_SELECT) == LOW) {
    executeMenu(current_menu);
    
    while (digitalRead(BUTTON_SELECT) == LOW) {
      delay(10);
    }
    delay(200);
  }
  
  delay(20);
}

void displayMenu() {
  Serial.println("\n=== МЕНЮ ===");
  for (int i = 0; i < MENU_SIZE; i++) {
    Serial.print(i == current_menu ? "> " : "  ");
    Serial.println(MENU_ITEMS[i]);
  }
}

void executeMenu(int choice) {
  Serial.print("\nВыбран: ");
  Serial.println(MENU_ITEMS[choice]);
  
  switch (choice) {
    case 0:
      Serial.println("Режим 1 активен");
      break;
    case 1:
      Serial.println("Режим 2 активен");
      break;
    case 2:
      Serial.println("Режим 3 активен");
      break;
    case 3:
      Serial.println("До свидания!");
      break;
  }
}
```

---

## 📝 Резюме урока

На этом уроке вы научились:

✅ Понимать принцип работы кнопок

✅ Подключать кнопки к Arduino

✅ Читать состояние кнопки

✅ Решать проблему дребезга (debounce)

✅ Обнаруживать нажатия кнопок

✅ Работать с множественными кнопками

✅ Использовать другие интерактивные элементы

✅ Создавать системы управления

---

## 🎯 Домашнее задание

1. Напишите программу, которая считает количество нажатий кнопки

2. Создайте систему с 3 кнопками и 3 LED (каждая кнопка управляет своим LED)

3. Напишите программу светофора, управляемого кнопками (вперёд/назад)

4. Создайте систему, где длинное нажатие делает одно, короткое - другое

5. Напишите простое меню (вверх/вниз/выбор)

6. Дополнительно: Создайте систему с таймером (кнопка старт/стоп)

---

## 🔗 Полезные ссылки

- 📖 **digitalWrite:** https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/
- 📖 **digitalRead:** https://www.arduino.cc/reference/en/language/functions/digital-io/digitalread/
- 📖 **pinMode:** https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/
- 📚 **Примеры:** https://www.arduino.cc/en/Tutorial/BuiltInExamples
- 💬 **Форум:** https://forum.arduino.cc

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **Кнопка** | Механический переключатель |
| **Нажатие** | Замыкание электрической цепи |
| **Отпускание** | Размыкание электрической цепи |
| **Дребезг** | Механические колебания контактов |
| **Debounce** | Защита от дребезга |
| **Pull-up резистор** | Резистор, который подтягивает сигнал к HIGH |
| **INPUT_PULLUP** | Встроенный pull-up резистор |
| **Фронт сигнала** | Переход из одного состояния в другое |
| **HIGH** | Логическая 1 (5V на Arduino UNO) |
| **LOW** | Логический 0 (0V на Arduino UNO) |
| **digitalRead** | Чтение цифрового вывода |
| **digitalWrite** | Установка цифрового вывода |

---

**Следующий урок:** 📡 [Серийная коммуникация (Serial): отладка и обмен данными](../Lesson_10/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025