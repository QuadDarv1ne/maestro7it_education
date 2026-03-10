#!/usr/bin/env python3
"""
CAN Bus Simulator and Testing Utility
Утилита для симуляции и тестирования CAN шины

Используется для наземных испытаний бортовой электроники.
"""

from dataclasses import dataclass, field
from typing import List, Callable, Optional, Dict
from enum import IntEnum
from collections import deque
import threading
import time
import struct
import hashlib


class CANStatus(IntEnum):
    """Статус CAN операции"""
    OK = 0
    ERROR = 1
    BUSY = 2
    TIMEOUT = 3
    BUS_OFF = 4


@dataclass
class CANMessage:
    """CAN сообщение"""
    id: int = 0
    extended: bool = False
    remote: bool = False
    data: bytes = field(default_factory=bytes)
    timestamp: float = 0.0
    
    def __post_init__(self):
        if len(self.data) > 8:
            raise ValueError("CAN data cannot exceed 8 bytes")
    
    @classmethod
    def from_bytes(cls, raw: bytes) -> 'CANMessage':
        """Десериализация сообщения из байтов."""
        if len(raw) < 4:
            raise ValueError("Message too short")
        
        header = struct.unpack('<I', raw[:4])[0]
        msg_id = header & 0x1FFFFFFF
        extended = bool(header & 0x80000000)
        remote = bool(header & 0x40000000)
        dlc = raw[4] if len(raw) > 4 else 0
        data = raw[5:5+dlc] if dlc > 0 else bytes()
        
        return cls(id=msg_id, extended=extended, remote=remote, data=data)
    
    def to_bytes(self) -> bytes:
        """Сериализация сообщения в байты."""
        header = self.id
        if self.extended:
            header |= 0x80000000
        if self.remote:
            header |= 0x40000000
        
        return struct.pack('<IB', header, len(self.data)) + self.data


class CANFilter:
    """Фильтр CAN сообщений"""
    
    def __init__(self, id_mask: int, mask: int, extended: bool = False):
        """
        Args:
            id_mask: Идентификатор для сравнения
            mask: Маска (1 = проверять бит, 0 = игнорировать)
            extended: Расширенный кадр
        """
        self.id_mask = id_mask
        self.mask = mask
        self.extended = extended
    
    def match(self, msg: CANMessage) -> bool:
        """Проверка соответствия сообщения фильтру."""
        if self.extended != msg.extended:
            return False
        
        return (msg.id & self.mask) == (self.id_mask & self.mask)


class CANStatistics:
    """Статистика CAN шины"""
    
    def __init__(self):
        self.tx_count = 0
        self.rx_count = 0
        self.error_count = 0
        self.bus_off_count = 0
        self.tx_error_counter = 0
        self.rx_error_counter = 0
        self._lock = threading.Lock()
    
    def increment_tx(self):
        with self._lock:
            self.tx_count += 1
    
    def increment_rx(self):
        with self._lock:
            self.rx_count += 1
    
    def increment_error(self):
        with self._lock:
            self.error_count += 1
    
    def get_stats(self) -> dict:
        with self._lock:
            return {
                'tx_count': self.tx_count,
                'rx_count': self.rx_count,
                'error_count': self.error_count,
                'bus_off_count': self.bus_off_count,
                'tx_error_counter': self.tx_error_counter,
                'rx_error_counter': self.rx_error_counter
            }
    
    def reset(self):
        with self._lock:
            self.tx_count = 0
            self.rx_count = 0
            self.error_count = 0


