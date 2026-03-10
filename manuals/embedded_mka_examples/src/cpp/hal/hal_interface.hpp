/**
 * @file hal_interface.hpp
 * @brief Hardware Abstraction Layer Interface for MKA embedded systems
 * 
 * Этот файл определяет абстрактные интерфейсы для аппаратного уровня
 * бортового ПО малого космического аппарата.
 */

#ifndef HAL_INTERFACE_HPP
#define HAL_INTERFACE_HPP

#include <cstdint>
#include <cstddef>
#include <functional>

namespace mka {
namespace hal {

/**
 * @brief Статус операции
 */
enum class Status {
    OK = 0,
    ERROR = 1,
    TIMEOUT = 2,
    BUSY = 3,
    INVALID_PARAM = 4,
    NOT_INITIALIZED = 5
};

/**
 * @brief Режим работы GPIO
 */
enum class GPIOMode {
    INPUT,
    OUTPUT_PUSH_PULL,
    OUTPUT_OPEN_DRAIN,
    ALTERNATE_FUNCTION,
    ANALOG
};

/**
 * @brief Состояние GPIO пина
 */
enum class GPIOState {
    LOW = 0,
    HIGH = 1
};

/**
 * @brief Абстрактный интерфейс GPIO
 */
class IGPIO {
public:
    virtual ~IGPIO() = default;
    
    /**
     * @brief Установить режим пина
     * @param pin Номер пина
     * @param mode Режим работы
     * @return Статус операции
     */
    virtual Status setMode(uint8_t pin, GPIOMode mode) = 0;
    
    /**
     * @brief Записать состояние пина
     * @param pin Номер пина
     * @param state Состояние
     * @return Статус операции
     */
    virtual Status write(uint8_t pin, GPIOState state) = 0;
    
    /**
     * @brief Прочитать состояние пина
     * @param pin Номер пина
     * @return Состояние пина
     */
    virtual GPIOState read(uint8_t pin) const = 0;
    
    /**
     * @brief Переключить состояние пина
     * @param pin Номер пина
     * @return Статус операции
     */
    virtual Status toggle(uint8_t pin) = 0;
};

/**
 * @brief Конфигурация UART
 */
struct UARTConfig {
    uint32_t baudRate;
    uint8_t dataBits;
    uint8_t stopBits;
    uint8_t parity;      // 0=none, 1=odd, 2=even
    bool flowControl;
};

/**
 * @brief Абстрактный интерфейс UART
 */
class IUART {
public:
    using RxCallback = std::function<void(const uint8_t* data, size_t len)>;
    
    virtual ~IUART() = default;
    
    /**
     * @brief Инициализация UART
     * @param config Конфигурация
     * @return Статус операции
     */
    virtual Status init(const UARTConfig& config) = 0;
    
    /**
     * @brief Деинициализация
     */
    virtual void deinit() = 0;
    
    /**
     * @brief Отправить данные (блокирующий режим)
     * @param data Указатель на данные
     * @param len Длина данных
     * @param timeout Таймаут в мс
     * @return Статус операции
     */
    virtual Status transmit(const uint8_t* data, size_t len, uint32_t timeout) = 0;
    
    /**
     * @brief Получить данные (блокирующий режим)
     * @param data Буфер для данных
     * @param len Ожидаемая длина
     * @param timeout Таймаут в мс
     * @return Статус операции
     */
    virtual Status receive(uint8_t* data, size_t len, uint32_t timeout) = 0;
    
    /**
     * @brief Установить callback для асинхронного приёма
     * @param callback Функция обратного вызова
     */
    virtual void setRxCallback(RxCallback callback) = 0;
    
    /**
     * @brief Начать асинхронный приём
     * @return Статус операции
     */
    virtual Status startAsyncReceive() = 0;
    
    /**
     * @brief Остановить асинхронный приём
     */
    virtual void stopAsyncReceive() = 0;
};

/**
 * @brief Конфигурация SPI
 */
struct SPIConfig {
    uint32_t clockSpeed;
    uint8_t mode;        // CPOL, CPHA combination (0-3)
    bool lsbFirst;
    bool masterMode;
};

/**
 * @brief Абстрактный интерфейс SPI
 */
class ISPI {
public:
    virtual ~ISPI() = default;
    
