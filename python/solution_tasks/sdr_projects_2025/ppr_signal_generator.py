"""
Генератор сигналов для российского стандарта ППР (DMR-based).

Характеристики:
- Диапазоны: VHF (146-174 МГц), UHF (400-470 МГц)
- Модуляция: 4-FSK (ETSI TS 102 361-2)
- Мощность: до 2 Вт (при TXVGA=47 dB + LNA)
- Лицензия: Требуется (РКН Приказ №432-П)
"""

import numpy as np
import hackrf
from scipy.signal import gaussord, resample_poly
from typing import List

class PPRTransmitter:
    """
    Класс для генерации и передачи сигналов стандарта ППР.

    Параметры:
        frequency (float): Центральная частота (Гц)
        sample_rate (float): Частота дискретизации (Гц)
        tx_gain (int): Усиление передатчика (0-47 dB)
        num_threads (int): Число потоков обработки
    """
    
    def __init__(
        self,
        frequency: float = 146.5e6,
        sample_rate: float = 2e6,
        tx_gain: int = 30,
        num_threads: int = 4
    ):
        self.hackrf = hackrf.HackRF()
        self.config = {
            'frequency': frequency,
            'sample_rate': sample_rate,
            'tx_gain': tx_gain,
            'num_threads': num_threads
        }
        
        # Настройка аппаратных параметров
        self.hackrf.sample_rate = sample_rate
        self.hackrf.center_freq = frequency
        self.hackrf.txvga_gain = tx_gain

    @staticmethod
    def generate_ppr_frame(
        station_id: int = 0xFFFF,
        payload: bytes = b''
    ) -> np.ndarray:
        """
        Генерация кадра ППР.

        Параметры:
            station_id (int): ID станции (16 бит)
            payload (bytes): Полезная нагрузка (до 256 бит)

        Возвращает:
            np.ndarray: ИКМ-сигнал (формат complex64)
        """
        # Преамбула (64 бита)
        preamble = np.array([1,0]*32, dtype=np.float32)
        
        # Заголовок
        header = np.unpackbits(
            np.array([station_id >> 8, station_id & 0xFF], dtype=np.uint8)
        
        # Формирование полного кадра
        frame = np.concatenate([preamble, header, np.unpackbits(np.frombuffer(payload, dtype=np.uint8))])
        
        # Гауссово формирование импульсов
        filtered = gaussord(frame, BT=0.5, samples_per_symbol=4)
        
        # Ресэмплинг до частоты HackRF
        return resample_poly(filtered, 8, 1).astype(np.complex64)

    def transmit(self, frames: List[np.ndarray]):
        """
        Передача кадров через HackRF.

        Параметры:
            frames (List[np.ndarray]): Список кадров для передачи
        """
        try:
            for frame in frames:
                self.hackrf.transmit(frame)
        except Exception as e:
            print(f"Ошибка передачи: {str(e)}")
        finally:
            self.hackrf.close()

if __name__ == "__main__":
    # Пример: Генерация тестового сигнала
    transmitter = PPRTransmitter(frequency=146.5e6, tx_gain=30)
    frames = [transmitter.generate_ppr_frame(payload=b"TEST") for _ in range(10)]
    transmitter.transmit(frames)
