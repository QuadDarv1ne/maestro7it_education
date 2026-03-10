/**
 * @file satellite_tasks.hpp
 * @brief FreeRTOS Tasks for MKA Onboard Software
 * 
 * Определение задач операционной системы реального времени
 * для бортового ПО малого космического аппарата.
 */

#ifndef SATELLITE_TASKS_HPP
#define SATELLITE_TASKS_HPP

#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include "timers.h"

#include <cstdint>
#include <array>

namespace mka {
namespace tasks {

// ============================================================================
// Константы конфигурации
// ============================================================================

namespace config {
    // Приоритеты задач (чем выше число, тем выше приоритет)
    constexpr UBaseType_t TASK_PRIORITY_LOW      = 1;
    constexpr UBaseType_t TASK_PRIORITY_NORMAL   = 2;
    constexpr UBaseType_t TASK_PRIORITY_HIGH     = 3;
    constexpr UBaseType_t TASK_PRIORITY_CRITICAL = 4;
    
    // Размеры стеков задач (в словах)
    constexpr uint16_t STACK_SIZE_SMALL  = 256;
    constexpr uint16_t STACK_SIZE_MEDIUM = 512;
    constexpr uint16_t STACK_SIZE_LARGE  = 1024;
    
    // Периоды задач (в мс)
    constexpr uint32_t TELEMETRY_PERIOD_MS    = 1000;
    constexpr uint32_t ADCS_PERIOD_MS         = 100;
    constexpr uint32_t POWER_MONITOR_PERIOD_MS = 500;
    constexpr uint32_t COMMUNICATION_PERIOD_MS = 100;
    constexpr uint32_t WATCHDOG_PERIOD_MS     = 10000;
}

// ============================================================================
// Очереди сообщений
// ============================================================================

/**
 * @brief Тип сообщения в очереди
 */
enum class MessageType : uint8_t {
    TELEMETRY_DATA,
    COMMAND,
    ADCS_UPDATE,
    POWER_ALERT,
    COMM_EVENT
};

/**
 * @brief Структура сообщения
 */
struct Message {
    MessageType type;
    uint8_t source;
    uint8_t destination;
    uint16_t length;
    std::array<uint8_t, 64> data;
    uint32_t timestamp;
};

/**
 * @brief Глобальные очереди сообщений
 */
struct SystemQueues {
    QueueHandle_t telemetryQueue;
    QueueHandle_t commandQueue;
    QueueHandle_t adcsQueue;
    QueueHandle_t commQueue;
    
    static SystemQueues& instance() {
        static SystemQueues queues;
        return queues;
    }
    
    bool create() {
        telemetryQueue = xQueueCreate(10, sizeof(Message));
        commandQueue = xQueueCreate(5, sizeof(Message));
        adcsQueue = xQueueCreate(10, sizeof(Message));
        commQueue = xQueueCreate(20, sizeof(Message));
        
        return (telemetryQueue && commandQueue && adcsQueue && commQueue);
    }
};

// ============================================================================
// Задача: Система ориентации и стабилизации (ADCS)
// ============================================================================

class ADCSTask {
public:
    static constexpr const char* NAME = "ADCS";
    
    static void create() {
        xTaskCreate(
            taskFunction,
            NAME,
            config::STACK_SIZE_LARGE,
            nullptr,
            config::TASK_PRIORITY_HIGH,
            &taskHandle_
        );
    }
    
    static TaskHandle_t getHandle() { return taskHandle_; }
    
private:
    static TaskHandle_t taskHandle_;
    
    static void taskFunction(void* pvParameters) {
        (void)pvParameters;
        
        TickType_t lastWakeTime = xTaskGetTickCount();
        
        // Инициализация датчиков ADCS
        initSensors();
        
        for (;;) {
            // Чтение данных с датчиков
            SensorData sensorData = readSensors();
            
            // Вычисление текущей ориентации
            AttitudeState attitude = computeAttitude(sensorData);
            
            // Расчёт управляющих воздействий
            ControlOutput control = computeControl(attitude);
            
            // Применение управления к маховикам/магнитным катушкам
            applyControl(control);
            
            // Отправка телеметрии
            sendTelemetry(attitude, sensorData);
            
            // Периодический запуск с фиксированным периодом
            vTaskDelayUntil(&lastWakeTime, 
                           pdMS_TO_TICKS(config::ADCS_PERIOD_MS));
        }
    }
    
    // Структуры данных (определяются в отдельном файле)
    struct SensorData {
        float gyroX, gyroY, gyroZ;
        float magX, magY, magZ;
        float sunX, sunY, sunZ;
        uint32_t timestamp;
    };
    
    struct AttitudeState {
        float quaternion[4];
        float angularVelocity[3];
        uint32_t timestamp;
    };
    
    struct ControlOutput {
        float wheelTorque[3];
        float magCoilCurrent[3];
    };
    
    static void initSensors() {
        // Инициализация гироскопов, магнитометров, солнечных датчиков
    }
    
