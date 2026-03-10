#!/usr/bin/env python3
"""
UART Simulator for Testing
Симулятор UART для модульного тестирования

Этот модуль предоставляет программную симуляцию UART интерфейса
для тестирования embedded-кода на хост-машине.
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Callable, Optional, List
from collections import deque
import threading
import time


class Status(IntEnum):
    """Статус операции"""
    OK = 0
    ERROR = 1
    TIMEOUT = 2
    BUSY = 3
    INVALID_PARAM = 4
    NOT_INITIALIZED = 5


class DMAMode(IntEnum):
    """Режим DMA"""
    DISABLED = 0
    ENABLED = 1


@dataclass
class UARTConfig:
    """Конфигурация UART"""
    baud_rate: int = 115200
    data_bits: int = 8
    stop_bits: int = 1
    parity: int = 0  # 0=none, 1=odd, 2=even
    flow_control: bool = False
    
    def __post_init__(self):
        if self.baud_rate <= 0:
            raise ValueError(f"Invalid baud rate: {self.baud_rate}")
        if self.data_bits not in [5, 6, 7, 8, 9]:
            raise ValueError(f"Invalid data bits: {self.data_bits}")
        if self.stop_bits not in [1, 2]:
            raise ValueError(f"Invalid stop bits: {self.stop_bits}")
        if self.parity not in [0, 1, 2]:
            raise ValueError(f"Invalid parity: {self.parity}")


class RingBuffer:
    """Кольцевой буфер для приёма/передачи данных"""
    
    def __init__(self, size: int = 256):
        self._buffer = bytearray(size)
        self._size = size
        self._head = 0
        self._tail = 0
        self._lock = threading.Lock()
    
    def push(self, data: bytes) -> int:
        """Добавить данные в буфер. Возвращает количество записанных байт."""
        with self._lock:
            written = 0
            for byte in data:
                next_head = (self._head + 1) % self._size
                if next_head == self._tail:
                    break  # Буфер полон
                self._buffer[self._head] = byte
                self._head = next_head
                written += 1
            return written
    
    def pop(self, size: int) -> bytes:
        """Извлечь данные из буфера."""
        with self._lock:
            result = bytearray()
            while len(result) < size and self._head != self._tail:
                result.append(self._buffer[self._tail])
                self._tail = (self._tail + 1) % self._size
            return bytes(result)
    
    def count(self) -> int:
        """Количество байт в буфере."""
        with self._lock:
            return (self._head - self._tail + self._size) % self._size
    
    def is_empty(self) -> bool:
        return self._head == self._tail
    
    def is_full(self) -> bool:
        return ((self._head + 1) % self._size) == self._tail
    
    def clear(self):
        """Очистить буфер."""
        with self._lock:
            self._head = 0
            self._tail = 0


class UARTDriver:
    """
    Симулятор UART драйвера для тестирования.
    
    Поддерживает:
    - Блокирующий и асинхронный режимы
    - DMA передачу
    - Ошибки связи (parity, framing, overrun)
    - Callback при приёме данных
    """
    
    def __init__(self, config: UARTConfig, 
                 dma_mode: DMAMode = DMAMode.DISABLED,
                 loopback: bool = False,
                 linked_to: Optional['UARTDriver'] = None):
        """
        Инициализация драйвера.
        
        Args:
            config: Конфигурация UART
            dma_mode: Режим DMA
            loopback: Режим внутренней петли (TX->RX)
            linked_to: Другой драйвер для связи
        """
        self._config = config
        self._dma_mode = dma_mode
        self._loopback = loopback
        self._linked_to = linked_to
        self._initialized = False
        
        # Буферы
        buffer_size = 1024 if dma_mode == DMAMode.ENABLED else 256
        self._tx_buffer = RingBuffer(buffer_size)
        self._rx_buffer = RingBuffer(buffer_size)
        
        # Состояние
        self._tx_busy = False
        self._rx_busy = False
        self._async_rx_enabled = False
        
        # Callback
        self._rx_callback: Optional[Callable[[bytes], None]] = None
        
        # Счётчики ошибок
        self._parity_errors = 0
        self._framing_errors = 0
        self._overrun_errors = 0
        
        # Инициализация
        self._init_hardware()
    
    def _init_hardware(self):
        """Инициализация аппаратной части (симуляция)."""
        # В реальном проекте здесь настройка регистров UART
        time.sleep(0.001)  # Симуляция задержки инициализации
        self._initialized = True
    
    def is_initialized(self) -> bool:
        """Проверка инициализации."""
        return self._initialized
    
    def close(self):
        """Деинициализация драйвера."""
        self._initialized = False
        self._async_rx_enabled = False
        self._rx_callback = None
    
    def transmit(self, data: bytes, timeout: int = 100) -> int:
        """
        Передача данных (блокирующий режим).
        
        Args:
            data: Данные для передачи
            timeout: Таймаут в мс
        
        Returns:
            Status код
        """
        if not self._initialized:
            return Status.NOT_INITIALIZED
        
        if not data:
            raise ValueError("Data cannot be empty")
        
        if self._tx_busy:
            return Status.BUSY
        
        self._tx_busy = True
        
        try:
            # Симуляция времени передачи
            byte_time = (10 * 1000) / self._config.baud_rate  # мс на байт
            total_time = len(data) * byte_time
            
            if total_time > timeout:
                return Status.TIMEOUT
            
            # Добавление в буфер передачи
            written = self._tx_buffer.push(data)
            
            # Loopback или передача связанному драйверу
            if self._loopback:
                self._rx_buffer.push(data[:written])
                if self._rx_callback and self._async_rx_enabled:
                    self._rx_callback(data[:written])
            elif self._linked_to:
                self._linked_to._rx_buffer.push(data[:written])
                if self._linked_to._rx_callback and self._linked_to._async_rx_enabled:
                    self._linked_to._rx_callback(data[:written])
            
            # Симуляция задержки
            time.sleep(total_time / 1000)
            
            return Status.OK
        
        finally:
            self._tx_busy = False
    
    def receive(self, buffer: bytearray, timeout: int = 100) -> int:
        """
        Приём данных (блокирующий режим).
        
        Args:
            buffer: Буфер для приёма данных
            timeout: Таймаут в мс
        
        Returns:
            Status код
        """
        if not self._initialized:
            return Status.NOT_INITIALIZED
        
        if self._rx_busy:
            return Status.BUSY
        
        self._rx_busy = True
        
        try:
            # Ожидание данных
            start_time = time.time()
            while self._rx_buffer.is_empty():
                elapsed = (time.time() - start_time) * 1000
                if elapsed >= timeout:
                    return Status.TIMEOUT
                time.sleep(0.001)
            
            # Чтение данных
            received = self._rx_buffer.pop(len(buffer))
            buffer[:len(received)] = received
            
            return Status.OK
        
        finally:
            self._rx_busy = False
    
    def set_rx_callback(self, callback: Callable[[bytes], None]):
        """Установка callback для асинхронного приёма."""
        self._rx_callback = callback
    
    def start_async_receive(self) -> int:
        """Запуск асинхронного приёма."""
        if not self._initialized:
            return Status.NOT_INITIALIZED
        
        self._async_rx_enabled = True
        return Status.OK
    
    def stop_async_receive(self):
        """Остановка асинхронного приёма."""
        self._async_rx_enabled = False
    
    def start_dma_circular_receive(self, buffer_size: int = 512) -> int:
        """Запуск DMA кругового приёма."""
        if not self._initialized:
            return Status.NOT_INITIALIZED
        
        if self._dma_mode == DMAMode.DISABLED:
            return Status.ERROR
        
        self._async_rx_enabled = True
        return Status.OK
    
    # Методы для симуляции (используются в тестах)
    
    def _simulate_rx_data(self, data: bytes):
        """Симуляция входящих данных."""
        written = self._rx_buffer.push(data)
        
        if written < len(data):
            self._overrun_errors += 1
        
        if self._rx_callback and self._async_rx_enabled:
            self._rx_callback(data[:written])
    
    def _simulate_parity_error(self):
        """Симуляция ошибки чётности."""
        self._parity_errors += 1
    
    def _simulate_framing_error(self):
        """Симуляция ошибки кадрирования."""
        self._framing_errors += 1
    
    def get_error_counts(self) -> dict:
        """Получить счётчиков ошибок."""
        return {
            'parity': self._parity_errors,
            'framing': self._framing_errors,
            'overrun': self._overrun_errors
        }
    
    def clear_errors(self):
        """Сброс счётчиков ошибок."""
        self._parity_errors = 0
        self._framing_errors = 0
        self._overrun_errors = 0


# ============================================================================
# Пример использования
# ============================================================================

def example_basic_usage():
    """Пример базового использования."""
    print("=== Basic UART Usage Example ===")
    
    # Создание конфигурации
    config = UARTConfig(
        baud_rate=115200,
        data_bits=8,
        stop_bits=1,
        parity=0
    )
    
    # Создание драйвера
    uart = UARTDriver(config, loopback=True)
    
    # Передача данных
    tx_data = bytes([0xDE, 0xAD, 0xBE, 0xEF])
    result = uart.transmit(tx_data, timeout=100)
    print(f"Transmit result: {Status(result).name}")
    
    # Приём данных
    rx_buffer = bytearray(4)
    result = uart.receive(rx_buffer, timeout=100)
    print(f"Receive result: {Status(result).name}")
    print(f"Received data: {rx_buffer.hex()}")
    
    uart.close()


def example_async_receive():
    """Пример асинхронного приёма."""
    print("\n=== Async Receive Example ===")
    
    received_messages = []
    
    def on_receive(data: bytes):
        received_messages.append(data)
        print(f"Received: {data.hex()}")
    
    config = UARTConfig(baud_rate=921600)
    uart = UARTDriver(config, loopback=True)
    
    # Настройка callback
    uart.set_rx_callback(on_receive)
    uart.start_async_receive()
    
    # Передача нескольких сообщений
    for i in range(5):
        data = bytes([i, i+1, i+2, i+3])
        uart.transmit(data, timeout=100)
    
    print(f"Total messages received: {len(received_messages)}")
    
    uart.close()


def example_linked_uarts():
    """Пример связанных UART."""
    print("\n=== Linked UARTs Example ===")
    
    config = UARTConfig(baud_rate=115200)
    
    # Создаём два связанных драйвера
    uart1 = UARTDriver(config)
    uart2 = UARTDriver(config, linked_to=uart1)
    
    # Callback для uart2
    def uart2_callback(data: bytes):
        print(f"UART2 received: {data.hex()}")
    
    uart2.set_rx_callback(uart2_callback)
    uart2.start_async_receive()
    
    # Передача от uart1 к uart2
    uart1.transmit(bytes([0x01, 0x02, 0x03]), timeout=100)
    
    uart1.close()
    uart2.close()


if __name__ == '__main__':
    example_basic_usage()
    example_async_receive()
    example_linked_uarts()
