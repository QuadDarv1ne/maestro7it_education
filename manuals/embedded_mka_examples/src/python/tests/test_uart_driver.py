#!/usr/bin/env python3
"""
Unit tests for STM32 UART Driver
Модульные тесты для драйвера UART STM32

Запуск: pytest test_uart_driver.py -v
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestUARTConfig:
    """Тесты конфигурации UART"""
    
    def test_default_config(self):
        """Тест создания конфигурации по умолчанию"""
        from uart_sim import UARTConfig
        
        config = UARTConfig()
        assert config.baud_rate == 115200
        assert config.data_bits == 8
        assert config.stop_bits == 1
        assert config.parity == 0
    
    @pytest.mark.parametrize("baud_rate,expected", [
        (9600, 9600),
        (115200, 115200),
        (921600, 921600),
        (1000000, 1000000),
    ])
    def test_valid_baud_rates(self, baud_rate, expected):
        """Тест валидных скоростей передачи"""
        from uart_sim import UARTConfig
        
        config = UARTConfig(baud_rate=baud_rate)
        assert config.baud_rate == expected
    
    def test_invalid_baud_rate(self):
        """Тест невалидной скорости"""
        from uart_sim import UARTConfig
        
        with pytest.raises(ValueError):
            UARTConfig(baud_rate=0)
        
        with pytest.raises(ValueError):
            UARTConfig(baud_rate=-1)


class TestUARTDriver:
    """Тесты драйвера UART"""
    
    @pytest.fixture
    def uart_driver(self):
        """Фикстура для создания драйвера"""
        from uart_sim import UARTDriver, UARTConfig
        
        config = UARTConfig(
            baud_rate=115200,
            data_bits=8,
            stop_bits=1,
            parity=0
        )
        driver = UARTDriver(config)
        yield driver
        driver.close()
    
    def test_init_success(self, uart_driver):
        """Тест успешной инициализации"""
        assert uart_driver.is_initialized()
    
    def test_transmit_success(self, uart_driver):
        """Тест успешной передачи"""
        data = bytes([0x01, 0x02, 0x03, 0x04])
        result = uart_driver.transmit(data, timeout=100)
        assert result == 0  # Success
    
    def test_transmit_empty_data(self, uart_driver):
        """Тест передачи пустых данных"""
        with pytest.raises(ValueError):
            uart_driver.transmit(b'', timeout=100)
    
    def test_transmit_large_data(self, uart_driver):
        """Тест передачи большого объёма данных"""
        # Создаём данные размером больше буфера
        large_data = bytes([0xAA] * 2048)
        result = uart_driver.transmit(large_data, timeout=1000)
        assert result == 0
    
    def test_receive_success(self, uart_driver):
        """Тест успешного приёма"""
        # Симулируем входящие данные
        uart_driver._simulate_rx_data(bytes([0x55, 0xAA, 0x00, 0xFF]))
        
        buffer = bytearray(4)
        result = uart_driver.receive(buffer, timeout=100)
        assert result == 0
        assert buffer == bytearray([0x55, 0xAA, 0x00, 0xFF])
    
    def test_receive_timeout(self, uart_driver):
        """Тест таймаута приёма"""
        buffer = bytearray(4)
        result = uart_driver.receive(buffer, timeout=10)
        assert result == 2  # Timeout error
    
    def test_async_receive(self, uart_driver):
        """Тест асинхронного приёма"""
        received_data = []
        
        def callback(data):
            received_data.append(data)
        
        uart_driver.set_rx_callback(callback)
        uart_driver.start_async_receive()
        
        # Симулируем входящие данные
        uart_driver._simulate_rx_data(bytes([0x01, 0x02]))
        
        # Проверяем, что callback был вызван
        assert len(received_data) > 0
        assert received_data[0] == bytes([0x01, 0x02])
    
    def test_ring_buffer_overflow(self, uart_driver):
        """Тест переполнения кольцевого буфера"""
        # Заполняем буфер больше его ёмкости
        overflow_count = 0
        
        for i in range(300):  # Буфер = 256 байт
            try:
                uart_driver._simulate_rx_data(bytes([i % 256]))
            except OverflowError:
                overflow_count += 1
        
        # Проверяем, что часть данных была потеряна
        assert overflow_count > 0
    
    def test_error_handling_parity(self, uart_driver):
        """Тест обработки ошибки чётности"""
        uart_driver._simulate_parity_error()
        
        buffer = bytearray(4)
        result = uart_driver.receive(buffer, timeout=100)
        # Должен вернуть ошибку или восстановиться
        assert result in [1, 0]  # Error или OK с пропуском байта
    
    def test_error_handling_framing(self, uart_driver):
        """Тест обработки ошибки кадрирования"""
        uart_driver._simulate_framing_error()
        
        buffer = bytearray(4)
        result = uart_driver.receive(buffer, timeout=100)
        assert result in [1, 0]


class TestUARTIntegration:
    """Интеграционные тесты UART"""
    
    def test_full_duplex_communication(self):
        """Тест полнодуплексной связи"""
        from uart_sim import UARTDriver, UARTConfig
        
        config = UARTConfig(baud_rate=115200)
        
        # Создаём два связанных драйвера
        driver1 = UARTDriver(config, loopback=True)
        driver2 = UARTDriver(config, linked_to=driver1)
        
        try:
            # Передача от driver1 к driver2
            tx_data = bytes([0xDE, 0xAD, 0xBE, 0xEF])
            driver1.transmit(tx_data, timeout=100)
            
            rx_buffer = bytearray(4)
            driver2.receive(rx_buffer, timeout=100)
            
            assert rx_buffer == bytearray(tx_data)
        finally:
            driver1.close()
            driver2.close()
    
    @pytest.mark.parametrize("baud_rate,delay_ms", [
        (9600, 50),
        (115200, 5),
        (921600, 1),
    ])
    def test_timing_accuracy(self, baud_rate, delay_ms):
        """Тест точности таймингов"""
        import time
        from uart_sim import UARTDriver, UARTConfig
        
        config = UARTConfig(baud_rate=baud_rate)
        driver = UARTDriver(config)
        
        try:
            # Измеряем время передачи известного объёма данных
            data_size = 1000
            data = bytes([0xAA] * data_size)
            
            start_time = time.time()
            driver.transmit(data, timeout=5000)
            elapsed = (time.time() - start_time) * 1000  # мс
            
            # Проверяем, что время примерно соответствует скорости
            expected_time = (data_size * 10 * 1000) / baud_rate  # 10 бит на байт
            tolerance = 0.2  # 20% допуск
            
            assert abs(elapsed - expected_time) / expected_time < tolerance
        finally:
            driver.close()


class TestUARTDMA:
    """Тесты DMA режима UART"""
    
    def test_dma_transmit(self):
        """Тест DMA передачи"""
        from uart_sim import UARTDriver, UARTConfig, DMAMode
        
        config = UARTConfig(baud_rate=921600)
        driver = UARTDriver(config, dma_mode=DMAMode.ENABLED)
        
        try:
            # Большой объём данных для DMA
            data = bytes(range(256)) * 10
            result = driver.transmit(data, timeout=100)
            assert result == 0
        finally:
            driver.close()
    
    def test_dma_circular_receive(self):
        """Тест кругового DMA приёма"""
        from uart_sim import UARTDriver, UARTConfig, DMAMode
        
        config = UARTConfig(baud_rate=115200)
        driver = UARTDriver(config, dma_mode=DMAMode.ENABLED)
        
        received = []
        
        def callback(data):
            received.extend(data)
        
        try:
            driver.set_rx_callback(callback)
            driver.start_dma_circular_receive(buffer_size=512)
            
            # Симулируем поток данных
            for i in range(10):
                driver._simulate_rx_data(bytes([i]))
            
            # Проверяем, что данные приняты
            assert len(received) >= 10
        finally:
            driver.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
