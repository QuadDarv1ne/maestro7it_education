void log(LogLevel level, const char* prefix, const char* msg) {
      if (level < currentLevel) return;
      
      // Время с начала сеанса
      unsigned long elapsed = (millis() - sessionStart) / 1000;
      
      Serial.print("[");
      if (elapsed < 10) Serial.print("0");
      if (elapsed < 100) Serial.print("0");
      Serial.print(elapsed);
      Serial.print("] ");
      
      Serial.print(prefix);
      Serial.print(" ");
      Serial.println(msg);
      
      messageCount++;
    }
    
    const char* getLevelName(LogLevel level) {
      switch(level) {
        case LL_DEBUG: return "DEBUG";
        case LL_INFO: return "INFO";
        case LL_WARNING: return "WARNING";
        case LL_ERROR: return "ERROR";
        case LL_CRITICAL: return "CRITICAL";
        default: return "UNKNOWN";
      }
    }
};

// ИСПОЛЬЗОВАНИЕ:

Logger logger(LL_DEBUG);

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  logger.info("Система стартует");
  logger.debug("Это отладочное сообщение");
  logger.warning("Это предупреждение");
}

void loop() {
  logger.info("Основной цикл");
  
  static unsigned long lastStats = 0;
  if (millis() - lastStats > 10000) {
    logger.printStats();
    lastStats = millis();
  }
  
  delay(1000);
}
```

### Вывод диагностической информации

```cpp
class DiagnosticMonitor {
  public:
    void printFullReport() {
      Serial.println("\n╔════════════════════════════════════════╗");
      Serial.println("║     ПОЛНЫЙ ОТЧЁТ О СИСТЕМЕ            ║");
      Serial.println("╠════════════════════════════════════════╣");
      
      printUptimeInfo();
      Serial.println("║                                        ║");
      
      printMemoryInfo();
      Serial.println("║                                        ║");
      
      printErrorStats();
      Serial.println("║                                        ║");
      
      printVersionInfo();
      Serial.println("╚════════════════════════════════════════╝\n");
    }
    
  private:
    void printUptimeInfo() {
      unsigned long uptime = millis() / 1000;
      int hours = uptime / 3600;
      int minutes = (uptime % 3600) / 60;
      int seconds = uptime % 60;
      
      Serial.print("║ Время работы: ");
      Serial.print(hours);
      Serial.print("h ");
      Serial.print(minutes);
      Serial.print("m ");
      Serial.print(seconds);
      Serial.println("s          ║");
    }
    
    void printMemoryInfo() {
      int free = freeRam();
      int used = 2048 - free;
      float percent = (used / 2048.0) * 100;
      
      Serial.print("║ Память: ");
      Serial.print(used);
      Serial.print("/2048 байт (");
      Serial.print((int)percent);
      Serial.println("%)        ║");
      
      if (free < 200) {
        Serial.println("║ ⚠️  КРИТИЧЕСКИ НИЗКО ПАМЯТИ!           ║");
      }
    }
    
    void printErrorStats() {
      Serial.print("║ Ошибок за сеанс: ");
      Serial.print(0);  // Здесь нужно сохранять счётчик
      Serial.println("                 ║");
      Serial.println("║ Статус: ✓ OK                           ║");
    }
    
    void printVersionInfo() {
      Serial.println("║ Версия: 1.0.0                         ║");
      Serial.println("║ Дата компиляции: 01.11.2025           ║");
    }
    
    int freeRam() {
      extern int __heap_start, *__brkval;
      int v;
      return (int) &v - (__brkval == 0 ? 
              (int) &__heap_start : (int) __brkval);
    }
};

// ИСПОЛЬЗОВАНИЕ:

DiagnosticMonitor diagnostics;

void setup() {
  Serial.begin(9600);
  delay(1000);
  diagnostics.printFullReport();
}

void loop() {
  delay(5000);
}
```

---

## Тестирование и отладка

### Модульное тестирование

```cpp
// Простая фреймворк для тестирования

class TestRunner {
  private:
    int testsRun;
    int testsPassed;
    int testsFailed;
    
  public:
    TestRunner() : testsRun(0), testsPassed(0), testsFailed(0) {}
    
    void assertEquals(int expected, int actual, const char* testName) {
      testsRun++;
      if (expected == actual) {
        Serial.print("✓ PASS: ");
        testsPassed++;
      } else {
        Serial.print("✗ FAIL: ");
        testsFailed++;
      }
      Serial.println(testName);
      
      if (expected != actual) {
        Serial.print("       Ожидали: ");
        Serial.print(expected);
        Serial.print(", получили: ");
        Serial.println(actual);
      }
    }
    
    void assertTrue(boolean condition, const char* testName) {
      assertEquals(1, condition ? 1 : 0, testName);
    }
    
    void assertFalse(boolean condition, const char* testName) {
      assertEquals(1, condition ? 0 : 1, testName);
    }
    
    void printSummary() {
      Serial.println("\n╔═══════════════════════════════════╗");
      Serial.println("║       РЕЗУЛЬТАТЫ ТЕСТОВ          ║");
      Serial.println("╠═══════════════════════════════════╣");
      Serial.print("║ Всего: ");
      Serial.print(testsRun);
      Serial.println(" тестов                      ║");
      Serial.print("║ Пройдено: ");
      Serial.print(testsPassed);
      Serial.println(" ✓                      ║");
      Serial.print("║ Провалено: ");
      Serial.print(testsFailed);
      Serial.println(" ✗                      ║");
      Serial.println("╚═══════════════════════════════════╝\n");
    }
};

// ПРИМЕРЫ ТЕСТОВ:

TestRunner tester;

void testMath() {
  Serial.println("\n=== ТЕСТЫ МАТЕМАТИКИ ===");
  tester.assertEquals(4, 2 + 2, "2 + 2 = 4");
  tester.assertEquals(7, 10 - 3, "10 - 3 = 7");
  tester.assertEquals(12, 3 * 4, "3 * 4 = 12");
}

void testGPIO() {
  Serial.println("\n=== ТЕСТЫ GPIO ===");
  
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  tester.assertTrue(digitalRead(13) == HIGH, "LED ON");
  
  digitalWrite(13, LOW);
  tester.assertTrue(digitalRead(13) == LOW, "LED OFF");
}

void testAnalog() {
  Serial.println("\n=== ТЕСТЫ АНАЛОГ ===");
  
  int reading = analogRead(A0);
  tester.assertTrue(reading >= 0 && reading <= 1023, "ADC в диапазоне");
}

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  Serial.println("╔═══════════════════════════════════╗");
  Serial.println("║    ЗАПУСК НАБОРА ТЕСТОВ          ║");
  Serial.println("╚═══════════════════════════════════╝");
  
  testMath();
  testGPIO();
  testAnalog();
  
  tester.printSummary();
}

