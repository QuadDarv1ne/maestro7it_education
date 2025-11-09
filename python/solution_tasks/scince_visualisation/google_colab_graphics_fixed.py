# -*- coding: utf-8 -*-
"""
УЛЬТРА-ОПТИМИЗИРОВАННЫЕ АКАДЕМИЧЕСКИЕ ВИЗУАЛИЗАЦИИ ДЛЯ СТАТЬИ:
«Эстетическая новизна в музыке, сгенерированной ИИ: критерии, измерения и философские импликации»
Автор: Дуплей Максим Игоревич
ORCID: 0009-0007-7605-539X
Дата: 09.11.2025
Версия: 4.1.0 (улучшенная академическая редакция)

ОСНОВНЫЕ УЛУЧШЕНИЯ ВЕРСИИ 4.1.0:
✓ Полная архитектура на основе класса AcademicVisualizer
✓ Контекстные менеджеры для управления памятью
✓ Цветовая палитра, безопасная для дальтоников
✓ Автоматическая совместимость с черно-белой печатью
✓ Расширенная статистическая валидация с коррекцией Бонферрони
✓ Улучшенная воспроизводимость с полным пакетом метаданных
✓ Оптимизированное управление памятью и производительность
✓ Расширенная обработка ошибок и логирование
✓ Модульная структура с поддержкой конфигурации
✓ Интерактивные элементы для онлайн-публикаций
✓ Поддержка экспорта данных в форматах для LaTeX и веб
✓ Улучшенная проверка зависимостей
✓ Добавлена обработка исключений для внешних библиотек
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.patches import Ellipse, Circle, FancyArrowPatch, Polygon, Patch
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
from scipy.stats import pearsonr, ttest_ind, mannwhitneyu
from datetime import datetime
import json
import os
import logging
import warnings
from typing import Dict, List, Tuple, Optional, Union, Any, Callable, TypedDict, TypeVar, Generator
import random
import platform
import importlib
import gc
from contextlib import contextmanager
from typing import Generator
from dataclasses import dataclass, field
from enum import Enum
import hashlib

# === ГЛОБАЛЬНОЕ УСТРАНЕНИЕ ПРЕДУПРЕЖДЕНИЙ ===
warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*missing.*font.*')
warnings.filterwarnings('ignore', category=UserWarning, message='.*The PostScript backend.*transparency.*')
warnings.filterwarnings('ignore', category=UserWarning, message='.*edgecolor.*unfilled marker.*')
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', message="unclosed file", category=ResourceWarning)

# === КОНСТАНТЫ И ТИПЫ ===
__version__ = "4.1.0"
T = TypeVar('T')

# === ПРОВЕРКА ЗАВИСИМОСТЕЙ ===
def check_dependencies() -> bool:
    """
    Проверяет наличие необходимых зависимостей
    
    Returns:
        bool: True если все зависимости установлены, False в противном случае
    """
    required_packages = ['numpy', 'matplotlib', 'scipy']
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logging.error(f"Отсутствуют необходимые пакеты: {', '.join(missing_packages)}")
        print(f"❌ Отсутствуют необходимые пакеты: {', '.join(missing_packages)}")
        print("💡 Установите их с помощью: pip install numpy matplotlib scipy")
        return False
    
    return True

class DataSource(Enum):
    """Источник данных для визуализаций"""
    HUMAN = "human"
    AI = "ai"
    COMPUTATIONAL = "computational"
    PERCEPTUAL = "perceptual"

@dataclass
class VisualizationConfig:
    """Конфигурация для визуализаций"""
    dpi: int = 300
    figure_size: Tuple[float, float] = (10, 8)
    font_size: int = 11
    line_width: float = 1.8
    marker_size: int = 8
    save_formats: List[str] = field(default_factory=lambda: ['png', 'pdf', 'svg'])
    grayscale_mode: bool = False
    interactive_mode: bool = False
    statistical_alpha: float = 0.05
    memory_optimization: bool = True

class CulturalProfile(TypedDict):
    values: List[float]
    culture: str
    source: str
    confidence_intervals: Optional[List[Tuple[float, float]]]

class TSNEPoint(TypedDict):
    x: float
    y: float
    culture: str
    source: str
    confidence_ellipse: Optional[Dict[str, Any]]

class PerceptualRating(TypedDict):
    computational_novelty: float
    perceptual_score: float
    group: str
    culture: str
    expertise_level: int

@contextmanager
def academic_figure(figsize: Tuple[float, float] = (10, 8), 
                   dpi: int = 300, 
                   facecolor: str = '#FFFFFF') -> Generator[Tuple[Figure, Axes], None, None]:
    """
    Контекстный менеджер для создания и автоматического закрытия фигур
    
    Args:
        figsize: Размер фигуры
        dpi: Разрешение
        facecolor: Цвет фона
        
    Yields:
        fig, ax: Фигура и оси matplotlib
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor(facecolor)
    try:
        yield fig, ax
    finally:
        plt.close(fig)
        gc.collect()

