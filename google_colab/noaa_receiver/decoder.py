"""
NOAA APT Decoder с улучшенной демодуляцией
"""

import numpy as np
from scipy import signal
from scipy.ndimage import median_filter
from typing import Tuple, Optional
from pathlib import Path

from .logger import get_logger
from .config import Config

logger = get_logger("noaa_receiver.decoder")


class NOAADecoder:
    """
    Декодер сигналов NOAA APT
    
    Особенности:
    - Квадратурный детектор для AM демодуляции
    - FIR-фильтры с окном Кайзера
    - Автоматическая регулировка усиления (AGC)
    - Удаление шумов
    """
    
    # Константы APT сигнала
    LINE_RATE = 2  # строк в секунду
    PIXELS_PER_LINE = 4160
    PIXEL_RATE = LINE_RATE * PIXELS_PER_LINE  # 8320 пикселей/сек
    
    # Частоты каналов (Гц)
    CHANNEL_FREQUENCIES = {
        'channel1': 2400,   # Видимый диапазон
        'channel2': 2400,   # Видимый диапазон (квадратура)
        'channel3a': 2400,  # Ближний ИК
        'channel3b': 2400,  # Тепловой ИК
        'channel4': 2400,   # Тепловой ИК
        'channel5': 2400,   # Тепловой ИК
    }
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.sample_rate = self.config.sample_rate
        self.carrier_freq = self.config.get("decoder", "carrier_freq", default=2400)
        self.audio_sample_rate = self.config.get("decoder", "audio_sample_rate", default=20800)
        
        # Параметры фильтров
        self.filter_config = self.config.config.get("filters", {})
        
        # AGC параметры
        self.agc_attack = 0.01
        self.agc_decay = 0.001
        self.agc_target = 0.5
        
    def demodulate_am(self, signal_data: np.ndarray) -> np.ndarray:
        """
        AM демодуляция через преобразование Гильберта
        
        Args:
            signal_data: Входной сигнал
        
        Returns:
            Огибающая сигнала
        """
        analytic = signal.hilbert(signal_data)
        envelope = np.abs(analytic)
        return envelope
    
    def demodulate_iq(self, iq_data: np.ndarray) -> np.ndarray:
        """
        Демодуляция IQ-данных
        
        Args:
            iq_data: Комплексные IQ-выборки
        
        Returns:
            Действительный сигнал (огибающая)
        """
        # Для комплексных данных огибающая — это модуль
        return np.abs(iq_data)
    
    def design_fir_bandpass(
        self,
        low_freq: float,
        high_freq: float,
        fs: float,
        numtaps: Optional[int] = None,
    ) -> np.ndarray:
        """
        Проектирование FIR полосового фильтра с окном Кайзера
        
        Args:
            low_freq: Нижняя частота среза
            high_freq: Верхняя частота среза
            fs: Частота дискретизации
            numtaps: Количество отсчётов фильтра
        
        Returns:
            Коэффициенты фильтра
        """
        if numtaps is None:
            numtaps = self.filter_config.get("fir_taps", 101)
        
        # Нормализованные частоты
        nyq = fs / 2
        low = low_freq / nyq
        high = high_freq / nyq
        
        # FIR фильтр с окном Кайзера
        taps = signal.firwin(
            numtaps,
            [low, high],
            pass_zero=False,
            window='kaiser',
            scale=True,
        )
        
        logger.debug(f"FIR фильтр: {numtaps} тапов, {low_freq}-{high_freq} Гц")
        
        return taps
    
    def apply_agc(
        self,
        signal_data: np.ndarray,
        target: Optional[float] = None,
    ) -> np.ndarray:
        """
        Автоматическая регулировка усиления (AGC)
        
        Args:
            signal_data: Входной сигнал
            target: Целевой уровень сигнала
        
        Returns:
            Сигнал с нормализованной амплитудой
        """
        if target is None:
            target = self.agc_target
        
        # Вычисление огибающей
        envelope = self.demodulate_am(signal_data)
        
        # Сглаживание огибающей для оценки уровня
        kernel_size = int(len(signal_data) * 0.01)  # 1% от длины
        if kernel_size < 3:
            kernel_size = 3
        smoothed_envelope = signal.medfilt(envelope, kernel_size=kernel_size)
        
        # Избегаем деления на ноль
        smoothed_envelope = np.maximum(smoothed_envelope, 1e-10)
        
        # Вычисление коэффициента усиления
        gain = target / smoothed_envelope
        
        # Ограничение усиления
        gain = np.clip(gain, 0.1, 10.0)
        
        # Применение AGC
        output = signal_data * gain
        
        logger.debug(f"AGC применён: target={target}, gain range=[{gain.min():.2f}, {gain.max():.2f}]")
        
        return output
    
    def decimate_signal(
        self,
        signal_data: np.ndarray,
        target_rate: float,
    ) -> Tuple[np.ndarray, float]:
        """
        Децимация сигнала до целевой частоты
        
        Args:
            signal_data: Входной сигнал
            target_rate: Целевая частота дискретизации
        
        Returns:
            (децимированный сигнал, новая частота дискретизации)
        """
        decimation_factor = int(self.sample_rate / target_rate)
        
        # FIR децимация с антиалиасинг фильтром
        decimated = signal.decimate(signal_data, decimation_factor, ftype='fir')
        
        new_rate = self.sample_rate / decimation_factor
        
        logger.debug(f"Децимация: {self.sample_rate/1e6:.2f} MHz → {new_rate/1e3:.1f} kHz")
        
        return decimated, new_rate
    
    def extract_apt_channel(
        self,
        audio_data: np.ndarray,
        fs: float,
        channel: str = 'channel1',
    ) -> np.ndarray:
        """
        Извлечение APT канала из аудиосигнала
        
        Args:
            audio_data: Аудиосигнал
            fs: Частота дискретизации
            channel: Имя канала
        
        Returns:
            Демодулированный сигнал канала
        """
        # Параметры полосового фильтра
        bp_low = self.filter_config.get("bandpass_low", 2300)
        bp_high = self.filter_config.get("bandpass_high", 2500)
        
        # FIR фильтрация
        if self.filter_config.get("use_fir", True):
            taps = self.design_fir_bandpass(bp_low, bp_high, fs)
            filtered = signal.lfilter(taps, [1.0], audio_data)
        else:
            # IIR фильтр ( Butterworth)
            sos = signal.butter(
                self.filter_config.get("filter_order", 5),
                [bp_low, bp_high],
                btype='band',
                fs=fs,
                output='sos',
            )
            filtered = signal.sosfilt(sos, audio_data)
        
        # Демодуляция огибающей
        envelope = self.demodulate_am(filtered)
        
        # Удаление DC компоненты
        envelope = envelope - np.mean(envelope)
        
        return envelope
    
    def resample_to_pixels(
        self,
        apt_signal: np.ndarray,
        fs: float,
    ) -> np.ndarray:
        """
        Ресемплинг сигнала к частоте пикселей
        
        Args:
            apt_signal: APT сигнал
            fs: Частота дискретизации сигнала
        
        Returns:
            Сигнал с частотой пикселей
        """
        target_samples = int(len(apt_signal) * self.PIXEL_RATE / fs)
        
        resampled = signal.resample(apt_signal, target_samples)
        
        logger.debug(f"Ресемплинг: {len(apt_signal)} → {len(resampled)} отсчётов")
        
        return resampled
    
    def form_image(
        self,
        pixel_data: np.ndarray,
        num_channels: int = 1,
    ) -> np.ndarray:
        """
        Формирование изображения из потока пикселей
        
        Args:
            pixel_data: Поток пикселей
            num_channels: Количество каналов
        
        Returns:
            Массив изображения (строки, пиксели)
        """
        # Обрезка до полного числа строк
        pixels_per_line = self.PIXELS_PER_LINE * num_channels
        num_lines = len(pixel_data) // pixels_per_line
        
        if num_lines == 0:
            raise ValueError("Недостаточно данных для формирования изображения")
        
        trimmed = pixel_data[:num_lines * pixels_per_line]
        
        # Формирование 2D массива
        image_2d = trimmed.reshape(num_lines, pixels_per_line)
        
        # Нормализация к 0-255
        image_min = image_2d.min()
        image_max = image_2d.max()
        
        if image_max - image_min > 0:
            image_normalized = (image_2d - image_min) / (image_max - image_min) * 255
        else:
            image_normalized = np.zeros_like(image_2d)
        
        return image_normalized.astype(np.uint8)
    
    def decode_full(
        self,
        iq_data: np.ndarray,
        save_intermediate: bool = False,
    ) -> dict:
        """
        Полное декодирование IQ-данных в изображение
        
        Args:
            iq_data: Комплексные IQ-выборки
            save_intermediate: Сохранять ли промежуточные данные
        
        Returns:
            Словарь с результатами:
            - image: основное изображение
            - channel1, channel2: отдельные каналы
            - metadata: метаданные
        """
        logger.info("🔄 Начало декодирования...")
        
        results = {
            'image': None,
            'channel1': None,
            'channel2': None,
            'metadata': {},
        }
        
        # Шаг 1: Демодуляция IQ
        logger.info("   [1/6] Демодуляция IQ...")
        audio_data = self.demodulate_iq(iq_data)
        results['metadata']['iq_samples'] = len(iq_data)
        
        # Шаг 2: Децимация до аудио частоты
        logger.info("   [2/6] Децимация до аудио частоты...")
        audio_decimated, audio_fs = self.decimate_signal(audio_data, self.audio_sample_rate)
        results['metadata']['audio_sample_rate'] = audio_fs
        
        # Шаг 3: AGC
        logger.info("   [3/6] Применение AGC...")
        audio_agc = self.apply_agc(audio_decimated)
        
        # Шаг 4: Извлечение APT каналов
        logger.info("   [4/6] Извлечение APT каналов...")
        channel1 = self.extract_apt_channel(audio_agc, audio_fs, 'channel1')
        channel2 = self.extract_apt_channel(audio_agc, audio_fs, 'channel2')
        
        # Шаг 5: Ресемплинг к частоте пикселей
        logger.info("   [5/6] Ресемплинг к частоте пикселей...")
        pixels_ch1 = self.resample_to_pixels(channel1, audio_fs)
        pixels_ch2 = self.resample_to_pixels(channel2, audio_fs)
        
        # Шаг 6: Формирование изображения
        logger.info("   [6/6] Формирование изображения...")
        img_ch1 = self.form_image(pixels_ch1)
        img_ch2 = self.form_image(pixels_ch2)
        
        # Сохранение промежуточных результатов
        if save_intermediate:
            results['channel1'] = img_ch1
            results['channel2'] = img_ch2
        
        # Создание композитного изображения
        combined = self.combine_channels(img_ch1, img_ch2)
        results['image'] = combined
        
        results['metadata']['image_shape'] = combined.shape
        results['metadata']['lines'] = combined.shape[0]
        
        logger.info(f"✅ Декодирование завершено: {combined.shape[0]} строк")
        
        return results
    
    def combine_channels(
        self,
        channel1: np.ndarray,
        channel2: np.ndarray,
    ) -> np.ndarray:
        """
        Комбинирование двух каналов в одно изображение
        
        Args:
            channel1: Первый канал
            channel2: Второй канал
        
        Returns:
            Комбинированное изображение
        """
        # Простое усреднение для монохромного изображения
        combined = (channel1.astype(np.float32) + channel2.astype(np.float32)) / 2
        return combined.astype(np.uint8)
    
    def apply_denoising(
        self,
        image: np.ndarray,
        strength: float = 0.5,
    ) -> np.ndarray:
        """
        Удаление шумов с изображения
        
        Args:
            image: Входное изображение
            strength: Сила фильтрации
        
        Returns:
            Изображение с удалёнными шумами
        """
        if not self.config.get("image", "apply_denoising", default=False):
            return image
        
        # Медианный фильтр для удаления импульсных шумов
        kernel_size = max(3, int(5 * strength))
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        denoised = median_filter(image, size=kernel_size)
        
        logger.debug(f"Медианный фильтр применён: kernel={kernel_size}")
        
        return denoised