class CANController:
    """
    Симулятор CAN контроллера.
    
    Поддерживает:
    - Standard (11-bit) и Extended (29-bit) идентификаторы
    - Фильтрация сообщений
    - Callback при приёме
    - Статистика ошибок
    - Режим loopback
    """
    
    def __init__(self, baud_rate: int = 500000, loopback: bool = False):
        """
        Args:
            baud_rate: Скорость CAN шины (бит/с)
            loopback: Режим внутренней петли
        """
        self._baud_rate = baud_rate
        self._loopback = loopback
        self._initialized = False
        self._bus_off = False
        
        # Очередь приёма
        self._rx_queue = deque(maxlen=100)
        self._rx_lock = threading.Lock()
        
        # Фильтры
        self._filters: List[CANFilter] = []
        
        # Callback
        self._rx_callback: Optional[Callable[[CANMessage], None]] = None
        
        # Статистика
        self._stats = CANStatistics()
        
        # Поток обработки
        self._running = False
        self._rx_thread: Optional[threading.Thread] = None
    
    def init(self) -> CANStatus:
        """Инициализация CAN контроллера."""
        if self._initialized:
            return CANStatus.OK
        
        # Расчёт таймингов (симуляция)
        # В реальном проекте настройка BTR регистров
        
        self._initialized = True
        return CANStatus.OK
    
    def close(self):
        """Деинициализация."""
        self._running = False
        if self._rx_thread:
            self._rx_thread.join(timeout=1.0)
        self._initialized = False
    
    def transmit(self, msg: CANMessage, timeout: int = 100) -> CANStatus:
        """
        Передача CAN сообщения.
        
        Args:
            msg: Сообщение для передачи
            timeout: Таймаут в мс
        
        Returns:
            Статус операции
        """
        if not self._initialized:
            return CANStatus.ERROR
        
        if self._bus_off:
            return CANStatus.BUS_OFF
        
        # Симуляция времени передачи
        frame_bits = 44 + len(msg.data) * 8  # Базовый кадр + данные
        if msg.extended:
            frame_bits += 18  # Extended ID
        
        tx_time = frame_bits / self._baud_rate * 1000  # мс
        time.sleep(min(tx_time / 1000, timeout / 1000))
        
        self._stats.increment_tx()
        
        # Loopback
        if self._loopback:
            self._receive_message(msg)
        
        return CANStatus.OK
    
    def receive(self, timeout: int = 100) -> Optional[CANMessage]:
        """
        Приём CAN сообщения (блокирующий).
        
        Args:
            timeout: Таймаут в мс
        
        Returns:
            Принятое сообщение или None при таймауте
        """
        start_time = time.time()
        
        while True:
            with self._rx_lock:
                if self._rx_queue:
                    msg = self._rx_queue.popleft()
                    self._stats.increment_rx()
                    return msg
            
            elapsed = (time.time() - start_time) * 1000
            if elapsed >= timeout:
                return None
            
            time.sleep(0.001)
    
    def add_filter(self, filter_obj: CANFilter):
        """Добавить фильтр приёма."""
        self._filters.append(filter_obj)
    
    def set_rx_callback(self, callback: Callable[[CANMessage], None]):
        """Установить callback для асинхронного приёма."""
        self._rx_callback = callback
    
    def _receive_message(self, msg: CANMessage):
        """Внутренний метод обработки принятого сообщения."""
        # Проверка фильтров
        if self._filters:
            matched = any(f.match(msg) for f in self._filters)
            if not matched:
                return
        
        # Добавление в очередь
        with self._rx_lock:
            self._rx_queue.append(msg)
        
        # Callback
        if self._rx_callback:
            self._rx_callback(msg)
    
    def get_statistics(self) -> dict:
        """Получить статистику шины."""
        return self._stats.get_stats()
    
    def simulate_bus_error(self):
        """Симуляция ошибки шины."""
        self._stats.increment_error()
    
    def simulate_bus_off(self):
        """Симуляция состояния bus-off."""
        self._bus_off = True
        self._stats.bus_off_count += 1
    
    def recover_bus(self):
        """Восстановление после bus-off."""
        self._bus_off = False


