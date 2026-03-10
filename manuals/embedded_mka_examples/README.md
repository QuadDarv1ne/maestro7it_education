# Embedded MKA Examples

## Примеры кода для Embedded-программистов малых космических аппаратов

Этот репозиторий содержит примеры кода и документацию для разработчиков бортового ПО наноспутников формата CubeSat.

## Структура проекта

```
embedded_mka_examples/
├── docs/                      # Документация
│   └── manual.md              # Технический мануал
├── src/
│   ├── cpp/                   # C++ примеры
│   │   ├── hal/               # Hardware Abstraction Layer
│   │   ├── drivers/           # Драйверы периферии
│   │   └── rtos/              # FreeRTOS задачи
│   └── python/                # Python утилиты
│       ├── tests/             # Модульные тесты
│       └── utils/             # Утилиты для наземных испытаний
└── README.md
```

## Содержимое

### C++ примеры

| Файл | Описание |
|------|----------|
| `hal/hal_interface.hpp` | Абстрактные интерфейсы HAL для GPIO, UART, SPI, I2C, CAN |
| `drivers/stm32_uart_driver.hpp` | Драйвер UART для STM32 с поддержкой DMA |
| `drivers/stm32_can_driver.hpp` | Драйвер CAN для STM32 bxCAN |
| `rtos/satellite_tasks.hpp` | FreeRTOS задачи для бортового ПО |

### Python утилиты

| Файл | Описание |
|------|----------|
| `tests/uart_sim.py` | Симулятор UART для модульного тестирования |
| `tests/test_uart_driver.py` | Модульные тесты UART драйвера |
| `utils/can_simulator.py` | Симулятор CAN шины с поддержкой CANopen |
| `utils/telemetry_generator.py` | Генератор телеметрии для тестирования НСУ |

## Требования

### C++

- Компилятор C++17 или выше
- STM32CubeIDE (для STM32 проектов)
- FreeRTOS 10.x

### Python

- Python 3.8+
- pytest (для запуска тестов)

```bash
pip install pytest
```

## Использование

### Запуск Python тестов

```bash
cd src/python
pytest tests/ -v
```

### Симулятор UART

```python
from uart_sim import UARTDriver, UARTConfig

config = UARTConfig(baud_rate=115200)
uart = UARTDriver(config, loopback=True)

# Передача данных
uart.transmit(bytes([0xDE, 0xAD, 0xBE, 0xEF]))

# Приём данных
buffer = bytearray(4)
uart.receive(buffer, timeout=100)
```

### Генератор телеметрии

```python
from telemetry_generator import TelemetryGenerator

gen = TelemetryGenerator(seed=42)

# Генерация телеметрии СЭП
power_frame = gen.generate_power()
print(power_frame.to_json())

# Кодирование в бинарный формат
encoded = power_frame.encode()
```

### CAN симулятор

```python
from can_simulator import CANController, CANMessage

can = CANController(baud_rate=500000, loopback=True)
can.init()

# Отправка сообщения
msg = CANMessage(id=0x123, data=bytes([0x01, 0x02, 0x03]))
can.transmit(msg)

# Приём сообщения
received = can.receive(timeout=100)
```

## Интеграция с STM32

### Добавление HAL интерфейсов

```cpp
#include "hal_interface.hpp"

class STM32GPIO : public mka::hal::IGPIO {
    // Реализация методов интерфейса
};

// Использование
mka::hal::IGPIO* gpio = new STM32GPIO();
gpio->setMode(5, mka::hal::GPIOMode::OUTPUT_PUSH_PULL);
gpio->write(5, mka::hal::GPIOState::HIGH);
```

### Использование FreeRTOS задач

```cpp
#include "satellite_tasks.hpp"

int main() {
    // Инициализация HAL
    
    // Создание задач
    mka::tasks::initTasks();
    
    // Запуск планировщика
    vTaskStartScheduler();
    
    return 0;
}
```

## Лицензия

Образовательный материал для подготовки Embedded-разработчиков.

## Контакты

Для вопросов и предложений обращайтесь к команде разработки МКА.

---

*Подготовлено для Embedded-программистов космической отрасли*