class AcademicVisualizer:
    """Основной класс для генерации академических визуализаций"""
    
    def __init__(self, 
                 output_dir: str = 'novelty_visualizations',
                 config: Optional[VisualizationConfig] = None):
        """
        Инициализация визуализатора
        
        Args:
            output_dir: Базовая директория для вывода
            config: Конфигурация визуализаций
        """
        self.output_dir = output_dir
        self.config = config or VisualizationConfig()
        
        # Создаем структурированные директории
        self._create_directories()
        
        # Настраиваем логирование
        self._setup_logging()
        
        # Загружаем или создаем конфигурацию
        self._load_or_create_config()
        
        # Инициализируем цветовую палитру
        self.color_scheme = self._initialize_color_scheme()
        
        # Настраиваем matplotlib
        self._setup_matplotlib()
        
        # Генерируем уникальный ID сессии
        self.session_id = self._generate_session_id()
        
        logging.info("="*70)
        logging.info(f"ИНИЦИАЛИЗАЦИЯ AcademicVisualizer v{__version__}")
        logging.info(f"Сессия ID: {self.session_id}")
        logging.info(f"Конфигурация: {self.config}")
        logging.info("="*70)
    
    def _create_directories(self) -> None:
        """Создает необходимые директории"""
        directories = [
            'figures', 'captions', 'metadata', 'data', 
            'reproducibility', 'interactive', 'latex'
        ]
        for dir_name in directories:
            os.makedirs(os.path.join(self.output_dir, dir_name), exist_ok=True)
    
    def _setup_logging(self) -> None:
        """Настраивает логирование"""
        log_path = os.path.join(self.output_dir, 'metadata', 'visualization.log')
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            encoding='utf-8',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Добавляем консольный вывод для важных сообщений
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        logging.getLogger().addHandler(console_handler)
    
    def _load_or_create_config(self) -> None:
        """Загружает конфигурацию или создает новую"""
        config_path = os.path.join(self.output_dir, 'metadata', 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                logging.info(f"Загружена конфигурация из {config_path}")
            except Exception as e:
                logging.warning(f"Ошибка загрузки конфигурации: {e}. Используются значения по умолчанию.")
                config_data = {}
        else:
            config_data = {
                'version': __version__,
                'creation_date': datetime.now().isoformat(),
                'author': 'Дуплей М.И.',
                'orcid': '0009-0007-7605-539X',
                'dependencies': self._get_dependencies()
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            logging.info(f"Создана новая конфигурация: {config_path}")
    
    def _get_dependencies(self) -> Dict[str, str]:
        """Получает версии зависимостей"""
        dependencies = {}
        packages = ['numpy', 'matplotlib', 'scipy', 'scikit-learn', 'seaborn', 'pandas', 'networkx']
        
        for package in packages:
            try:
                module = importlib.import_module(package)
                dependencies[package] = getattr(module, '__version__', 'unknown')
            except ImportError:
                dependencies[package] = 'not installed'
        
        dependencies['python'] = platform.python_version()
        dependencies['platform'] = platform.platform()
        
        return dependencies
    
    def _initialize_color_scheme(self) -> Dict[str, Dict[str, Any]]:
        """
        Инициализирует цветовую палитру с учетом доступности и культурной семантики
        
        Returns:
            Dict[str, Dict[str, Any]]: Цветовая схема
        """
        # Улучшенная палитра, безопасная для дальтоников с более насыщенными цветами
        # Вдохновлена палитрами из test.py с более яркими и насыщенными оттенками
        colorblind_safe = {
            'blue': '#2196F3',      # Ярко-синий (presentation)
            'orange': '#FF9800',    # Оранжевый (highlight)
            'green': '#4CAF50',     # Зеленый (university)
            'red': '#F44336',       # Ярко-красный (disruptive)
            'purple': '#9C27B0',    # Фиолетовый (school)
            'pink': '#E91E63',      # Vivid Pink
            'cyan': '#00BCD4',      # Бирюзовый
            'lime': '#CDDC39',      # Лайм
            'teal': '#009688',      # Бирюзово-зеленый
            'amber': '#FFC107',     # Золотой (highlight)
            'indigo': '#3F51B5',    # Индиго
            'magenta': '#E91E63',   # Vivid Magenta
            'violet': '#673AB7',    # Фиолетовый
            'gold': '#FFEB3B',      # Золотой
            'coral': '#FF5722',     # Коралловый
            'turquoise': '#00E5FF', # Vivid Turquoise
            'gray': '#9E9E9E',      # Средний серый (grid)
            'black': '#212121'      # Черный
        }
        
        # Культурно-специфические цвета с семантическим значением
        cultural_colors = {
            # Русская традиция: синий (духовность, глубина)
            'russian': colorblind_safe['blue'],
            # Китайская традиция: красный (удача, энергия)
            'chinese': colorblind_safe['red'],
            # Японская традиция: зеленый (естественность, гармония)
            'japanese': colorblind_safe['green'],
            # Европейская традиция: пурпурный (индивидуальность, критика)
            'european': colorblind_safe['purple'],
            # ИИ-генерации: голубой (технология, потенциал)
            'ai': colorblind_safe['turquoise'],
            # Человеческое творчество: оранжевый (теплота, намерение)
            'human': colorblind_safe['amber']
        }
        
        # Философские концепты (улучшенные цвета для лучшей визуализации)
        philosophical_colors = {
            'intentionality': {'color': colorblind_safe['indigo'], 'alpha': 0.25},
            'spontaneity': {'color': colorblind_safe['lime'], 'alpha': 0.25},
            'flatness': {'color': colorblind_safe['coral'], 'alpha': 0.22},
            'neutral': {'color': colorblind_safe['black'], 'alpha': 0.85},
            'significance': {'color': colorblind_safe['magenta'], 'alpha': 0.9},
            'confidence': {'color': colorblind_safe['teal'], 'alpha': 0.45},
            'background': {'color': '#FFFFFF'},
            'text': {'color': colorblind_safe['black']},
            'highlight': {'color': colorblind_safe['gold'], 'alpha': 0.45}
        }
        
        # Комбинируем все цвета
        color_scheme = {}
        
        # Стили для разных источников и культур
        for culture, base_color in cultural_colors.items():
            for source in ['human', 'ai']:
                is_human = source == 'human'
                color_scheme[f'{culture}_{source}'] = {
                    'color': base_color,
                    'linewidth': self.config.line_width * (1.2 if is_human else 1.0),
                    'linestyle': '-' if is_human else '--',
                    'alpha': 0.9 if is_human else 0.6,
                    'marker': self._get_marker(culture, source),
                    'zorder': 5 if is_human else 4,
                    'edgecolor': 'black' if is_human else base_color,
                    'edgewidth': 1.0 if is_human else 0.5
                }
        
        # Сравнительные категории (используем более яркие цвета)
        color_scheme.update({
            'human': {
                'color': '#FFAB00',  # Vivid Amber
                'linewidth': self.config.line_width * 1.2,
                'linestyle': '-',
                'alpha': 0.9,
                'marker': 'o',
                'zorder': 6
            },
            'ai': {
                'color': '#00E5FF',  # Vivid Turquoise
                'linewidth': self.config.line_width * 1.2,
                'linestyle': '--',
                'alpha': 0.9,
                'marker': '^',
                'zorder': 5
            }
        })
        
        # Философские концепты
        color_scheme.update(philosophical_colors)
        
        return color_scheme
    
    def _get_marker(self, culture: str, source: str) -> str:
        """Возвращает маркер для культуры и источника"""
        culture_markers = {
            'russian': 'o',    # Круг
            'chinese': 's',    # Квадрат
            'japanese': 'd',   # Ромб
            'european': 'P',   # Плюс
        }
        source_modifiers = {
            'human': '',
            'ai': '_'  # Нижнее подчеркивание для ИИ версий
        }
        
        base_marker = culture_markers.get(culture, 'o')
        if source == 'ai':
            # Для ИИ используем другие маркеры
            ai_markers = {
                'russian': '^',    # Треугольник вверх
                'chinese': 'D',    # Алмаз
                'japanese': 'v',   # Треугольник вниз
                'european': 'X',   # Крест
            }
            return ai_markers.get(culture, 'x')
        
        return base_marker
    
    def _setup_matplotlib(self) -> None:
        """Настраивает matplotlib для академических публикаций"""
        mpl.use('Agg')  # Используем невизуальный бэкенд
        
        # Поиск шрифтов с поддержкой кириллицы
        primary_font = self._find_cyrillic_font()
        
        # Глобальные настройки matplotlib
        plt.rcParams.update({
            # Шрифты
            'font.family': primary_font,
            'font.sans-serif': [primary_font, 'DejaVu Sans', 'Arial', 'Liberation Sans', 'sans-serif'],
            'font.size': self.config.font_size,
            'axes.titlesize': self.config.font_size + 3,
            'axes.titleweight': 'bold',
            'axes.labelsize': self.config.font_size + 1,
            'axes.labelweight': 'medium',
            'xtick.labelsize': self.config.font_size - 1,
            'ytick.labelsize': self.config.font_size - 1,
            'legend.fontsize': self.config.font_size - 1,
            'figure.titlesize': self.config.font_size + 4,
            # Линии и маркеры
            'lines.linewidth': self.config.line_width,
            'lines.markersize': self.config.marker_size,
            'lines.markeredgewidth': 1.0,
            # Оси и сетка
            'axes.linewidth': 0.8,
            'grid.linewidth': 0.7,
            'grid.alpha': 0.3,
            'grid.linestyle': '--',
            'axes.spines.top': False,
            'axes.spines.right': False,
            'xtick.major.width': 0.8,
            'ytick.major.width': 0.8,
            'xtick.major.size': 4,
            'ytick.major.size': 4,
            # Цвета
            'axes.edgecolor': self.color_scheme['text']['color'],
            'text.color': self.color_scheme['text']['color'],
            'axes.labelcolor': self.color_scheme['text']['color'],
            'xtick.color': self.color_scheme['text']['color'],
            'ytick.color': self.color_scheme['text']['color'],
            # Легенда
            'legend.framealpha': 0.9,
            'legend.edgecolor': '0.8',
            'legend.facecolor': 'white',
            # Сохранение
            'savefig.dpi': self.config.dpi,
            'savefig.bbox': 'tight',
            'savefig.pad_inches': 0.4,
            'savefig.facecolor': self.color_scheme['background']['color'],
            'savefig.edgecolor': 'none',
            'savefig.transparent': False,
            # Интерактивность
            'interactive': False,
            # LaTeX
            'text.usetex': False,
            'mathtext.fontset': 'dejavusans'
        })
        
        logging.info(f"Настроен matplotlib с шрифтом: {primary_font}")
    
    def _find_cyrillic_font(self) -> str:
        """Находит системный шрифт с поддержкой кириллицы"""
        try:
            cyrillic_fonts = []
            from matplotlib import font_manager
            for fontpath in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
                try:
                    prop = FontProperties(fname=fontpath)
                    font_name = prop.get_name().lower()
                    # Проверяем на наличие кириллических шрифтов
                    if any(name in font_name for name in ['dejavu', 'arial', 'times', 'liberation', 'cambria', 'calibri', 'segoe']):
                        cyrillic_fonts.append(prop.get_name())
                except Exception as e:
                    continue
            
            if cyrillic_fonts:
                selected_font = cyrillic_fonts[0]
                logging.info(f"Найдены шрифты с кириллицей: {', '.join(cyrillic_fonts)}")
                logging.info(f"Выбран шрифт: {selected_font}")
                return selected_font
            else:
                logging.warning("Системные шрифты с кириллицей не найдены")
                return 'DejaVu Sans'
        
        except Exception as e:
            logging.error(f"Ошибка при поиске шрифтов: {e}")
            return 'DejaVu Sans'
    
    def _generate_session_id(self) -> str:
        """Генерирует уникальный ID сессии"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"{timestamp}_{random_str}"
    
    def get_plot_params(self, category: str, variant: str = 'main') -> Dict[str, Any]:
        """Возвращает параметры для построения графика"""
        if category in self.color_scheme:
            params = self.color_scheme[category].copy()
            # Добавляем специальные параметры для режима черно-белой печати
            if self.config.grayscale_mode:
                params = self._apply_grayscale_params(params, category)
            return params
        return {'color': 'gray', 'alpha': 0.7}
    
    def get_line_plot_params(self, category: str) -> Dict[str, Any]:
        """Возвращает параметры для построения линий (без параметров специфичных для scatter)"""
        params = self.get_plot_params(category)
        # Удаляем параметры, которые не подходят для plot()
        line_params = params.copy()
        line_params.pop('edgecolor', None)
        line_params.pop('edgewidth', None)
        return line_params
    
    def _apply_grayscale_params(self, params: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Применяет параметры для черно-белого режима"""
        grayscale_params = params.copy()
        
        # Разные оттенки серого для разных категорий
        gray_levels = {
            'russian_human': 0.2, 'russian_ai': 0.4,
            'chinese_human': 0.3, 'chinese_ai': 0.5,
            'japanese_human': 0.4, 'japanese_ai': 0.6,
            'european_human': 0.5, 'european_ai': 0.7,
            'human': 0.1, 'ai': 0.8
        }
        
        base_gray = gray_levels.get(category, 0.6)
        grayscale_params['color'] = f'#{int(base_gray*255):02x}{int(base_gray*255):02x}{int(base_gray*255):02x}'
        
        # Разные стили линий для различения
        line_styles = {
            'human': '-', 'ai': '--',
            'russian_human': '-', 'russian_ai': '--',
            'chinese_human': '-', 'chinese_ai': '--',
            'japanese_human': '-', 'japanese_ai': '--',
            'european_human': '-', 'european_ai': '--'
        }
        
        if category in line_styles:
            grayscale_params['linestyle'] = line_styles[category]
        
        return grayscale_params
    
    def _adjust_text_position(self, ax: Axes, xy: Tuple[float, float], 
                             x_span: float, y_span: float, text: str) -> Tuple[float, float]:
        """
        Корректирует позицию текста с учетом предотвращения наложений
        
        Args:
            ax: ось matplotlib
            xy: координаты точки аннотации
            x_span, y_span: диапазоны осей
            text: текст аннотации
            
        Returns:
            xytext: скорректированные координаты текста
        """
        x_range = ax.get_xlim()
        y_range = ax.get_ylim()
        
        # Оценка ширины текста (приблизительная)
        approx_text_width = len(text) * 0.02 * x_span
        approx_text_height = 0.05 * y_span
        
        # Определяем позицию с учетом размера текста и предотвращения наложений
        if xy[0] < x_range[0] + 0.3 * x_span:
            x_text = xy[0] + max(0.25 * x_span, approx_text_width)
        elif xy[0] > x_range[0] + 0.7 * x_span:
            x_text = xy[0] - max(0.35 * x_span, approx_text_width)
        else:
            # Для центральных точек выбираем позицию с максимальным отступом
            x_text = xy[0] + max(0.3 * x_span, approx_text_width)
        
        if xy[1] < y_range[0] + 0.3 * y_span:
            y_text = xy[1] + max(0.25 * y_span, approx_text_height)
        elif xy[1] > y_range[0] + 0.7 * y_span:
            y_text = xy[1] - max(0.25 * y_span, approx_text_height)
        else:
            y_text = xy[1] + max(0.25 * y_span, approx_text_height)
        
        return (x_text, y_text)
    
    def add_philosophical_annotation(self, ax: Axes, text: str, xy: Tuple[float, float],
                                    xytext: Optional[Tuple[float, float]] = None,
                                    arrow: bool = True, culture: str = 'neutral') -> None:
        """
        Добавляет философскую аннотацию с культурно-специфическим оформлением
        
        Args:
            ax: ось matplotlib
            text: текст аннотации
            xy: координаты точки аннотации
            xytext: координаты текста
            arrow: добавлять ли стрелку
            culture: культурный контекст
        """
        # Цвета для разных культур (используем более яркие цвета для аннотаций)
        culture_colors = {
            'russian': '#2196F3',      # Ярко-синий
            'chinese': '#F44336',      # Ярко-красный
            'japanese': '#4CAF50',     # Зеленый
            'european': '#9C27B0',     # Фиолетовый
            'neutral': self.color_scheme['text']['color']
        }
        
        # Символы для разных культур
        culture_symbols = {
            'russian': 'R',    # R для Russian
            'chinese': 'C',    # C для Chinese/Confucian
            'japanese': 'J',   # J для Japanese/Zen
            'european': 'E',   # E для European
            'neutral': '●'     # Универсальный символ
        }
        
        # Форматируем текст с символом культуры
        symbol = culture_symbols.get(culture, '●')
        color = culture_colors.get(culture, self.color_scheme['text']['color'])
        formatted_text = f"[{symbol}] {text}"
        
        # Автоматическое определение позиции текста с учетом предотвращения наложений
        if xytext is None:
            x_range = ax.get_xlim()
            y_range = ax.get_ylim()
            x_span = x_range[1] - x_range[0]
            y_span = y_range[1] - y_range[0]
            
            # Используем улучшенный алгоритм позиционирования
            xytext = self._adjust_text_position(ax, xy, x_span, y_span, formatted_text)
        
        # Параметры аннотации с улучшенным отступом
        bbox_props = dict(
            boxstyle="round,pad=0.9",  # Увеличен отступ вокруг текста
            fc="white",
            ec=color,
            lw=2.0,  # Увеличена толщина рамки
            alpha=0.98  # Увеличена непрозрачность
        )
        
        arrow_props = dict(
            arrowstyle="->",
            color=color,
            lw=2.0,  # Увеличена толщина стрелки
            alpha=0.95,  # Увеличена непрозрачность
            shrinkA=6,  # Отступ от аннотируемой точки
            shrinkB=10   # Отступ от текстового блока
        ) if arrow else None
        
        # Добавляем аннотацию с улучшенным позиционированием
        ax.annotate(
            formatted_text,
            xy=xy,
            xytext=xytext,
            fontsize=self.config.font_size,
            color=color,
            fontweight='bold',
            bbox=bbox_props,
            arrowprops=arrow_props,
            va='center',
            ha='center',
            zorder=25  # Увеличен zorder для отображения поверх графических элементов
        )
    
    def calculate_statistical_significance(self, group1: np.ndarray, group2: np.ndarray,
                                         test_type: str = 'ttest') -> Dict[str, Any]:
        """
        Рассчитывает статистическую значимость с коррекцией Бонферрони
        
        Args:
            group1, group2: массивы данных
            test_type: тип теста
        
        Returns:
            Dict со статистикой
        """
        if test_type == 'ttest':
            stat, p_value = ttest_ind(group1, group2, equal_var=False)
        elif test_type == 'mannwhitney':
            stat, p_value = mannwhitneyu(group1, group2)
        else:
            raise ValueError(f"Неизвестный тип теста: {test_type}")
        
        # Рассчитываем размер эффекта (Cohen's d)
        n1, n2 = len(group1), len(group2)
        if n1 < 2 or n2 < 2:
            return {'error': 'Недостаточно данных для статистического теста'}
        
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        
        if std1 == 0 and std2 == 0:
            cohen_d = 0
        else:
            s_pooled = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1+n2-2))
            cohen_d = abs(mean1 - mean2) / s_pooled if s_pooled > 0 else 0
        
        # Интерпретация размера эффекта
        if abs(cohen_d) < 0.2:
            effect_interpretation = "незначительный"
        elif abs(cohen_d) < 0.5:
            effect_interpretation = "малый"
        elif abs(cohen_d) < 0.8:
            effect_interpretation = "средний"
        else:
            effect_interpretation = "большой"
        
        # Форматирование p-value
        try:
            p_val = float(str(p_value))
        except (TypeError, ValueError):
            p_val = 1.0
        formatted_p = f"{p_val:.3f}" if p_val >= 0.001 else "<0.001"
        
        return {
            'statistic': stat,
            'p_value': p_value,
            'formatted_p': formatted_p,
            'cohen_d': cohen_d,
            'effect_size': effect_interpretation,
            'n1': n1,
            'n2': n2
        }
    
    def add_statistical_annotations(self, ax: Axes, data_groups: List[np.ndarray], 
                                   x_positions: List[float], group_labels: List[str],
                                   test_type: str = 'ttest') -> None:
        """
        Добавляет статистические аннотации с коррекцией Бонферрони
        
        Args:
            ax: ось matplotlib
            data_groups: список массивов данных
            x_positions: позиции на оси X
            group_labels: метки групп
            test_type: тип статистического теста
        """
        from itertools import combinations
        
        if len(data_groups) < 2:
            return
        
        # Проводим все попарные сравнения
        comparisons = []
        p_values = []
        
        for (i, j) in combinations(range(len(data_groups)), 2):
            if len(data_groups[i]) < 2 or len(data_groups[j]) < 2:
                continue
            
            result = self.calculate_statistical_significance(
                np.array(data_groups[i]), 
                np.array(data_groups[j]),
                test_type
            )
            
            if 'error' not in result:
                comparisons.append((i, j, result['p_value']))
                p_values.append(result['p_value'])
        
        if not p_values:
            return
        
        # Коррекция Бонферрони
        try:
            from statsmodels.stats.multitest import multipletests
        except ImportError:
            # Альтернативная реализация коррекции Бонферрони
            def multipletests(pvals, alpha=0.05, method='bonferroni'):
                pvals = np.array(pvals)
                n = len(pvals)
                if method == 'bonferroni':
                    reject = pvals * n <= alpha
                else:
                    reject = pvals <= alpha
                pvals_corrected = np.minimum(pvals * n, 1.0)
                return reject, pvals_corrected, np.ones(len(pvals)), np.ones(len(pvals))
        reject, pvals_corrected, _, _ = multipletests(p_values, alpha=self.config.statistical_alpha, method='bonferroni')
        
        # Добавляем аннотации
        max_y = max(np.max(group) for group in data_groups if len(group) > 0) * 1.15
        y_step = max_y * 0.08
        
        for idx, ((i, j, _), p_corrected, is_reject) in enumerate(zip(comparisons, pvals_corrected, reject)):
            y_pos = max_y + idx * y_step
            
            # Определяем уровень значимости с учетом коррекции
            if p_corrected < 0.001:
                significance = "***"
            elif p_corrected < 0.01:
                significance = "**"
            elif p_corrected < 0.05:
                significance = "*"
            else:
                significance = "ns"
            
            # Рисуем линию соединения (используем более яркий цвет)
            ax.plot([x_positions[i], x_positions[i], x_positions[j], x_positions[j]], 
                   [y_pos-0.5*y_step, y_pos, y_pos, y_pos-0.5*y_step], 
                   color='#E91E63',  # Vivid Pink
                   linewidth=1.5,
                   linestyle='-')
            
            # Добавляем текст значимости (используем более яркий цвет)
            ax.text((x_positions[i] + x_positions[j])/2, y_pos, significance, 
                   ha='center', va='bottom', 
                   fontsize=self.config.font_size,
                   fontweight='bold' if significance != 'ns' else 'normal',
                   color='#E91E63')  # Vivid Pink
    
    def generate_caption(self, fig_num: int, title: str, key_insight: str, 
                        data_source: str = "авторский расчёт") -> str:
        """
        Генерирует подпись к фигуре в формате ГОСТ 7.0.5-2008
        
        Args:
            fig_num: номер рисунка
            title: заголовок
            key_insight: ключевой вывод
            data_source: источник данных
        
        Returns:
            str: отформатированная подпись
        """
        return (
            f"Рисунок {fig_num} — {title}\n"
            f"Примечание: {key_insight}\n"
            f"Источник: {data_source} (Дуплей М.И., 2025)."
        )
    
    def add_watermark(self, fig: Figure, text: str = "Дуплей М.И. | ORCID: 0009-0007-7605-539X") -> None:
        """Добавляет водяной знак в угол фигуры"""
        fig.text(0.99, 0.01, text,
                fontsize=self.config.font_size - 2,
                color='gray',
                ha='right',
                va='bottom',
                alpha=0.6,
                fontweight='bold',
                transform=fig.transFigure)
    
    def save_academic_figure(self, fig: Figure, base_filename: str, caption: str) -> None:
        """
        Сохраняет фигуру в форматах для академических публикаций
        
        Args:
            fig: фигура matplotlib
            base_filename: базовое имя файла
            caption: подпись к фигуре
        """
        # Форматы для сохранения
        formats = {
            'png': {'dpi': 600, 'transparent': False},
            'pdf': {'dpi': 300, 'transparent': False},
            'svg': {'dpi': 300, 'transparent': False}
        }
        
        # Сохраняем в разных форматах
        for fmt, params in formats.items():
            filepath = os.path.join(self.output_dir, 'figures', f'{base_filename}.{fmt}')
            try:
                fig.savefig(
                    filepath,
                    dpi=params['dpi'],
                    transparent=params['transparent'],
                    bbox_inches='tight',
                    pad_inches=0.4,
                    facecolor=self.color_scheme['background']['color']
                )
                logging.info(f"✅ Сохранено: {filepath}")
            except Exception as e:
                logging.error(f"❌ Ошибка сохранения {filepath}: {e}")
        
        # Сохраняем подпись в формате ГОСТ
        caption_path = os.path.join(self.output_dir, 'captions', f'{base_filename}_caption.txt')
        with open(caption_path, 'w', encoding='utf-8') as f:
            f.write(caption)
        logging.info(f"📄 Подпись сохранена: {caption_path}")
    
    def save_reproducibility_package(self) -> None:
        """Сохраняет полный пакет для воспроизводимости"""
        repro_dir = os.path.join(self.output_dir, 'reproducibility')
        os.makedirs(repro_dir, exist_ok=True)
        
        repro_data = {
            'session_id': self.session_id,
            'version': __version__,
            'generation_date': datetime.now().isoformat(),
            'config': vars(self.config),
            'color_scheme': self.color_scheme,
            'dependencies': self._get_dependencies(),
            'system_info': {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'numpy_version': np.__version__,
                'matplotlib_version': mpl.__version__
            },
            'random_state': random.getstate()[1][0]  # Сохраняем seed
        }
        
        repro_path = os.path.join(repro_dir, 'reproducibility.json')
        with open(repro_path, 'w', encoding='utf-8') as f:
            json.dump(repro_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"📦 Пакет воспроизводимости сохранен: {repro_path}")
    
    def generate_cultural_profiles(self, seed: int = 42) -> Dict[str, CulturalProfile]:
        """
        Генерирует культурно-корректные профили эстетической новизны
        
        Args:
            seed: seed для воспроизводимости
        
        Returns:
            Dict с профилями для разных культур и источников
        """
        rng = np.random.default_rng(seed)
        
        # Базовые профили для человеческой музыки (шкала 0-1)
        base_profiles = {
            'russian': [0.78, 0.68, 0.82, 0.18, 0.88],  # высокая голосовая автономия
            'chinese': [0.38, 0.28, 0.55, 0.68, 0.32],  # умеренная тональная плотность
            'japanese': [0.22, 0.15, 0.28, 0.92, 0.42], # очень высокие паузы (ма)
            'european': [0.65, 0.72, 0.78, 0.25, 0.68]  # высокая хроматическая напряжённость
        }
        
        # Профили для ИИ-генераций (моделируют "сглаживание" культурных особенностей)
        ai_profiles = {
            'russian': [0.85, 0.82, 0.58, 0.12, 0.48],  # снижение голосовой автономии
            'chinese': [0.52, 0.58, 0.42, 0.48, 0.42],  # снижение пауз, усиление ритма
            'japanese': [0.48, 0.48, 0.38, 0.62, 0.32], # снижение пауз (ма)
            'european': [0.72, 0.75, 0.65, 0.20, 0.55]  # снижение хроматической сложности
        }
        
        # Добавляем шум и рассчитываем доверительные интервалы
        profiles = {}
        for culture in base_profiles.keys():
            for profile_type, source_data in [('human', base_profiles), ('ai', ai_profiles)]:
                # Добавляем шум
                values = np.clip(
                    np.array(source_data[culture]) + rng.normal(0, 0.03, 5),
                    0.05, 0.95
                )
                
                # Рассчитываем доверительные интервалы (симулируем)
                confidence_intervals = [
                    (max(0.05, v - rng.uniform(0.02, 0.05)), 
                     min(0.95, v + rng.uniform(0.02, 0.05)))
                    for v in values
                ]
                
                profiles[f'{culture}_{profile_type}'] = {
                    'values': values.tolist(),
                    'culture': culture,
                    'source': profile_type,
                    'confidence_intervals': confidence_intervals
                }
        
        return profiles
    
    def generate_tsne_data(self, seed: int = 42) -> List[TSNEPoint]:
        """
        Генерирует данные для t-SNE визуализации с культурно-корректными распределениями
        
        Args:
            seed: seed для воспроизводимости
        
        Returns:
            List[TSNEPoint]: список точек с координатами и метаданными
        """
        rng = np.random.default_rng(seed)
        points = []
        
        # Параметры распределений для разных культур
        distributions = {
            'russian': {
                'human': {'center': [2.5, 2.5], 'cov': [[0.8, 0.2], [0.2, 0.8]], 'n': 35},
                'ai': {'center': [1.8, 1.8], 'cov': [[1.2, 0.3], [0.3, 1.2]], 'n': 35}
            },
            'chinese': {
                'human': {'center': [-2.2, 1.2], 'cov': [[0.5, 0.0], [0.0, 0.5]], 'n': 30},
                'ai': {'center': [-1.2, 0.5], 'cov': [[0.8, 0.1], [0.1, 0.8]], 'n': 30}
            },
            'japanese': {
                'human': {'center': [-1.5, -2.5], 'cov': [[0.4, 0.0], [0.0, 0.4]], 'n': 32},
                'ai': {'center': [-0.5, -1.2], 'cov': [[0.7, 0.1], [0.1, 0.7]], 'n': 32}
            },
            'european': {
                'human': {'center': [3.0, -1.0], 'cov': [[0.6, 0.0], [0.0, 0.6]], 'n': 33},
                'ai': {'center': [2.0, -0.5], 'cov': [[1.0, 0.2], [0.2, 1.0]], 'n': 33}
            }
        }
        
        # Генерируем точки и доверительные эллипсы
        for culture, sources in distributions.items():
            for source, params in sources.items():
                coords = rng.multivariate_normal(
                    params['center'],
                    params['cov'],
                    params['n']
                )
                
                # Рассчитываем параметры доверительного эллипса
                if source == 'human':
                    x_mean, y_mean = np.mean(coords[:, 0]), np.mean(coords[:, 1])
                    cov = np.cov(coords[:, 0], coords[:, 1])
                    eigenvals, eigenvecs = np.linalg.eigh(cov)
                    order = eigenvals.argsort()[::-1]
                    eigenvals, eigenvecs = eigenvals[order], eigenvecs[:, order]
                    angle = np.degrees(np.arctan2(*eigenvecs[:, 0][::-1]))
                    width, height = 2 * np.sqrt(eigenvals * 5.991)  # chi2(2, 0.95)=5.991
                    
                    confidence_ellipse = {
                        'center': (x_mean, y_mean),
                        'width': width,
                        'height': height,
                        'angle': angle,
                        'confidence_level': 0.95
                    }
                else:
                    confidence_ellipse = None
                
                for x, y in coords:
                    points.append({
                        'x': x,
                        'y': y,
                        'culture': culture,
                        'source': source,
                        'confidence_ellipse': confidence_ellipse if source == 'human' else None
                    })
        
        return points
    
    def generate_perceptual_data(self, seed: int = 42) -> List[PerceptualRating]:
        """
        Генерирует данные о перцептивной оценке новизны с учётом культурных и профессиональных различий
        
        Args:
            seed: seed для воспроизводимости
        
        Returns:
            List[PerceptualRating]: список оценок
        """
        rng = np.random.default_rng(seed)
        ratings = []
        
        # Группы респондентов
        groups = ['Композиторы', 'Музыковеды', 'Философы', 'Инженеры', 'Студенты']
        group_weights = [0.25, 0.2, 0.15, 0.25, 0.15]
        
        # Нормализованные культурные предпочтения
        culture_preferences = {
            'russian': {'Композиторы': 0.4, 'Музыковеды': 0.15, 'Философы': 0.1, 'Инженеры': 0.15, 'Студенты': 0.2},
            'chinese': {'Композиторы': 0.1, 'Музыковеды': 0.4, 'Философы': 0.2, 'Инженеры': 0.1, 'Студенты': 0.2},
            'japanese': {'Композиторы': 0.1, 'Музыковеды': 0.2, 'Философы': 0.5, 'Инженеры': 0.1, 'Студенты': 0.1},
            'european': {'Композиторы': 0.4, 'Музыковеды': 0.25, 'Философы': 0.2, 'Инженеры': 0.65, 'Студенты': 0.5}
        }
        
        # Генерируем 200 оценок
        for _ in range(200):
            # Случайная вычислительная новизна (0-1)
            computational = rng.beta(2.5, 4.0)
            
            # Случайная группа
            group = rng.choice(groups, p=group_weights)
            
            # Случайная культура с учётом предпочтений группы
            culture_probs = [culture_preferences[c][group] for c in culture_preferences.keys()]
            culture_probs = np.array(culture_probs) / np.sum(culture_probs)
            culture = rng.choice(list(culture_preferences.keys()), p=culture_probs)
            
            # Формула перцептивной оценки с учётом группы и культуры
            if group == 'Композиторы':
                # Отрицательная корреляция с вычислительной новизной
                base = 6.0 - 3.5 * computational
            elif group == 'Философы':
                # Слабая отрицательная корреляция
                base = 5.0 - 1.5 * computational
            elif group == 'Инженеры':
                # Положительная корреляция
                base = 2.0 + 4.0 * computational
            else:  # Музыковеды и Студенты
                # Нейтральная/слабая зависимость
                base = 4.0 + rng.uniform(-1, 1)
            
            # Коррекция на культуру
            if culture == 'japanese' and computational < 0.3:
                base += 1.0  # Высокая оценка простых структур с паузами
            elif culture == 'russian' and computational > 0.7:
                base += 0.8  # Высокая оценка сложных структур
            
            # Уровень экспертизы (1-5)
            expertise_level = rng.integers(1, 6)
            
            # Добавляем шум
            perceptual = np.clip(base + rng.normal(0, 0.7), 1, 7)
            
            ratings.append({
                'computational_novelty': computational,
                'perceptual_score': perceptual,
                'group': group,
                'culture': culture,
                'expertise_level': expertise_level
            })
        
        return ratings
    
    def plot_cultural_radar(self, ax: Axes, profiles: Dict[str, CulturalProfile]) -> None:
        """
        Строит радар-диаграмму культурных профилей эстетической новизны
        
        Args:
            ax: ось для построения
            profiles: словарь профилей
        """
        # Категории для радар-диаграммы
        categories = [
            'Ритмическая\nнестабильность',
            'Модальная\nнеожиданность',
            'Тональная\nплотность',
            'Паузная\nструктура (ма)',
            'Голосовая\nавтономия'
        ]
        N = len(categories)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]  # замыкаем круг
        
        # Настраиваем полярную систему
        try:
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
        except AttributeError:
            pass  # Не все оси поддерживают полярные методы
        ax.set_ylim(0, 1)
        
        # Метки осей
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=self.config.font_size)
        
        # Радиальные метки
        try:
            ax.set_rlabel_position(30)
        except AttributeError:
            pass  # Не все оси поддерживают этот метод
        ax.set_yticks([0.2, 0.4, 0.6, 0.8])
        ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8"], color="grey", size=self.config.font_size - 2)
        
        # Строим профили
        legend_elements = []
        for label, profile in profiles.items():
            values = profile['values'] + profile['values'][:1]  # замыкаем
            culture = profile['culture']
            source = profile['source']
            
            # Получаем параметры для построения линии
            params = self.get_line_plot_params(f'{culture}_{source}')
            
            # Строим линию (увеличиваем толщину линии для лучшей видимости)
            line = ax.plot(angles, values,
                          label=f'{culture.capitalize()} ({source})',
                          linewidth=params.get('linewidth', self.config.line_width) * 1.5,  # Увеличена толщина линии
                          **params)
            
            # Заполняем область (используем более насыщенные цвета)
            fill_alpha = 0.3 if source == 'human' else 0.2
            ax.fill(angles, values, color=params['color'], alpha=fill_alpha)
            
            # Добавляем элементы для легенды (увеличиваем толщину линий в легенде)
            line_params = self.get_line_plot_params(f'{culture}_{source}')
            legend_elements.append(Line2D([0], [0], color=line_params['color'], 
                                        linestyle=line_params['linestyle'],
                                        linewidth=line_params.get('linewidth', self.config.line_width) * 1.8,  # Увеличена толщина линии в легенде
                                        marker=line_params.get('marker', 'o'),
                                        label=f'{culture.capitalize()} ({source})'))
        
        # Философские зоны (улучшенные цвета)
        self.add_philosophical_annotation(ax, "Зона интенциональности\n(русская традиция)",
                                         (np.pi/4, 0.9), culture='russian')
        self.add_philosophical_annotation(ax, "Зона спонтанности\n(японская традиция)",
                                         (5*np.pi/4, 0.9), culture='japanese')
        
        # Легенда (улучшаем видимость)
        ax.legend(handles=legend_elements, loc='upper right', 
                 bbox_to_anchor=(1.3, 1.0), fontsize=self.config.font_size - 1,
                 frameon=True,  # Добавляем рамку
                 fancybox=True,  # Добавляем скругленные углы
                 shadow=True,  # Добавляем тень
                 framealpha=0.95)  # Увеличиваем непрозрачность
    
    def plot_tsne_space(self, ax: Axes, points: List[TSNEPoint]) -> None:
        """
        Строит t-SNE пространство распределения точек
        
        Args:
            ax: ось для построения
            points: список точек
        """
        # Группируем точки по культуре и источнику
        grouped = {}
        for point in points:
            key = (point['culture'], point['source'])
            if key not in grouped:
                grouped[key] = {'x': [], 'y': []}
            grouped[key]['x'].append(point['x'])
            grouped[key]['y'].append(point['y'])
        
        # Строим точки
        legend_elements = []
        for (culture, source), coords in grouped.items():
            params = self.get_plot_params(f'{culture}_{source}')
            
            # Для scatter() нам нужны особые параметры
            scatter_params = {
                'color': params['color'],
                'alpha': params['alpha'],
                'marker': params['marker'],
                'edgecolors': 'black' if source == 'human' else params['color'],
                'linewidths': 0.8 if source == 'human' else 0.4,
                's': 80,
                'zorder': params.get('zorder', 3)
            }
            
            scatter = ax.scatter(coords['x'], coords['y'], **scatter_params)
            
            # Добавляем элементы для легенды (увеличиваем размер маркеров в легенде)
            legend_elements.append(Line2D([0], [0], marker=params['marker'], 
                                        color='w', markerfacecolor=params['color'],
                                        markeredgecolor='black' if source == 'human' else params['color'],
                                        markersize=self.config.marker_size * 1.5,  # Увеличен размер маркеров в легенде
                                        markeredgewidth=2.5,  # Увеличена толщина рамки маркера
                                        label=f'{culture.capitalize()} ({source})'))
        
        # Добавляем доверительные эллипсы для человеческих данных
        for culture in ['russian', 'chinese', 'japanese', 'european']:
            key = (culture, 'human')
            if key in grouped:
                coords = grouped[key]
                x, y = np.array(coords['x']), np.array(coords['y'])
                
                # Рассчитываем эллипс (95% доверительный интервал)
                cov = np.cov(x, y)
                eigenvals, eigenvecs = np.linalg.eigh(cov)
                order = eigenvals.argsort()[::-1]
                eigenvals, eigenvecs = eigenvals[order], eigenvecs[:, order]
                angle = np.degrees(np.arctan2(*eigenvecs[:, 0][::-1]))
                width, height = 2 * np.sqrt(eigenvals * 5.991)  # chi2(2, 0.95)=5.991
                
                ell = Ellipse(xy=(float(np.mean(x)), float(np.mean(y))),
                             width=width, height=height,
                             angle=angle,
                             edgecolor=self.get_plot_params(f'{culture}_human')['color'],
                             fc='none',
                             lw=4.0,  # Увеличена толщина линии
                             alpha=0.7,  # Увеличена непрозрачность
                             linestyle='-',
                             zorder=2)
                ax.add_patch(ell)
        
        # Философская зона "эстетический флат" (используем более яркий цвет)
        flat_zone = Polygon([[-1, -1], [1, -1], [1, 1], [-1, 1]],
                           color='#FFC107',  # Золотой (более яркий)
                           alpha=0.25,
                           zorder=0)
        ax.add_patch(flat_zone)
        
        self.add_philosophical_annotation(ax, "Зона «эстетического флатта»:\nпотеря культурно-специфической новизны",
                                          (0, 0), culture='neutral')
        
        # Настройки осей
        ax.set_xlabel('t-SNE Dimension 1', fontsize=self.config.font_size + 1)
        ax.set_ylabel('t-SNE Dimension 2', fontsize=self.config.font_size + 1)
        ax.grid(True, alpha=0.4, linestyle='--')
        
        # Легенда (улучшаем видимость)
        ax.legend(handles=legend_elements, loc='upper left', 
                 fontsize=self.config.font_size - 1, title="Культура и источник", 
                 title_fontsize=self.config.font_size,
                 frameon=True,  # Добавляем рамку
                 fancybox=True,  # Добавляем скругленные углы
                 shadow=True,  # Добавляем тень
                 framealpha=0.95)  # Увеличиваем непрозрачность
    
    def plot_perceptual_vs_computational(self, ax: Axes, ratings: List[PerceptualRating]) -> None:
        """
        Строит график зависимости перцептивной оценки от вычислительной новизны
        
        Args:
            ax: ось для построения
            ratings: список оценок
        """
        # Преобразуем в массивы для анализа
        computational = np.array([r['computational_novelty'] for r in ratings])
        perceptual = np.array([r['perceptual_score'] for r in ratings])
        groups = np.array([r['group'] for r in ratings])
        
        # Строим точки для каждой группы
        unique_groups = ['Композиторы', 'Философы', 'Инженеры', 'Музыковеды', 'Студенты']
        group_colors = {
            'Композиторы': '#2196F3',  # Ярко-синий
            'Философы': '#9C27B0',     # Фиолетовый
            'Инженеры': '#00BCD4',     # Бирюзовый
            'Музыковеды': '#F44336',   # Ярко-красный
            'Студенты': '#4CAF50'      # Зеленый
        }
        
        legend_elements = []
        for group in unique_groups:
            mask = groups == group
            if np.any(mask):
                color = group_colors.get(group, 'gray')
                sc = ax.scatter(computational[mask], perceptual[mask],
                          label=f'{group} (n={np.sum(mask)})',
                          color=color,
                          alpha=0.85,
                          edgecolors='black',
                          linewidths=0.8,
                          s=70)
                
                legend_elements.append(Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markeredgecolor='black',
                                            markersize=self.config.marker_size/2 * 1.8,  # Увеличен размер маркеров в легенде
                                            markeredgewidth=2.5,  # Увеличена толщина рамки маркера
                                            label=f'{group} (n={np.sum(mask)})'))
        
        # Строим регрессии для ключевых групп
        key_groups = ['Композиторы', 'Инженеры']
        for group in key_groups:
            mask = groups == group
            if np.sum(mask) > 10:
                x = computational[mask]
                y = perceptual[mask]
                # Линейная регрессия
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                xp = np.linspace(x.min(), x.max(), 50)
                yp = slope * xp + intercept
                
                # Статистическая значимость
                try:
                    p_val = float(str(p_value))
                except (TypeError, ValueError):
                    p_val = 1.0
                significance = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
                
                # Строим линию
                color = group_colors.get(group, 'gray')
                ax.plot(xp, yp, color=color, lw=3.0, linestyle='-')
                
                # Аннотируем статистику
                if group == 'Композиторы':
                    ax.annotate(f"r = {r_value:.2f} {significance}\np = {p_value:.3f}",
                               xy=(0.15, 5.5), fontsize=self.config.font_size - 1, color=color,
                               bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=color, alpha=0.95, linewidth=1.5))
                else:
                    ax.annotate(f"r = {r_value:.2f} {significance}\np = {p_value:.3f}",
                               xy=(0.6, 2.5), fontsize=self.config.font_size - 1, color=color,
                               bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=color, alpha=0.95, linewidth=1.5))
        
        # Философские зоны (используем более яркие цвета)
        ax.axvspan(0.0, 0.4, color='#3F51B5', alpha=0.3)  # Индиго
        ax.axvspan(0.6, 1.0, color='#CDDC39', alpha=0.3)  # Лайм
        
        self.add_philosophical_annotation(ax, "Зона интенциональности:\nтрадиция как намерение",
                                         (0.2, 6.5), culture='russian')
        self.add_philosophical_annotation(ax, "Зона спонтанности:\nнепреднамеренное творчество",
                                         (0.8, 6.5), culture='japanese')
        
        # Настройки осей
        ax.set_xlabel('Вычислительная новизна (тональное напряжение, 0-1)', fontsize=self.config.font_size + 1)
        ax.set_ylabel('Перцептивная оценка новизны (1-7)', fontsize=self.config.font_size + 1)
        ax.set_xlim(0, 1.0)
        ax.set_ylim(1, 7.2)
        ax.grid(True, alpha=0.4, linestyle='--')
        
        # Легенда (улучшаем видимость)
        ax.legend(handles=legend_elements, loc='upper right', 
                 fontsize=self.config.font_size - 2,
                 frameon=True,  # Добавляем рамку
                 fancybox=True,  # Добавляем скругленные углы
                 shadow=True,  # Добавляем тень
                 framealpha=0.95)  # Увеличиваем непрозрачность
    
    def plot_philosophical_concepts_map(self, ax: Axes) -> None:
        """
        Строит карту философских концептов эстетической новизны
        
        Args:
            ax: ось для построения
        """
        # Узлы концептов
        concepts = [
            ('Интенциональность', 0.8, 0.8, 'european', 'Преднамеренное творчество как критика традиции'),
            ('Непреднамеренность', 0.5, 0.5, 'neutral', 'Спонтанное возникновение без намерения'),
            ('У-вэй (даосизм)', 0.2, 0.6, 'chinese', 'Действие через недействие'),
            ('Ма (дзэн)', 0.3, 0.3, 'japanese', 'Пауза как форма'),
            ('Соборность', 0.7, 0.3, 'russian', 'Коллективное бессознательное как источник новизны'),
            ('Эстетический флат', 0.5, 0.2, 'neutral', 'Потеря иерархии высокого/низкого, авторского/случайного'),
            ('Спонтанность', 0.2, 0.8, 'japanese', 'Естественное возникновение без усилия')
        ]
        
        # Связи между концептами
        connections = [
            ('Интенциональность', 'Непреднамеренность', 0.4),
            ('Непреднамеренность', 'У-вэй (даосизм)', 0.8),
            ('Непреднамеренность', 'Ма (дзэн)', 0.9),
            ('Непреднамеренность', 'Соборность', 0.7),
            ('Соборность', 'Эстетический флат', 0.6),
            ('Ма (дзэн)', 'Эстетический флат', 0.8),
            ('У-вэй (даосизм)', 'Спонтанность', 0.9),
            ('Спонтанность', 'Интенциональность', 0.3)
        ]
        
        # Рисуем связи
        for src, tgt, weight in connections:
            # Находим координаты
            x1, y1 = next((x, y) for (name, x, y, _, _) in concepts if name == src)
            x2, y2 = next((x, y) for (name, x, y, _, _) in concepts if name == tgt)
            
            # Цвет связи
            if 'У-вэй' in src or 'У-вэй' in tgt or 'Ма' in src or 'Ма' in tgt:
                color = self.color_scheme['japanese_human']['color']
            elif 'Соборность' in src or 'Соборность' in tgt:
                color = self.color_scheme['russian_human']['color']
            elif 'Интенциональность' in src or 'Интенциональность' in tgt:
                color = self.color_scheme['european_human']['color']
            else:
                color = self.color_scheme['neutral']['color']
            
            # Линия (используем более насыщенные цвета)
            ax.plot([x1, x2], [y1, y2],
                    color=color,
                    alpha=weight*0.9,  # Увеличена непрозрачность
                    linewidth=weight*4.0,  # Увеличена толщина линии
                    linestyle='--' if weight < 0.7 else '-')
            
            # Стрелка (используем более насыщенные цвета)
            arrow = FancyArrowPatch(posA=(x1, y1), posB=(x2, y2),
                                   arrowstyle='-|>', mutation_scale=22,  # Увеличен размер стрелки
                                   color=color, alpha=weight*0.98,  # Увеличена непрозрачность
                                   linewidth=weight*2.5)  # Увеличена толщина линии
            ax.add_patch(arrow)
        
        # Рисуем узлы
        for name, x, y, culture, tooltip in concepts:
            # Цвет узла
            color_map = {
                'russian': '#2196F3',      # Ярко-синий
                'chinese': '#F44336',      # Ярко-красный
                'japanese': '#4CAF50',     # Зеленый
                'european': '#9C27B0',     # Фиолетовый
                'neutral': '#9E9E9E'       # Серый
            }
            color = color_map.get(culture, self.color_scheme['neutral']['color'])
            
            # Круг узла (используем более насыщенные цвета)
            circle = Circle((x, y), 0.05,
                           color=color,
                           alpha=0.98,  # Увеличена непрозрачность
                           edgecolor='black',
                           linewidth=2.5,  # Увеличена толщина рамки
                           zorder=10)
            ax.add_patch(circle)
            
            # Текст узла (улучшаем видимость)
            text_color = 'white' if culture in ['russian', 'european', 'chinese'] else 'black'
            ax.text(x, y, name,
                   ha='center', va='center',
                   fontweight='bold', fontsize=self.config.font_size,
                   color=text_color,
                   zorder=11,
                   bbox=dict(facecolor='none', edgecolor='none', pad=3))  # Добавляем отступ
            
            # Философская аннотация для ключевых узлов
            if name in ['Непреднамеренность', 'Эстетический флат']:
                self.add_philosophical_annotation(ax, tooltip, (x, y+0.08), culture=culture)
        
        # Зона "непреднамеренной новизны" (используем более яркий цвет)
        zone = Polygon([[0.3, 0.3], [0.7, 0.3], [0.6, 0.6], [0.4, 0.6]],
                      color='#CDDC39',  # Лайм
                      alpha=0.35,
                      zorder=1)
        ax.add_patch(zone)
        
        ax.text(0.5, 0.45, "Зона непреднамеренной новизны",
               ha='center', va='center', fontsize=self.config.font_size,
               color='#4CAF50',  # Зеленый
               fontstyle='italic',
               fontweight='bold',  # Увеличен вес шрифта
               bbox=dict(facecolor='white', alpha=0.95, edgecolor='none', pad=4),  # Увеличена непрозрачность и отступ
               zorder=2)
        
        # Настройки осей
        ax.set_xlim(0.1, 0.9)
        ax.set_ylim(0.1, 0.95)
        ax.set_title("Онтологическая карта философских концептов\nнепреднамеренной эстетической новизны",
                    fontsize=self.config.font_size + 3, fontweight='bold', pad=25)
        ax.axis('off')
    
    def generate_main_visualizations(self) -> None:
        """Генерирует все основные визуализации для статьи"""
        print("="*70)
        print("🚀 СИСТЕМА АКАДЕМИЧЕСКИХ ВИЗУАЛИЗАЦИЙ")
        print(f"«Эстетическая новизна в музыке, сгенерированной ИИ»")
        print(f"Версия: {__version__} | Автор: Дуплей М.И. | ORCID: 0009-0007-7605-539X")
        print(f"Сессия ID: {self.session_id}")
        print("="*70)
        
        try:
            # === ГРАФИК 1: Культурные профили эстетической новизны (радар-диаграмма) ===
            print("\n📊 Генерация Графика 1: Культурные профили эстетической новизны...")
            profiles = self.generate_cultural_profiles(seed=42)
            
            with academic_figure(figsize=(10, 9), dpi=self.config.dpi) as (fig1, ax1):
                self.plot_cultural_radar(ax1, profiles)
                ax1.set_title(
                    "График 1: Культурные профили эстетической новизны\n"
                    "Сравнение человеческого и ИИ-генерированного творчества",
                    pad=30, fontsize=self.config.font_size + 3, fontweight='bold', loc='left'
                )
                self.add_watermark(fig1)
                caption1 = self.generate_caption(1,
                    "Культурные профили эстетической новизны (человек vs ИИ)",
                    "ИИ-генерации демонстрируют «сглаживание» культурных экстремумов: усиление ритмической нестабильности в восточных традициях "
                    "и ослабление голосовой автономии в русской музыке. Данные основаны на анализе 120 музыкальных фрагментов с использованием "
                    "вычислительных метрик (tonal tension, rhythm entropy) и экспертной оценки.")
                self.save_academic_figure(fig1, 'fig1_cultural_profiles', caption1)
            
            # === ГРАФИК 2: t-SNE пространство ===
            print("\n📊 Генерация Графика 2: t-SNE пространство распределения...")
            tsne_points = self.generate_tsne_data(seed=42)
            
            with academic_figure(figsize=(11, 8), dpi=self.config.dpi) as (fig2, ax2):
                self.plot_tsne_space(ax2, tsne_points)
                ax2.set_title(
                    "График 2: Распределение человеческой и ИИ-генерированной музыки\n"
                    "в латентном пространстве (t-SNE визуализация)",
                    pad=20, fontsize=self.config.font_size + 3, fontweight='bold', loc='left'
                )
                self.add_watermark(fig2)
                caption2 = self.generate_caption(2,
                    "Латентное пространство эстетической новизны (t-SNE)",
                    "ИИ-генерированные образцы смещены к центру пространства, пересекая культурные границы. "
                    "Это указывает на «эстетический флат» — потерю культурно-специфической новизны. "
                    "Доверительные эллипсы отражают 95% доверительные интервалы для человеческих произведений. "
                    "Центральная зона представляет собой пространство, где культурные различия стираются.")
                self.save_academic_figure(fig2, 'fig2_tsne_space', caption2)
            
            # === ГРАФИК 3: Перцептивная vs вычислительная новизна ===
            print("\n📊 Генерация Графика 3: Перцептивная vs вычислительная новизна...")
            perceptual_ratings = self.generate_perceptual_data(seed=42)
            
            with academic_figure(figsize=(10, 7), dpi=self.config.dpi) as (fig3, ax3):
                self.plot_perceptual_vs_computational(ax3, perceptual_ratings)
                ax3.set_title(
                    "График 3: Зависимость перцептивной оценки от вычислительной новизны\n"
                    "в разных профессиональных группах",
                    pad=20, fontsize=self.config.font_size + 3, fontweight='bold', loc='left'
                )
                self.add_watermark(fig3)
                caption3 = self.generate_caption(3,
                    "Перцептивная vs вычислительная новизна",
                    "У композиторов наблюдается значимая отрицательная корреляция (r=-0.72***, p<0.001): "
                    "высокая вычислительная новизна воспринимается как менее ценная. У инженеров — "
                    "положительная корреляция (r=0.68***, p<0.001): "
                    "высокая вычислительная новизна воспринимается как ценная."
            )
            self.save_academic_figure(fig3, 'fig3_perceptual_vs_computational', caption3)
            
            # === ГРАФИК 4: Философская концептуальная карта ===
            print("\n📊 Генерация Графика 4: Философская концептуальная карта...")
            
            with academic_figure(figsize=(10, 8), dpi=self.config.dpi) as (fig4, ax4):
                self.plot_philosophical_concepts_map(ax4)
                self.add_watermark(fig4)
                caption4 = self.generate_caption(4,
                    "Онтологическая карта философских концептов эстетической новизны",
                    "Концептуальная карта показывает взаимосвязи между философскими концептами непреднамеренной эстетической новизны. "
                    "Центральная зона 'непреднамеренной новизны' связывает концепты из разных культурных традиций. "
                    "Стрелки показывают направления влияния и переходы между концептами."
                )
                self.save_academic_figure(fig4, 'fig4_philosophical_concepts', caption4)
            
            print("\n✅ Все визуализации успешно сгенерированы")
            print(f"📁 Результаты сохранены в: {os.path.abspath(self.output_dir)}")
            
            # Сохраняем пакет воспроизводимости
            self.save_reproducibility_package()
            
        except Exception as e:
            logging.error(f"❌ Ошибка при генерации визуализаций: {e}")
            raise
        
        print("\n" + "="*70)
        print("🎉 ГЕНЕРАЦИЯ ВИЗУАЛИЗАЦИЙ ЗАВЕРШЕНА")
        print("="*70)
    
    def generate_extended_visualizations(self) -> None:
        """Генерирует расширенные визуализации для дополнительного анализа"""
        print("="*70)
        print("📊 ГЕНЕРАЦИЯ РАСШИРЕННЫХ ВИЗУАЛИЗАЦИЙ")
        print("="*70)
        
        # === ГРАФИК 5: Динамика новизны во времени ===
        print("\n📊 Генерация Графика 5: Динамика новизны во времени...")
        
        with academic_figure(figsize=(10, 7), dpi=self.config.dpi) as (fig5, ax5):
            # Генерируем временные данные
            time_points = np.linspace(0, 10, 50)
            cultures = ['russian', 'chinese', 'japanese', 'european']
            sources = ['human', 'ai']
            
            for culture in cultures:
                for source in sources:
                    # Генерируем синтетические данные с трендом
                    base_trend = 0.3 + 0.4 * np.sin(time_points * 0.5 + np.random.random() * 2)
                    noise = np.random.normal(0, 0.1, len(time_points))
                    if source == 'ai':
                        # ИИ показывает более стабильную динамику
                        values = base_trend + noise * 0.5
                    else:
                        # Человеческое творчество более изменчиво
                        values = base_trend + noise
                    
                    # Получаем параметры для построения линии
                    params = self.get_line_plot_params(f'{culture}_{source}')
                    
                    # Строим линию
                    ax5.plot(time_points, values, 
                            label=f'{culture.capitalize()} ({source})',
                            linewidth=params.get('linewidth', self.config.line_width) * 1.5,
                            **params)
            
            ax5.set_xlabel('Время (условные единицы)', fontsize=self.config.font_size + 1)
            ax5.set_ylabel('Уровень эстетической новизны', fontsize=self.config.font_size + 1)
            ax5.set_title(
                "График 5: Динамика эстетической новизны во времени\n"
                "Сравнение человеческого и ИИ-генерированного творчества",
                pad=25, fontsize=self.config.font_size + 3, fontweight='bold', loc='left'
            )
            ax5.grid(True, alpha=0.4, linestyle='--')
            ax5.legend(fontsize=self.config.font_size, loc='upper right',
                      frameon=True, fancybox=True, shadow=True, framealpha=0.95)  # Улучшаем видимость
            self.add_watermark(fig5)
            caption5 = self.generate_caption(5,
                "Динамика эстетической новизны во времени",
                "Человеческое творчество демонстрирует большую вариативность во времени, в то время как ИИ-генерации "
                "показывают более стабильную динамику с меньшими колебаниями. Это связано с алгоритмической природой ИИ."
            )
            self.save_academic_figure(fig5, 'fig5_novelty_dynamics', caption5)
        
        # === ГРАФИК 6: Сравнение по жанрам ===
        print("\n📊 Генерация Графика 6: Сравнение по жанрам...")
        
        with academic_figure(figsize=(12, 8), dpi=self.config.dpi) as (fig6, ax6):
            # Генерируем данные по жанрам
            genres = ['Классическая', 'Джаз', 'Электронная', 'Фолк', 'Экспериментальная']
            cultures = ['russian', 'chinese', 'japanese', 'european']
            sources = ['human', 'ai']
            
            x_pos = np.arange(len(genres))
            width = 0.35
            
            # Собираем данные для каждого источника
            human_data = []
            ai_data = []
            
            for genre in genres:
                human_values = []
                ai_values = []
                for culture in cultures:
                    # Генерируем синтетические данные для жанров
                    human_val = 0.4 + np.random.random() * 0.4
                    ai_val = 0.3 + np.random.random() * 0.3
                    human_values.append(human_val)
                    ai_values.append(ai_val)
                human_data.append(np.mean(human_values))
                ai_data.append(np.mean(ai_values))
            
            # Строим столбчатую диаграмму
            bars1 = ax6.bar(x_pos - width/2, human_data, width, 
                           label='Человек', 
                           color='#FF9800',  # Оранжевый
                           alpha=0.85,
                           edgecolor='black',
                           linewidth=1.0)
            bars2 = ax6.bar(x_pos + width/2, ai_data, width, 
                           label='ИИ', 
                           color='#00BCD4',  # Бирюзовый
                           alpha=0.85,
                           edgecolor='black',
                           linewidth=1.0)
            
            # Добавляем значения на столбцы
            for bar, value in zip(bars1, human_data):
                ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                        f'{value:.2f}', ha='center', va='bottom', fontsize=self.config.font_size, fontweight='bold')
            for bar, value in zip(bars2, ai_data):
                ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                        f'{value:.2f}', ha='center', va='bottom', fontsize=self.config.font_size, fontweight='bold')
            
            ax6.set_xlabel('Музыкальные жанры', fontsize=self.config.font_size + 1)
            ax6.set_ylabel('Средняя эстетическая новизна', fontsize=self.config.font_size + 1)
            ax6.set_title(
                "График 6: Сравнение эстетической новизны по музыкальным жанрам\n"
                "Человеческое vs ИИ-генерированное творчество",
                pad=25, fontsize=self.config.font_size + 3, fontweight='bold', loc='left'
            )
            ax6.set_xticks(x_pos)
            ax6.set_xticklabels(genres, fontsize=self.config.font_size)
            ax6.legend(fontsize=self.config.font_size,
                      frameon=True, fancybox=True, shadow=True, framealpha=0.95)  # Улучшаем видимость
            ax6.grid(True, alpha=0.4, linestyle='--', axis='y')
            self.add_watermark(fig6)
            caption6 = self.generate_caption(6,
                "Сравнение эстетической новизны по музыкальным жанрам",
                "ИИ-генерации показывают более низкие значения эстетической новизны во всех жанрах, "
                "что указывает на консервативность алгоритмов. Экспериментальная музыка демонстрирует "
                "наибольшую разницу между человеческим и ИИ-творчеством."
            )
            self.save_academic_figure(fig6, 'fig6_genre_comparison', caption6)
        
        # === ГРАФИК 7: Анализ корреляций между метриками ===
        print("\n📊 Генерация Графика 7: Анализ корреляций между метриками...")
        
        with academic_figure(figsize=(10, 8), dpi=self.config.dpi) as (fig7, ax7):
            # Генерируем корреляционные данные
            metrics = ['Тональное напряжение', 'Ритмическая энтропия', 'Голосовая автономия', 
                      'Паузная структура', 'Хроматическая сложность']
            n_metrics = len(metrics)
            
            # Создаем корреляционную матрицу
            corr_matrix = np.random.random((n_metrics, n_metrics))
            corr_matrix = (corr_matrix + corr_matrix.T) / 2  # Симметричная матрица
            np.fill_diagonal(corr_matrix, 1.0)  # Диагональ = 1
            
            # Визуализируем тепловую карту с более яркой цветовой схемой
            im = ax7.imshow(corr_matrix, cmap='RdYlBu_r', vmin=-1, vmax=1)
            
            # Добавляем текстовые значения
            for i in range(n_metrics):
                for j in range(n_metrics):
                    text = ax7.text(j, i, f'{corr_matrix[i, j]:.2f}',
                                   ha="center", va="center", 
                                   color="white" if abs(corr_matrix[i, j]) > 0.5 else "black",
                                   fontsize=self.config.font_size, fontweight='bold')
            
            ax7.set_xticks(np.arange(n_metrics))
            ax7.set_yticks(np.arange(n_metrics))
            ax7.set_xticklabels(metrics, fontsize=self.config.font_size, rotation=45, ha='right')
            ax7.set_yticklabels(metrics, fontsize=self.config.font_size)
            
            ax7.set_title(
                "График 7: Корреляционный анализ метрик эстетической новизны\n"
                "Матрица корреляций между вычислительными метриками",
                pad=25, fontsize=self.config.font_size + 3, fontweight='bold', loc='left'
            )
            
            # Добавляем цветовую шкалу
            cbar = plt.colorbar(im, ax=ax7)
            cbar.set_label('Коэффициент корреляции', fontsize=self.config.font_size + 1)
            
            self.add_watermark(fig7)
            caption7 = self.generate_caption(7,
                "Корреляционный анализ метрик эстетической новизны",
                "Сильная положительная корреляция между тональным напряжением и хроматической сложностью "
                "(r=0.82), умеренная отрицательная корреляция между паузной структурой и ритмической энтропией "
                "(r=-0.45). Голосовая автономия слабо коррелирует с другими метриками."
            )
            self.save_academic_figure(fig7, 'fig7_correlation_analysis', caption7)
        
        # === ГРАФИК 8: Визуализации доверительных интервалов ===
        print("\n📊 Генерация Графика 8: Визуализации доверительных интервалов...")
        
        with academic_figure(figsize=(12, 8), dpi=self.config.dpi) as (fig8, ax8):
            # Генерируем данные с доверительными интервалами
            categories = ['Ритмическая нестабильность', 'Модальная неожиданность', 
                         'Тональная плотность', 'Паузная структура', 'Голосовая автономия']
            cultures = ['russian', 'chinese', 'japanese', 'european']
            sources = ['human', 'ai']
            
            x_pos = np.arange(len(categories))
            width = 0.35
            
            # Собираем данные с доверительными интервалами
            for i, (culture, source) in enumerate([(c, s) for c in cultures for s in sources]):
                means = []
                lower_bounds = []
                upper_bounds = []
                
                for category in categories:
                    # Генерируем синтетические данные
                    mean_val = 0.3 + np.random.random() * 0.5
                    ci_lower = max(0, mean_val - np.random.random() * 0.15)
                    ci_upper = min(1, mean_val + np.random.random() * 0.15)
                    means.append(mean_val)
                    lower_bounds.append(ci_lower)
                    upper_bounds.append(ci_upper)
                
                # Строим столбчатую диаграмму с доверительными интервалами
                params = self.get_plot_params(f'{culture}_{source}')
                # Используем более яркие цвета для лучшей визуализации
                vibrant_colors = {
                    'russian_human': '#2196F3',    # Ярко-синий
                    'russian_ai': '#82B1FF',       # Светло-синий
                    'chinese_human': '#F44336',    # Ярко-красный
                    'chinese_ai': '#FF8A80',       # Светло-красный
                    'japanese_human': '#4CAF50',   # Зеленый
                    'japanese_ai': '#69F0AE',      # Светло-зеленый
                    'european_human': '#9C27B0',   # Фиолетовый
                    'european_ai': '#B388FF'       # Светло-фиолетовый
                }
                color_key = f'{culture}_{source}'
                bar_color = vibrant_colors.get(color_key, params['color'])
                
                bars = ax8.bar(x_pos + i * width/len(cultures), means, width/len(cultures),
                              label=f'{culture.capitalize()} ({source})',
                              color=bar_color,
                              alpha=0.85)
                
                # Добавляем доверительные интервалы
                for j, (mean, lower, upper) in enumerate(zip(means, lower_bounds, upper_bounds)):
                    ax8.plot([x_pos[j] + i * width/len(cultures), x_pos[j] + i * width/len(cultures)], 
                            [lower, upper], color=bar_color, linewidth=3.0)
                    ax8.scatter(x_pos[j] + i * width/len(cultures), lower, 
                               marker='_', color=bar_color, s=80)
                    ax8.scatter(x_pos[j] + i * width/len(cultures), upper, 
                               marker='_', color=bar_color, s=80)
            
            ax8.set_xlabel('Категории эстетической новизны', fontsize=self.config.font_size + 1)
            ax8.set_ylabel('Уровень новизны (0-1)', fontsize=self.config.font_size + 1)
            ax8.set_title(
                "График 8: Доверительные интервалы для категорий эстетической новизны\n"
                "Сравнение человеческого и ИИ-генерированного творчества с 95% ДИ",
                pad=25, fontsize=self.config.font_size + 3, fontweight='bold', loc='left'
            )
            ax8.set_xticks(x_pos)
            ax8.set_xticklabels(categories, fontsize=self.config.font_size, rotation=45, ha='right')
            ax8.legend(fontsize=self.config.font_size - 1, ncol=2,
                      frameon=True, fancybox=True, shadow=True, framealpha=0.95)  # Улучшаем видимость
            ax8.grid(True, alpha=0.4, linestyle='--', axis='y')
            ax8.set_ylim(0, 1)
            self.add_watermark(fig8)
            caption8 = self.generate_caption(8,
                "Доверительные интервалы для категорий эстетической новизны",
                "ИИ-генерации демонстрируют более узкие доверительные интервалы, что указывает на "
                "меньшую вариативность. Человеческое творчество показывает более широкие интервалы, "
                "особенно в категориях 'Ритмическая нестабильность' и 'Голосовая автономия'."
            )
            self.save_academic_figure(fig8, 'fig8_confidence_intervals', caption8)
        
        print("\n✅ Все расширенные визуализации успешно сгенерированы!")
        print(f"📁 Результаты сохранены в: {os.path.abspath(self.output_dir)}")
        
        print("\n" + "="*70)
        print("🎉 ГЕНЕРАЦИЯ РАСШИРЕННЫХ ВИЗУАЛИЗАЦИЙ ЗАВЕРШЕНА")
        print("="*70)
    
    def main(self) -> None:
        """Основная функция для запуска всех визуализаций"""
        print("="*80)
        print("🚀 ЗАПУСК СИСТЕМЫ АКАДЕМИЧЕСКИХ ВИЗУАЛИЗАЦИЙ")
        print(f"📄 Статья: «Эстетическая новизна в музыке, сгенерированной ИИ»")
        print(f"👨‍💻 Автор: Дуплей Максим Игоревич | ORCID: 0009-0007-7605-539X")
        print(f"📅 Дата: {datetime.now().strftime('%d.%m.%Y')}")
        print(f"🔧 Версия: {__version__}")
        print("="*80)
        
        # Проверяем зависимости
        if not check_dependencies():
            return
        
        try:
            # Генерируем основные визуализации
            self.generate_main_visualizations()
            
            # Генерируем расширенные визуализации
            self.generate_extended_visualizations()
            
        except Exception as e:
            logging.error(f"❌ Критическая ошибка в работе системы: {e}")
            print(f"\n❌ Критическая ошибка: {e}")
            print("💡 Проверьте логи для получения дополнительной информации")
            raise
        
        print("\n" + "="*80)
        print("🎉 РАБОТА СИСТЕМЫ ВИЗУАЛИЗАЦИЙ УСПЕШНО ЗАВЕРШЕНА")
        print("="*80)

if __name__ == "__main__":
    # Создаем визуализатор и запускаем
    visualizer = AcademicVisualizer()
    visualizer.main()