    /**
     * @brief Инициализация SPI
     */
    virtual Status init(const SPIConfig& config) = 0;
    
    /**
     * @brief Выбрать устройство (активировать CS)
     */
    virtual Status selectDevice() = 0;
    
    /**
     * @brief Отпустить устройство (деактивировать CS)
     */
    virtual void deselectDevice() = 0;
    
    /**
     * @brief Обмен данными (полнодуплексный)
     * @param txData Данные для передачи
     * @param rxData Буфер для приёма
     * @param len Длина данных
     * @param timeout Таймаут в мс
     * @return Статус операции
     */
    virtual Status transfer(const uint8_t* txData, uint8_t* rxData, 
                           size_t len, uint32_t timeout) = 0;
    
    /**
     * @brief Передать данные (полудуплексный)
     */
    virtual Status transmit(const uint8_t* data, size_t len, uint32_t timeout) = 0;
    
    /**
     * @brief Принять данные (полудуплексный)
     */
    virtual Status receive(uint8_t* data, size_t len, uint32_t timeout) = 0;
};

/**
 * @brief Конфигурация I2C
 */
struct I2CConfig {
    uint32_t clockSpeed;
    uint8_t ownAddress;
    bool generalCall;
};

/**
 * @brief Абстрактный интерфейс I2C
 */
class II2C {
public:
    virtual ~II2C() = default;
    
    /**
     * @brief Инициализация I2C
     */
    virtual Status init(const I2CConfig& config) = 0;
    
    /**
     * @brief Записать данные в устройство
     * @param devAddress Адрес устройства (7 бит)
     * @param regAddress Адрес регистра
     * @param data Данные для записи
     * @param len Длина данных
     * @param timeout Таймаут в мс
     */
    virtual Status write(uint8_t devAddress, uint8_t regAddress,
                        const uint8_t* data, size_t len, uint32_t timeout) = 0;
    
    /**
     * @brief Прочитать данные из устройства
     */
    virtual Status read(uint8_t devAddress, uint8_t regAddress,
                       uint8_t* data, size_t len, uint32_t timeout) = 0;
    
    /**
     * @brief Сканировать шину на наличие устройств
     * @param foundDevices Массив для найденных адресов
     * @param maxDevices Максимальное количество устройств
     * @return Количество найденных устройств
     */
    virtual size_t scanBus(uint8_t* foundDevices, size_t maxDevices) = 0;
};

/**
 * @brief Конфигурация CAN
 */
struct CANConfig {
    uint32_t baudRate;
    uint32_t txMailbox;
    bool loopbackMode;
};

/**
 * @brief CAN сообщение
 */
struct CANMessage {
    uint32_t id;
    bool extended;
    bool remote;
    uint8_t dlc;          // Data Length Code (0-8)
    uint8_t data[8];
};

/**
 * @brief Абстрактный интерфейс CAN
 */
class ICAN {
public:
    using RxCallback = std::function<void(const CANMessage& msg)>;
    
    virtual ~ICAN() = default;
    
    /**
     * @brief Инициализация CAN
     */
    virtual Status init(const CANConfig& config) = 0;
    
    /**
     * @brief Отправить сообщение
     */
    virtual Status transmit(const CANMessage& msg, uint32_t timeout) = 0;
    
    /**
     * @brief Установить фильтр приёма
     * @param id Идентификатор
     * @param mask Маска
     * @param extended Расширенный кадр
     */
    virtual Status setFilter(uint32_t id, uint32_t mask, bool extended) = 0;
    
    /**
     * @brief Установить callback для приёма сообщений
     */
    virtual void setRxCallback(RxCallback callback) = 0;
    
    /**
     * @brief Включить прерывания приёма
     */
    virtual Status enableRxInterrupt() = 0;
};

} // namespace hal
} // namespace mka

#endif // HAL_INTERFACE_HPP
