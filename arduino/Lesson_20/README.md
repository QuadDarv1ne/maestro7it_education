# 🚀 Урок 20: Итоговый проект - создание собственного IoT устройства

**Версия:** 1.0  
**Дата:** 01.11.2025  
**Автор:** Дуплей Максим Игоревич

---

## 📋 Содержание

1. [Введение в итоговый проект](#введение)
2. [Выбор идеи проекта](#выбор-идеи)
3. [Проектирование системы](#проектирование)
4. [Выбор компонентов](#компоненты)
5. [Создание схемы](#схема)
6. [Разработка кода](#разработка)
7. [Тестирование](#тестирование)
8. [Облачная интеграция](#облако)
9. [Мобильное приложение](#мобильное)
10. [Презентация проекта](#презентация)

---

## Введение

### Что такое итоговый проект?

Итоговый проект - это возможность применить **все знания**, полученные за 19 уроков:

```
УРОКИ 1-16: ОСНОВЫ
  └─ GPIO, датчики, исполнители, протоколы

УРОКИ 17-18: РАСШИРЕНИЕ
  └─ Модули расширения, Wi-Fi, IoT, облако

УРОКИ 19: АРХИТЕКТУРА
  └─ Проектирование, структурирование, тестирование

ИТОГОВЫЙ ПРОЕКТ: ПРИМЕНЕНИЕ
  └─ Создание полнофункционального IoT устройства
```

### Цели проекта

```
✅ Применить все изученные технологии
✅ Создать работающее устройство
✅ Интегрировать с облаком
✅ Создать мобильный интерфейс
✅ Документировать решение
✅ Представить результаты
```

---

## Выбор идеи проекта

### Топ идей для IoT проектов

| Проект | Сложность | Компоненты | Время |
|--------|-----------|-----------|-------|
| **Метеостанция** | ⭐⭐ | DHT, BMP, ESP8266 | 20-30ч |
| **Система полива** | ⭐⭐⭐ | Датчики влаги, насос, реле | 25-35ч |
| **Умное освещение** | ⭐⭐⭐⭐ | RGB LED, датчик движения, реле | 30-40ч |
| **Система безопасности** | ⭐⭐⭐⭐ | Датчик движения, двери, камера | 35-50ч |
| **Климат контроль** | ⭐⭐⭐⭐⭐ | Датчики, кондиционер, обогреватель | 40-60ч |
| **Трекер растений** | ⭐⭐ | Датчики влаги, света, pH | 15-25ч |
| **Аквариум** | ⭐⭐⭐ | Датчики воды, света, помпы | 25-35ч |
| **Кормушка для животных** | ⭐⭐⭐ | Сервомотор, датчик, реле | 20-30ч |

### Как выбрать проект?

```
ВЫБИРАЙТЕ ПРОЕКТ, КОТОРЫЙ:

✅ Вас интересует
   └─ Будет мотивация работать

✅ Не слишком сложный
   └─ Реально завершить за 2-4 недели

✅ Имеет практическую ценность
   └─ Можно использовать в жизни

✅ Использует разные компоненты
   └─ Применить все знания

✅ Интегрируется с облаком
   └─ IoT функциональность

✅ Имеет визуальный интерфейс
   └─ Красиво показать результаты
```

### Примеры проектов студентов

```
📱 Метеостанция с облаком
   ├─ Датчики: DHT11, BMP180
   ├─ Микроконтроллер: ESP8266
   ├─ Облако: ThingSpeak
   └─ Результат: ⭐⭐⭐⭐⭐

🌱 Система умного полива
   ├─ Датчики: влажности почвы, дождя
   ├─ Исполнители: водяной насос, реле
   ├─ Управление: MQTT + Telegram
   └─ Результат: ⭐⭐⭐⭐⭐

💡 Умное освещение комнаты
   ├─ Датчики: движения, света, температуры
   ├─ Исполнители: LED, RGB, реле
   ├─ Управление: веб-интерфейс + мобильное приложение
   └─ Результат: ⭐⭐⭐⭐⭐

🎯 Трекер здоровья растений
   ├─ Датчики: влажность, свет, pH, температура
   ├─ Отправка: MQTT в облако
   ├─ Уведомления: Telegram, Email
   └─ Результат: ⭐⭐⭐⭐⭐
```

---

## Проектирование системы

### Фаза 1: Определение требований

```
1. ФУНКЦИОНАЛЬНЫЕ ТРЕБОВАНИЯ
   ├─ Какие данные собирать?
   ├─ Как часто обновлять?
   ├─ Какие действия выполнять?
   └─ Какие уведомления отправлять?

2. НЕ-ФУНКЦИОНАЛЬНЫЕ ТРЕБОВАНИЯ
   ├─ Точность измерений (±1°C, ±5%)
   ├─ Время отклика (< 1 сек)
   ├─ Надёжность (99.9% uptime)
   ├─ Длительность работы (24/7)
   └─ Бюджет ($50-200)

3. ОГРАНИЧЕНИЯ
   ├─ Питание: 5V USB или батарея
   ├─ Размер: маленький и компактный
   ├─ Шум: менее 50 дБ
   └─ Температурный диапазон: 0-50°C
```

### Фаза 2: Архитектура системы

```
┌─────────────────────────────────┐
│  ОБЛАКО (Cloud)                 │
│  ├─ Хранение данных             │
│  ├─ Аналитика                   │
│  └─ Управление                  │
└─────────────┬───────────────────┘
              │ Wi-Fi / MQTT
┌─────────────▼───────────────────┐
│  ESP8266 (Микроконтроллер)      │
│  ├─ Сбор данных                 │
│  ├─ Обработка                   │
│  ├─ Управление компонентами     │
│  └─ Синхронизация               │
└─────────────┬───────────────────┘
              │ I2C / Analog / Digital
┌─────────────▼───────────────────┐
│  ДАТЧИКИ & ИСПОЛНИТЕЛИ          │
│  ├─ DHT11 (температура)         │
│  ├─ BMP180 (давление)           │
│  ├─ Реле (вентилятор)           │
│  └─ LED (статус)                │
└─────────────────────────────────┘
```

### Фаза 3: Блок-схема операций

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
┌──────▼──────────────┐
│ Инициализация       │
│ ├─ Wi-Fi            │
│ ├─ Датчики          │
│ └─ EEPROM           │
└──────┬──────────────┘
       │
┌──────▼──────────────────┐
│ ГЛАВНЫЙ ЦИК             │
│                         │
│  1. Прочитать датчики   │◄────┐
│  2. Обработать данные   │     │
│  3. Если условие → действие    │
│  4. Отправить в облако  │     │
│  5. Ждать 30 сек        │     │
└──────┬──────────────────┘     │
       │ LOOP                ───┘
       │
       ├──▶ Ошибка?
       │    └─ Восстановление
       │
       └──▶ MQTT команда?
            └─ Выполнить действие
```

---

## Выбор компонентов

### Рекомендуемый комплект (Метеостанция)

```
КОЛИЧЕСТВО | КОМПОНЕНТ | ЦЕНА | НАЗНАЧЕНИЕ
-----------|-----------|------|----------
1 | ESP8266 D1 Mini | $5 | Микроконтроллер
1 | DHT11 | $2 | Темп. + влажность
1 | BMP180 | $2 | Давление
1 | OLED экран 128x64 | $3 | Дисплей
1 | USB кабель | $1 | Питание
1 | Макетная плата | $1 | Монтаж
10 | Перемычки | $1 | Соединения
-----------|-----------|------|----------
ИТОГО:            | $15 | Базовый набор
        +Облако: $0 | (ThingSpeak бесплатно)
        +Приложение: $0 | (Blynk бесплатно)
```

### Альтернативные компоненты

```
ДАТЧИКИ:
  ├─ Температура: DHT22, LM35, TMP36
  ├─ Влажность: DHT11/22, HS3003
  ├─ Давление: BMP180, BMP280, BMP390
  ├─ Свет: LDR, BH1750
  ├─ Влаги почвы: Capacitive Sensor, Resistive
  ├─ pH: pH электрод + ADS1115
  ├─ Движения: PIR HC-SR501
  └─ Расстояния: HC-SR04, VL53L0X

ИСПОЛНИТЕЛИ:
  ├─ Реле: SRD-05VDC, модули на 2/4/8 каналов
  ├─ LED: обычные, RGB, адресуемые (WS2812)
  ├─ Моторы: DC, сервомоторы, шаговые
  ├─ Звук: Buzzer пассивный/активный
  └─ Дисплеи: LCD 16x2, OLED 128x64, TFT

МИКРОКОНТРОЛЛЕРЫ:
  ├─ Arduino UNO (без Wi-Fi, надёжный)
  ├─ ESP8266 (Wi-Fi, мало памяти)
  ├─ ESP32 (Wi-Fi + BLE, много ресурсов)
  └─ Arduino MKR WiFi 1010 (профессиональный)
```

---

## Создание схемы

### Схема подключения (Метеостанция)

```
ESP8266 D1 Mini
┌──────────────────┐
│ GND ─────────┬───┤ GND
│ 5V  ─────────┼───┤ 5V
│ D2  ─────────┼───┤ SDA (DHT, BMP)
│ D1  ─────────┼───┤ SCL (DHT, BMP)
│ A0  ─────────┼───┤ A0 (аналоговый вход)
│ D5  ─────────┼───┤ D5 (реле/LED)
│ D6  ─────────┼───┤ D6 (RGB LED)
│ D7  ─────────┼───┤ D7 (RGB LED)
└──────────────┼───┘
               │
        ┌──────┴──────┐
        │             │
    ┌───▼───┐    ┌───▼───┐
    │ DHT11 │    │ BMP180│
    │       │    │       │
    │ GND GND│    │ GND GND│
    │ 3V3 VCC│    │ 3V3 VCC│
    │ SDA I2C│    │ SDA I2C│
    │ SCL I2C│    │ SCL I2C│
    └───────┘    └───────┘

        РЕЛЕ (D5)
        ┌─────────┐
    ─5V─┤+ IN GND ├─ GND
        │ COM NO NC│
        │         │
        └─────┬───┘
              │ 220V
           (устройство)
```

### Экспортировать схему

```
Инструменты для создания схем:
  ├─ Fritzing (визуальный, бесплатный)
  ├─ Tinkercad (онлайн, простой)
  ├─ KiCad (профессиональный, бесплатный)
  └─ LTspice (для симуляции)

Как экспортировать:
  1. Создать схему в Fritzing
  2. File → Export → Image
  3. Сохранить как PNG/PDF
  4. Вставить в документацию
```

---

## Разработка кода

### Структура проекта

```
IoT_Project/
├── README.md                 # Описание проекта
├── HARDWARE.md              # Схема и компоненты
├── CODE_STRUCTURE.md        # Архитектура кода
│
├── src/
│   ├── main.ino             # Главный файл
│   ├── sensors.h/.cpp       # Работа с датчиками
│   ├── actuators.h/.cpp     # Управление исполнителями
│   ├── cloud.h/.cpp         # Облачная интеграция
│   ├── logger.h/.cpp        # Логирование
│   └── config.h             # Конфигурация
│
├── examples/
│   ├── test_sensor.ino      # Тест датчика
│   ├── test_wifi.ino        # Тест Wi-Fi
│   └── test_relay.ino       # Тест реле
│
├── docs/
│   ├── architecture.md      # Архитектура
│   ├── api.md               # API облака
│   └── troubleshooting.md   # Решение проблем
│
└── tools/
    ├── calibration.ino      # Калибровка датчиков
    └── eeprom_manager.ino   # Управление EEPROM
```

### Полный пример кода (Метеостанция)

```cpp
// ===== ПРОЕКТ: IoT МЕТЕОСТАНЦИЯ =====
// Версия: 1.0
// Микроконтроллер: ESP8266
// Датчики: DHT11, BMP180
// Облако: ThingSpeak

#include <Wire.h>
#include <Adafruit_DHT.h>
#include <Adafruit_BMP085.h>
#include <ThingSpeak.h>
#include <ESP8266WiFi.h>
#include <EEPROM.h>

// ===== КОНФИГУРАЦИЯ =====
#define VERSION "1.0.0"
#define DHTPIN D2
#define DHTTYPE DHT11
#define RELAY_PIN D5
#define UPDATE_INTERVAL 30000  // 30 секунд

// Wi-Fi
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// ThingSpeak
unsigned long channelID = 123456;
const char* apiKey = "YOUR_API_KEY";

// ===== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;
WiFiClient client;

struct SensorData {
  float temperature;
  float humidity;
  float pressure;
  float altitude;
  unsigned long timestamp;
};

SensorData currentData;
unsigned long lastUpdate = 0;

enum SystemState {
  BOOTING,
  INITIALIZING,
  READY,
  TRANSMITTING,
  ERROR
};

SystemState state = BOOTING;

// ===== SETUP =====
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n=== IoT МЕТЕОСТАНЦИЯ v" VERSION " ===");
  
  initializeHardware();
  connectToWiFi();
  ThingSpeak.begin(client);
  
  state = READY;
  Serial.println("✓ Система готова!");
}

// ===== ГЛАВНЫЙ ЦИК =====
void loop() {
  handleState();
  
  if (millis() - lastUpdate > UPDATE_INTERVAL) {
    readSensors();
    transmitData();
    lastUpdate = millis();
  }
  
  delay(100);
}

// ===== ИНИЦИАЛИЗАЦИЯ =====
void initializeHardware() {
  Serial.println("Инициализация датчиков...");
  
  dht.begin();
  if (!bmp.begin()) {
    Serial.println("❌ Ошибка BMP180!");
    state = ERROR;
    return;
  }
  
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  
  Serial.println("✓ Датчики инициализированы");
}

// ===== ПОДКЛЮЧЕНИЕ К WI-FI =====
void connectToWiFi() {
  Serial.print("Подключение к Wi-Fi: ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  Serial.println();
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("✓ Подключено!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("❌ Ошибка подключения!");
    state = ERROR;
  }
}

// ===== ЧТЕНИЕ ДАТЧИКОВ =====
void readSensors() {
  Serial.println("\n--- Чтение датчиков ---");
  
  currentData.temperature = dht.readTemperature();
  currentData.humidity = dht.readHumidity();
  currentData.pressure = bmp.readPressure() / 100.0;
  currentData.altitude = bmp.readAltitude();
  currentData.timestamp = millis() / 1000;
  
  // Проверка на ошибки
  if (isnan(currentData.temperature) || isnan(currentData.humidity)) {
    Serial.println("❌ Ошибка чтения DHT!");
    state = ERROR;
    return;
  }
  
  printSensorData();
  checkAlerts();
}

// ===== ВЫВОД ДАННЫХ ДАТЧИКОВ =====
void printSensorData() {
  Serial.print("Температура: ");
  Serial.print(currentData.temperature);
  Serial.println("°C");
  
  Serial.print("Влажность: ");
  Serial.print(currentData.humidity);
  Serial.println("%");
  
  Serial.print("Давление: ");
  Serial.print(currentData.pressure);
  Serial.println(" hPa");
  
  Serial.print("Высота: ");
  Serial.print(currentData.altitude);
  Serial.println(" м");
}

// ===== ПРОВЕРКА УСЛОВИЙ =====
void checkAlerts() {
  // Если жарко - включить вентилятор
  if (currentData.temperature > 30.0) {
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("⚠️  Высокая температура! Вентилятор ВКЛ");
  } else if (currentData.temperature < 25.0) {
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("✓ Нормальная температура. Вентилятор ВЫКЛ");
  }
}

// ===== ПЕРЕДАЧА ДАННЫХ В ОБЛАКО =====
void transmitData() {
  Serial.println("\n--- Передача данных ---");
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ Wi-Fi не подключено!");
    state = ERROR;
    return;
  }
  
  state = TRANSMITTING;
  
  ThingSpeak.setField(1, currentData.temperature);
  ThingSpeak.setField(2, currentData.humidity);
  ThingSpeak.setField(3, currentData.pressure);
  ThingSpeak.setField(4, currentData.altitude);
  
  int code = ThingSpeak.writeFields(channelID, apiKey);
  
  if (code == 200) {
    Serial.println("✓ Данные отправлены на ThingSpeak");
  } else {
    Serial.println("❌ Ошибка отправки: " + String(code));
  }
  
  state = READY;
}

// ===== ОБРАБОТКА СОСТОЯНИЙ =====
void handleState() {
  static unsigned long lastPrint = 0;
  
  if (millis() - lastPrint > 60000) {  // Каждую минуту
    Serial.print("Статус: ");
    
    switch(state) {
      case BOOTING:
        Serial.println("🔄 ЗАГРУЗКА");
        break;
      case INITIALIZING:
        Serial.println("⚙️  ИНИЦИАЛИЗАЦИЯ");
        break;
      case READY:
        Serial.println("✓ ГОТОВА");
        break;
      case TRANSMITTING:
        Serial.println("📤 ПЕРЕДАЧА");
        break;
      case ERROR:
        Serial.println("❌ ОШИБКА!");
        break;
    }
    
    printSystemInfo();
    lastPrint = millis();
  }
}

// ===== ИНФОРМАЦИЯ О СИСТЕМЕ =====
void printSystemInfo() {
  unsigned long uptime = millis() / 1000;
  int hours = uptime / 3600;
  int minutes = (uptime % 3600) / 60;
  
  Serial.print("Время работы: ");
  Serial.print(hours);
  Serial.print("h ");
  Serial.print(minutes);
  Serial.println("m");
  
  Serial.print("Wi-Fi: ");
  Serial.println(WiFi.SSID());
  
  Serial.print("Сигнал: ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
}
```

---

## Тестирование

### Стратегия тестирования

```
УРОВЕНЬ 1: КОМПОНЕНТНОЕ ТЕСТИРОВАНИЕ
  ├─ Датчик DHT11: читает ли температуру?
  ├─ Датчик BMP180: читает ли давление?
  ├─ Реле: включается/выключается?
  └─ LED: мигает корректно?

УРОВЕНЬ 2: ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ
  ├─ Датчики → Обработка → Реле
  ├─ Датчики → Логирование
  └─ Датчики → Облако

УРОВЕНЬ 3: СИСТЕМНОЕ ТЕСТИРОВАНИЕ
  ├─ Работает 24 часа без перезагрузок
  ├─ Восстанавливается после сбоя
  ├─ Обрабатывает ошибки корректно
  └─ Питание стабильное

УРОВЕНЬ 4: ПРИЕМОЧНОЕ ТЕСТИРОВАНИЕ
  ├─ Пользователь может управлять
  ├─ Данные видны в облаке
  ├─ Уведомления работают
  └─ Интерфейс удобный
```

### Тестовые сценарии

```
СЦЕНАРИЙ 1: Холодный старт
  1. Отключить питание на 1 минуту
  2. Включить питание
  3. Проверить: загружается ли система?
  4. Проверить: подключается ли к Wi-Fi?
  5. Результат: PASS/FAIL

СЦЕНАРИЙ 2: Отсутствие Wi-Fi
  1. Отключить Wi-Fi маршрутизатор
  2. Проверить: продолжает ли система работать локально?
  3. Проверить: пытается ли переподключиться?
  4. Включить Wi-Fi обратно
  5. Проверить: автоматически ли переподключается?
  6. Результат: PASS/FAIL

СЦЕНАРИЙ 3: Ошибка датчика
  1. Отключить датчик DHT
  2. Проверить: обнаружена ли ошибка?
  3. Проверить: система продолжает работать?
  4. Проверить: есть ли попытка восстановления?
  5. Подключить датчик обратно
  6. Проверить: датчик работает?
  7. Результат: PASS/FAIL

СЦЕНАРИЙ 4: Стресс-тест
  1. Быстро включать/выключать питание 10 раз
  2. Проверить: система не сломалась
  3. Проверить: EEPROM не повреждена
  4. Результат: PASS/FAIL
```

---

## Облачная интеграция

### Использование ThingSpeak

```cpp
// 1. Зарегистрируйтесь на thingspeak.com
// 2. Создайте новый Channel
// 3. Получите Channel ID и API Key

unsigned long channelID = 123456;
const char* apiKey = "YOUR_API_KEY";

// 4. В коде используйте:
ThingSpeak.setField(1, temperature);
ThingSpeak.setField(2, humidity);
ThingSpeak.setField(3, pressure);

int code = ThingSpeak.writeFields(channelID, apiKey);

if (code == 200) {
  Serial.println("✓ Отправлено");
}
```

### Использование MQTT

```cpp
#include <PubSubClient.h>

const char* mqtt_server = "broker.mqtt-dashboard.com";
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Публикуем данные
  char tempStr[8];
  dtostrf(temperature, 1, 2, tempStr);
  client.publish("home/temperature", tempStr);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP8266Client")) {
      client.subscribe("home/command/#");
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Обработка команд из облака
}
```

---

## Мобильное приложение

### Вариант 1: Blynk (Easiest)

```cpp
#include <BlynkSimpleEsp8266.h>

char auth[] = "YOUR_BLYNK_TOKEN";
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

void setup() {
  Serial.begin(115200);
  Blynk.begin(auth, ssid, password);
}

void loop() {
  Blynk.run();
  
  // Отправляем значения на виртуальные пины
  Blynk.virtualWrite(V0, temperature);
  Blynk.virtualWrite(V1, humidity);
}

// Обработка кнопки в приложении
BLYNK_WRITE(V2) {
  int button = param.asInt();
  if (button == 1) {
    digitalWrite(RELAY_PIN, HIGH);
  } else {
    digitalWrite(RELAY_PIN, LOW);
  }
}
```

### Вариант 2: Веб-интерфейс (More Control)

```cpp
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

void setup() {
  WiFi.begin(ssid, password);
  
  server.on("/", handleRoot);
  server.on("/api/data", handleAPI);
  server.on("/api/relay", handleRelay);
  
  server.begin();
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  String html = R"(
    <!DOCTYPE html>
    <html>
    <head>
      <title>IoT Метеостанция</title>
      <style>
        body { font-family: Arial; background: #f0f0f0; }
        .container { max-


        

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