void loop() {}
```

---

## Реальные примеры проектов

### Пример 1: Умная метеостанция

```cpp
#include <EEPROM.h>

class MeteoStation {
  private:
    enum State { INIT, READY, TRANSMIT, ERROR };
    State state;
    Logger logger;
    
    // Данные
    float temperature;
    float humidity;
    float pressure;
    unsigned long lastReadTime;
    
  public:
    MeteoStation() : state(INIT), logger(LL_INFO) {}
    
    void init() {
      logger.info("Инициализация метеостанции");
      
      // Инициализация датчиков
      if (!initializeSensors()) {
        logger.critical("Ошибка инициализации датчиков!");
        state = ERROR;
        return;
      }
      
      state = READY;
      logger.info("✓ Готова к работе");
    }
    
    void update() {
      switch(state) {
        case READY:
          if (shouldRead()) {
            readSensors();
            state = TRANSMIT;
          }
          break;
          
        case TRANSMIT:
          transmitData();
          state = READY;
          break;
          
        case ERROR:
          logger.error("Система в состоянии ошибки");
          delay(5000);
          break;
          
        case INIT:
          break;
      }
    }
    
    void printStatus() {
      Serial.print("T:");
      Serial.print(temperature);
      Serial.print("°C H:");
      Serial.print(humidity);
      Serial.print("% P:");
      Serial.print(pressure);
      Serial.println("hPa");
    }
    
  private:
    boolean initializeSensors() {
      // Инициализация датчиков
      return true;
    }
    
    boolean shouldRead() {
      return (millis() - lastReadTime) > 10000;
    }
    
    void readSensors() {
      logger.info("Чтение датчиков...");
      
      // Симулируем показания
      temperature = 20.0 + (random(0, 100) / 10.0);
      humidity = 40.0 + (random(0, 600) / 10.0);
      pressure = 1013.0 + (random(-50, 50) / 100.0);
      
      lastReadTime = millis();
      printStatus();
    }
    
    void transmitData() {
      logger.info("Передача данных в облако...");
      // Отправляем данные
      logger.info("✓ Данные отправлены");
    }
};

MeteoStation station;

void setup() {
  Serial.begin(9600);
  delay(1000);
  station.init();
}

void loop() {
  station.update();
  delay(100);
}
```

### Пример 2: Система с приоритетами задач

```cpp
class PriorityTaskQueue {
  private:
    static const int MAX_TASKS = 8;
    
    struct Task {
      const char* name;
      int priority;
      unsigned long interval;
      unsigned long lastRun;
      void (*callback)();
      boolean enabled;
    };
    
    Task tasks[MAX_TASKS];
    int taskCount;
    Logger logger;
    
  public:
    PriorityTaskQueue() : taskCount(0), logger(LL_INFO) {}
    
    void addTask(const char* name, int priority, 
                 unsigned long interval, void (*callback)()) {
      if (taskCount < MAX_TASKS) {
        tasks[taskCount].name = name;
        tasks[taskCount].priority = priority;
        tasks[taskCount].interval = interval;
        tasks[taskCount].lastRun = 0;
        tasks[taskCount].callback = callback;
        tasks[taskCount].enabled = true;
        
        Serial.print("✓ Задача добавлена: ");
        Serial.println(name);
        
        taskCount++;
      }
    }
    
    void execute() {
      // Выполняем по приоритетам (высший первый)
      for (int p = 10; p >= 0; p--) {
        for (int i = 0; i < taskCount; i++) {
          Task& t = tasks[i];
          
          if (t.enabled && t.priority == p) {
            if ((millis() - t.lastRun) >= t.interval) {
              logger.debug(t.name);
              t.callback();
              t.lastRun = millis();
            }
          }
        }
      }
    }
    
    void printSchedule() {
      Serial.println("\n=== РАСПИСАНИЕ ЗАДАЧ ===");
      for (int i = 0; i < taskCount; i++) {
        Serial.print(i);
        Serial.print(". [");
        Serial.print(tasks[i].priority);
        Serial.print("] ");
        Serial.print(tasks[i].name);
        Serial.print(" - ");
        Serial.print(tasks[i].interval);
        Serial.println("ms");
      }
      Serial.println();
    }
  };

// ИСПОЛЬЗОВАНИЕ:

PriorityTaskQueue queue;

void criticalTask() {
  Serial.println("  ⚡ КРИТИЧНАЯ ЗАДАЧА");
}

void normalTask() {
  Serial.println("  ▶️  ОБЫЧНАЯ ЗАДАЧА");
}

void backgroundTask() {
  Serial.println("   🔷 ФОНОВАЯ ЗАДАЧА");
}

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  queue.addTask("Критичная", 10, 1000, criticalTask);
  queue.addTask("Обычная", 5, 5000, normalTask);
  queue.addTask("Фоновая", 1, 10000, backgroundTask);
  
  queue.printSchedule();
}

void loop() {
  queue.execute();
  delay(10);
}
```

---

## Лучшие практики и антипаттерны

### ✅ ЛУЧШИЕ ПРАКТИКИ

```cpp
// 1. КОНСТАНТЫ ВМЕСТО МАГИЧЕСКИХ ЧИСЕЛ
#define MAX_ATTEMPTS 10
#define SENSOR_THRESHOLD 500
#define TIMEOUT_MS 5000

// 2. ПОНЯТНЫЕ ИМЕНА
int temperatureValue;       // ✓ Ясно
int t;                      // ✗ Непонятно

// 3. ОДНА ФУНКЦИЯ = ОДНА ЗАДАЧА
void readAndProcessData() {  // ✗ Делает два дела
  int data = readSensor();
  processData(data);
}

void readSensor() {          // ✓ Одна задача
  // код
}

// 4. ФУНКЦИИ С ЧЁТКИМИ ВОЗВРАЩАЕМЫМИ ЗНАЧЕНИЯМИ
ErrorCode initSystem() {     // ✓ Возвращает статус
  // ...
  return SUCCESS;
}

void initSystem() {          // ✗ Как узнать, прошла ли инициализация?
  // ...
}

// 5. КОММЕНТАРИИ ДЛЯ СЛОЖНОГО КОДА
// ✓ ХОРОШО - объясняет ЧТО и ПОЧЕМУ
// Конвертируем аналоговое значение (0-1023) в температуру (-40 до +125°C)
// Используем калибровочный коэффициент для компенсации погрешности датчика
float temp = (raw / 1024.0 * 165.0 - 40.0) * CALIBRATION_FACTOR;

// ✗ ПЛОХО - очевидный код
float temp = raw / 1024.0;  // делим на 1024

// 6. СТРУКТУРИРОВАННЫЙ КОД
// ✓ Разделено на блоки
void setup() {
  // === ИНИЦИАЛИЗАЦИЯ ===
  initializeHardware();
  initializeNetwork();
  
  // === ДИАГНОСТИКА ===
  runDiagnostics();
}

