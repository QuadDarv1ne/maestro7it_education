"""
Обработка и улучшение изображений NOAA
"""

import numpy as np
from scipy import ndimage
from scipy.interpolate import interp1d
from typing import Tuple, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from PIL import Image

from .logger import get_logger
from .config import Config

logger = get_logger("noaa_receiver.image_processor")


class ImageProcessor:
    """
    Процессор изображений NOAA APT
    
    Поддерживает:
    - Удаление шумов
    - Коррекцию искажений
    - Геопривязку
    - Синтез цветовых каналов
    - Улучшение контраста
    """
    
    # Калибровочные коэффициенты для каналов
    CHANNEL_CALIBRATION = {
        'channel1': {'gamma': 1.0, 'contrast': 1.2},
        'channel2': {'gamma': 1.0, 'contrast': 1.2},
        'channel3a': {'gamma': 0.9, 'contrast': 1.3},
        'channel3b': {'gamma': 0.8, 'contrast': 1.4},
        'channel4': {'gamma': 0.7, 'contrast': 1.5},
        'channel5': {'gamma': 0.7, 'contrast': 1.5},
    }
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.image_config = self.config.config.get("image", {})
        
    def enhance_contrast(
        self,
        image: np.ndarray,
        method: str = 'clahe',
        clip_limit: float = 2.0,
    ) -> np.ndarray:
        """
        Улучшение контраста изображения
        
        Args:
            image: Входное изображение
            method: Метод ('clahe', 'histogram', 'gamma')
            clip_limit: Предел отсечения для CLAHE
        
        Returns:
            Изображение с улучшенным контрастом
        """
        if image.dtype != np.uint8:
            image = self._normalize_to_uint8(image)
        
        if method == 'clahe':
            try:
                import cv2
                clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
                enhanced = clahe.apply(image)
                logger.debug(f"CLAHE применён: clip_limit={clip_limit}")
            except ImportError:
                logger.warning("OpenCV не найден, используется гистограммный метод")
                enhanced = self._equalize_histogram(image)
        elif method == 'histogram':
            enhanced = self._equalize_histogram(image)
        elif method == 'gamma':
            gamma = self.image_config.get('gamma_correction', 0.8)
            enhanced = self._gamma_correction(image, gamma)
        else:
            enhanced = image
        
        return enhanced
    
    def _equalize_histogram(self, image: np.ndarray) -> np.ndarray:
        """Выравнивание гистограммы"""
        from scipy import stats
        
        # Вычисление кумулятивной функции распределения
        hist, bin_edges = np.histogram(image.flatten(), bins=256, range=(0, 256))
        cdf = hist.cumsum()
        cdf_normalized = (cdf - cdf[0]) * 255 / (cdf[-1] - cdf[0])
        cdf_normalized = np.interp(cdf_normalized, cdf_normalized[cdf_normalized > 0], 
                                   np.arange(cdf_normalized[cdf_normalized > 0].size))
        
        # Применение преобразования
        enhanced = np.interp(image.flatten(), bin_edges[:-1], cdf_normalized)
        return enhanced.reshape(image.shape).astype(np.uint8)
    
    def _gamma_correction(self, image: np.ndarray, gamma: float) -> np.ndarray:
        """Гамма-коррекция"""
        image_normalized = image.astype(np.float32) / 255.0
        corrected = np.power(image_normalized, 1.0 / gamma)
        return (corrected * 255).astype(np.uint8)
    
    def denoise(
        self,
        image: np.ndarray,
        method: str = 'median',
        strength: float = 0.5,
    ) -> np.ndarray:
        """
        Удаление шумов
        
        Args:
            image: Входное изображение
            method: Метод ('median', 'gaussian', 'bilateral', 'nlmeans')
            strength: Сила фильтрации (0-1)
        
        Returns:
            Изображение с удалёнными шумами
        """
        if not self.image_config.get("apply_denoising", True):
            return image
        
        if image.dtype != np.uint8:
            image = self._normalize_to_uint8(image)
        
        kernel_size = max(3, int(5 * strength))
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        if method == 'median':
            result = ndimage.median_filter(image, size=kernel_size)
        elif method == 'gaussian':
            sigma = strength * 2
            result = ndimage.gaussian_filter(image, sigma=sigma)
        elif method == 'bilateral':
            try:
                import cv2
                d = int(5 * strength) + 1
                sigma_color = strength * 75
                sigma_space = strength * 75
                result = cv2.bilateralFilter(image, d, sigma_color, sigma_space)
            except ImportError:
                result = ndimage.median_filter(image, size=kernel_size)
        elif method == 'nlmeans':
            try:
                import cv2
                h = int(10 * strength)
                result = cv2.fastNlMeansDenoising(image, h=h)
            except ImportError:
                result = ndimage.median_filter(image, size=kernel_size)
        else:
            result = image
        
        logger.debug(f"Шумоподавление: method={method}, kernel={kernel_size if method == 'median' else 'N/A'}")
        
        return result
    
    def correct_geometric_distortion(
        self,
        image: np.ndarray,
        satellite_altitude: float = 850,
        earth_radius: float = 6371,
    ) -> np.ndarray:
        """
        Коррекция геометрических искажений
        
        Учитывает кривизну Земли и перспективу
        
        Args:
            image: Входное изображение
            satellite_altitude: Высота спутника (км)
            earth_radius: Радиус Земли (км)
        
        Returns:
            Изображение с коррекцией искажений
        """
        if not self.image_config.get("apply_geocorrection", True):
            return image
        
        rows, cols = image.shape
        
        # Создание карты искажений
        y, x = np.mgrid[0:rows, 0:cols]
        
        # Нормализованные координаты
        x_norm = (x - cols / 2) / (cols / 2)
        y_norm = y / rows
        
        # Коррекция кривизны (параболическая аппроксимация)
        curvature_factor = earth_radius / (earth_radius + satellite_altitude)
        x_corrected = x_norm * curvature_factor
        y_corrected = y_norm
        
        # Обратное преобразование
        x_new = ((x_corrected + 1) * cols / 2).astype(np.float32)
        y_new = (y_corrected * rows).astype(np.float32)
        
        # Интерполяция
        result = np.zeros_like(image, dtype=np.float32)
        
        for i in range(rows):
            mask = (y_new[i, :] == i) & (x_new[i, :] >= 0) & (x_new[i, :] < cols)
            if np.any(mask):
                x_indices = x_new[i, mask].astype(int)
                result[i, x_indices] = image[i, x_indices]
        
        logger.debug("Геометрическая коррекция применена")
        
        return result.astype(np.uint8)
    
    def combine_channels_color(
        self,
        channel1: np.ndarray,
        channel2: np.ndarray,
        channel3a: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Создание цветного изображения из каналов
        
        Args:
            channel1: Канал 1 (видимый)
            channel2: Канал 2 (видимый, квадратура)
            channel3a: Канал 3A (ближний ИК, опционально)
        
        Returns:
            Цветное изображение RGB
        """
        # Нормализация каналов
        ch1 = self._normalize_to_uint8(channel1)
        ch2 = self._normalize_to_uint8(channel2)
        
        if channel3a is not None:
            ch3a = self._normalize_to_uint8(channel3a)
        else:
            ch3a = None
        
        # Создание RGB изображения
        # Канал 1 и 2 дают информацию о видимом диапазоне
        # Канал 3A добавляет информацию о растительности
        
        if ch3a is not None:
            # Псевдоцветное изображение
            r = ch2  # Красный канал
            g = (ch1.astype(np.float32) + ch3a.astype(np.float32)) / 2  # Зелёный
            b = ch1  # Синий
        else:
            # Монохромное с тонированием
            avg = (ch1.astype(np.float32) + ch2.astype(np.float32)) / 2
            r = g = b = avg
        
        rgb = np.stack([
            np.clip(r, 0, 255),
            np.clip(g, 0, 255),
            np.clip(b, 0, 255),
        ], axis=-1).astype(np.uint8)
        
        logger.debug(f"RGB изображение создано: {rgb.shape}")
        
        return rgb
    
    def apply_colormap(
        self,
        image: np.ndarray,
        colormap: str = 'gray',
    ) -> np.ndarray:
        """
        Применение цветовой карты
        
        Args:
            image: Изображение в оттенках серого
            colormap: Название colormap ('gray', 'viridis', 'plasma', 'inferno', 'magma')
        
        Returns:
            Цветное изображение
        """
        import matplotlib.pyplot as plt
        
        if image.dtype != np.uint8:
            image = self._normalize_to_uint8(image)
        
        cmap = plt.get_cmap(colormap)
        colored = (cmap(image / 255.0)[:, :, :3] * 255).astype(np.uint8)
        
        plt.close('all')
        
        logger.debug(f"Colormap применён: {colormap}")
        
        return colored
    
    def _normalize_to_uint8(self, image: np.ndarray) -> np.ndarray:
        """Нормализация изображения к uint8"""
        if image.dtype == np.uint8:
            return image
        
        img_min = image.min()
        img_max = image.max()
        
        if img_max - img_min > 0:
            normalized = (image - img_min) / (img_max - img_min) * 255
        else:
            normalized = np.zeros_like(image)
        
        return normalized.astype(np.uint8)
    
    def save_image(
        self,
        image: np.ndarray,
        filepath: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Сохранение изображения с метаданными
        
        Args:
            image: Изображение
            filepath: Путь к файлу
            metadata: Метаданные (опционально)
        
        Returns:
            Путь к сохранённому файлу
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Конвертация к PIL Image
        if image.ndim == 2:
            img = Image.fromarray(image, mode='L')
        elif image.ndim == 3 and image.shape[2] == 3:
            img = Image.fromarray(image, mode='RGB')
        elif image.ndim == 3 and image.shape[2] == 4:
            img = Image.fromarray(image, mode='RGBA')
        else:
            raise ValueError(f"Неподдерживаемый формат изображения: {image.shape}")
        
        # Сохранение
        save_kwargs = {}
        if metadata and path.suffix.upper() in ['.PNG', '.TIFF']:
            save_kwargs['pnginfo'] = self._create_png_metadata(metadata)
        
        img.save(path, **save_kwargs)
        
        logger.info(f"✅ Изображение сохранено: {filepath}")
        
        return str(path)
    
    def _create_png_metadata(self, metadata: Dict[str, Any]) -> 'PngImagePlugin.PngInfo':
        """Создание PNG метаданных"""
        from PIL import PngImagePlugin
        
        pnginfo = PngImagePlugin.PngInfo()
        
        for key, value in metadata.items():
            pnginfo.add_text(str(key), str(value))
        
        return pnginfo
    
    def create_animation(
        self,
        images: list,
        output_file: str,
        duration: int = 100,
    ) -> str:
        """
        Создание анимации из серии изображений
        
        Args:
            images: Список изображений
            output_file: Путь к выходному файлу
            duration: Длительность кадра (мс)
        
        Returns:
            Путь к сохранённому файлу
        """
        if not images:
            raise ValueError("Список изображений пуст")
        
        # Конвертация к PIL
        pil_images = []
        for img in images:
            if img.ndim == 2:
                pil_images.append(Image.fromarray(img, mode='L'))
            else:
                pil_images.append(Image.fromarray(img, mode='RGB'))
        
        # Сохранение анимации
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        pil_images[0].save(
            path,
            save_all=True,
            append_images=pil_images[1:],
            duration=duration,
            loop=0,
        )
        
        logger.info(f"✅ Анимация сохранена: {output_file}")
        
        return str(path)
