# Embedded MKA Manual

## Технический мануал для Embedded-программистов малых космических аппаратов

---

## Содержание

1. [Наноспутники формата CubeSat](#1-наноспутники-формата-cubesat)
2. [Бортовое программное обеспечение МКА](#2-бортовое-программное-обеспечение-мка)
3. [Микроконтроллеры STM32](#3-микроконтроллеры-stm32)
4. [Интерфейсы связи](#4-интерфейсы-связи)
5. [Soft-процессоры Nios II](#5-soft-процессоры-nios-ii)
6. [Практические рекомендации](#6-практические-рекомендации)

---

## 1. Наноспутники формата CubeSat

### 1.1. История и стандарт CubeSat

Формат CubeSat был разработан в 1999 году профессорами Бобом Твиггсом из Стэнфордского университета и Хорди Пуиг-Суари из Калифорнийского политехнического государственного университета. Основная цель создания этого стандарта заключалась в обеспечении доступного доступа к космосу для университетских исследований и образовательных проектов.

Базовой единицей формата CubeSat является модуль размером 10×10×10 см с массой не более 1,33 кг. Этот модуль получил обозначение **1U** (одна unit-единица). Спутники могут состоять из одного или нескольких таких модулей:

| Форм-фактор | Размеры | Масса |
|-------------|---------|-------|
| 1U | 10×10×10 см | до 1.33 кг |
| 2U | 10×10×20 см | до 2.66 кг |
| 3U | 10×10×30 см | до 4.00 кг |
| 6U | 20×10×30 см | до 8.00 кг |
| 12U | 20×20×30 см | до 16.00 кг |

### 1.2. Архитектура и подсистемы наноспутника

Типичный наноспутник CubeSat состоит из нескольких функциональных подсистем:

```
┌─────────────────────────────────────────┐
│              Payload (Полезная нагрузка) │
├─────────────────────────────────────────┤
│         OBC (Бортовой компьютер)         │
├───────────┬───────────┬─────────────────┤
│    СЭП    │    СОС    │   Система связи  │
│(Электро-  │ (Ориентация│                 │
| питание)  |и стабили- │                 │
│           | зация)    │                 │
└───────────┴───────────┴─────────────────┘
```

**Система электропитания (СЭП):**
- Солнечные панели
- Аккумуляторные батареи
- Контроллеры заряда/разряда
- Распределение питания

**Система ориентации и стабилизации (СОС):**
- Датчики: магнитометры, гироскопы, солнечные датчики
- Исполнительные органы: маховики, магнитные катушки

**Система связи:**
- Приёмник команд (UHF/VHF)
- Передатчик телеметрии (S-band, X-band)
- Антенны

### 1.3. Требования к бортовому оборудованию

#### Температурный диапазон
- Рабочий: -40°C ... +85°C
- Хранение: -55°C ... +125°C

#### Радиационная стойкость
- Околоземная орбита: ~100-1000 rad/год
- Методы митигации: TMR, scrubbing, watchdog

#### Вакуум
- Отсутствие конвекции → специфическое охлаждение
- Проблемы с материалами (outgassing)

---

## 2. Бортовое программное обеспечение МКА

### 2.1. Архитектура бортового ПО

```
┌────────────────────────────────────────────────┐
│              Прикладной уровень                 │
│  (логика миссии, управление payload)           │
├────────────────────────────────────────────────┤
│             Уровень сервисов                    │
│  (FS, протоколы связи, logging)                │
├────────────────────────────────────────────────┤
│             Уровень драйверов                   │
│  (UART, SPI, I2C, CAN, GPIO)                   │
├────────────────────────────────────────────────┤
│   HAL (Hardware Abstraction Layer)             │
├────────────────────────────────────────────────┤
│         Аппаратное обеспечение                  │
└────────────────────────────────────────────────┘
```

#### Bare Metal vs RTOS

| Аспект | Bare Metal | RTOS |
|--------|------------|------|
| Накладные расходы | Минимальные | Незначительные |
| Предсказуемость | Максимальная | Зависит от конфигурации |
| Сложность разработки | Высокая для больших проектов | Средняя |
| Поддержка многозадачности | Ручная | Встроенная |

**Рекомендуемые RTOS:**
- FreeRTOS (открытый исходный код)
- NuttX (POSIX-совместимый)
- Zephyr (Linux Foundation)

### 2.2. Основные режимы работы

```
┌──────────────┐
│     LAUNCH   │  ← Запуск, сложенные панели
└──────┬───────┘
       ↓
┌──────────────┐
│   DETUMBLING │  ← Гашение начальной угловой скорости
└──────┬───────┘
       ↓
┌──────────────┐
│  NOMINAL     │  ← Рабочий режим, выполнение миссии
└──────┬───────┘
       ↓
┌──────────────┐
│  SAFE MODE   │  ← Аварийный режим, минимальное потребление
└──────────────┘
```

### 2.3. Протоколы межмодульного обмена

#### CANopen для бортовой сети

```cpp
// Пример структуры CANopen сообщения
struct CANopenMessage {
    uint16_t cob_id;      // Communication Object ID
    uint8_t  node_id;     // 1-127
    uint8_t  data[8];     // Payload
};

// NMT (Network Management)
// COB-ID: 0x000
// Запуск узла: [0x01, node_id]
// Остановка:   [0x02, node_id]

// SDO (Service Data Object)
// Чтение OD: COB-ID = 0x600 + node_id
// Ответ:     COB-ID = 0x580 + node_id
```

---

## 3. Микроконтроллеры STM32

### 3.1. Обзор семейства

| Семейство | Ядро | Частота | Особенности |
|-----------|------|---------|-------------|
| STM32F4 | Cortex-M4F | до 180 MHz | FPU, DSP |
| STM32F7 | Cortex-M7 | до 216 MHz | FPU, L1 cache |
| STM32H7 | Cortex-M7/M4 | до 480 MHz | Двухъядерный |

### 3.2. Ключевые периферийные модули

#### DMA (Direct Memory Access)

```cpp
// Пример конфигурации DMA для UART
void UART_DMACfg(UART_HandleTypeDef* huart) {
    DMA_HandleTypeDef hdma_usart_tx;
    
    hdma_usart_tx.Instance = DMA1_Stream4;
    hdma_usart_tx.Init.Channel = DMA_CHANNEL_4;
    hdma_usart_tx.Init.Direction = DMA_MEMORY_TO_PERIPH;
    hdma_usart_tx.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_usart_tx.Init.MemInc = DMA_MINC_ENABLE;
    hdma_usart_tx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hdma_usart_tx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hdma_usart_tx.Init.Mode = DMA_NORMAL;
    hdma_usart_tx.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_usart_tx);
    __HAL_LINKDMA(huart, hdmatx, hdma_usart_tx);
}
```

#### NVIC (Nested Vectored Interrupt Controller)

```cpp
// Приоритеты прерываний для МКА
// Чем меньше число - тем выше приоритет

// Критические: Watchdog, HardFault
HAL_NVIC_SetPriority(HardFault_IRQn, 0, 0);

// Высокий: ADCS, Power monitoring
HAL_NVIC_SetPriority(TIM1_UP_TIM10_IRQn, 1, 0);

// Средний: Communication, CAN
HAL_NVIC_SetPriority(USART1_IRQn, 2, 0);

// Низкий: Logging, non-critical
HAL_NVIC_SetPriority(DMA1_Stream0_IRQn, 3, 0);
```

### 3.3. Watchdog и восстановление

```cpp
// Конфигурация независимого watchdog (IWDG)
void IWDG_Init(void) {
    IWDG_HandleTypeDef hiwdg;
    
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_256;
    hiwdg.Init.Reload = 0x0FFF;  // ~26 секунд при LSI=32kHz
    
    HAL_IWDG_Init(&hiwdg);
}

// Обновление watchdog в основном цикле
void main_loop(void) {
    while (1) {
        // ... выполнение задач ...
        
        // Кик watchdog
        HAL_IWDG_Refresh(&hiwdg);
    }
}
```

---

## 4. Интерфейсы связи

### 4.1. CAN (Controller Area Network)

**Физический уровень:**
- Дифференциальная пара: CAN_H, CAN_L
- Волновое сопротивление: 120 Ом
- Скорость: до 1 Мбит/с

**Формат кадра CAN:**

```
┌─────┬──────┬─────┬──────────┬────────┬───────┬──────┬─────┬────────┐
│ SOF │  ID  │ RTR │ IDE/r0   │  DLC   │ DATA  │ CRC  │ ACK │  EOF   │
│ 1 b │11/29b│ 1 b │ 2-6 b   │ 4 b    │0-8 B  │ 15 b │ 2 b │ 7 b    │
└─────┴──────┴─────┴──────────┴────────┴───────┴──────┴─────┴────────┘
```

### 4.2. UART

**Стандартные скорости:**

| Скорость | Применение |
|----------|------------|
| 9600 | Медленные модемы |
| 115200 | Отладка, GPS |
| 921600 | Высокоскоростные радиомодули |

**Формат кадра:**
```
┌──────┬────────────┬───────┬─────────┐
│Start │ Data (5-9b)│Parity │ Stop(1-2)│
│  0   │            │  opt  │    1    │
└──────┴────────────┴───────┴─────────┘
```

### 4.3. SPI

**Режимы SPI:**

| Mode | CPOL | CPHA | Описание |
|------|------|------|----------|
| 0 | 0 | 0 | Низкий в простое, выборка по переднему фронту |
| 1 | 0 | 1 | Низкий в простое, выборка по заднему фронту |
| 2 | 1 | 0 | Высокий в простое, выборка по переднему фронту |
| 3 | 1 | 1 | Высокий в простое, выборка по заднему фронту |

**Подключение:**
```
Master                    Slave
─────────               ─────────
    MOSI ──────────────────→ MOSI
    MISO ←────────────────── MISO
     SCK ──────────────────→ SCK
     CS  ──────────────────→ CS
```

### 4.4. I2C

**Адресация:**
- 7-бит: до 127 устройств
- 10-бит: до 1023 устройств

**Типичная последовательность:**
```
Master: [START][ADDR+W][REG_ADDR][DATA...][STOP]
Slave:              [ACK]    [ACK]    [ACK]
```

### 4.5. SDIO

**Режимы передачи:**
- 1-bit: одна линия данных
- 4-bit: четыре линии параллельно

**Скорости:**
| Режим | Скорость |
|-------|----------|
| Default | 25 MB/s |
| High Speed | 50 MB/s |
| SDR104 | 104 MB/s |

---

## 5. Soft-процессоры Nios II

### 5.1. Варианты ядер

| Параметр | Nios II/e | Nios II/s | Nios II/f |
|----------|-----------|-----------|-----------|
| Кэш инструкций | Нет | До 64 KB | До 64 KB |
| Кэш данных | Нет | Нет | До 64 KB |
| HW умножитель | Нет | Есть | Есть |
| HW делитель | Нет | Нет | Есть |
| Ресурсы | ~700 LE | ~1000 LE | ~1500 LE |
| Производительность | ~20 DMIPS | ~80 DMIPS | ~200 DMIPS |

### 5.2. Структура проекта

```
nios2_project/
├── hardware/
│   ├── qsys_system.qsys    # Platform Designer система
│   ├── top_module.v        # Топ-модуль ПЛИС
│   └── constraints.sdc     # Тайминговые ограничения
├── software/
│   ├── bsp/                # Board Support Package
│   ├── app/                # Приложение
│   │   ├── main.c
│   │   ├── drivers/
│   │   └── Makefile
│   └── scripts/
└── docs/
```

### 5.3. Пользовательские инструкции

```verilog
// Пример пользовательской инструкции CRC32
module crc32_instruction (
    input  wire        clk,
    input  wire [31:0] data_a,    // Операнд A
    input  wire [31:0] data_b,    // Операнд B (текущий CRC)
    input  wire        start,
    output reg  [31:0] result,
    output reg         done
);

    // Реализация CRC32
    always @(posedge clk) begin
        if (start) begin
            result <= crc32_compute(data_a, data_b);
            done <= 1'b1;
        end else begin
            done <= 1'b0;
        end
    end

endmodule
```

```c
// Использование в C-коде
uint32_t calculate_crc32(const uint8_t* data, size_t len) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; i++) {
        // Пользовательская инструкция вызывается как функция
        crc = alt_crc32(data[i], crc);
    }
    return crc ^ 0xFFFFFFFF;
}
```

---

## 6. Практические рекомендации

### 6.1. Стандарт MISRA C:2012 (ключевые правила)

```cpp
// Правило 11.3: Не приводить указатель к несовместимому типу
// НЕПРАВИЛЬНО:
uint32_t* ptr = (uint32_t*)0x20000000;

// ПРАВИЛЬНО:
volatile uint32_t* const REG = (volatile uint32_t* const)0x20000000;

// Правило 18.4: Не использовать объединения для интерпретации памяти
// НЕПРАВИЛЬНО:
union {
    float f;
    uint32_t u;
} converter;

// ПРАВИЛЬНО: использовать memcpy
float f = 1.0f;
uint32_t u;
memcpy(&u, &f, sizeof(u));
```

### 6.2. Защита от радиации

```cpp
// Тройное модульное резервирование (TMR)
template<typename T>
class TMRVariable {
public:
    T get() const {
        T v0 = values_[0];
        T v1 = values_[1];
        T v2 = values_[2];
        
        // Голосование большинством
        if (v0 == v1) return v0;
        if (v0 == v2) return v0;
        if (v1 == v2) return v1;
        
        // Все разные - ошибка
        return T{}; // или обработка ошибки
    }
    
    void set(T value) {
        values_[0] = value;
        values_[1] = value;
        values_[2] = value;
    }
    
private:
    volatile T values_[3];
};

// Использование
TMRVariable<uint32_t> critical_counter;
```

### 6.3. Структура проекта

```
mka_software/
├── src/
│   ├── hal/                  # Hardware Abstraction Layer
│   │   ├── hal_gpio.cpp
│   │   ├── hal_uart.cpp
│   │   ├── hal_spi.cpp
│   │   └── hal_can.cpp
│   ├── drivers/              # Драйверы периферии
│   │   ├── imu_driver.cpp
│   │   ├── radio_driver.cpp
│   │   └── flash_driver.cpp
│   ├── subsystems/           # Подсистемы спутника
│   │   ├── adcs/
│   │   ├── eps/
│   │   └── comm/
│   ├── application/          # Прикладная логика
│   │   ├── mission.cpp
│   │   └── payload.cpp
│   └── main.cpp
├── include/
├── tests/
│   ├── unit/
│   └── integration/
├── tools/
│   └── telemetry_decoder.py
├── docs/
├── CMakeLists.txt
└── README.md
```

### 6.4. Тестирование

```python
# Пример модульного теста (Google Test)
import unittest

class TestUARTDriver(unittest.TestCase):
    def setUp(self):
        self.uart = UARTDriver(config)
        self.uart.init()
    
    def tearDown(self):
        self.uart.close()
    
    def test_transmit_success(self):
        data = bytes([0x01, 0x02, 0x03])
        result = self.uart.transmit(data, timeout=100)
        self.assertEqual(result, Status.OK)
    
    def test_receive_timeout(self):
        buffer = bytearray(10)
        result = self.uart.receive(buffer, timeout=10)
        self.assertEqual(result, Status.TIMEOUT)

if __name__ == '__main__':
    unittest.main()
```

---

## Приложения

### A. Полезные ресурсы

- [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html)
- [FreeRTOS](https://www.freertos.org/)
- [MISRA C:2012](https://www.misra.org.uk/)
- [CubeSat Design Specification](https://www.cubesat.org/)

### B. Словарь терминов

| Термин | Расшифровка |
|--------|-------------|
| МКА | Малый космический аппарат |
| СЭП | Система электропитания |
| СОС | Система ориентации и стабилизации |
| НСУ | Наземная система управления |
| TMR | Triple Modular Redundancy |

---

*Документ подготовлен для Embedded-разработчиков бортового ПО МКА*
