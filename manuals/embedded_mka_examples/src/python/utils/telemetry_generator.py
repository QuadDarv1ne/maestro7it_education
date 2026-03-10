#!/usr/bin/env python3
"""
Telemetry Generator for MKA Ground Testing
Генератор телеметрии для наземных испытаний МКА

Используется для тестирования наземной системы управления (НСУ).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Callable
from enum import IntEnum
import struct
import time
import json
import random


class TelemetryType(IntEnum):
    """Типы телеметрии"""
    HOUSEKEEPING = 0x01
    ADCS = 0x02
    POWER = 0x03
    PAYLOAD = 0x04
    THERMAL = 0x05
    COMM = 0x06


@dataclass
class TelemetryParameter:
    """Параметр телеметрии"""
    name: str
    value: float
    unit: str
    min_value: float
    max_value: float
    timestamp: float = 0.0
    
    def is_in_range(self) -> bool:
        """Проверка нахождения в допустимом диапазоне."""
        return self.min_value <= self.value <= self.max_value


class TelemetryFrame:
    """Кадр телеметрии"""
    
    HEADER = bytes([0xEB, 0x90])  # Sync word
    FOOTER = bytes([0x0D, 0x0A])  # CR LF
    
    def __init__(self, frame_type: TelemetryType, sequence: int = 0):
        self.frame_type = frame_type
        self.sequence = sequence
        self.timestamp = time.time()
        self.parameters: Dict[str, TelemetryParameter] = {}
    
    def add_parameter(self, name: str, value: float, unit: str,
                     min_val: float, max_val: float):
        """Добавление параметра."""
        self.parameters[name] = TelemetryParameter(
            name=name,
            value=value,
            unit=unit,
            min_value=min_val,
            max_value=max_val,
            timestamp=self.timestamp
        )
    
    def encode(self) -> bytes:
        """Кодирование кадра в байты."""
        # Формат кадра:
        # [HEADER(2)][TYPE(1)][SEQ(4)][TIME(4)][PARAM_COUNT(1)][PARAMS][CRC16(2)][FOOTER(2)]
        
        data = bytearray()
        data.extend(self.HEADER)
        data.append(self.frame_type)
        data.extend(struct.pack('<I', self.sequence))
        data.extend(struct.pack('<I', int(self.timestamp)))
        data.append(len(self.parameters))
        
        # Кодирование параметров
        for name, param in self.parameters.items():
            # [NAME_LEN(1)][NAME][VALUE(4)][MIN(4)][MAX(4)]
            name_bytes = name.encode('ascii')[:15]
            data.append(len(name_bytes))
            data.extend(name_bytes)
            data.extend(struct.pack('<f', param.value))
            data.extend(struct.pack('<f', param.min_value))
            data.extend(struct.pack('<f', param.max_value))
        
        # CRC16
        crc = self._calculate_crc16(bytes(data))
        data.extend(struct.pack('<H', crc))
        data.extend(self.FOOTER)
        
        return bytes(data)
    
    @classmethod
    def decode(cls, data: bytes) -> Optional['TelemetryFrame']:
        """Декодирование кадра из байтов."""
        if len(data) < 15:  # Минимальный размер
            return None
        
        if data[:2] != cls.HEADER:
            return None
        
        if data[-2:] != cls.FOOTER:
            return None
        
        frame_type = TelemetryType(data[2])
        sequence = struct.unpack('<I', data[3:7])[0]
        timestamp = struct.unpack('<I', data[7:11])[0]
        param_count = data[11]
        
        frame = cls(frame_type, sequence)
        frame.timestamp = timestamp
        
        offset = 12
        for _ in range(param_count):
            name_len = data[offset]
            offset += 1
            name = data[offset:offset+name_len].decode('ascii')
            offset += name_len
            
            value = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            min_val = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            max_val = struct.unpack('<f', data[offset:offset+4])[0]
            offset += 4
            
            frame.add_parameter(name, value, '', min_val, max_val)
        
        return frame
    
    @staticmethod
    def _calculate_crc16(data: bytes) -> int:
        """Расчёт CRC16-CCITT."""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc
    
    def to_json(self) -> str:
        """Преобразование в JSON."""
        return json.dumps({
            'type': self.frame_type.name,
            'sequence': self.sequence,
            'timestamp': self.timestamp,
            'parameters': {
                name: {
                    'value': param.value,
                    'unit': param.unit,
                    'range': [param.min_value, param.max_value],
                    'in_range': param.is_in_range()
                }
                for name, param in self.parameters.items()
            }
        }, indent=2)


class TelemetryGenerator:
    """
    Генератор телеметрии для тестирования НСУ.
    
    Генерирует реалистичные данные телеметрии с учётом:
    - Временны́х зависимостей (орбитальный период)
    - Корреляций между параметрами
    - Шумов и погрешностей измерений
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Args:
            seed: Seed для генератора случайных чисел (для воспроизводимости)
        """
        if seed is not None:
            random.seed(seed)
        
        self._sequence = 0
        self._start_time = time.time()
        
        # Состояние спутника
        self._orbit_phase = 0.0  # 0-1 за орбитальный период
        self._orbit_period = 5400  # с (90 минут для НОО)
        self._battery_charge = 100.0  # %
        self._temperature_internal = 20.0  # °C
        
        # Callback для пользовательских параметров
        self._custom_generators: List[Callable[[TelemetryFrame], None]] = []
    
    def add_custom_generator(self, generator: Callable[[TelemetryFrame], None]):
        """Добавление генератора пользовательских параметров."""
        self._custom_generators.append(generator)
    
    def update_orbit(self, dt: float):
        """Обновление фазы орбиты."""
        self._orbit_phase += dt / self._orbit_period
        if self._orbit_phase >= 1.0:
            self._orbit_phase -= 1.0
    
    def is_in_sunlight(self) -> bool:
        """Проверка нахождения на освещённой части орбиты."""
        # Примерно 60% орбиты на освещённой стороне
        return self._orbit_phase < 0.6
    
    def generate_housekeeping(self) -> TelemetryFrame:
        """Генерация телеметрии домика."""
        frame = TelemetryFrame(TelemetryType.HOUSEKEEPING, self._sequence)
        self._sequence += 1
        
        # Обновление состояния
        dt = 1.0  # Период генерации
        self.update_orbit(dt)
        
        # Температура внутренняя
        if self.is_in_sunlight():
            self._temperature_internal += 0.1 * random.gauss(1, 0.2)
        else:
            self._temperature_internal -= 0.05 * random.gauss(1, 0.2)
        self._temperature_internal = max(-10, min(50, self._temperature_internal))
        
        # Добавление параметров
        frame.add_parameter('CPU_LOAD', random.gauss(25, 5), '%', 0, 100)
        frame.add_parameter('MEM_USED', random.gauss(45, 10), '%', 0, 100)
        frame.add_parameter('UPTIME', time.time() - self._start_time, 's', 0, 1e9)
        frame.add_parameter('TEMP_INTERNAL', self._temperature_internal, 'degC', -40, 85)
        frame.add_parameter('RESET_COUNT', random.randint(0, 10), '', 0, 255)
        frame.add_parameter('WATCHDOG_RESETS', random.randint(0, 3), '', 0, 255)
        
        return frame
    
    def generate_power(self) -> TelemetryFrame:
        """Генерация телеметрии СЭП."""
        frame = TelemetryFrame(TelemetryType.POWER, self._sequence)
        self._sequence += 1
        
        # Напряжение батареи зависит от заряда
        battery_voltage = 6.0 + 2.4 * (self._battery_charge / 100.0)
        battery_voltage += random.gauss(0, 0.1)
        
        # Ток солнечных панелей
        if self.is_in_sunlight():
            solar_current = random.gauss(800, 50)  # mA
            self._battery_charge = min(100, self._battery_charge + 0.5)
        else:
            solar_current = random.gauss(5, 2)  # mA (темновой ток)
            self._battery_charge = max(0, self._battery_charge - 0.2)
        
        # Токи потребителей
        current_3v3 = random.gauss(150, 20)  # mA
        current_5v = random.gauss(100, 15)  # mA
        current_battery = solar_current - current_3v3 - current_5v
        
        frame.add_parameter('VBAT', battery_voltage, 'V', 5.0, 8.4)
        frame.add_parameter('IBAT', current_battery / 1000, 'A', -2.0, 2.0)
        frame.add_parameter('BAT_CHARGE', self._battery_charge, '%', 0, 100)
        frame.add_parameter('ISOLAR', solar_current, 'mA', 0, 2000)
        frame.add_parameter('V3V3', 3.3 + random.gauss(0, 0.05), 'V', 3.0, 3.6)
        frame.add_parameter('V5V', 5.0 + random.gauss(0, 0.1), 'V', 4.5, 5.5)
        frame.add_parameter('I3V3', current_3v3, 'mA', 0, 500)
        frame.add_parameter('I5V', current_5v, 'mA', 0, 500)
        
        # Температуры элементов СЭП
        frame.add_parameter('TEMP_BAT', random.gauss(15, 5), 'degC', -20, 60)
        frame.add_parameter('TEMP_SOLAR', random.gauss(25 if self.is_in_sunlight() else -20, 10), 
                          'degC', -60, 100)
        
        return frame
    
    def generate_adcs(self) -> TelemetryFrame:
        """Генерация телеметрии СОС."""
        frame = TelemetryFrame(TelemetryType.ADCS, self._sequence)
        self._sequence += 1
        
        # Угловые скорости (медленное вращение)
        omega_x = random.gauss(0.001, 0.0005)  # рад/с
        omega_y = random.gauss(0.001, 0.0005)
        omega_z = random.gauss(0.001, 0.0005)
        
        # Кватернион ориентации (нормированный)
        q = [random.gauss(0, 0.1) for _ in range(3)] + [1.0]
        norm = sum(x*x for x in q) ** 0.5
        q = [x/norm for x in q]
        
        # Магнитное поле (зависит от положения на орбите)
        mag_scale = 30000 + 10000 * (1 - abs(self._orbit_phase - 0.5) * 2)
        mag_x = random.gauss(0, mag_scale)
        mag_y = random.gauss(mag_scale * 0.7, mag_scale * 0.1)
        mag_z = random.gauss(-mag_scale * 0.5, mag_scale * 0.1)
        
        frame.add_parameter('OMEGA_X', omega_x * 1000, 'mrad/s', -100, 100)
        frame.add_parameter('OMEGA_Y', omega_y * 1000, 'mrad/s', -100, 100)
        frame.add_parameter('OMEGA_Z', omega_z * 1000, 'mrad/s', -100, 100)
        frame.add_parameter('Q0', q[3], '', -1, 1)
        frame.add_parameter('Q1', q[0], '', -1, 1)
        frame.add_parameter('Q2', q[1], '', -1, 1)
        frame.add_parameter('Q3', q[2], '', -1, 1)
        frame.add_parameter('MAG_X', mag_x, 'nT', -60000, 60000)
        frame.add_parameter('MAG_Y', mag_y, 'nT', -60000, 60000)
        frame.add_parameter('MAG_Z', mag_z, 'nT', -60000, 60000)
        
        # Состояние маховиков
        frame.add_parameter('WHEEL_SPEED_1', random.gauss(500, 50), 'rpm', 0, 6000)
        frame.add_parameter('WHEEL_SPEED_2', random.gauss(500, 50), 'rpm', 0, 6000)
        frame.add_parameter('WHEEL_SPEED_3', random.gauss(500, 50), 'rpm', 0, 6000)
        
        return frame
    
    def generate_thermal(self) -> TelemetryFrame:
        """Генерация тепловой телеметрии."""
        frame = TelemetryFrame(TelemetryType.THERMAL, self._sequence)
        self._sequence += 1
        
        in_sun = self.is_in_sunlight()
        
        # Температуры различных элементов
        frame.add_parameter('TEMP_PANEL_P', random.gauss(50 if in_sun else -30, 10), 
                          'degC', -60, 100)
        frame.add_parameter('TEMP_PANEL_S', random.gauss(-40, 15), 
                          'degC', -60, 100)  # Теневая панель
        frame.add_parameter('TEMP_BAT', random.gauss(20, 5), 'degC', -20, 60)
        frame.add_parameter('TEMP_RADIO', random.gauss(30, 8), 'degC', -30, 70)
        frame.add_parameter('TEMP_CPU', random.gauss(35, 5), 'degC', -30, 85)
        frame.add_parameter('TEMP_PAYLOAD', random.gauss(25, 6), 'degC', -30, 70)
        
        # Состояние терморегулирования
        frame.add_parameter('HEATER_STATE', 0 if in_sun else 1, '', 0, 1)
        frame.add_parameter('HEATER_POWER', 0 if in_sun else random.gauss(2, 0.5), 'W', 0, 10)
        
        return frame
    
    def generate_all(self) -> List[TelemetryFrame]:
        """Генерация всех типов телеметрии."""
        frames = [
            self.generate_housekeeping(),
            self.generate_power(),
            self.generate_adcs(),
            self.generate_thermal()
        ]
        
        # Применение пользовательских генераторов
        for frame in frames:
            for generator in self._custom_generators:
                generator(frame)
        
        return frames


def example_usage():
    """Пример использования генератора."""
    print("=== Telemetry Generator Example ===\n")
    
    # Создание генератора
    gen = TelemetryGenerator(seed=42)
    
    # Генерация нескольких кадров
    for i in range(5):
        print(f"--- Frame {i+1} ---")
        
        # Генерация и вывод телеметрии СЭП
        power_frame = gen.generate_power()
        print(power_frame.to_json())
        
        # Кодирование в бинарный формат
        encoded = power_frame.encode()
        print(f"Encoded size: {len(encoded)} bytes")
        
        # Декодирование обратно
        decoded = TelemetryFrame.decode(encoded)
        if decoded:
            print(f"Decoded successfully: {len(decoded.parameters)} parameters")
        
        print()
        time.sleep(0.1)


if __name__ == '__main__':
    example_usage()