// ✗ Всё подряд
void setup() {
  // 200 строк кода
}
```

### ❌ АНТИПАТТЕРНЫ (Что НЕ делать)

```cpp
// АНТИПАТТЕРН 1: Глобальные переменные везде
int globalCounter;          // ✗ ПЛОХО
float globalTemperature;    // ✗ ПЛОХО
byte globalStatus;          // ✗ ПЛОХО

// Как исправить:
class SensorData {
  int counter;
  float temperature;
  byte status;
};

// АНТИПАТТЕРН 2: Магические числа
if (value > 512) {          // ✗ ПЛОХО - откуда 512?
  digitalWrite(13, HIGH);
}

// Как исправить:
#define THRESHOLD 512
if (value > THRESHOLD) {    // ✓ ХОРОШО
  digitalWrite(13, HIGH);
}

// АНТИПАТТЕРН 3: Огромные функции
void loop() {
  // 500 строк кода - АДСКИЙ СПАГЕТТИ
}

// Как исправить:
void loop() {
  updateSensors();
  processData();
  updateDisplay();
  handleNetwork();
}

// АНТИПАТТЕРН 4: Отсутствие обработки ошибок
WiFi.begin(ssid, password);  // ✗ ПЛОХО - не проверяем результат
sendData();                  // может не сработать

// Как исправить:
if (WiFi.begin(ssid, password) != WL_CONNECTED) {
  handleError(WIFI_ERROR);
  return;
}

if (!sendData()) {
  handleError(NETWORK_ERROR);
  return;
}

// АНТИПАТТЕРН 5: Отсутствие логирования
digitalWrite(13, HIGH);     // ✗ ПЛОХО - не знаем что произошло

// Как исправить:
digitalWrite(13, HIGH);
logger.info("LED включен");  // ✓ ХОРОШО
```

### 📋 Контрольный список качества кода

```
ПЕРЕД ЗАГРУЗКОЙ ПРОВЕРЬТЕ:

СТРУКТУРА:
  ☐ Код разделён на функции
  ☐ Каждая функция решает одну задачу
  ☐ Нет глобальных переменных (где возможно)
  ☐ Есть константы вместо магических чисел
  
НАДЁЖНОСТЬ:
  ☐ Все ошибки обработаны
  ☐ Есть таймауты для сетевых операций
  ☐ Есть проверка памяти
  ☐ Есть восстановление при сбоях
  
ПРОИЗВОДИТЕЛЬНОСТЬ:
  ☐ Нет ненужных delay()
  ☐ Большие данные в FLASH, не SRAM
  ☐ Функции оптимизированы
  ☐ Свободно минимум 500 байт памяти
  
ОТЛАДКА:
  ☐ Есть логирование
  ☐ Есть диагностика
  ☐ Можно включить DEBUG режим
  ☐ Есть тесты для компонентов
  
ДОКУМЕНТАЦИЯ:
  ☐ Есть комментарии для сложного кода
  ☐ Функции подписаны
  ☐ Есть версия и дата
  ☐ Есть описание основных переменных
  
ТЕСТИРОВАНИЕ:
  ☐ Работает > 24 часов без перезагрузок
  ☐ Работает при различных напряжениях
  ☐ Работает при температурных изменениях
  ☐ Тестировались все режимы ошибок
```

---

## 🎯 Резюме урока

На этом уроке вы научились:

✅ Проектировать архитектуру сложных систем

✅ Структурировать код на модули и функции

✅ Использовать паттерны проектирования (State Machine, классы, очереди)

✅ Оптимизировать память и производительность

✅ Обрабатывать ошибки и восстанавливаться

✅ Логировать и диагностировать проблемы

✅ Тестировать компоненты и систему

✅ Следовать лучшим практикам разработки

---

## 📚 Дополнительные материалы

### Шаблон структурированного проекта

```cpp
// ===== ПРОЕКТ: Название =====
// Версия: 1.0.0
// Автор: Ваше имя
// Дата: 01.11.2025

// ===== БЛОК 1: БИБЛИОТЕКИ =====
#include <Wire.h>
#include <EEPROM.h>

// ===== БЛОК 2: КОНСТАНТЫ =====
#define VERSION "1.0.0"
#define BAUD_RATE 9600
#define MAX_RETRIES 3

// ===== БЛОК 3: ТИПЫ ДАННЫХ =====
enum SystemState { INIT, RUNNING, ERROR };

// ===== БЛОК 4: КЛАССЫ =====
class Sensor { };
class Controller { };

// ===== БЛОК 5: ПЕРЕМЕННЫЕ =====
SystemState state = INIT;

// ===== БЛОК 6: ИНИЦИАЛИЗАЦИЯ =====
void setup() {
  Serial.begin(BAUD_RATE);
  delay(1000);
  initializeSystem();
}

// ===== БЛОК 7: ГЛАВНЫЙ ЦИК =====
void loop() {
  handleState();
  delay(100);
}

// ===== БЛОК 8: ОСНОВНЫЕ ФУНКЦИИ =====
void initializeSystem() { }
void handleState() { }

// ===== БЛОК 9: ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
void printDiagnostics() { }
```

---

## 🔗 Полезные ресурсы

- 📖 **Arduino Best Practices:** https://www.arduino.cc/en/Guide/
- 📖 **C++ для встроенных систем:** https://www.embedded.com/
- 📚 **Книга: The C Programming Language** (Kernighan, Ritchie)
- 💬 **Arduino Forum:** https://forum.arduino.cc
- 🐙 **GitHub примеры:** https://github.com/arduino/

---

**Следующий урок:** 🚀 [Итоговый проект: создание собственного IoT устройства](../Lesson_20/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 2.0 (Улучшенная)

**Дата:** 01.11.2025# 🛠️ Проектирование и отладка сложных систем на Arduino

---

## 📋 Содержание урока

1. [Введение в системное проектирование](#введение-в-системное-проектирование)
2. [Архитектура больших проектов](#архитектура-больших-проектов)
3. [Структурирование кода](#структурирование-кода)
4. [Паттерны проектирования](#паттерны-проектирования)
5. [Оптимизация памяти и производительности](#оптимизация-памяти-и-производительности)
6. [Обработка ошибок и восстановление](#обработка-ошибок-и-восстановление)
7. [Логирование и диагностика](#логирование-и-диагностика)
8. [Тестирование и отладка](#тестирование-и-отладка)
9. [Реальные примеры проектов](#реальные-примеры-проектов)
10. [Лучшие практики и антипаттерны](#лучшие-практики-и-антипаттерны)

---

## Введение в системное проектирование

### Почему нужно проектировать систему?

```
МАЛЕНЬКИЙ ПРОЕКТ (< 100 строк):
  ✓ Можно писать в одной функции loop()
  ✓ Простая отладка
  ✓ Быстрое прототипирование