    static SensorData readSensors() {
        SensorData data{};
        // Чтение данных по I2C/SPI
        return data;
    }
    
    static AttitudeState computeAttitude(const SensorData& data) {
        AttitudeState state{};
        // Фильтр Калмана или Маджвика
        return state;
    }
    
    static ControlOutput computeControl(const AttitudeState& state) {
        ControlOutput control{};
        // PD-регулятор или LQR
        return control;
    }
    
    static void applyControl(const ControlOutput& control) {
        // Управление маховиками и магнитными катушками
    }
    
    static void sendTelemetry(const AttitudeState& attitude,
                             const SensorData& sensors) {
        Message msg;
        msg.type = MessageType::TELEMETRY_DATA;
        msg.source = 0x01; // ADCS subsystem
        // Заполнение данных
        xQueueSend(SystemQueues::instance().telemetryQueue, 
                  &msg, 0);
    }
};

// ============================================================================
// Задача: Мониторинг электропитания
// ============================================================================

class PowerMonitorTask {
public:
    static constexpr const char* NAME = "PWR_MON";
    
    static void create() {
        xTaskCreate(
            taskFunction,
            NAME,
            config::STACK_SIZE_MEDIUM,
            nullptr,
            config::TASK_PRIORITY_HIGH,
            &taskHandle_
        );
    }
    
    static TaskHandle_t getHandle() { return taskHandle_; }
    
private:
    static TaskHandle_t taskHandle_;
    
    // Пороговые значения
    static constexpr float BATTERY_LOW_THRESHOLD = 6.5f;    // В
    static constexpr float BATTERY_CRITICAL_THRESHOLD = 5.8f; // В
    static constexpr float OVERCURRENT_THRESHOLD = 3.0f;    // А
    
    static void taskFunction(void* pvParameters) {
        (void)pvParameters;
        
        TickType_t lastWakeTime = xTaskGetTickCount();
        
        for (;;) {
            // Измерение параметров СЭП
            PowerData power = measurePower();
            
            // Проверка на аварийные ситуации
            if (power.batteryVoltage < BATTERY_CRITICAL_THRESHOLD) {
                // Критический разряд - переход в safe mode
                triggerSafeMode();
            } else if (power.batteryVoltage < BATTERY_LOW_THRESHOLD) {
                // Низкий заряд - уведомление
                sendPowerAlert(AlertLevel::LOW_BATTERY);
            }
            
            if (power.totalCurrent > OVERCURRENT_THRESHOLD) {
                sendPowerAlert(AlertLevel::OVERCURRENT);
            }
            
            // Отправка телеметрии
            sendPowerTelemetry(power);
            
            vTaskDelayUntil(&lastWakeTime,
                           pdMS_TO_TICKS(config::POWER_MONITOR_PERIOD_MS));
        }
    }
    
    struct PowerData {
        float batteryVoltage;
        float batteryCurrent;
        float batteryCharge;      // %
        float solarCurrent;
        float busVoltage3V3;
        float busVoltage5V;
        float totalCurrent;
        float temperatures[4];
        uint32_t timestamp;
    };
    
    enum class AlertLevel : uint8_t {
        LOW_BATTERY,
        CRITICAL_BATTERY,
        OVERCURRENT,
        OVERTEMPERATURE
    };
    
    static PowerData measurePower() {
        PowerData data{};
        // Чтение АЦП по каналам
        return data;
    }
    
    static void triggerSafeMode() {
        // Переключение в минимальный режим потребления
    }
    
    static void sendPowerAlert(AlertLevel level) {
        Message msg;
        msg.type = MessageType::POWER_ALERT;
        msg.data[0] = static_cast<uint8_t>(level);
        xQueueSend(SystemQueues::instance().telemetryQueue, &msg, 0);
    }
    
    static void sendPowerTelemetry(const PowerData& data) {
        Message msg;
        msg.type = MessageType::TELEMETRY_DATA;
        msg.source = 0x02; // Power subsystem
        // Копирование данных
        xQueueSend(SystemQueues::instance().telemetryQueue, &msg, 0);
    }
};

// ============================================================================
// Задача: Связь с наземной станцией
// ============================================================================

class CommunicationTask {
public:
    static constexpr const char* NAME = "COMM";
    
    static void create() {
        xTaskCreate(
            taskFunction,
            NAME,
            config::STACK_SIZE_LARGE,
            nullptr,
            config::TASK_PRIORITY_NORMAL,
            &taskHandle_
        );
    }
    
    static TaskHandle_t getHandle() { return taskHandle_; }
    
private:
    static TaskHandle_t taskHandle_;
    static SemaphoreHandle_t radioMutex_;
    
    // Размеры пакетов
    static constexpr size_t TM_PACKET_MAX_SIZE = 256;
    static constexpr size_t TC_PACKET_MAX_SIZE = 128;
    