class CANopenNode:
    """
    Симулятор CANopen узла для тестирования бортовой сети.
    
    Поддерживает:
    - NMT (Network Management)
    - SDO (Service Data Object)
    - PDO (Process Data Object)
    - Heartbeat
    """
    
    # CANopen COB-IDs
    COB_NMT = 0x000
    COB_SYNC = 0x080
    COB_EMCY = 0x080
    COB_TPDO1 = 0x180
    COB_RPDO1 = 0x200
    COB_TPDO2 = 0x280
    COB_RPDO2 = 0x300
    COB_TSDO = 0x580
    COB_RSDO = 0x600
    
    def __init__(self, node_id: int, can: CANController):
        """
        Args:
            node_id: Идентификатор узла (1-127)
            can: CAN контроллер
        """
        if node_id < 1 or node_id > 127:
            raise ValueError("Node ID must be 1-127")
        
        self._node_id = node_id
        self._can = can
        self._state = 'INIT'
        self._heartbeat_interval = 1000  # мс
        self._od: Dict[int, bytes] = {}  # Object Dictionary
        
        # Регистрация callback
        can.set_rx_callback(self._on_can_message)
        
        # Инициализация Object Dictionary
        self._init_object_dictionary()
    
    def _init_object_dictionary(self):
        """Инициализация типовых объектов."""
        # Device type
        self._od[0x1000] = struct.pack('<I', 0x00000000)
        # Error register
        self._od[0x1001] = bytes([0x00])
        # Status word
        self._od[0x1002] = bytes([0x00])
    
    def _on_can_message(self, msg: CANMessage):
        """Обработка входящего CAN сообщения."""
        cob_id = msg.id >> 7
        node_id = msg.id & 0x7F
        
        if node_id != self._node_id:
            return
        
        if cob_id == 0x0:  # NMT
            self._handle_nmt(msg)
        elif cob_id == 0xB:  # RSDO
            self._handle_sdo_request(msg)
    
    def _handle_nmt(self, msg: CANMessage):
        """Обработка NMT команды."""
        if len(msg.data) < 1:
            return
        
        command = msg.data[0]
        
        if command == 0x01:  # Start
            self._state = 'OPERATIONAL'
        elif command == 0x02:  # Stop
            self._state = 'STOPPED'
        elif command == 0x80:  # Pre-operational
            self._state = 'PRE_OPERATIONAL'
        elif command == 0x81:  # Reset node
            self._state = 'INIT'
            self._init_object_dictionary()
    
    def _handle_sdo_request(self, msg: CANMessage):
        """Обработка SDO запроса."""
        if len(msg.data) < 8:
            return
        
        cs = msg.data[0] >> 5  # Command specifier
        index = struct.unpack('<H', msg.data[1:3])[0]
        subindex = msg.data[3]
        
        if cs == 1:  # Initiate SDO Upload (read request)
            self._send_sdo_response(index, subindex)
        elif cs == 2:  # Initiate SDO Download (write request)
            self._write_od_entry(index, subindex, msg.data[4:8])
    
    def _send_sdo_response(self, index: int, subindex: int):
        """Отправка SDO ответа."""
        key = (index << 8) | subindex
        data = self._od.get(key, bytes(4))
        
        response = bytearray(8)
        response[0] = 0x43  # Upload response, 4 bytes
        response[1:3] = struct.pack('<H', index)
        response[3] = subindex
        response[4:8] = data[:4]
        
        cob_id = self.COB_TSDO + self._node_id
        msg = CANMessage(id=cob_id, data=bytes(response))
        self._can.transmit(msg)
    
    def _write_od_entry(self, index: int, subindex: int, data: bytes):
        """Запись в Object Dictionary."""
        key = (index << 8) | subindex
        self._od[key] = data
    
    def send_heartbeat(self):
        """Отправка heartbeat сообщения."""
        state_codes = {
            'INIT': 0x00,
            'PRE_OPERATIONAL': 0x7F,
            'OPERATIONAL': 0x05,
            'STOPPED': 0x04
        }
        
        cob_id = 0x700 + self._node_id
        data = bytes([state_codes.get(self._state, 0x00)])
        
        msg = CANMessage(id=cob_id, data=data)
        self._can.transmit(msg)
    
    def send_pdo(self, pdo_num: int, data: bytes):
        """Отправка PDO."""
        cob_ids = {
            1: self.COB_TPDO1 + self._node_id,
            2: self.COB_TPDO2 + self._node_id
        }
        
        cob_id = cob_ids.get(pdo_num)
        if cob_id:
            msg = CANMessage(id=cob_id, data=data)
            self._can.transmit(msg)
    
    def get_state(self) -> str:
        """Получение состояния узла."""
        return self._state


# ============================================================================
# Пример использования
# ============================================================================

def example_can_basic():
    """Пример базового использования CAN."""
    print("=== Basic CAN Example ===")
    
    # Создание CAN контроллера
    can = CANController(baud_rate=500000, loopback=True)
    can.init()
    
    # Добавление фильтра (приём сообщений с ID 0x100-0x1FF)
    can.add_filter(CANFilter(id_mask=0x100, mask=0x700))
    
    # Отправка сообщения
    msg = CANMessage(id=0x123, data=bytes([0xDE, 0xAD, 0xBE, 0xEF]))
    result = can.transmit(msg)
    print(f"Transmit status: {CANStatus(result).name}")
    
    # Приём сообщения
    received = can.receive(timeout=100)
    if received:
        print(f"Received: ID=0x{received.id:03X}, Data={received.data.hex()}")
    
    # Статистика
    stats = can.get_statistics()
    print(f"Statistics: TX={stats['tx_count']}, RX={stats['rx_count']}")
    
    can.close()


def example_canopen():
    """Пример использования CANopen."""
    print("\n=== CANopen Example ===")
    
    can = CANController(baud_rate=500000, loopback=True)
    can.init()
    
    # Создание узла CANopen
    node = CANopenNode(node_id=1, can=can)
    
    # Отправка heartbeat
    node.send_heartbeat()
    print(f"Node state: {node.get_state()}")
    
    # Отправка PDO
    node.send_pdo(1, bytes([0x01, 0x02, 0x03, 0x04]))
    
    # Приём сообщения
    received = can.receive(timeout=100)
    if received:
        print(f"Received PDO: ID=0x{received.id:03X}, Data={received.data.hex()}")
    
    can.close()


if __name__ == '__main__':
    example_can_basic()
    example_canopen()