СРЕДНИЙ ПРОЕКТ (100-1000 строк):
  ⚠️  Начинают появляться проблемы
  ❌ Трудно найти ошибку
  ❌ Трудно добавить функцию
  ❌ Дублирование кода

БОЛЬШОЙ ПРОЕКТ (> 1000 строк):
  🔴 НУЖНА АРХИТЕКТУРА!
  ✅ Разделение на модули
  ✅ Четкие интерфейсы
  ✅ Тестируемость
  ✅ Масштабируемость
```

### Проблемы без архитектуры

```
КОД БЕЗ АРХИТЕКТУРЫ:

❌ "Спагетти-код" (spaghetti code)
   └─ Переплетение логики, трудно разобраться

❌ Глобальные переменные везде
   └─ Непредсказуемое поведение

❌ Повторение кода (copy-paste)
   └─ Одна ошибка в 5 местах

❌ Невозможно переиспользовать
   └─ Полностью переписываешь для нового проекта

❌ Невозможно тестировать
   └─ Можешь проверить только на железе

❌ Невозможно поддерживать
   └─ Даже автор забывает как это работало
```

### Преимущества хорошей архитектуры

```
✅ МОДУЛЬНОСТЬ
   └─ Каждый модуль решает одну задачу

✅ ТЕСТИРУЕМОСТЬ
   └─ Можно тестировать каждый компонент отдельно

✅ МАСШТАБИРУЕМОСТЬ
   └─ Легко добавлять новые функции

✅ ПЕРЕИСПОЛЬЗОВАНИЕ
   └─ Код можно брать в другие проекты

✅ ПОДДЕРЖИВАЕМОСТЬ
   └─ Легко разбираться и исправлять

✅ ПРОИЗВОДИТЕЛЬНОСТЬ
   └─ Можно оптимизировать каждый модуль
```

---

## Архитектура больших проектов

### Слоистая архитектура IoT системы

```
┌──────────────────────────────────────────┐
│  LAYER 4: APPLICATION (Приложение)       │
│  ────────────────────────────────────────│
│  • Главная логика системы                │
│  • Управление состояниями                │
│  • Координация компонентов               │
│  • Пользовательские команды              │
└──────────────────────────────────────────┘
            ↕ (использует)
┌──────────────────────────────────────────┐
│  LAYER 3: BUSINESS LOGIC (Бизнес-логика) │
│  ────────────────────────────────────────│
│  • Алгоритмы обработки данных            │
│  • Правила принятия решений              │
│  • Валидация данных                      │
│  • Расчёты и преобразования              │
└──────────────────────────────────────────┘
            ↕ (использует)
┌──────────────────────────────────────────┐
│  LAYER 2: COMMUNICATION (Коммуникация)    │
│  ────────────────────────────────────────│
│  • Wi-Fi / MQTT / HTTP                   │
│  • Отправка данных                       │
│  • Получение команд                      │
│  • Обработка сетевых ошибок             │
└──────────────────────────────────────────┘
            ↕ (использует)
┌──────────────────────────────────────────┐
│  LAYER 1: HAL (Hardware Abstraction)      │
│  ────────────────────────────────────────│
│  • Датчики (DHT, BMP, pH, и т.д.)       │
│  • Исполнители (реле, моторы, LED)      │
│  • Прямое управление GPIO/I2C/SPI       │
└──────────────────────────────────────────┘
```

### Пример: Система умного полива

```
СЦЕНАРИЙ: "Если почва сухая, полить 5 минут"

╔════════════════════════════════════════════╗
║ APPLICATION                                ║
║ • Главный цикл                            ║
║ • Обработка пользовательских команд       ║
║ "Начать автоматический полив"             ║
╚════════════════════════════════════════════╝
                    ↓
╔════════════════════════════════════════════╗
║ BUSINESS LOGIC                             ║
║ • Если влажность < 30% → включить насос   ║
║ • Если влажность > 60% → выключить насос  ║
║ • Максимум 5 минут полива                 ║
╚════════════════════════════════════════════╝
                    ↓
╔════════════════════════════════════════════╗
║ COMMUNICATION                              ║
║ • Отправить статус на сервер              ║
║ • Получить команду из приложения          ║
║ • Хранить историю в облаке                ║
╚════════════════════════════════════════════╝
                    ↓
╔════════════════════════════════════════════╗
║ HAL (Hardware)                             ║
║ • Прочитать датчик влажности (A0)         ║
║ • Управлять насосом (D5)                  ║
║ • Включить LED индикатор (D13)            ║
╚════════════════════════════════════════════╝
```

---

## Структурирование кода

### Сравнение подходов: Монолит vs Модули

#### ❌ МОНОЛИТНЫЙ КОД (ПЛОХО)

```cpp
// Всё в одном месте - 500+ строк в loop()!

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  pinMode(A0, INPUT);
  // 50 строк инициализации
}

void loop() {
  // 300 строк логики в одной функции
  int reading = analogRead(A0);
  
  if (reading > 500) {
    digitalWrite(13, HIGH);
    delay(1000);
  } else {
    digitalWrite(13, LOW);
  }
  
  // Ещё 250 строк - невозможно разобраться!
}
```

**Проблемы:**
- 🔴 Трудно найти ошибку
- 🔴 Невозможно переиспользовать код
- 🔴 Трудно добавить функцию
- 🔴 Невозможно протестировать отдельные части

#### ✅ МОДУЛЬНЫЙ КОД (ХОРОШО)

```cpp
// Разделено на логические блоки

#define SENSOR_PIN A0
#define LED_PIN 13
#define THRESHOLD 500

// ===== БЛОК 1: ИНИЦИАЛИЗАЦИЯ =====
void setup() {
  Serial.begin(9600);
  initializeHardware();
  Serial.println("✓ Система готова");
}

// ===== БЛОК 2: ГЛАВНЫЙ ЦИК =====
void loop() {
  int value = readSensor();
  processValue(value);
  updateLED(value);
}

