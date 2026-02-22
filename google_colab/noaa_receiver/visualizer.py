"""
Визуализация сигналов и спектров
"""

import numpy as np
from typing import Optional, Tuple, List
from pathlib import Path
from datetime import datetime

from .logger import get_logger
from .config import Config

logger = get_logger("noaa_receiver.visualizer")


class SignalVisualizer:
    """
    Класс для визуализации сигналов и спектров
    
    Поддерживает:
    - Временные графики сигнала
    - Спектр мощности (FFT)
    - Спектрограмму (waterfall)
    - Сохранение в файлы
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.viz_config = self.config.config.get("visualization", {})
        
        # Настройки matplotlib
        self.dpi = self.viz_config.get("dpi", 150)
        self.figsize = tuple(self.viz_config.get("figsize", [12, 8]))
        
    def plot_signal(
        self,
        signal_data: np.ndarray,
        sample_rate: float,
        title: str = "Сигнал во времени",
        output_file: Optional[str] = None,
        show: bool = False,
    ) -> 'matplotlib.figure.Figure':
        """
        Построение графика сигнала во времени
        
        Args:
            signal_data: Массив сигнала
            sample_rate: Частота дискретизации
            title: Заголовок графика
            output_file: Путь для сохранения
            show: Показывать ли график
        
        Returns:
            Figure объект matplotlib
        """
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Время в секундах
        duration = len(signal_data) / sample_rate
        t = np.linspace(0, duration, len(signal_data))
        
        # Для больших массивов — прореживание
        max_points = 100000
        if len(t) > max_points:
            step = len(t) // max_points
            t = t[::step]
            signal_data = signal_data[::step]
        
        ax.plot(t, signal_data, linewidth=0.5, color='blue', alpha=0.7)
        ax.set_xlabel("Время (сек)")
        ax.set_ylabel("Амплитуда")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_file:
            self._save_figure(fig, output_file)
        
        if show:
            plt.show()
        
        logger.debug(f"График сигнала сохранён: {output_file}" if output_file else "График сигнала построен")
        
        return fig
    
    def plot_spectrum(
        self,
        signal_data: np.ndarray,
        sample_rate: float,
        title: str = "Спектр мощности",
        output_file: Optional[str] = None,
        show: bool = False,
        nfft: int = 4096,
    ) -> 'matplotlib.figure.Figure':
        """
        Построение спектра мощности (FFT)
        
        Args:
            signal_data: Массив сигнала
            sample_rate: Частота дискретизации
            title: Заголовок
            output_file: Путь для сохранения
            show: Показывать ли график
            nfft: Количество точек FFT
        
        Returns:
            Figure объект matplotlib
        """
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Вычисление FFT
        nfft = min(nfft, len(signal_data))
        fft_data = np.fft.fft(signal_data[:nfft])
        freq = np.fft.fftfreq(nfft, 1/sample_rate)
        
        # Только положительная частота
        pos_mask = freq > 0
        freq = freq[pos_mask]
        magnitude = np.abs(fft_data[pos_mask])
        
        # Перевод в dB
        magnitude_db = 20 * np.log10(magnitude + 1e-10)
        
        # Нормализация
        magnitude_db = magnitude_db - magnitude_db.max()
        
        ax.plot(freq / 1000, magnitude_db, linewidth=0.5, color='red')
        ax.set_xlabel("Частота (кГц)")
        ax.set_ylabel("Мощность (dB)")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        # Выделение частоты 2400 Гц
        ax.axvline(x=2.4, color='green', linestyle='--', alpha=0.7, label='2400 Гц')
        ax.legend()
        
        plt.tight_layout()
        
        if output_file:
            self._save_figure(fig, output_file)
        
        if show:
            plt.show()
        
        logger.debug(f"Спектр сохранён: {output_file}" if output_file else "Спектр построен")
        
        return fig
    
    def plot_waterfall(
        self,
        signal_data: np.ndarray,
        sample_rate: float,
        title: str = "Спектрограмма",
        output_file: Optional[str] = None,
        show: bool = False,
        nfft: int = 1024,
        noverlap: Optional[int] = None,
    ) -> 'matplotlib.figure.Figure':
        """
        Построение спектрограммы (waterfall plot)
        
        Args:
            signal_data: Массив сигнала
            sample_rate: Частота дискретизации
            title: Заголовок
            output_file: Путь для сохранения
            show: Показывать ли график
            nfft: Количество точек FFT для каждого окна
            noverlap: Количество перекрывающихся точек
        
        Returns:
            Figure объект matplotlib
        """
        import matplotlib.pyplot as plt
        from matplotlib import colors
        
        if noverlap is None:
            noverlap = nfft // 2
        
        fig, ax = plt.subplots(figsize=(self.figsize[0], self.figsize[1] * 1.2), dpi=self.dpi)
        
        # Вычисление спектрограммы
        nperseg = min(nfft, len(signal_data) // 10)
        if nperseg < 64:
            nperseg = 64
        
        f, t, Sxx = signal.spectrogram(
            signal_data,
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=noverlap,
            window='hann',
            scaling='spectrum',
        )
        
        # Перевод в dB
        Sxx_db = 10 * np.log10(Sxx + 1e-10)
        
        # Отображение
        im = ax.pcolormesh(
            t,
            f / 1000,
            Sxx_db,
            shading='gouraud',
            cmap='viridis',
            norm=colors.Normalize(vmin=Sxx_db.min(), vmax=Sxx_db.max()),
        )
        
        ax.set_xlabel("Время (сек)")
        ax.set_ylabel("Частота (кГц)")
        ax.set_title(title)
        
        # Цветовая шкала
        cbar = fig.colorbar(im, ax=ax, label='Мощность (dB)')
        
        # Выделение частоты 2400 Гц
        ax.axhline(y=2.4, color='red', linestyle='--', alpha=0.7, linewidth=2)
        
        plt.tight_layout()
        
        if output_file:
            self._save_figure(fig, output_file)
        
        if show:
            plt.show()
        
        logger.debug(f"Спектрограмма сохранена: {output_file}" if output_file else "Спектрограмма построена")
        
        return fig
    
    def plot_iq_constellation(
        self,
        iq_data: np.ndarray,
        title: str = "IQ созвездие",
        output_file: Optional[str] = None,
        show: bool = False,
        max_points: int = 10000,
    ) -> 'matplotlib.figure.Figure':
        """
        Построение IQ созвездия (constellation diagram)
        
        Args:
            iq_data: Комплексные IQ-выборки
            title: Заголовок
            output_file: Путь для сохранения
            show: Показывать ли график
            max_points: Максимум точек для отображения
        
        Returns:
            Figure объект matplotlib
        """
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(8, 8), dpi=self.dpi)
        
        # Прореживание для больших массивов
        if len(iq_data) > max_points:
            step = len(iq_data) // max_points
            iq_data = iq_data[::step]
        
        i_component = np.real(iq_data)
        q_component = np.imag(iq_data)
        
        ax.scatter(i_component, q_component, s=0.5, alpha=0.3, color='blue')
        ax.set_xlabel("I (In-phase)")
        ax.set_ylabel("Q (Quadrature)")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        plt.tight_layout()
        
        if output_file:
            self._save_figure(fig, output_file)
        
        if show:
            plt.show()
        
        logger.debug(f"IQ созвездие сохранено: {output_file}" if output_file else "IQ созвездие построено")
        
        return fig
    
    def plot_all(
        self,
        iq_data: np.ndarray,
        sample_rate: float,
        output_dir: str,
        prefix: str = "",
    ) -> List[str]:
        """
        Построение всех визуализаций
        
        Args:
            iq_data: Комплексные IQ-выборки
            sample_rate: Частота дискретизации
            output_dir: Директория для сохранения
            prefix: Префикс имён файлов
        
        Returns:
            Список сохранённых файлов
        """
        import matplotlib
        matplotlib.use('Agg')  # Неинтерактивный режим
        import matplotlib.pyplot as plt
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []
        
        # Демодуляция для графиков
        audio_data = np.abs(iq_data)
        
        # 1. Сигнал во времени
        signal_file = output_path / f"{prefix}signal_time.png"
        self.plot_signal(
            audio_data[:int(sample_rate * 10)],  # Первые 10 секунд
            sample_rate,
            title="Сигнал во времени (первые 10 сек)",
            output_file=str(signal_file),
        )
        saved_files.append(str(signal_file))
        
        # 2. Спектр
        spectrum_file = output_path / f"{prefix}spectrum.png"
        self.plot_spectrum(
            audio_data,
            sample_rate,
            title="Спектр мощности сигнала",
            output_file=str(spectrum_file),
        )
        saved_files.append(str(spectrum_file))
        
        # 3. Спектрограмма
        waterfall_file = output_path / f"{prefix}waterfall.png"
        self.plot_waterfall(
            audio_data[:int(sample_rate * 60)],  # Первые 60 секунд
            sample_rate,
            title="Спектрограмма (первые 60 сек)",
            output_file=str(waterfall_file),
        )
        saved_files.append(str(waterfall_file))
        
        # 4. IQ созвездие
        constellation_file = output_path / f"{prefix}constellation.png"
        self.plot_iq_constellation(
            iq_data[:10000],
            title="IQ созвездие",
            output_file=str(constellation_file),
        )
        saved_files.append(str(constellation_file))
        
        plt.close('all')
        
        logger.info(f"📊 Визуализации сохранены: {len(saved_files)} файлов")
        
        return saved_files
    
    def _save_figure(self, fig: 'matplotlib.figure.Figure', filepath: str) -> None:
        """Сохранение figure в файл"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        fig.savefig(
            path,
            dpi=self.dpi,
            bbox_inches='tight',
            facecolor='white',
        )
        logger.debug(f"Файл сохранён: {filepath}")


# Импорт для совместимости
import scipy.signal as signal