    static void taskFunction(void* pvParameters) {
        (void)pvParameters;
        
        // Создание мьютекса для радиомодуля
        radioMutex_ = xSemaphoreCreateMutex();
        
        TickType_t lastWakeTime = xTaskGetTickCount();
        Message msg;
        
        for (;;) {
            // Проверка очереди команд
            if (xQueueReceive(SystemQueues::instance().commQueue, 
                             &msg, 0) == pdTRUE) {
                processMessage(msg);
            }
            
            // Проверка наличия входящих данных
            if (hasIncomingData()) {
                receiveCommand();
            }
            
            // Передача телеметрии при наличии связи
            if (isGroundStationVisible()) {
                transmitTelemetry();
            }
            
            vTaskDelayUntil(&lastWakeTime,
                           pdMS_TO_TICKS(config::COMMUNICATION_PERIOD_MS));
        }
    }
    
    static bool hasIncomingData() {
        // Проверка радиомодуля на наличие данных
        return false;
    }
    
    static bool isGroundStationVisible() {
        // Проверка видимости НС (по расчёту или сигналу)
        return false;
    }
    
    static void receiveCommand() {
        uint8_t buffer[TC_PACKET_MAX_SIZE];
        size_t len = 0;
        
        // Приём данных от радиомодуля по UART/SPI
        
        // Парсинг и валидация команды
        
        // Отправка в очередь команд
        Message msg;
        msg.type = MessageType::COMMAND;
        std::memcpy(msg.data.data(), buffer, len);
        msg.length = static_cast<uint16_t>(len);
        
        xQueueSend(SystemQueues::instance().commandQueue, &msg, 
                   pdMS_TO_TICKS(100));
    }
    
    static void transmitTelemetry() {
        if (xSemaphoreTake(radioMutex_, pdMS_TO_TICKS(100)) != pdTRUE) {
            return;
        }
        
        // Формирование пакета телеметрии
        // Передача в радиомодуль
        
        xSemaphoreGive(radioMutex_);
    }
    
    static void processMessage(const Message& msg) {
        switch (msg.type) {
            case MessageType::TELEMETRY_DATA:
                // Буферизация для передачи
                break;
            case MessageType::COMM_EVENT:
                // Обработка события связи
                break;
            default:
                break;
        }
    }
};

// ============================================================================
// Задача: Обработка команд
// ============================================================================

class CommandProcessorTask {
public:
    static constexpr const char* NAME = "CMD_PROC";
    
    static void create() {
        xTaskCreate(
            taskFunction,
            NAME,
            config::STACK_SIZE_LARGE,
            nullptr,
            config::TASK_PRIORITY_HIGH,
            &taskHandle_
        );
    }
    
private:
    static TaskHandle_t taskHandle_;
    
    static void taskFunction(void* pvParameters) {
        (void)pvParameters;
        
        Message msg;
        
        for (;;) {
            // Блокирующее ожидание команды
            if (xQueueReceive(SystemQueues::instance().commandQueue,
                             &msg, portMAX_DELAY) == pdTRUE) {
                executeCommand(msg);
            }
        }
    }
    
    static void executeCommand(const Message& msg) {
        // Расшифровка команды
        uint8_t commandId = msg.data[0];
        
        switch (commandId) {
            case 0x01:  // Установка режима
                handleSetMode(msg);
                break;
            case 0x02:  // Запрос телеметрии
                handleTelemetryRequest(msg);
                break;
            case 0x03:  // Загрузка ПО
                handleFirmwareUpload(msg);
                break;
            case 0x04:  // Управление полезной нагрузкой
                handlePayloadCommand(msg);
                break;
            default:
                // Неизвестная команда
                break;
        }
    }
    
    static void handleSetMode(const Message& msg) {
        // Изменение режима работы спутника
    }
    
    static void handleTelemetryRequest(const Message& msg) {
        // Формирование ответа с телеметрией
    }
    
    static void handleFirmwareUpload(const Message& msg) {
        // Приём новой версии ПО
    }
    
    static void handlePayloadCommand(const Message& msg) {
        // Управление научной аппаратурой
    }
};

// ============================================================================
// Инициализация системы задач
// ============================================================================

inline bool initTasks() {
    // Создание очередей
    if (!SystemQueues::instance().create()) {
        return false;
    }
    
    // Создание задач
    ADCSTask::create();
    PowerMonitorTask::create();
    CommunicationTask::create();
    CommandProcessorTask::create();
    
    return true;
}

// Определение статических членов
TaskHandle_t ADCSTask::taskHandle_ = nullptr;
TaskHandle_t PowerMonitorTask::taskHandle_ = nullptr;
TaskHandle_t CommunicationTask::taskHandle_ = nullptr;
TaskHandle_t CommandProcessorTask::taskHandle_ = nullptr;
SemaphoreHandle_t CommunicationTask::radioMutex_ = nullptr;

} // namespace tasks
} // namespace mka

#endif // SATELLITE_TASKS_HPP