// ===== БЛОК 3: ДАТЧИК =====
void initializeHardware() {
  pinMode(SENSOR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

int readSensor() {
  return analogRead(SENSOR_PIN);
}

// ===== БЛОК 4: ОБРАБОТКА =====
void processValue(int value) {
  Serial.print("Значение: ");
  Serial.println(value);
}

// ===== БЛОК 5: УПРАВЛЕНИЕ LED =====
void updateLED(int value) {
  if (value > THRESHOLD) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
```

**Преимущества:**
- ✅ Каждая функция делает одно
- ✅ Легко найти и исправить
- ✅ Можно переиспользовать функции
- ✅ Легко тестировать

---

## Паттерны проектирования

### Паттерн 1: State Machine (Конечный автомат)

```cpp
// Система с чёткими состояниями и переходами

enum SystemState {
  BOOTING,           // Загрузка
  IDLE,              // Ожидание
  RUNNING,           // Работа
  WARNING,           // Предупреждение
  ERROR,             // Ошибка
  SHUTDOWN           // Остановка
};

SystemState state = BOOTING;
unsigned long stateEntryTime = 0;

void setup() {
  Serial.begin(9600);
  enterState(BOOTING);
}

void loop() {
  updateState();
  handleState();
}

void enterState(SystemState newState) {
  if (newState != state) {
    Serial.print("Переход: ");
    Serial.print(getStateName(state));
    Serial.print(" → ");
    Serial.println(getStateName(newState));
    
    state = newState;
    stateEntryTime = millis();
  }
}

void updateState() {
  // Проверяем условия для переходов
  switch(state) {
    case BOOTING:
      if (millis() - stateEntryTime > 2000) {
        enterState(IDLE);
      }
      break;
      
    case IDLE:
      if (userInput()) {
        enterState(RUNNING);
      }
      break;
      
    case RUNNING:
      if (systemError()) {
        enterState(ERROR);
      }
      if (systemWarning()) {
        enterState(WARNING);
      }
      break;
      
    case WARNING:
      if (millis() - stateEntryTime > 5000) {
        enterState(RUNNING);
      }
      break;
      
    case ERROR:
      if (userReset()) {
        enterState(IDLE);
      }
      break;
  }
}

void handleState() {
  // Выполняем действия в зависимости от состояния
  switch(state) {
    case BOOTING:
      Serial.println("🔄 Загрузка системы...");
      break;
      
    case IDLE:
      // Ничего не делаем, ждём команды
      break;
      
    case RUNNING:
      Serial.println("▶️  Система работает");
      break;
      
    case WARNING:
      Serial.println("⚠️  ВНИМАНИЕ!");
      break;
      
    case ERROR:
      Serial.println("❌ ОШИБКА!");
      break;
      
    case SHUTDOWN:
      Serial.println("🛑 Остановка...");
      break;
  }
}

String getStateName(SystemState s) {
  switch(s) {
    case BOOTING: return "BOOTING";
    case IDLE: return "IDLE";
    case RUNNING: return "RUNNING";
    case WARNING: return "WARNING";
    case ERROR: return "ERROR";
    case SHUTDOWN: return "SHUTDOWN";
    default: return "UNKNOWN";
  }
}

// Вспомогательные функции
boolean userInput() { return false; }
boolean systemError() { return false; }
boolean systemWarning() { return false; }
boolean userReset() { return false; }
```

### Паттерн 2: Инкапсуляция через классы

```cpp
// Класс для управления датчиком температуры

class TemperatureSensor {
  private:
    int pin;
    float lastTemperature;
    unsigned long lastReadTime;
    const float CALIBRATION = 0.95;  // Калибровка
    
  public:
    TemperatureSensor(int sensorPin) {
      pin = sensorPin;
      lastTemperature = 0;
      lastReadTime = 0;
    }
    
    void init() {
      pinMode(pin, INPUT);
      Serial.println("✓ Датчик температуры инициализирован");
    }
    
    float readTemperature() {
      int raw = analogRead(pin);
      lastTemperature = convertRawToTemperature(raw);
      lastReadTime = millis();
      return lastTemperature;
    }
    
    float getLastTemperature() const {
      return lastTemperature;
    }
    
    unsigned long getLastReadTime() const {
      return lastReadTime;
    }
    
    boolean isReading() {
      return (millis() - lastReadTime) < 5000;  // Данные свежие?
    }
    
    void printStatus() {
      Serial.print("Температура: ");
      Serial.print(lastTemperature);
      Serial.println("°C");
    }
    
  private:
    float convertRawToTemperature(int raw) {
      // Формула конвертирования
      float voltage = (raw / 1024.0) * 5.0;
      float tempC = (voltage - 0.5) * 100.0;
      return tempC * CALIBRATION;
    }
};

// ИСПОЛЬЗОВАНИЕ:

TemperatureSensor tempSensor(A0);

void setup() {
  Serial.begin(9600);
  tempSensor.init();
}

void loop() {
  float temp = tempSensor.readTemperature();
  tempSensor.printStatus();
  delay(1000);
}
```

### Паттерн 3: Очередь задач (Task Queue)

```cpp
// Система для управления несколькими задачами

struct Task {
  const char* name;
  int priority;              // 0=низкий, 1=средний, 2=высокий
  unsigned long interval;    // Интервал выполнения (мс)
  unsigned long lastRun;     // Время последнего запуска
  void (*function)();        // Функция для выполнения
  boolean enabled;           // Включена ли задача
};

class TaskScheduler {
  private:
    static const int MAX_TASKS = 10;
    Task tasks[MAX_TASKS];
    int taskCount;
    
  public:
    TaskScheduler() : taskCount(0) {}
    
    void registerTask(const char* name, int priority, 
                     unsigned long interval, void (*func)()) {
      if (taskCount < MAX_TASKS) {
        tasks[taskCount].name = name;
        tasks[taskCount].priority = priority;
        tasks[taskCount].interval = interval;
        tasks[taskCount].lastRun = 0;
        tasks[taskCount].function = func;
        tasks[taskCount].enabled = true;
        
        taskCount++;
        Serial.print("✓ Задача зарегистрирована: ");
        Serial.println(name);
      }
    }
    
    void run() {
      // Выполняем по приоритетам
      for (int p = 2; p >= 0; p--) {
        for (int i = 0; i < taskCount; i++) {
          if (tasks[i].priority == p && tasks[i].enabled) {
            if (shouldRun(i)) {
              Serial.print("→ Выполняю: ");
              Serial.println(tasks[i].name);
              
              tasks[i].function();
              tasks[i].lastRun = millis();
            }
          }
        }
      }
    }
    
    void disableTask(int index) {
      if (index < taskCount) {
        tasks[index].enabled = false;
      }
    }
    
    void enableTask(int index) {
      if (index < taskCount) {
        tasks[index].enabled = true;
      }
    }
    
    void printStatus() {
      Serial.println("\n=== СТАТУС ЗАДАЧ ===");
      for (int i = 0; i < taskCount; i++) {
        Serial.print(i);
        Serial.print(". ");
        Serial.print(tasks[i].name);
        Serial.print(" - ");
        Serial.println(tasks[i].enabled ? "ВКЛ" : "ВЫКЛ");
      }
      Serial.println();
    }
    
  private:
    boolean shouldRun(int index) {
      return (millis() - tasks[index].lastRun) >= tasks[index].interval;
    }
};

// ИСПОЛЬЗОВАНИЕ:

TaskScheduler scheduler;

void readSensors() {
  Serial.println("  [КРИТИЧНАЯ] Чтение датчиков");
}

void processData() {
  Serial.println("  [ОБЫЧНАЯ] Обработка данных");
}

void logData() {
  Serial.println("  [НИЗКАЯ] Логирование");
}

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  scheduler.registerTask("Чтение датчиков", 2, 1000, readSensors);
  scheduler.registerTask("Обработка данных", 1, 5000, processData);
  scheduler.registerTask("Логирование", 0, 10000, logData);
  
  scheduler.printStatus();
}

void loop() {
  scheduler.run();
  delay(10);
}
```

---

## Оптимизация памяти и производительности

### Анализ использования памяти

```cpp
// Функция для проверки памяти

int freeRam() {
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? 
          (int) &__heap_start : (int) __brkval);
}

void printMemoryInfo() {
  Serial.println("\n=== ИНФОРМАЦИЯ ОБ ПАМЯТИ ===");
  Serial.print("Свободная SRAM: ");
  Serial.print(freeRam());
  Serial.println(" байт");
  
  Serial.print("Использовано: ");
  Serial.print(2048 - freeRam());  // Arduino UNO имеет 2KB SRAM
  Serial.println(" байт");
  
  Serial.print("Фрагментация: ");
  float fragmentation = ((2048 - freeRam()) / 2048.0) * 100;
  Serial.print(fragmentation);
  Serial.println("%");
  
  if (freeRam() < 200) {
    Serial.println("⚠️  ВНИМАНИЕ: Критически низко памяти!");
  }
}

void setup() {
  Serial.begin(9600);
  delay(1000);
  printMemoryInfo();
}

void loop() {
  printMemoryInfo();
  delay(5000);
}
```

### Техники оптимизации памяти

```cpp
// ❌ РАСТОЧИТЕЛЬНО - много памяти тратится

void badExample() {
  String message = "Это строка";        // ~30 байт в SRAM
  String sensor = "DHT11";              // ~20 байт в SRAM
  String location = "Living Room";      // ~20 байт в SRAM
  
  Serial.println(message);
  Serial.println(sensor);
  Serial.println(location);
}

// ✅ ОПТИМАЛЬНО - используем FLASH память

void goodExample() {
  // Строки в FLASH памяти (32KB), не в SRAM (2KB)
  Serial.println(F("Это строка"));
  Serial.println(F("DHT11"));
  Serial.println(F("Living Room"));
}

// ✅ ЕЩЁ ЛУЧШЕ - используем PROGMEM

const char message[] PROGMEM = "Это строка";
const char sensor[] PROGMEM = "DHT11";

void bestExample() {
  char buffer[20];
  strcpy_P(buffer, message);
  Serial.println(buffer);
}

// ✅ МАССИВЫ В FLASH

const byte DIGIT_PATTERNS[] PROGMEM = {
  0x3F, 0x06, 0x5B, 0x4F, 0x66,
  0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

void displayDigit(int digit) {
  byte pattern = pgm_read_byte(&DIGIT_PATTERNS[digit]);
  Serial.println(pattern);
}
```

### Профилирование производительности

```cpp
// Измеряем время выполнения функций

class PerformanceMonitor {
  private:
    unsigned long startTime;
    const char* name;
    
  public:
    PerformanceMonitor(const char* taskName) : name(taskName) {
      startTime = micros();
    }
    
    ~PerformanceMonitor() {
      unsigned long duration = micros() - startTime;
      Serial.print("[PERFORMANCE] ");
      Serial.print(name);
      Serial.print(": ");
      Serial.print(duration);
      Serial.println(" µs");
    }
};

// Использование автоматически вычисляет время

void expensiveOperation() {
  PerformanceMonitor pm("Дорогая операция");
  
  float result = 0;
  for (int i = 0; i < 1000; i++) {
    result += sqrt(i);
  }
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  expensiveOperation();
  delay(1000);
}
```

---

## Обработка ошибок и восстановление

### Система кодов ошибок

```cpp
// Вместо try-catch используем коды возврата

enum ErrorCode {
  SUCCESS = 0,
  SENSOR_ERROR = 1,
  WIFI_ERROR = 2,
  TIMEOUT_ERROR = 3,
  MEMORY_ERROR = 4,
  INVALID_DATA = 5
};

ErrorCode lastError = SUCCESS;

// Функция возвращает код ошибки

ErrorCode initializeSensor() {
  if (!Wire.begin()) {
    return SENSOR_ERROR;
  }
  if (freeRam() < 100) {
    return MEMORY_ERROR;
  }
  return SUCCESS;
}

void handleError(ErrorCode error) {
  switch(error) {
    case SUCCESS:
      Serial.println("✓ ОК");
      break;
      
    case SENSOR_ERROR:
      Serial.println("❌ Ошибка датчика");
      Serial.println("   → Проверьте подключение I2C");
      Serial.println("   → Проверьте адрес датчика");
      break;
      
    case WIFI_ERROR:
      Serial.println("❌ Ошибка Wi-Fi");
      Serial.println("   → Проверьте SSID и пароль");
      Serial.println("   → Проверьте расстояние до маршрутизатора");
      break;
      
    case TIMEOUT_ERROR:
      Serial.println("❌ Timeout");
      Serial.println("   → Увеличьте время ожидания");
      Serial.println("   → Проверьте соединение");
      break;
      
    case MEMORY_ERROR:
      Serial.println("❌ Недостаточно памяти");
      Serial.println("   → Упростите код");
      Serial.println("   → Используйте FLASH вместо SRAM");
      break;
      
    case INVALID_DATA:
      Serial.println("❌ Неверные данные");
      Serial.println("   → Проверьте формат данных");
      break;
  }
  
  lastError = error;
}

void setup() {
  Serial.begin(9600);
  ErrorCode err = initializeSensor();
  handleError(err);
}

void loop() {}
```

### Механизм восстановления с EEPROM

```cpp
#include <EEPROM.h>

#define RESTART_COUNTER_ADDR 0
#define MAX_RESTART_ATTEMPTS 3
#define SAFE_MODE_TIMEOUT 60000  // 1 минута

class RestartRecovery {
  private:
    int restartCount;
    unsigned long bootTime;
    boolean inSafeMode;
    
  public:
    RestartRecovery() {
      bootTime = millis();
      inSafeMode = false;
      restartCount = EEPROM.read(RESTART_COUNTER_ADDR);
    }
    
    void init() {
      Serial.print("Попытка загрузки #");
      Serial.println(restartCount + 1);
      
      if (restartCount >= MAX_RESTART_ATTEMPTS) {
        Serial.println("🔴 КРИТИЧЕСКАЯ ОШИБКА!");
        Serial.println("Слишком много перезагрузок подряд");
        enterSafeMode();
        inSafeMode = true;
      } else {
        incrementRestartCounter();
      }
    }
    
    void loop() {
      // Если прошла 1 минута - сбросить счётчик
      if ((millis() - bootTime) > SAFE_MODE_TIMEOUT) {
        resetRestartCounter();
        Serial.println("✓ Счётчик перезагрузок сброшен");
      }
    }
    
    boolean isInSafeMode() {
      return inSafeMode;
    }
    
  private:
    void incrementRestartCounter() {
      EEPROM.write(RESTART_COUNTER_ADDR, restartCount + 1);
    }
    
    void resetRestartCounter() {
      EEPROM.write(RESTART_COUNTER_ADDR, 0);
    }
    
    void enterSafeMode() {
      Serial.println("\n⚠️  ВКЛЮЧЕН БЕЗОПАСНЫЙ РЕЖИМ");
      Serial.println("• Минимальная функциональность");
      Serial.println("• Отключены некритичные функции");
      Serial.println("• Ожидаем восстановления...\n");
    }
};

RestartRecovery recovery;

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  recovery.init();
}

void loop() {
  recovery.loop();
  
  if (recovery.isInSafeMode()) {
    // Безопасный режим - только мигаем LED
    digitalWrite(13, millis() % 1000 < 500 ? HIGH : LOW);
  } else {
    // Нормальная работа
    Serial.println("▶️  Система работает");
  }
  
  delay(1000);
}
```

---

## Логирование и диагностика

### Система логирования с уровнями

```cpp
enum LogLevel {
  LL_DEBUG = 0,
  LL_INFO = 1,
  LL_WARNING = 2,
  LL_ERROR = 3,
  LL_CRITICAL = 4
};

class Logger {
  private:
    LogLevel currentLevel;
    unsigned long sessionStart;
    int messageCount;
    
  public:
    Logger(LogLevel level = LL_INFO) {
      currentLevel = level;
      sessionStart = millis();
      messageCount = 0;
    }
    
    void setLevel(LogLevel level) {
      currentLevel = level;
      Serial.print("Уровень логирования: ");
      Serial.println(getLevelName(level));
    }
    
    void debug(const char* msg) {
      log(LL_DEBUG, "[DEBUG]", msg);
    }
    
    void info(const char* msg) {
      log(LL_INFO, "[INFO]", msg);
    }
    
    void warning(const char* msg) {
      log(LL_WARNING, "[⚠️  WARNING]", msg);
    }
    
    void error(const char* msg) {
      log(LL_ERROR, "[❌ ERROR]", msg);
    }
    
    void critical(const char* msg) {
      log(LL_CRITICAL, "[🔴 CRITICAL]", msg);
    }
    
    void printStats() {
      unsigned long uptime = (millis() - sessionStart) / 1000;
      Serial.println("\n=== СТАТИСТИКА ЛОГОВ ===");
      Serial.print("Время работы: ");
      Serial.print(uptime);
      Serial.println(" сек");
      Serial.print("Всего сообщений: ");
      Serial.println(messageCount);
      Serial.println();
    }
    
  private:
    void log(LogLevel level, const char* prefix, const char* msg) {
      if (level < currentLevel) return;
      
      // Время с начала сеанса
      unsigned long elapsed = (millis() - sessionStart) / 1000;
      
      Serial.print("[");
      if (elapsed < 10) Serial.print("0");
      if (elapsed < 100) Serial.print("0");
      Serial.print(elapsed);
      Serial.print("] ");
      
      Serial.print(prefix);
      Serial.print(" ");
      Serial.println(msg);
      
      messageCount++;
    }
    
    const char* getLevelName(LogLevel level) {
      switch(level) {
        case LL_DEBUG: return "DEBUG";
        case LL_INFO: return "INFO";
        case LL_WARNING: return "WARNING";
        case LL_ERROR: return "ERROR";
        case LL_CRITICAL: return "CRITICAL";
        default: return "UNKNOWN";
      }
    }
};

// ИСПОЛЬЗОВАНИЕ:
Logger logger(LL_DEBUG);

void setup() {
  Serial.begin(9600);
  logger.info("Система стартует");
  logger.debug("Отладка");
  logger.warning("Предупреждение");
}

void loop() {
  logger.info("Цикл");
  delay(1000);
}
```

### Диагностический монитор

```cpp
class DiagnosticMonitor {
  public:
    void printFullReport() {
      Serial.println("\n╔════════════════════════════════════════╗");
      Serial.println("║     ПОЛНЫЙ ОТЧЁТ О СИСТЕМЕ            ║");
      Serial.println("╠════════════════════════════════════════╣");
      
      printUptimeInfo();
      printMemoryInfo();
      printVersionInfo();
      
      Serial.println("╚════════════════════════════════════════╝\n");
    }
    
  private:
    void printUptimeInfo() {
      unsigned long uptime = millis() / 1000;
      int hours = uptime / 3600;
      int minutes = (uptime % 3600) / 60;
      int seconds = uptime % 60;
      
      Serial.print("║ Время: ");
      Serial.print(hours);
      Serial.print("h ");
      Serial.print(minutes);
      Serial.print("m ");
      Serial.print(seconds);
      Serial.println("s              ║");
    }
    
    void printMemoryInfo() {
      int free = freeRam();
      int used = 2048 - free;
      
      Serial.print("║ Память: ");
      Serial.print(used);
      Serial.print("/2048 байт              ║");
      
      if (free < 200) {
        Serial.println("║ ⚠️  КРИТИЧЕСКИ НИЗКО!             ║");
      }
    }
    
    void printVersionInfo() {
      Serial.println("║ Версия: 1.0.0                        ║");
      Serial.println("║ Статус: ✓ OK                         ║");
    }
    
    int freeRam() {
      extern int __heap_start, *__brkval;
      int v;
      return (int) &v - (__brkval == 0 ? 
              (int) &__heap_start : (int) __brkval);
    }
};
```

---

## Тестирование

```cpp
class TestRunner {
  private:
    int testsRun;
    int testsPassed;
    int testsFailed;
    
  public:
    TestRunner() : testsRun(0), testsPassed(0), testsFailed(0) {}
    
    void assertEquals(int expected, int actual, const char* testName) {
      testsRun++;
      if (expected == actual) {
        Serial.print("✓ PASS: ");
        testsPassed++;
      } else {
        Serial.print("✗ FAIL: ");
        testsFailed++;
      }
      Serial.println(testName);
    }
    
    void assertTrue(boolean condition, const char* testName) {
      assertEquals(1, condition ? 1 : 0, testName);
    }
    
    void printSummary() {
      Serial.println("\n╔═══════════════════════════════╗");
      Serial.println("║    РЕЗУЛЬТАТЫ ТЕСТОВ         ║");
      Serial.print("║ Всего: ");
      Serial.print(testsRun);
      Serial.println("                    ║");
      Serial.print("║ Пройдено: ");
      Serial.print(testsPassed);
      Serial.println(" ✓                ║");
      Serial.print("║ Провалено: ");
      Serial.print(testsFailed);
      Serial.println(" ✗                ║");
      Serial.println("╚═══════════════════════════════╝\n");
    }
};

// ИСПОЛЬЗОВАНИЕ:
TestRunner tester;

void testMath() {
  Serial.println("\n=== ТЕСТЫ МАТЕМАТИКИ ===");
  tester.assertEquals(4, 2 + 2, "2 + 2 = 4");
  tester.assertEquals(7, 10 - 3, "10 - 3 = 7");
}

void testGPIO() {
  Serial.println("\n=== ТЕСТЫ GPIO ===");
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  tester.assertTrue(digitalRead(13) == HIGH, "LED ON");
  digitalWrite(13, LOW);
  tester.assertTrue(digitalRead(13) == LOW, "LED OFF");
}

void setup() {
  Serial.begin(9600);
  Serial.println("╔═══════════════════════════════╗");
  Serial.println("║   ЗАПУСК НАБОРА ТЕСТОВ       ║");
  Serial.println("╚═══════════════════════════════╝");
  
  testMath();
  testGPIO();
  tester.printSummary();
}

void loop() {}
```

---

## Реальные примеры

### Пример 1: Умная метеостанция

```cpp
#include <EEPROM.h>

class MeteoStation {
  private:
    enum State { INIT, READY, TRANSMIT, ERROR };
    State state;
    Logger logger;
    
    float temperature;
    float humidity;
    float pressure;
    unsigned long lastReadTime;
    
  public:
    MeteoStation() : state(INIT), logger(LL_INFO) {}
    
    void init() {
      logger.info("Инициализация метеостанции");
      
      if (!initializeSensors()) {
        logger.critical("Ошибка датчиков!");
        state = ERROR;
        return;
      }
      
      state = READY;
      logger.info("✓ Готова");
    }
    
    void update() {
      switch(state) {
        case READY:
          if (shouldRead()) {
            readSensors();
            state = TRANSMIT;
          }
          break;
          
        case TRANSMIT:
          transmitData();
          state = READY;
          break;
          
        case ERROR:
          logger.error("Ошибка системы");
          delay(5000);
          break;
      }
    }
    
    void printStatus() {
      Serial.print("T:");
      Serial.print(temperature);
      Serial.print("°C H:");
      Serial.print(humidity);
      Serial.print("% P:");
      Serial.print(pressure);
      Serial.println("hPa");
    }
    
  private:
    boolean initializeSensors() {
      return true;
    }
    
    boolean shouldRead() {
      return (millis() - lastReadTime) > 10000;
    }
    
    void readSensors() {
      logger.info("Чтение датчиков...");
      temperature = 20.0 + (random(0, 100) / 10.0);
      humidity = 40.0 + (random(0, 600) / 10.0);
      pressure = 1013.0 + (random(-50, 50) / 100.0);
      lastReadTime = millis();
      printStatus();
    }
    
    void transmitData() {
      logger.info("Передача данных...");
      logger.info("✓ Отправлено");
    }
};

MeteoStation station;

void setup() {
  Serial.begin(9600);
  station.init();
}

void loop() {
  station.update();
  delay(100);
}
```

---

## Лучшие практики

### ✅ ПРАВИЛЬНО

```cpp
#define THRESHOLD 512        // Константы ЗАГЛАВНЫМИ
int temperatureValue;        // Понятные имена
void readSensor() { }        // Действительное имя
ErrorCode initSystem() { }   // Возвращает статус

// Комментарии для сложного кода
float temp = (raw / 1024.0 * 165.0 - 40.0) * CALIB;
```

### ❌ НЕПРАВИЛЬНО

```cpp
if (value > 512) { }         // Магические числа!
int t;                       // Непонятная переменная
void init2() { }             // Неинформативное имя
void loop() {                // 500 строк кода
  // Спагетти-код
}
```

### 📋 Контрольный список

```
ПЕРЕД ЗАГРУЗКОЙ:

СТРУКТУРА:
  ☐ Код разделён на функции
  ☐ Каждая функция решает одну задачу
  ☐ Нет глобальных переменных
  ☐ Есть константы

НАДЁЖНОСТЬ:
  ☐ Все ошибки обработаны
  ☐ Есть таймауты
  ☐ Есть восстановление
  ☐ > 500 байт свободной памяти

ОТЛАДКА:
  ☐ Есть логирование
  ☐ Есть диагностика
  ☐ Есть тесты
  ☐ Работает 24+ часа

ДОКУМЕНТАЦИЯ:
  ☐ Комментарии к сложному коду
  ☐ Версия и дата
  ☐ Описание переменных
```

---

## 📚 Шаблон проекта

```cpp
// ===== ПРОЕКТ: Название =====
// Версия: 1.0.0
// Автор: Ваше имя
// Дата: 01.11.2025

// ===== БИБЛИОТЕКИ =====
#include <Wire.h>
#include <EEPROM.h>

// ===== КОНСТАНТЫ =====
#define VERSION "1.0.0"
#define BAUD_RATE 9600

// ===== ТИПЫ ДАННЫХ =====
enum SystemState { INIT, RUNNING, ERROR };

// ===== КЛАССЫ =====
class Sensor { };

// ===== ПЕРЕМЕННЫЕ =====
SystemState state = INIT;

// ===== ИНИЦИАЛИЗАЦИЯ =====
void setup() {
  Serial.begin(BAUD_RATE);
  delay(1000);
  initializeSystem();
}

// ===== ГЛАВНЫЙ ЦИК =====
void loop() {
  handleState();
  delay(100);
}

// ===== ФУНКЦИИ =====
void initializeSystem() { }
void handleState() { }
```

---

## 🎯 Резюме

На этом уроке вы научились:

✅ Проектировать архитектуру сложных систем  
✅ Структурировать код на модули  
✅ Использовать паттерны проектирования  
✅ Оптимизировать память и производительность  
✅ Обрабатывать ошибки корректно  
✅ Логировать и диагностировать  
✅ Тестировать компоненты  
✅ Следовать лучшим практикам  

---

## 📝 Домашнее задание

1. Рефакторьте один из предыдущих проектов, разделив код на функции
2. Создайте систему логирования для вашего проекта
3. Напишите тесты для всех компонентов
4. Измерьте использование памяти
5. Добавьте обработку ошибок и восстановление
6. **Дополнительно:** Создайте систему с состояниями (State Machine)

---

## 🔗 Полезные ресурсы

- 📖 [Arduino Best Practices](https://www.arduino.cc/en/Guide/)
- 📖 [C++ для встроенных систем](https://www.embedded.com/)
- 💬 [Arduino Forum](https://forum.arduino.cc)
- 🐙 [GitHub примеры](https://github.com/arduino/)

---

**Следующий урок:** 🚀 [Урок 20: Итоговый проект - создание собственного IoT устройства](../Lesson_20/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
