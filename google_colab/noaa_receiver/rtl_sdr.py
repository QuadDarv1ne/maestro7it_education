"""
Интерфейс для работы с RTL-SDR приёмником
"""

import numpy as np
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

from .logger import get_logger
from .config import Config

logger = get_logger("noaa_receiver.rtl_sdr")


class RTLSDRInterface:
    """
    Класс для работы с RTL-SDR приёмником
    
    Поддерживает:
    - Захват IQ-данных с RTL-SDR
    - Калибровку частоты (PPM correction)
    - Сохранение IQ-данных в файл
    - Загрузку ранее записанных IQ-данных
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.sdr = None
        self._is_device_available = False
        
    def connect(self) -> bool:
        """
        Подключение к RTL-SDR устройству
        
        Returns:
            True если подключение успешно
        """
        try:
            from rtlsdr import RtlSdr
            
            self.sdr = RtlSdr()
            self._configure_sdr()
            self._is_device_available = True
            
            logger.info("✅ RTL-SDR устройство подключено")
            logger.info(f"   Sample rate: {self.sdr.sample_rate/1e6:.2f} MHz")
            logger.info(f"   Center freq: {self.sdr.center_freq/1e6:.2f} MHz")
            logger.info(f"   Gain: {self.sdr.gain} dB")
            
            return True
            
        except ImportError:
            logger.warning("⚠️  Библиотека pyrtlsdr не найдена. Запуск в режиме симуляции.")
            logger.warning("   Установите: pip install pyrtlsdr")
            return False
            
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к RTL-SDR: {e}")
            return False
    
    def _configure_sdr(self) -> None:
        """Настройка параметров RTL-SDR"""
        if not self.sdr:
            return
        
        sdr_config = self.config.config.get("sdr", {})
        
        self.sdr.sample_rate = sdr_config.get("sample_rate", 2.4e6)
        self.sdr.center_freq = sdr_config.get("center_freq", 137.62e6)
        self.sdr.gain = sdr_config.get("gain", 40)
        
        # Применение коррекции частоты (PPM)
        ppm = sdr_config.get("ppm_correction", 0)
        if ppm != 0:
            self.sdr.freq_correction = ppm
            logger.info(f"   Применена коррекция частоты: {ppm} PPM")
    
    def read_samples(self, num_samples: int) -> np.ndarray:
        """
        Чтение IQ-выборок с устройства
        
        Args:
            num_samples: Количество выборок
        
        Returns:
            Массив комплексных выборок
        """
        if self._is_device_available and self.sdr:
            samples = self.sdr.read_samples(num_samples)
            logger.debug(f"Прочитано {len(samples)} выборок")
            return samples
        else:
            # Возврат симулированных данных
            logger.debug("Используются симулированные данные")
            return self._simulate_iq_signal(num_samples)
    
    def capture(
        self,
        duration: float,
        output_file: Optional[str] = None,
    ) -> np.ndarray:
        """
        Захват сигнала заданной длительности
        
        Args:
            duration: Длительность захвата в секундах
            output_file: Путь для сохранения IQ-данных (опционально)
        
        Returns:
            Массив комплексных выборок
        """
        sample_rate = self.config.sample_rate
        num_samples = int(sample_rate * duration)
        
        logger.info(f"📡 Начало захвата на {duration} секунд...")
        logger.info(f"   Количество выборок: {num_samples:,}")
        
        # Чтение данных блоками для избежания переполнения памяти
        block_size = int(sample_rate)  # 1 секунда
        all_samples = []
        
        start_time = datetime.now()
        
        for i in range(0, num_samples, block_size):
            remaining = min(block_size, num_samples - i)
            samples = self.read_samples(remaining)
            all_samples.append(samples)
            
            # Прогресс
            elapsed = (datetime.now() - start_time).total_seconds()
            progress = min(100, (i + remaining) / num_samples * 100)
            if i % block_size == 0:
                logger.debug(f"   Прогресс: {progress:.1f}%")
        
        samples_array = np.concatenate(all_samples)
        
        # Сохранение IQ-данных
        if output_file or self.config.get("output", "save_iq", default=False):
            save_path = output_file or self._generate_iq_filename()
            self.save_iq(samples_array, save_path)
        
        elapsed_total = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Захват завершён за {elapsed_total:.1f} сек")
        
        return samples_array
    
    def save_iq(self, samples: np.ndarray, filepath: str) -> None:
        """
        Сохранение IQ-данных в файл
        
        Args:
            samples: Комплексные выборки
            filepath: Путь к файлу
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Сохранение в формате complex64
        samples.astype(np.complex64).tofile(path)
        
        file_size_mb = path.stat().st_size / (1024 * 1024)
        logger.info(f"💾 IQ-данные сохранены: {path.name} ({file_size_mb:.1f} MB)")
    
    def load_iq(self, filepath: str, dtype: np.dtype = np.complex64) -> np.ndarray:
        """
        Загрузка IQ-данных из файла
        
        Args:
            filepath: Путь к файлу
            dtype: Тип данных
        
        Returns:
            Массив комплексных выборок
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        
        samples = np.fromfile(path, dtype=dtype)
        logger.info(f"📂 Загружено {len(samples):,} выборок из {filepath}")
        
        return samples
    
    def _simulate_iq_signal(self, num_samples: int) -> np.ndarray:
        """
        Симуляция IQ-сигнала NOAA APT
        
        Args:
            num_samples: Количество выборок
        
        Returns:
            Комплексные выборки с симулированным сигналом
        """
        sample_rate = self.config.sample_rate
        duration = num_samples / sample_rate
        
        t = np.arange(0, duration, 1/sample_rate)
        
        # Несущая на 2400 Гц
        carrier_freq = self.config.get("decoder", "carrier_freq", default=2400)
        
        # Модулирующий сигнал (имитация строк изображения)
        line_rate = self.config.get("decoder", "line_rate", default=2)
        
        # Создаём "строки" изображения
        modulation = 0.5 * (1 + np.sin(2 * np.pi * line_rate * t))
        
        # Добавляем вариации для реалистичности
        modulation *= 0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t)
        
        # AM модуляция
        carrier = np.cos(2 * np.pi * carrier_freq * t)
        signal = modulation * carrier
        
        # Квадратурная компонента
        quadrature = modulation * np.sin(2 * np.pi * carrier_freq * t)
        
        # Добавляем шум
        noise_level = 0.1
        signal += noise_level * np.random.randn(len(t))
        quadrature += noise_level * np.random.randn(len(t))
        
        # Комплексный сигнал
        iq_signal = signal + 1j * quadrature
        
        return iq_signal
    
    def _generate_iq_filename(self) -> str:
        """Генерация имени файла для IQ-данных"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        freq_mhz = self.config.center_freq / 1e6
        return f"iq_{timestamp}_{freq_mhz:.2f}MHz.bin"
    
    def close(self) -> None:
        """Закрытие соединения с устройством"""
        if self.sdr:
            try:
                self.sdr.close()
                logger.info("RTL-SDR устройство закрыто")
            except Exception as e:
                logger.warning(f"Ошибка при закрытии: {e}")
            finally:
                self.sdr = None
                self._is_device_available = False
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
