# 🌐 Wi-Fi и IoT: Arduino с модулями ESP8266/ESP32

---

## 📋 Содержание урока

1. [Введение в IoT](#введение-в-iot)
2. [Arduino vs ESP8266 vs ESP32](#arduino-vs-esp8266-vs-esp32)
3. [Подключение и установка](#подключение-и-установка)
4. [Первое подключение к Wi-Fi](#первое-подключение-к-wi-fi)
5. [HTTP запросы и REST API](#http-запросы-и-rest-api)
6. [MQTT протокол](#mqtt-протокол)
7. [Облачные сервисы](#облачные-сервисы)
8. [Практические примеры](#практические-примеры)
9. [Справочная информация](#справочная-информация)

---

## Введение в IoT

### Что такое IoT?

**IoT (Internet of Things)** — это сеть физических устройств, собирающих и обменивающихся данными через интернет.

```
┌─────────────────────────────────────────────────┐
│ АРХИТЕКТУРА IoT СИСТЕМЫ                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  ☁️ ОБЛАКО (Cloud)                             │
│  ├─ Сервер получает данные                    │
│  ├─ Обрабатывает информацию                   │
│  ├─ Хранит историю                            │
│  └─ Отправляет команды                        │
│       ↑              ↓                         │
│       │ Wi-Fi/4G/5G  │                        │
│       │              │                         │
│  📱 УСТРОЙСТВА (Devices)                       │
│  ├─ Arduino/ESP8266/ESP32                     │
│  ├─ Датчики (температура, влажность)        │
│  ├─ Исполнители (реле, моторы)              │
│  └─ Локальный интеллект                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Реальные примеры IoT

```
МЕТЕОСТАНЦИЯ:
  1. Датчик измеряет T°C и влажность
  2. Arduino собирает данные
  3. ESP8266 отправляет в облако
  4. Пользователь видит в приложении

УМНЫЙ ДОМ:
  1. Датчик движения обнаруживает человека
  2. Arduino включает свет через реле
  3. ESP8266 отправляет уведомление на телефон
  4. Пользователь может управлять из любого места

СИСТЕМА ПОЛИВА:
  1. Датчик влажности почвы показывает 40%
  2. Arduino включает насос
  3. ESP8266 логирует действие
  4. Сервер анализирует паттерны полива
  5. Рекомендует оптимальное время полива
```

---

## Arduino vs ESP8266 vs ESP32

### Сравнение платформ

```
┌────────────────┬──────────────┬──────────────┬──────────────┐
│ Характеристика │ Arduino UNO  │ ESP8266      │ ESP32        │
├────────────────┼──────────────┼──────────────┼──────────────┤
│ Процессор      │ ATmega328    │ Xtensa       │ Xtensa (2)   │
│ Частота        │ 16 MHz       │ 80/160 MHz   │ 80/160 MHz   │
│ ОЗУ (SRAM)     │ 2 KB         │ 160 KB       │ 520 KB       │
│ FLASH          │ 32 KB        │ 4 MB         │ 16 MB        │
│ GPIO           │ 14           │ 11           │ 34           │
│ ADC            │ 6 (10-bit)   │ 1 (10-bit)   │ 18 (12-bit)  │
│ PWM            │ 6            │ 4            │ 16           │
│ UART           │ 1            │ 1            │ 3            │
│ I2C            │ 1            │ 1            │ 2            │
│ SPI            │ 1            │ 2            │ 4            │
│                │              │              │              │
│ Wi-Fi          │ ❌           │ ✅ 802.11b/g│ ✅ 802.11b/g │
│ Bluetooth      │ ❌           │ ❌           │ ✅ BLE+BR/EDR│
│ Цена           │ $10-15       │ $3-5         │ $7-12        │
│                │              │              │              │
│ Идеален для    │ Базовые      │ IoT + WiFi   │ Сложные      │
│                │ проекты      │ проекты      │ IoT системы  │
│                │              │              │ с BLE        │
└────────────────┴──────────────┴──────────────┴──────────────┘
```

### Когда что использовать?

```
ИСПОЛЬЗУЙ ARDUINO UNO ЕСЛИ:
  ✓ Работаешь с аналоговыми датчиками
  ✓ Нужна максимальная стабильность
  ✓ Не нужен интернет
  ✓ Просто нужен контроллер
  ✓ Учишь основы программирования

ИСПОЛЬЗУЙ ESP8266 ЕСЛИ:
  ✓ Нужен Wi-Fi
  ✓ Бюджет ограничен
  ✓ Один датчик/исполнитель
  ✓ IoT проект начального уровня
  ✓ Не нужен Bluetooth

ИСПОЛЬЗУЙ ESP32 ЕСЛИ:
  ✓ Нужен Wi-Fi + Bluetooth
  ✓ Много GPIO и ADC
  ✓ Сложный проект
  ✓ Нужна высокая производительность
  ✓ Требуется несколько UART портов
```

---

## Подключение и установка

### Физическое подключение ESP8266

```
ESP8266 (WeMos D1 Mini)

┌────────────────────┐
│ USB                │ ← Подключи сюда USB кабель
├────────────────────┤
│                    │
│ D1  ∘∘  5V         │
│ D2  ∘∘  GND        │
│ D3  ∘∘  3V3        │
│ D4  ∘∘  RX         │
│ D5  ∘∘  TX         │
│ D6  ∘∘  D0         │
│ D7  ∘∘  D8         │
│ D8  ∘∘  RST        │
│                    │
└────────────────────┘

⚠️  ВАЖНО!
   Используй 3.3V, НЕ 5V!
   (может сгореть микроконтроллер)
```

### Установка Arduino IDE для ESP8266

```
ШАГ 1: Откройте Arduino IDE

ШАГ 2: Файл → Параметры (File → Preferences)

ШАГ 3: Найдите поле "Дополнительные URL для менеджера плат"
        Добавьте:
        https://arduino.esp8266.com/stable/package_esp8266com_index.json

ШАГ 4: Нажмите OK

ШАГ 5: Инструменты → Плата → Менеджер плат
        (Tools → Board → Boards Manager)

ШАГ 6: Поиск: "ESP8266"

ШАГ 7: Найдите "esp8266 by ESP8266 Community"
        Нажмите "Install"

ШАГ 8: Ждите установки (~100 МБ)

ШАГ 9: Инструменты → Плата → "Generic ESP8266 Module"
        или "WeMos D1 Mini" (если используешь WeMos)

ШАГ 10: Инструменты → Порт → Выбрать COM порт
         (обычно это COM3, COM4 или /dev/ttyUSB0)
```

### Установка для ESP32

```
ШАГ 1: Файл → Параметры

ШАГ 2: Добавьте в "Дополнительные URL":
        https://dl.espressif.com/dl/package_esp32_index.json

ШАГ 3: Инструменты → Плата → Менеджер плат

ШАГ 4: Поиск: "ESP32"

ШАГ 5: Установите "esp32 by Espressif Systems"

ШАГ 6: Инструменты → Плата → "ESP32 Dev Module"

ШАГ 7: Выберите COM порт
```

### Первая загрузка - Blink для ESP8266

```cpp
// ESP8266 Blink - мигание встроенного LED
// Используем D4 (встроенный LED на WeMos D1 Mini)

void setup() {
  Serial.begin(115200);
  delay(1000);
  pinMode(D4, OUTPUT);
  Serial.println("✓ Blink ESP8266 запущен!");
}

void loop() {
  digitalWrite(D4, LOW);   // Светодиод ВКЛ (инверсия!)
  Serial.println("LED ON");
  delay(1000);
  
  digitalWrite(D4, HIGH);  // Светодиод ВЫКЛ
  Serial.println("LED OFF");
  delay(1000);
}

// ⚠️  ВАЖНО: На ESP8266 логика ИНВЕРСИРОВАНА!
//    LOW = светодиод горит
//    HIGH = светодиод выключен
```

---

## Первое подключение к Wi-Fi

### Сканирование доступных сетей

```cpp
#include <ESP8266WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n=== Сканирование Wi-Fi сетей ===");
  
  // Включаем режим станции (подключение к сети)
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  
  // Начинаем сканирование
  Serial.println("Сканирование...");
  int networks = WiFi.scanNetworks();
  
  Serial.println("\nНайденные сети:");
  for (int i = 0; i < networks; ++i) {
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.print(WiFi.SSID(i));           // Имя сети
    Serial.print(" (");
    Serial.print(WiFi.RSSI(i));           // Мощность сигнала
    Serial.print(" dBm) ");
    Serial.println(WiFi.isHidden(i) ? "СКРЫТАЯ" : "ОТКРЫТАЯ");
  }
}

void loop() {
  delay(1000);
}
```

### Подключение к Wi-Fi

```cpp
#include <ESP8266WiFi.h>

// Замените на свои данные!
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n=== Подключение к Wi-Fi ===");
  Serial.print("Подключение к: ");
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
    Serial.println("✓ ПОДКЛЮЧЕНО!");
    Serial.print("IP адрес: ");
    Serial.println(WiFi.localIP());
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
    Serial.print("Мощность сигнала: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("✗ ОШИБКА подключения");
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Подключено");
  } else {
    Serial.println("Отключено");
  }
  delay(5000);
}
```

### Управление подключением через Serial

```cpp
#include <ESP8266WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n=== Wi-Fi Управление ===");
  Serial.println("Команды:");
  Serial.println("  SCAN - сканировать сети");
  Serial.println("  CONNECT SSID PASSWORD - подключиться");
  Serial.println("  DISCONNECT - отключиться");
  Serial.println("  STATUS - статус подключения");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd == "SCAN") {
      scanNetworks();
    }
    else if (cmd.startsWith("CONNECT")) {
      // Пример: CONNECT MyWiFi mypassword
      int spaceIndex = cmd.indexOf(' ');
      String ssid = cmd.substring(8, cmd.indexOf(' ', 8));
      String password = cmd.substring(cmd.indexOf(' ', 8) + 1);
      
      connectToWiFi(ssid.c_str(), password.c_str());
    }
    else if (cmd == "DISCONNECT") {
      WiFi.disconnect();
      Serial.println("✓ Отключено от Wi-Fi");
    }
    else if (cmd == "STATUS") {
      printStatus();
    }
  }
}

void scanNetworks() {
  Serial.println("Сканирование...");
  int n = WiFi.scanNetworks();
  Serial.println("Найдено сетей: " + String(n));
  for (int i = 0; i < n; i++) {
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.print(WiFi.SSID(i));
    Serial.print(" (");
    Serial.print(WiFi.RSSI(i));
    Serial.println(" dBm)");
  }
}

void connectToWiFi(const char* ssid, const char* password) {
  Serial.println("Подключение к " + String(ssid));
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  Serial.println();
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("✓ ПОДКЛЮЧЕНО!");
    Serial.println("IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("✗ ОШИБКА подключения");
  }
}

void printStatus() {
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Статус: ПОДКЛЮЧЕНО");
    Serial.println("Сеть: " + WiFi.SSID());
    Serial.println("IP: " + WiFi.localIP().toString());
    Serial.print("Сигнал: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("Статус: НЕ ПОДКЛЮЧЕНО");
  }
}
```

---

## HTTP запросы и REST API

### Отправка GET запроса

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  WiFi.begin(ssid, password);
  
  Serial.print("Подключение к Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n✓ Подключено!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    // Публичный API для тестирования
    String url = "http://jsonplaceholder.typicode.com/todos/1";
    
    Serial.println("\nОтправка GET запроса...");
    Serial.println("URL: " + url);
    
    http.begin(url);
    
    // Отправляем запрос
    int httpCode = http.GET();
    
    Serial.print("HTTP Код: ");
    Serial.println(httpCode);
    
    if (httpCode > 0) {
      // Получаем ответ
      String payload = http.getString();
      Serial.println("\nОтвет:");
      Serial.println(payload);
    } else {
      Serial.println("Ошибка запроса!");
    }
    
    http.end();
  }
  
  delay(10000);  // Запрос каждые 10 секунд
}
```

### Отправка POST запроса с JSON

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("✓ Wi-Fi подключено!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Создаём JSON объект
    DynamicJsonDocument doc(200);
    doc["temperature"] = 25.3;
    doc["humidity"] = 60;
    doc["device"] = "weather_station_01";
    
    // Преобразуем в строку
    String json;
    serializeJson(doc, json);
    
    Serial.println("Отправляемые данные:");
    Serial.println(json);
    
    // Отправляем POST
    HTTPClient http;
    String url = "http://jsonplaceholder.typicode.com/posts";
    
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST(json);
    
    Serial.print("HTTP Код: ");
    Serial.println(httpCode);
    
    if (httpCode == 201) {
      Serial.println("✓ Данные успешно отправлены!");
      String response = http.getString();
      Serial.println("Ответ: " + response);
    } else {
      Serial.println("✗ Ошибка при отправке");
    }
    
    http.end();
  }
  
  delay(30000);  // Отправляем каждые 30 секунд
}
```

### Создание простого REST API на ESP8266

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "ESP8266_AP";
const char* password = "12345678";

ESP8266WebServer server(80);

// Данные устройства
float temperature = 23.5;
float humidity = 55.0;
boolean pump_status = false;
int light_brightness = 50;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Создаём точку доступа (AP mode)
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  
  Serial.println("\n=== REST API сервер ===");
  Serial.println("SSID: " + String(ssid));
  Serial.println("IP: " + WiFi.softAPIP().toString());
  
  // Определяем маршруты
  server.on("/", handleRoot);
  server.on("/api/sensor", handleSensor);
  server.on("/api/pump", handlePump);
  server.on("/api/pump/on", handlePumpOn);
  server.on("/api/pump/off", handlePumpOff);
  server.on("/api/light", handleLight);
  
  server.begin();
  Serial.println("✓ Сервер запущен!");
}

void loop() {
  server.handleClient();
  
  // Симуляция изменения данных
  static unsigned long lastUpdate = 0;
  if (millis() - lastUpdate > 5000) {
    lastUpdate = millis();
    temperature += random(-10, 10) / 10.0;
    humidity += random(-5, 5) / 10.0;
  }
}

void handleRoot() {
  String html = "<!DOCTYPE html><html>";
  html += "<head><meta charset='UTF-8'>";
  html += "<title>ESP8266 API</title>";
  html += "</head>";
  html += "<body>";
  html += "<h1>🌐 REST API Сервер</h1>";
  html += "<p>Температура: " + String(temperature) + "°C</p>";
  html += "<p>Влажность: " + String(humidity) + "%</p>";
  html += "<p>Насос: " + String(pump_status ? "ВКЛ" : "ВЫКЛ") + "</p>";
  html += "<p>Яркость: " + String(light_brightness) + "%</p>";
  html += "</body>";
  html += "</html>";
  
  server.send(200, "text/html; charset=utf-8", html);
}

void handleSensor() {
  String json = "{\"temperature\":" + String(temperature) + 
                ",\"humidity\":" + String(humidity) + "}";
  server.send(200, "application/json", json);
}

void handlePump() {
  String json = "{\"pump_status\":" + String(pump_status ? "true" : "false") + "}";
  server.send(200, "application/json", json);
}

void handlePumpOn() {
  pump_status = true;
  Serial.println("Насос включен через API");
  server.send(200, "application/json", "{\"status\":\"on\"}");
}

void handlePumpOff() {
  pump_status = false;
  Serial.println("Насос выключен через API");
  server.send(200, "application/json", "{\"status\":\"off\"}");
}

void handleLight() {
  if (server.hasArg("brightness")) {
    light_brightness = server.arg("brightness").toInt();
    if (light_brightness > 255) light_brightness = 255;
    if (light_brightness < 0) light_brightness = 0;
    
    Serial.print("Яркость установлена: ");
    Serial.println(light_brightness);
  }
  
  String json = "{\"brightness\":" + String(light_brightness) + "}";
  server.send(200, "application/json", json);
}
```

---

## MQTT протокол

### Что такое MQTT?

**MQTT** (Message Queuing Telemetry Transport) — это облегчённый протокол обмена сообщениями для IoT.

```
КОНЦЕПЦИЯ:

PUBLISHER (издатель)    →    BROKER (брокер)    ←    SUBSCRIBER (подписчик)
                          (mosquitto, HiveMQ и т.д.)

ПРИМЕР:
ESP8266 публикует:              Брокер получает      Android app подписана:
"home/temp" = 25.3      →       и распределяет    →   "home/temp"
                                                        Получает: 25.3

ПРЕИМУЩЕСТВА:
  ✓ Малый трафик (даже меньше чем HTTP)
  ✓ Надёжен при плохой связи (повторная отправка)
  ✓ "Подписка" на события (не нужно постоянно опрашивать)
  ✓ Централизованный брокер
  ✓ Идеален для IoT
```

### Подключение к публичному MQTT брокеру

```cpp
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "broker.mqtt-dashboard.com";  // Публичный брокер

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n=== MQTT Клиент ===");
  
  // Подключение к Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Подключение к Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✓ Wi-Fi подключено!");
  
  // Подключение к MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  // Переподключиться если отключился
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Публикуем данные каждые 10 секунд
  static unsigned long lastMsg = 0;
  unsigned long now = millis();
  if (now - lastMsg > 10000) {
    lastMsg = now;
    
    float temperature = 25.3 + (random(-50, 50) / 100.0);
    float humidity = 60.0 + (random(-100, 100) / 100.0);
    
    // Преобразуем в строки
    char tempStr[8], humStr[8];
    dtostrf(temperature, 1, 2, tempStr);
    dtostrf(humidity, 1, 2, humStr);
    
    // Публикуем
    client.publish("home/temperature", tempStr);
    client.publish("home/humidity", humStr);
    
    Serial.print("Опубликовано: temp=");
    Serial.print(temperature);
    Serial.print(", humidity=");
    Serial.println(humidity);
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Подключение к MQTT...");
    
    // Генерируем уникальный ID
    String clientId = "ESP8266-";
    clientId += String(random(0xffff), HEX);
    
    // Пытаемся подключиться
    if (client.connect(clientId.c_str())) {
      Serial.println("✓ Подключено!");
      
      // Подписываемся на топики
      client.subscribe("home/lamp/command");
      client.subscribe("home/pump/command");
      
    } else {
      Serial.print("✗ Ошибка: ");
      Serial.println(client.state());
      delay(5000);
    }
  }
}

// Обработка входящих сообщений
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Получено [");
  Serial.print(topic);
  Serial.print("]: ");
  
  // Преобразуем payload в строку
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);
  
  // Обработка команд
  if (String(topic) == "home/lamp/command") {
    if (message == "ON") {
      Serial.println("→ Лампа ВКЛЮЧЕНА");
      // digitalWrite(LED_PIN, HIGH);
    } else if (message == "OFF") {
      Serial.println("→ Лампа ВЫКЛЮЧЕНА");
      // digitalWrite(LED_PIN, LOW);
    }
  }
}
```

### Публичные MQTT брокеры

```
📍 MOSQUITTO (Рекомендуется для начинающих)
   Адрес: broker.mqtt-dashboard.com
   Порт: 1883 (без шифрования)
   Топики: любые (home/*, test/*, и т.д.)
   Веб-интерфейс: http://www.mqtt-dashboard.com/
   Особенность: Полностью бесплатный, видны все сообщения

📍 HiveMQ
   Адрес: broker.hivemq.com
   Порт: 1883
   Веб-интерфейс: есть
   Особенность: Надёжный и быстрый

📍 Adafruit IO (с аккаунтом)
   Адрес: io.adafruit.com
   Порт: 1883
   Требует: Регистрация + токен
   Плюсы: Облачное хранилище, графики

⚠️  ВАЖНО: Публичные брокеры видят все данные!
   Используй только для тестов, не для приватных данных
```

---

## Облачные сервисы

### ThingSpeak

```cpp
#include <ESP8266WiFi.h>
#include <ThingSpeak.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* server = "api.thingspeak.com";
unsigned long channelID = 123456;  // Твой Channel ID
const char* apiKey = "YOUR_API_KEY";

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  
  Serial.println("✓ Wi-Fi подключено!");
  ThingSpeak.begin(client);
}

void loop() {
  // Снимаем показания датчиков
  float temperature = 25.3 + (random(-50, 50) / 100.0);
  float humidity = 60.0 + (random(-100, 100) / 100.0);
  float pressure = 1013.25;
  
  // Устанавливаем значения для полей
  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);
  ThingSpeak.setField(3, pressure);
  
  // Отправляем на ThingSpeak
  int code = ThingSpeak.writeFields(channelID, apiKey);
  
  if (code == 200) {
    Serial.println("✓ Данные отправлены на ThingSpeak");
  } else {
    Serial.println("✗ Ошибка: " + String(code));
  }
  
  // ThingSpeak требует минимум 15 секунд между запросами
  delay(20000);
}
```

---

## Практические примеры

### Пример 1: Метеостанция с отправкой на облако

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* server = "http://api.example.com";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n✓ Подключено!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Симулируем показания датчиков
    float temperature = 20.0 + (random(0, 150) / 10.0);
    float humidity = 30.0 + (random(0, 700) / 10.0);
    
    Serial.print("Температура: ");
    Serial.print(temperature);
    Serial.print("°C, Влажность: ");
    Serial.println(humidity);
    
    // Отправляем на сервер
    HTTPClient http;
    String url = String(server) + "/api/weather?temp=" + 
                 String(temperature) + "&humidity=" + String(humidity);
    
    http.begin(url);
    int httpCode = http.GET();
    
    if (httpCode == 200) {
      Serial.println("✓ Данные отправлены");
    } else {
      Serial.println("✗ Ошибка: " + String(httpCode));
    }
    
    http.end();
  }
  
  delay(60000);  // Отправляем каждую минуту
}
```

### Пример 2: Умный дом с веб-интерфейсом

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "SmartHome_AP";
const char* password = "12345678";

ESP8266WebServer server(80);

// Пины для управления
const int LAMP1 = D8;
const int LAMP2 = D7;
const int PUMP = D6;

// Состояния
boolean lamp1_state = false;
boolean lamp2_state = false;
boolean pump_state = false;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Инициализация пинов
  pinMode(LAMP1, OUTPUT);
  pinMode(LAMP2, OUTPUT);
  pinMode(PUMP, OUTPUT);
  
  digitalWrite(LAMP1, LOW);
  digitalWrite(LAMP2, LOW);
  digitalWrite(PUMP, LOW);
  
  // Запуск точки доступа
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  
  Serial.println("\n=== Умный дом ===");
  Serial.println("SSID: " + String(ssid));
  Serial.println("IP: " + WiFi.softAPIP().toString());
  
  // Маршруты
  server.on("/", handleRoot);
  server.on("/api/lamp1/toggle", handleLamp1Toggle);
  server.on("/api/lamp2/toggle", handleLamp2Toggle);
  server.on("/api/pump/toggle", handlePumpToggle);
  server.on("/api/status", handleStatus);
  
  server.begin();
  Serial.println("✓ Сервер запущен!");
}

void loop() {
  server.handleClient();
  delay(10);
}

void handleRoot() {
  String html = "<!DOCTYPE html><html>";
  html += "<head><meta charset='UTF-8'>";
  html += "<title>Умный дом</title>";
  html += "<style>";
  html += "body { font-family: Arial; margin: 20px; background: #f0f0f0; }";
  html += ".device { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }";
  html += ".button { padding: 10px 20px; margin: 5px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }";
  html += ".button:hover { background: #45a049; }";
  html += ".on { background: #2196F3; }";
  html += ".off { background: #f44336; }";
  html += "h1 { color: #333; }";
  html += "p { margin: 5px 0; }";
  html += "</style></head>";
  html += "<body>";
  html += "<h1>🏠 Система Умного Дома</h1>";
  
  html += "<div class='device'>";
  html += "<h2>💡 Лампа 1</h2>";
  html += "<p>Статус: <b>" + String(lamp1_state ? "ВКЛ" : "ВЫКЛ") + "</b></p>";
  html += "<button class='button " + String(lamp1_state ? "on" : "off") + "' onclick=\"fetch('/api/lamp1/toggle').then(() => location.reload())\">Переключить</button>";
  html += "</div>";
  
  html += "<div class='device'>";
  html += "<h2>💡 Лампа 2</h2>";
  html += "<p>Статус: <b>" + String(lamp2_state ? "ВКЛ" : "ВЫКЛ") + "</b></p>";
  html += "<button class='button " + String(lamp2_state ? "on" : "off") + "' onclick=\"fetch('/api/lamp2/toggle').then(() => location.reload())\">Переключить</button>";
  html += "</div>";
  
  html += "<div class='device'>";
  html += "<h2>💧 Насос</h2>";
  html += "<p>Статус: <b>" + String(pump_state ? "ВКЛ" : "ВЫКЛ") + "</b></p>";
  html += "<button class='button " + String(pump_state ? "on" : "off") + "' onclick=\"fetch('/api/pump/toggle').then(() => location.reload())\">Переключить</button>";
  html += "</div>";
  
  html += "</body></html>";
  
  server.send(200, "text/html; charset=utf-8", html);
}

void handleLamp1Toggle() {
  lamp1_state = !lamp1_state;
  digitalWrite(LAMP1, lamp1_state ? HIGH : LOW);
  server.send(200, "application/json", "{\"status\":\"" + String(lamp1_state ? "on" : "off") + "\"}");
  Serial.println("Лампа 1: " + String(lamp1_state ? "ВКЛ" : "ВЫКЛ"));
}

void handleLamp2Toggle() {
  lamp2_state = !lamp2_state;
  digitalWrite(LAMP2, lamp2_state ? HIGH : LOW);
  server.send(200, "application/json", "{\"status\":\"" + String(lamp2_state ? "on" : "off") + "\"}");
  Serial.println("Лампа 2: " + String(lamp2_state ? "ВКЛ" : "ВЫКЛ"));
}

void handlePumpToggle() {
  pump_state = !pump_state;
  digitalWrite(PUMP, pump_state ? HIGH : LOW);
  server.send(200, "application/json", "{\"status\":\"" + String(pump_state ? "on" : "off") + "\"}");
  Serial.println("Насос: " + String(pump_state ? "ВКЛ" : "ВЫКЛ"));
}

void handleStatus() {
  String json = "{\"lamp1\":" + String(lamp1_state ? "true" : "false") +
                ",\"lamp2\":" + String(lamp2_state ? "true" : "false") +
                ",\"pump\":" + String(pump_state ? "true" : "false") + "}";
  server.send(200, "application/json", json);
}
```

### Пример 3: IoT датчик температуры с MQTT

```cpp
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "broker.mqtt-dashboard.com";

WiFiClient espClient;
PubSubClient client(espClient);

const char* device_id = "esp8266_weather";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n✓ Wi-Fi подключено!");
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // Отправляем данные каждые 30 секунд
  static unsigned long lastMsg = 0;
  unsigned long now = millis();
  if (now - lastMsg > 30000) {
    lastMsg = now;
    publishData();
  }
}

void publishData() {
  // Симулируем показания датчика
  float temperature = 20.0 + (random(0, 150) / 10.0);
  float humidity = 40.0 + (random(0, 500) / 10.0);
  
  // Преобразуем в строки
  char tempStr[8], humStr[8];
  dtostrf(temperature, 1, 2, tempStr);
  dtostrf(humidity, 1, 2, humStr);
  
  // Публикуем
  client.publish("home/temperature", tempStr);
  client.publish("home/humidity", humStr);
  client.publish("home/device/status", "online");
  
  Serial.print("Опубликовано: T=");
  Serial.print(temperature);
  Serial.print("°C H=");
  Serial.println(humidity);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Подключение к MQTT...");
    
    String clientId = device_id;
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("✓ Подключено!");
      
      // Публикуем статус
      client.publish("home/device/status", "online");
      
      // Подписываемся
      client.subscribe("home/command/#");
      
    } else {
      Serial.print("✗ Ошибка: ");
      Serial.println(client.state());
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("Получено [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);
}
```

---

## Справочная информация

### Установка необходимых библиотек

```
1. ArduinoJson (для JSON)
   Arduino IDE → Sketch → Include Library → Manage Libraries
   Поиск: "ArduinoJson"
   Установить: "ArduinoJson by Benoit Blanchon" (версия 6.0+)

2. PubSubClient (для MQTT)
   Поиск: "PubSubClient"
   Установить: "PubSubClient by Nick O'Leary"

3. ThingSpeak (опционально)
   Поиск: "ThingSpeak"
   Установить: "ThingSpeak by MathWorks"
```

### Таблица статусов Wi-Fi

```
WL_CONNECTED = 3        ✓ Подключено
WL_IDLE_STATUS = 0      ⏳ Инициализация
WL_NO_SSID_AVAIL = 1    ✗ Сеть не найдена
WL_SCAN_COMPLETED = 2   ℹ  Сканирование завершено
WL_CONNECT_FAILED = 4   ✗ Ошибка подключения
WL_CONNECTION_LOST = 5  ✗ Соединение потеряно
WL_DISCONNECTED = 6     ✗ Отключено
```

### Таблица кодов MQTT

```
client.state():
  -4: Connection lost
  -3: Connect failed
  -2: Not connected
  -1: Disconnected
  0: Connected ✓
  1: Bad protocol version
  2: Bad client identifier
  3: Server unavailable
  4: Bad username/password
  5: Not authorized
```

### Сравнение облачных платформ

```
┌──────────────┬─────────────┬─────────────┬─────────────┐
│ Платформа    │ ThingSpeak  │ Blynk       │ MQTT Broker │
├──────────────┼─────────────┼─────────────┼─────────────┤
│ Цена         │ Бесплатный  │ Бесплатный  │ Бесплатный  │
│              │ +платный    │ +платный    │             │
│ Сложность    │ ⭐⭐ Легко   │ ⭐⭐⭐ Сред.│ ⭐⭐⭐ Сред.│
│ Графики      │ ✅ Есть     │ ✅ Есть     │ ❌ Нет      │
│ Мобильное app│ ✅ Есть     │ ✅ Есть     │ ❌ Нужно    │
│ Real-time    │ Хорошо      │ Отличный    │ Отличный    │
│ Настройка    │ 5 мин       │ 10 мин      │ 15 мин      │
│ Идеален для  │ Обучение    │ Мобильное   │ Домашний    │
│              │             │ управление  │ сервер      │
└──────────────┴─────────────┴─────────────┴─────────────┘
```

### Быстрая справка по командам

```cpp
// Wi-Fi
WiFi.begin(ssid, password);        // Подключиться
WiFi.disconnect();                  // Отключиться
WiFi.status();                      // Получить статус
WiFi.localIP();                     // Получить IP адрес
WiFi.RSSI();                        // Мощность сигнала (dBm)

// HTTP
HTTPClient http;
http.begin(url);                    // Начать подключение
http.GET();                         // GET запрос
http.POST(data);                    // POST запрос
http.getString();                   // Получить ответ
http.end();                         // Закончить

// MQTT
PubSubClient client(espClient);
client.setServer(broker, port);     // Установить брокер
client.connect(id);                 // Подключиться
client.publish(topic, msg);         // Опубликовать
client.subscribe(topic);            // Подписаться
client.loop();                      // Обработать сообщения

// JSON
DynamicJsonDocument doc(200);
doc["key"] = value;                 // Установить
serializeJson(doc, json);           // В строку
deserializeJson(doc, json);         // Из строки
```

---

## 🎯 Резюме урока

На этом уроке вы научились:

✅ Различать Arduino, ESP8266, ESP32

✅ Устанавливать IDE для ESP8266/ESP32

✅ Подключаться к Wi-Fi сетям

✅ Сканировать доступные сети

✅ Отправлять GET/POST HTTP запросы

✅ Создавать REST API на ESP8266

✅ Использовать MQTT для обмена данными

✅ Интегрироваться с облачными сервисами

---

## 📝 Домашнее задание

1. Подключитесь к Wi-Fi и выведите IP адрес в Serial монитор

2. Отправьте GET запрос на публичный API (например, jsonplaceholder.typicode.com)

3. Создайте REST API с 2 эндпоинтами (GET для чтения, POST для управления)

4. Подключитесь к публичному MQTT брокеру и опубликуйте сообщение

5. Создайте метеостанцию, отправляющую данные каждые 5 минут

6. Дополнительно: Создайте веб-интерфейс управления 3 устройствами

---

## 🔗 Полезные ссылки

- 📖 **ESP8266 Arduino:** https://arduino-esp8266.readthedocs.io/
- 📖 **ESP32 Arduino:** https://docs.espressif.com/projects/arduino-esp32/
- 📖 **MQTT Протокол:** https://mqtt.org/
- 🐙 **GitHub Arduino-esp8266:** https://github.com/esp8266/Arduino
- 💬 **Arduino Forum:** https://forum.arduino.cc
- 🌐 **MQTT Broker List:** https://github.com/mqtt/mqtt.github.io/wiki/public_brokers

---

## Ключевые термины

| Термин | Значение |
|--------|----------|
| **IoT** | Internet of Things - сеть устройств в интернете |
| **REST** | Representational State Transfer - архитектура веб-сервисов |
| **HTTP** | HyperText Transfer Protocol - протокол передачи данных |
| **MQTT** | Message Queuing Telemetry Transport - облегчённый протокол |
| **JSON** | JavaScript Object Notation - формат данных |
| **API** | Application Programming Interface - интерфейс приложения |
| **Wi-Fi** | Беспроводная сеть локального доступа |
| **Брокер** | Сервер, распределяющий сообщения между клиентами |
| **Топик** | Адрес канала в MQTT (например: home/temperature) |
| **Payload** | Полезная нагрузка (данные) сообщения |
| **GPIO** | General-Purpose Input/Output - универсальные входы/выходы |
| **SSID** | Service Set Identifier - имя Wi-Fi сети |

---

**Следующий урок:** 🛠️ [Проектирование и отладка сложных систем](../Lesson_19/README.md)

---

**Автор:** Дуплей Максим Игоревич

**Версия:** 1.0

**Дата:** 01.11.2025
