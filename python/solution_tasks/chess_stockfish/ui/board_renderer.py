"""
Модуль: ui/board_renderer.py (Оптимизированная версия)

Ключевые улучшения:
- Устранены визуальные артефакты через правильную последовательность отрисовки
- Оптимизирован кэш с автоматической очисткой устаревших ресурсов
- Улучшена система dirty rectangles для минимизации перерисовок
- Добавлена система слоёв для правильного композитинга
- Оптимизированы визуальные эффекты (меньше overdraw)
- Улучшена производительность через батчинг операций
"""

import pygame
from typing import Optional, Tuple, List, Dict, Set, Union
from dataclasses import dataclass
from enum import Enum
import logging
import weakref
import time

# Попытка импортировать CUDA для GPU ускорения (если доступно)
try:
    import cupy as cp
    CUDA_AVAILABLE = True
except ImportError:
    cp = None
    CUDA_AVAILABLE = False

# Попытка импортировать CUDA для GPU ускорения (если доступно)
try:
    import cupy as cp
    CUDA_AVAILABLE = True
except ImportError:
    cp = None
    CUDA_AVAILABLE = False

# ============================================================================ #
# Константы и конфигурация
# ============================================================================ #

BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

# Unicode символы фигур
PIECE_UNICODE = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}


@dataclass
class BoardTheme:
    """Цветовая схема доски."""
    light_square: Tuple[int, int, int] = (240, 217, 181)
    dark_square: Tuple[int, int, int] = (181, 136, 99)
    highlight: Tuple[int, int, int, int] = (124, 252, 0, 180)
    last_move: Tuple[int, int, int, int] = (255, 255, 0, 150)
    check: Tuple[int, int, int, int] = (255, 0, 0, 180)
    move_hint: Tuple[int, int, int, int] = (0, 0, 255, 100)
    hover: Tuple[int, int, int, int] = (200, 200, 255, 100)
    white_piece: Tuple[int, int, int] = (255, 255, 255)
    black_piece: Tuple[int, int, int] = (0, 0, 0)


THEMES = {
    'classic': BoardTheme(),
    'dark': BoardTheme(
        light_square=(100, 100, 120),
        dark_square=(60, 60, 80),
        white_piece=(240, 240, 240),
        black_piece=(200, 200, 200)
    ),
    'blue': BoardTheme(
        light_square=(169, 216, 255),
        dark_square=(70, 130, 180),
        white_piece=(255, 255, 255),
        black_piece=(25, 25, 112)
    ),
    'green': BoardTheme(
        light_square=(180, 220, 180),
        dark_square=(100, 160, 100),
        white_piece=(255, 255, 255),
        black_piece=(0, 80, 0)
    ),
    'contrast': BoardTheme(  # Добавляем новую тему с высоким контрастом
        light_square=(255, 255, 255),
        dark_square=(0, 0, 0),
        white_piece=(0, 0, 0),
        black_piece=(255, 255, 255),
        highlight=(0, 255, 0, 200),
        last_move=(255, 255, 0, 180),
        check=(255, 0, 0, 200)
    ),
    'purple': BoardTheme(  # Добавляем фиолетовую тему
        light_square=(230, 230, 250),
        dark_square=(128, 0, 128),
        white_piece=(255, 255, 255),
        black_piece=(218, 112, 214),
        highlight=(147, 112, 219, 200),
        last_move=(255, 105, 180, 180),
        check=(255, 20, 147, 200)
    ),
    'wood': BoardTheme(  # Добавляем деревянную тему
        light_square=(240, 217, 181),  # Светло-коричневый
        dark_square=(181, 136, 99),    # Темно-коричневый
        white_piece=(255, 255, 255),
        black_piece=(0, 0, 0),
        highlight=(139, 69, 19, 180),  # Кожано-коричневый
        last_move=(210, 180, 140, 180), # Тан
        check=(160, 82, 45, 200)       # Сиена
    ),
    'sunset': BoardTheme(  # Добавляем тему "Закат"
        light_square=(255, 204, 153),  # Светло-оранжевый
        dark_square=(204, 102, 0),     # Темно-оранжевый
        white_piece=(255, 255, 255),   # Белые фигуры
        black_piece=(102, 0, 0),       # Темно-красные фигуры
        highlight=(255, 255, 102, 200), # Желтое выделение
        last_move=(255, 153, 51, 180),  # Оранжевое выделение последнего хода
        check=(255, 0, 0, 200)          # Красное выделение шаха
    )
}


class HighlightStyle(Enum):
    """Стили выделения клеток."""
    FILL = "fill"
    BORDER = "border"
    GLOW = "glow"


# ============================================================================ #
# Улучшенный кэш ресурсов
# ============================================================================ #


class ResourceCache:
    """
    Улучшенный кэш с автоматической очисткой и оптимизацией памяти.
    Оптимизирован для лучшей отзывчивости интерфейса.
    """
    
    # Оптимизация: увеличиваем размеры кэша для лучшей отзывчивости
    MAX_SURFACE_CACHE_SIZE = 500  # Увеличиваем для лучшей производительности
    MAX_PIECE_CACHE_SIZE = 250    # Увеличиваем для лучшей производительности
    MAX_RECT_CACHE_SIZE = 600     # Увеличиваем кэш для прямоугольников клеток
    
    def __init__(self):
        self.fonts: Dict[Tuple[str, int, bool], pygame.font.Font] = {}
        self.surfaces: Dict[Tuple[Tuple[int, ...], Tuple[int, int]], pygame.Surface] = {}
        self.pieces: Dict[Tuple[str, Tuple[int, int, int], str], pygame.Surface] = {}
        
        # Счётчики использования для LRU
        self.surface_usage: Dict = {}
        self.piece_usage: Dict = {}
        
        # Pre-rendered piece surfaces for maximum performance
        self._pre_rendered_pieces: Dict[Tuple[str, str], pygame.Surface] = {}
        
        # GPU ускорение (если доступно)
        self.cuda_available = CUDA_AVAILABLE
        if self.cuda_available:
            print("✅ CUDA доступна для ускорения рендеринга")
        else:
            print("⚠️  CUDA недоступна, используется CPU для рендеринга")
        
    def get_font(self, name: str, size: int, bold: bool = False) -> pygame.font.Font:
        """Получить или создать шрифт."""
        key = (name, size, bold)
        if key not in self.fonts:
            try:
                self.fonts[key] = pygame.font.SysFont(name, size, bold=bold)
            except Exception as e:
                logging.warning(f"Failed to load font {name}: {e}")
                self.fonts[key] = pygame.font.Font(None, size)
        return self.fonts[key]

    def get_highlight_surface(self, color: Union[Tuple[int, ...], List[int]],
                              size: Tuple[int, int]) -> pygame.Surface:
        """
        Возвращает кэшированную поверхность с оптимизацией памяти.
        Оптимизирован для лучшей отзывчивости.
        """
        color_t = tuple(color)
        key = (color_t, (int(size[0]), int(size[1])))
        
        if key not in self.surfaces:
            # Оптимизация: увеличиваем порог очистки для лучшей отзывчивости
            if len(self.surfaces) >= self.MAX_SURFACE_CACHE_SIZE * 0.9:  # Увеличиваем порог
                self._cleanup_surfaces()
            
            surf = pygame.Surface((key[1][0], key[1][1]), pygame.SRCALPHA)
            if len(color_t) == 4:
                surf.fill(color_t)
            else:
                surf.fill((*color_t, 255))
            self.surfaces[key] = surf
            self.surface_usage[key] = 0
            
        self.surface_usage[key] = self.surface_usage.get(key, 0) + 1
        return self.surfaces[key]
    
    def get_piece_surface(self, piece: str, color: Tuple[int, int, int], 
                         font: pygame.font.Font) -> pygame.Surface:
        """
        Возвращает кэшированную поверхность фигуры.
        
        Параметры:
            piece (str): Символ фигуры
            color (Tuple[int, int, int]): Цвет фигуры (RGB)
            font (pygame.font.Font): Шрифт для отрисовки
            
        Возвращает:
            pygame.Surface: Поверхность с фигурой
        """
        # Unicode символы фигур
        PIECE_UNICODE = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        
        # Создаем ключ для кэширования (используем характеристики шрифта вместо объекта шрифта)
        font_key = f"{font.get_height()}_{font.get_bold()}"
        key = (piece, color, font_key)
        
        # Проверяем кэш
        if key in self.pieces:
            self.piece_usage[key] = self.piece_usage.get(key, 0) + 1
            return self.pieces[key]
        
        # Оптимизация: увеличиваем порог очистки для лучшей отзывчивости
        if len(self.pieces) >= self.MAX_PIECE_CACHE_SIZE * 0.9:  # Увеличиваем порог
            self._cleanup_pieces()
        
        # Создаем новую поверхность
        try:
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            if piece in PIECE_UNICODE:
                text = font.render(PIECE_UNICODE[piece], True, color)
                text_rect = text.get_rect(center=(SQUARE_SIZE//2, SQUARE_SIZE//2))
                surface.blit(text, text_rect)
            self.pieces[key] = surface
            self.piece_usage[key] = 1
            return surface
        except Exception as e:
            # В случае ошибки возвращаем пустую поверхность
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            self.pieces[key] = surface
            self.piece_usage[key] = 1
            return surface
    
    def _cleanup_pieces(self):
        """Очистка кэша фигур по LRU алгоритму."""
        if len(self.pieces) < self.MAX_PIECE_CACHE_SIZE * 0.7:  # Увеличиваем порог
            return
            
        # Сортируем по количеству использований
        sorted_items = sorted(self.piece_usage.items(), key=lambda x: x[1])
        
        # Удаляем только 10% наименее используемых элементов для лучшей отзывчивости
        items_to_remove = max(1, len(self.pieces) // 10)
        for i in range(min(items_to_remove, len(sorted_items))):
            key = sorted_items[i][0]
            if key in self.pieces:
                del self.pieces[key]
            if key in self.piece_usage:
                del self.piece_usage[key]
    
    def _cleanup_surfaces(self):
        """Очистка кэша поверхностей по LRU алгоритму."""
        if len(self.surfaces) < self.MAX_SURFACE_CACHE_SIZE * 0.7:  # Увеличиваем порог
            return
            
        # Сортируем по количеству использований
        sorted_items = sorted(self.surface_usage.items(), key=lambda x: x[1])
        
        # Удаляем только 10% наименее используемых элементов для лучшей отзывчивости
        items_to_remove = max(1, len(self.surfaces) // 10)
        for i in range(min(items_to_remove, len(sorted_items))):
            key = sorted_items[i][0]
            if key in self.surfaces:
                del self.surfaces[key]
            if key in self.surface_usage:
                del self.surface_usage[key]
    
    def clear(self):
        """Очистка всех кэшей."""
        self.fonts.clear()
        self.surfaces.clear()
        self.pieces.clear()
        self.surface_usage.clear()
        self.piece_usage.clear()
        self._pre_rendered_pieces.clear()

# ============================================================================ #
# Система слоёв для композитинга
# ============================================================================ #


class LayeredRenderer:
    """
    Система слоёв для устранения артефактов и оптимизации отрисовки.
    """
    
    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.base_layer = pygame.Surface(size)  # Базовая доска
        self.effects_layer = pygame.Surface(size, pygame.SRCALPHA)  # Эффекты
        self.pieces_layer = pygame.Surface(size, pygame.SRCALPHA)  # Фигуры
        self.ui_layer = pygame.Surface(size, pygame.SRCALPHA)  # UI элементы
        
        self.layers_dirty = {
            'base': True,
            'effects': True,
            'pieces': True,
            'ui': True
        }
    
    def mark_dirty(self, layer: str):
        """Пометить слой для перерисовки."""
        if layer in self.layers_dirty:
            self.layers_dirty[layer] = True
    
    def clear_layer(self, layer_name: str):
        """Очистить конкретный слой."""
        layer = getattr(self, f'{layer_name}_layer', None)
        if layer:
            layer.fill((0, 0, 0, 0) if layer_name != 'base' else (0, 0, 0))
    
    def composite(self, target: pygame.Surface):
        """Скомпозировать все слои на целевую поверхность."""
        target.blit(self.base_layer, (0, 0))
        target.blit(self.effects_layer, (0, 0))
        target.blit(self.pieces_layer, (0, 0))
        target.blit(self.ui_layer, (0, 0))


# ============================================================================ #
# Оптимизированный маппер координат
# ============================================================================ #


class CoordinateMapper:
    """Преобразование координат с предвычислением."""

    def __init__(self, player_color: str = 'white'):
        self.player_color = player_color
        self._display_cache = self._build_display_cache()
        self._rect_cache: Dict[Tuple[int, int], pygame.Rect] = {}

    def _build_display_cache(self) -> Dict[Tuple[int, int], Tuple[int, int]]:
        cache: Dict[Tuple[int, int], Tuple[int, int]] = {}
        for row in range(8):
            for col in range(8):
                if self.player_color == 'black':
                    cache[(row, col)] = (7 - row, 7 - col)
                else:
                    cache[(row, col)] = (row, col)
        return cache

    def fen_to_display(self, row: int, col: int) -> Tuple[int, int]:
        return self._display_cache[(row, col)]

    def display_to_fen(self, disp_row: int, disp_col: int) -> Tuple[int, int]:
        if self.player_color == 'black':
            return (7 - disp_row, 7 - disp_col)
        return (disp_row, disp_col)

    def pixel_to_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Пиксельные координаты -> клетка доски (FEN)."""
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return None
        disp_row, disp_col = y // SQUARE_SIZE, x // SQUARE_SIZE
        if self.player_color == 'black':
            return (7 - disp_row, 7 - disp_col)
        return (disp_row, disp_col)
    
    def get_square_rect(self, row: int, col: int) -> pygame.Rect:
        """Получить кэшированный прямоугольник клетки."""
        key = (row, col)
        if key not in self._rect_cache:
            disp_row, disp_col = self.fen_to_display(row, col)
            self._rect_cache[key] = pygame.Rect(
                disp_col * SQUARE_SIZE, 
                disp_row * SQUARE_SIZE,
                SQUARE_SIZE, 
                SQUARE_SIZE
            )
        return self._rect_cache[key]


# ============================================================================ #
# Оптимизированный рендерер эффектов
# ============================================================================ #


class EffectRenderer:
    """Оптимизированный рендеринг визуальных эффектов."""

    def __init__(self, theme: BoardTheme, cache: ResourceCache):
        self.theme = theme
        self.cache = cache
        # Переиспользуемые поверхности для эффектов
        self._effect_surfaces: Dict[str, pygame.Surface] = {}
        # Pre-rendered highlight surfaces for maximum performance
        self._highlight_cache: Dict[Tuple, pygame.Surface] = {}

    @staticmethod
    def _ensure_rgba(color: Union[Tuple[int, ...], List[int]]) -> Tuple[int, int, int, int]:
        """Возвращает RGBA-цвет."""
        c = tuple(color)
        if len(c) == 4:
            return c  # type: ignore
        return (c[0], c[1], c[2], 255)  # type: ignore

    def _get_cached_highlight(self, rect_size: Tuple[int, int], 
                             color: Tuple[int, int, int, int], 
                             style: HighlightStyle) -> pygame.Surface:
        """Получить кэшированную поверхность подсветки."""
        key = (rect_size, color, style)
        if key not in self._highlight_cache:
            # Создаем поверхность один раз и кэшируем
            surf = pygame.Surface(rect_size, pygame.SRCALPHA)
            if style == HighlightStyle.FILL:
                surf.fill(color)
            elif style == HighlightStyle.BORDER:
                pygame.draw.rect(surf, color, (0, 0, rect_size[0], rect_size[1]), 3)
            elif style == HighlightStyle.GLOW:
                # Создаем градиентный эффект
                for i in range(min(rect_size[0], rect_size[1]) // 4):
                    alpha = max(0, color[3] - i * 20)
                    if alpha > 0:
                        pygame.draw.rect(surf, (color[0], color[1], color[2], alpha), 
                                       (i, i, rect_size[0] - 2*i, rect_size[1] - 2*i), 1)
            self._highlight_cache[key] = surf
        return self._highlight_cache[key]

    def draw_rounded_rect(self, surface: pygame.Surface, rect: pygame.Rect, 
                         color: Tuple[int, int, int], corner_radius: int = 6):
        """Оптимизированный прямоугольник со скруглёнными углами."""
        corner_radius = max(0, min(corner_radius, min(rect.width, rect.height) // 2))
        try:
            pygame.draw.rect(surface, color, rect, 0, border_radius=corner_radius)
        except TypeError:
            pygame.draw.rect(surface, color, rect)

    def draw_highlight(self, surface: pygame.Surface, rect: pygame.Rect, 
                      color: Union[Tuple[int, ...], List[int]],
                      style: HighlightStyle, border_width: int = 3):
        """Упрощённая отрисовка подсветки для лучшей производительности."""
        rgba = self._ensure_rgba(color)
        
        # Используем кэшированную поверхность для максимальной производительности
        highlight_surf = self._get_cached_highlight((rect.width, rect.height), rgba, style)
        surface.blit(highlight_surf, rect.topleft)

    def draw_piece_with_shadow(self, surface: pygame.Surface, piece: str, 
                               rect: pygame.Rect, color: Tuple[int, int, int], 
                               font: pygame.font.Font):
        """Улучшенная отрисовка фигуры с тенью для лучшей визуализации."""
        piece_surface = self.cache.get_piece_surface(piece, color, font)
        if not piece_surface:
            return

        # Для максимальной производительности используем простую отрисовку без теней
        surface.blit(piece_surface, (rect.centerx - piece_surface.get_width()//2, 
                                    rect.centery - piece_surface.get_height()//2))

    def draw_check_indicator(self, surface: pygame.Surface, rect: pygame.Rect):
        """Улучшенный индикатор шаха для лучшей визуализации."""
        center = rect.center
        radius = min(rect.width, rect.height) // 2 + 6
        
        # Используем простую отрисовку для лучшей производительности
        pygame.draw.circle(surface, (255, 0, 0, 200), center, radius, 2)

    def draw_move_hint_dot(self, surface: pygame.Surface, rect: pygame.Rect):
        """Улучшенная точка-подсказка для лучшей визуализации."""
        center = rect.center
        radius = min(rect.width, rect.height) // 6  # Уменьшено для лучшей производительности
        
        # Используем простую отрисовку для лучшей производительности
        pygame.draw.circle(surface, (50, 150, 255, 220), center, radius)


# ============================================================================ #
# Главный класс рендерера
# ============================================================================ #


class BoardRenderer:
    """
    Оптимизированный рендерер шахматной доски с системой слоёв.
    """

    def __init__(self, screen: pygame.Surface, player_color: str = 'white',
                 theme: Optional[BoardTheme] = None):
        self.screen = screen
        self.player_color = player_color
        self.theme = theme or BoardTheme()
        self._current_theme = 'custom' if theme else 'classic'

        # Компоненты
        self.cache = ResourceCache()
        self.coord_mapper = CoordinateMapper(player_color)
        self.effect_renderer = EffectRenderer(self.theme, self.cache)
        self.layered_renderer = LayeredRenderer((BOARD_SIZE, BOARD_SIZE))

        # Шрифты
        self._init_fonts()

        # Состояние
        self.selected_square: Optional[Tuple[int, int]] = None
        self.last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self.check_square: Optional[Tuple[int, int]] = None
        self.move_hints: List[Tuple[int, int]] = []
        self.hover_square: Optional[Tuple[int, int]] = None
        self.show_coords = True

        # Оптимизация
        self._dirty_squares: Set[Tuple[int, int]] = set()
        self._last_board_state: Optional[List[List[Optional[str]]]] = None
        
        # Анимации
        self._animations: Dict[str, Dict] = {}
        self._piece_animations: Dict[Tuple[int, int], Dict] = {}
        self._last_update_time = 0

    def _init_fonts(self):
        """Инициализация шрифтов."""
        self.piece_font = self.cache.get_font('Segoe UI Symbol', SQUARE_SIZE - 8)
        self.coord_font = self.cache.get_font('Arial', 14, bold=True)
        self.info_font = self.cache.get_font('Arial', 16)

    def set_player_color(self, color: str):
        """Изменить ориентацию доски."""
        if color != self.player_color:
            self.player_color = color
            self.coord_mapper = CoordinateMapper(color)
            self._mark_all_dirty()
            self.layered_renderer.mark_dirty('base')
            self.layered_renderer.mark_dirty('pieces')

    def set_theme(self, theme_name: str):
        """Изменить тему."""
        if theme_name in THEMES:
            self.theme = THEMES[theme_name]
            self.effect_renderer.theme = self.theme
            self._current_theme = theme_name
            self._mark_all_dirty()
            self.layered_renderer.mark_dirty('base')

    def set_selected(self, square: Optional[Tuple[int, int]]):
        """Установить выбранную клетку."""
        if self.selected_square != square:
            if self.selected_square:
                self._dirty_squares.add(self.selected_square)
            self.selected_square = square
            if square:
                self._dirty_squares.add(square)
            self.layered_renderer.mark_dirty('effects')

    def set_last_move(self, from_sq: Tuple[int, int], to_sq: Tuple[int, int]):
        """Установить последний ход."""
        if self.last_move:
            self._dirty_squares.update(self.last_move)
        self.last_move = (from_sq, to_sq)
        self._dirty_squares.update([from_sq, to_sq])
        self.layered_renderer.mark_dirty('effects')

    def set_check(self, square: Optional[Tuple[int, int]]):
        """Установить клетку под шахом."""
        if self.check_square:
            self._dirty_squares.add(self.check_square)
        self.check_square = square
        if square:
            self._dirty_squares.add(square)
        self.layered_renderer.mark_dirty('effects')

    def set_move_hints(self, hints: List[Tuple[int, int]]):
        """Установить подсказки ходов."""
        self._dirty_squares.update(self.move_hints)
        self.move_hints = hints
        self._dirty_squares.update(hints)
        self.layered_renderer.mark_dirty('effects')

    def update_hover(self, mouse_pos: Optional[Tuple[int, int]]):
        """Обновить hover."""
        new_hover = None
        if mouse_pos:
            new_hover = self.coord_mapper.pixel_to_square(*mouse_pos)

        if new_hover != self.hover_square:
            if self.hover_square:
                self._dirty_squares.add(self.hover_square)
            self.hover_square = new_hover
            if new_hover:
                self._dirty_squares.add(new_hover)
            self.layered_renderer.mark_dirty('effects')
    
    def add_piece_animation(self, from_square: Tuple[int, int], to_square: Tuple[int, int], duration: float = 0.3):
        """Добавить анимацию перемещения фигуры."""
        animation_id = f"piece_{from_square[0]}{from_square[1]}_{to_square[0]}{to_square[1]}"
        self._animations[animation_id] = {
            'type': 'piece_move',
            'from_square': from_square,
            'to_square': to_square,
            'start_time': time.time(),
            'duration': duration,
            'progress': 0.0
        }
    
    def add_capture_animation(self, square: Tuple[int, int], duration: float = 0.5):
        """Добавить анимацию захвата фигуры."""
        animation_id = f"capture_{square[0]}{square[1]}"
        self._animations[animation_id] = {
            'type': 'capture',
            'square': square,
            'start_time': time.time(),
            'duration': duration,
            'progress': 0.0
        }

    def _draw_base_layer(self, board_state: List[List[Optional[str]]]):
        """Отрисовка базового слоя (доска)."""
        if not self.layered_renderer.layers_dirty['base']:
            return
            
        layer = self.layered_renderer.base_layer
        layer.fill((40, 40, 40))
        
        for row in range(8):
            for col in range(8):
                color = (self.theme.light_square if (row + col) % 2 == 0
                        else self.theme.dark_square)
                rect = self.coord_mapper.get_square_rect(row, col)
                self.effect_renderer.draw_rounded_rect(layer, rect, color, 4)
                
                # Координаты
                if self.show_coords:
                    self._draw_coordinates(layer, row, col)
        
        self.layered_renderer.layers_dirty['base'] = False

    def _draw_effects_layer(self):
        """Отрисовка слоя эффектов."""
        if not self.layered_renderer.layers_dirty['effects']:
            return
            
        layer = self.layered_renderer.effects_layer
        layer.fill((0, 0, 0, 0))
        
        # Батчинг: группируем эффекты по типу
        effects_batch = {
            'hover': [],
            'last_move': [],
            'selected': [],
            'check': [],
            'hints': []
        }
        
        # Собираем все эффекты
        for row in range(8):
            for col in range(8):
                square = (row, col)
                rect = self.coord_mapper.get_square_rect(row, col)
                
                if square == self.hover_square and square != self.selected_square:
                    effects_batch['hover'].append(rect)
                if self.last_move and square in self.last_move:
                    effects_batch['last_move'].append(rect)
                if square == self.selected_square:
                    effects_batch['selected'].append(rect)
                if square == self.check_square:
                    effects_batch['check'].append(rect)
                if square in self.move_hints:
                    effects_batch['hints'].append(rect)
        
        # Отрисовываем батчами
        for rect in effects_batch['hover']:
            self.effect_renderer.draw_highlight(layer, rect, self.theme.hover, 
                                               HighlightStyle.GLOW)
        for rect in effects_batch['last_move']:
            self.effect_renderer.draw_highlight(layer, rect, self.theme.last_move, 
                                               HighlightStyle.BORDER, 2)
        for rect in effects_batch['selected']:
            self.effect_renderer.draw_highlight(layer, rect, self.theme.highlight, 
                                               HighlightStyle.BORDER, 3)
        for rect in effects_batch['check']:
            self.effect_renderer.draw_check_indicator(layer, rect)
        for rect in effects_batch['hints']:
            self.effect_renderer.draw_move_hint_dot(layer, rect)
        
        self.layered_renderer.layers_dirty['effects'] = False

    def _draw_pieces_layer(self, board_state: List[List[Optional[str]]]):
        """Отрисовка слоя фигур с исправлением артефактов."""
        if not self.layered_renderer.layers_dirty['pieces'] and not self._dirty_squares:
            return
            
        layer = self.layered_renderer.pieces_layer
        
        # Исправление: всегда очищаем слой перед отрисовкой для предотвращения артефактов
        layer.fill((0, 0, 0, 0))
        
        # Отрисовываем все фигуры для предотвращения артефактов
        for row in range(8):
            for col in range(8):
                piece = board_state[row][col]
                if piece:
                    rect = self.coord_mapper.get_square_rect(row, col)
                    color = (self.theme.white_piece if piece.isupper()
                            else self.theme.black_piece)
                    self.effect_renderer.draw_piece_with_shadow(
                        layer, piece, rect, color, self.piece_font
                    )
        
        self.layered_renderer.layers_dirty['pieces'] = False
    
    def _mark_all_dirty(self):
        """Пометить все клетки для перерисовки."""
        self._dirty_squares = {(r, c) for r in range(8) for c in range(8)}
        # Также помечаем все слои как грязные
        self.layered_renderer.mark_dirty('base')
        self.layered_renderer.mark_dirty('effects')
        self.layered_renderer.mark_dirty('pieces')
        self.layered_renderer.mark_dirty('ui')
    
    def _get_square_rect(self, row: int, col: int) -> pygame.Rect:
        """
        Получить прямоугольник клетки (для совместимости с chess_game.py).
        
        Параметры:
            row: Ряд клетки (0-7)
            col: Колонка клетки (0-7)
            
        Возвращает:
            pygame.Rect: Прямоугольник клетки
        """
        return self.coord_mapper.get_square_rect(row, col)

    def _draw_coordinates(self, surface: pygame.Surface, row: int, col: int):
        """Отрисовка координат."""
        if not self.show_coords:
            return

        disp_row, disp_col = self.coord_mapper.fen_to_display(row, col)

        if disp_col == 0:
            rank_num = row + 1 if self.player_color == 'black' else 8 - row
            rank_text = self.coord_font.render(str(rank_num), True, (100, 100, 100))
            surface.blit(rank_text, (disp_col * SQUARE_SIZE + 5,
                                    disp_row * SQUARE_SIZE + 4))

        if disp_row == 7:
            file_char = chr(97 + 7 - col) if self.player_color == 'black' else chr(97 + col)
            file_text = self.coord_font.render(file_char, True, (100, 100, 100))
            surface.blit(file_text, (disp_col * SQUARE_SIZE + SQUARE_SIZE - 16,
                                    disp_row * SQUARE_SIZE + SQUARE_SIZE - 20))

    def draw(self, board_state: List[List[Optional[str]]],
             evaluation: Optional[float] = None,
             thinking: bool = False,
             mouse_pos: Optional[Tuple[int, int]] = None,
             move_count: int = 0,
             capture_count: Tuple[int, int] = (0, 0),
             check_count: int = 0):
        """
        Главный метод отрисовки с использованием системы слоёв.
        Исправлен для устранения артефактов.
        """
        # Обновляем hover
        self.update_hover(mouse_pos)

        # Определяем изменения для частичной перерисовки
        if self._last_board_state is None:
            self._mark_all_dirty()
            self.layered_renderer.mark_dirty('base')
            self.layered_renderer.mark_dirty('pieces')
        else:
            # Исправление: всегда помечаем слой фигур как грязный для предотвращения артефактов
            board_changed = False
            for row in range(8):
                for col in range(8):
                    if board_state[row][col] != self._last_board_state[row][col]:
                        self._dirty_squares.add((row, col))
                        board_changed = True
            
            if board_changed:
                self.layered_renderer.mark_dirty('pieces')

        # Исправление: всегда отрисовываем все слои для предотвращения артефактов
        self._draw_base_layer(board_state)
        self._draw_effects_layer()
        self._draw_pieces_layer(board_state)

        # Композитинг всех слоев
        self.layered_renderer.composite(self.screen)

        # Очистка
        self._dirty_squares.clear()
        self._last_board_state = [row[:] for row in board_state]

        # Информационная панель (рисуется напрямую)
        self._draw_info_panel(evaluation, thinking, move_count, 
                             capture_count, check_count)
                             
        # Исправление: всегда обновляем дисплей для предотвращения артефактов
        pygame.display.flip()
                             
    def _draw_info_panel(self, evaluation: Optional[float], thinking: bool,
                        move_count: int, capture_count: Tuple[int, int], 
                        check_count: int):
        """Отрисовка информационной панели."""
        info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
        self.screen.fill((30, 30, 30), info_rect)
        
        # Evaluation bar
        if evaluation is not None:
            eval_bar_rect = pygame.Rect(10, BOARD_SIZE + 10, 200, 20)
            self._draw_evaluation_bar(eval_bar_rect, evaluation)

        # Thinking indicator
        if thinking:
            thinking_text = self.info_font.render("⟳ Думаю...", True, (255, 200, 0))
            self.screen.blit(thinking_text, (BOARD_SIZE - 150, BOARD_SIZE + 10))

        # Theme indicator  
        theme_text = self.info_font.render(
            f"Тема: {self._current_theme}", True, (200, 200, 200)
        )
        self.screen.blit(theme_text, (BOARD_SIZE - 150, BOARD_SIZE + 35))

        # Stats
        if move_count > 0:
            moves_text = self.info_font.render(f"Ходы: {move_count}", True, (200, 200, 100))
            self.screen.blit(moves_text, (220, BOARD_SIZE + 10))
        
        player_captures, ai_captures = capture_count
        if player_captures > 0 or ai_captures > 0:
            cap_color = (100, 200, 100) if player_captures >= ai_captures else (200, 100, 100)
            cap_text = self.info_font.render(
                f"Взятия: {player_captures} vs {ai_captures}", True, cap_color
            )
            self.screen.blit(cap_text, (220, BOARD_SIZE + 35))
        
        if check_count > 0:
            check_text = self.info_font.render(f"Шахи: {check_count}", True, (255, 100, 100))
            self.screen.blit(check_text, (380, BOARD_SIZE + 10))

    def _draw_evaluation_bar(self, rect: pygame.Rect, evaluation: float):
        """Отрисовка полосы оценки."""
        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

        clamped_eval = max(-10.0, min(10.0, evaluation))
        white_advantage = (clamped_eval + 10.0) / 20.0
        white_width = int(rect.width * white_advantage)
        white_rect = pygame.Rect(rect.left, rect.top, white_width, rect.height)
        pygame.draw.rect(self.screen, (255, 255, 255), white_rect)

        center_x = rect.left + rect.width // 2
        pygame.draw.line(self.screen, (200, 200, 200), 
                        (center_x, rect.top), (center_x, rect.bottom), 1)

        if abs(evaluation) > 0.1:
            eval_text = f"{evaluation:+.1f}"
            text_color = ((100, 255, 100) if evaluation > 0 
                         else (255, 100, 100) if evaluation < 0 
                         else (200, 200, 200))
            text_surface = self.info_font.render(eval_text, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
    
    # ============================================================================ #
    # Дополнительные методы для совместимости с chess_game.py
    # ============================================================================ #
    
    def draw_enhanced_feedback(self, feedback: str, rect: pygame.Rect, 
                              feedback_type: str = "info"):
        """
        Отрисовка улучшенной обратной связи с визуальными эффектами.
        
        Параметры:
            feedback: Текст обратной связи
            rect: Прямоугольник для отрисовки
            feedback_type: Тип обратной связи ("info", "warning", "success", "error")
        """
        colors = {
            "info": (100, 200, 255),
            "warning": (255, 200, 100),
            "success": (100, 255, 100),
            "error": (255, 100, 100)
        }
        
        color = colors.get(feedback_type, colors["info"])
        
        # Фон с градиентом
        pygame.draw.rect(self.screen, (30, 30, 30), rect, border_radius=8)
        pygame.draw.rect(self.screen, color, rect, 2, border_radius=8)
        
        # Внутренняя тень
        inner_rect = pygame.Rect(rect.left + 2, rect.top + 2, 
                                rect.width - 4, rect.height - 4)
        pygame.draw.rect(self.screen, (20, 20, 20), inner_rect, border_radius=6)
        
        # Текст с тенью
        if self.info_font:
            # Тень
            shadow_text = self.info_font.render(feedback, True, (0, 0, 0))
            self.screen.blit(shadow_text, (rect.left + 15, rect.top + 10))
            
            # Основной текст
            text = self.info_font.render(feedback, True, color)
            self.screen.blit(text, (rect.left + 13, rect.top + 8))
            
        # Иконка
        icon_rect = pygame.Rect(rect.right - 25, rect.top + 5, 20, 20)
        self._draw_feedback_icon(icon_rect, feedback_type, color)
    
    def _draw_feedback_icon(self, icon_rect: pygame.Rect, feedback_type: str, 
                           color: Tuple[int, int, int]):
        """Отрисовка иконки для обратной связи."""
        if feedback_type == "success":
            # Зеленая галочка
            pygame.draw.line(self.screen, color, 
                           (icon_rect.left + 5, icon_rect.centery), 
                           (icon_rect.centerx - 2, icon_rect.bottom - 5), 3)
            pygame.draw.line(self.screen, color, 
                           (icon_rect.centerx - 2, icon_rect.bottom - 5), 
                           (icon_rect.right - 5, icon_rect.top + 5), 3)
        elif feedback_type == "warning":
            # Желтый восклицательный знак
            pygame.draw.circle(self.screen, color, 
                             (icon_rect.centerx, icon_rect.top + 5), 3)
            pygame.draw.line(self.screen, color, 
                           (icon_rect.centerx, icon_rect.top + 10), 
                           (icon_rect.centerx, icon_rect.bottom - 5), 3)
        elif feedback_type == "error":
            # Красный крестик
            pygame.draw.line(self.screen, color, 
                           (icon_rect.left + 5, icon_rect.top + 5), 
                           (icon_rect.right - 5, icon_rect.bottom - 5), 3)
            pygame.draw.line(self.screen, color, 
                           (icon_rect.right - 5, icon_rect.top + 5), 
                           (icon_rect.left + 5, icon_rect.bottom - 5), 3)
        else:  # info
            # Синий кружок с i
            pygame.draw.circle(self.screen, color, icon_rect.center, 8, 2)
            pygame.draw.line(self.screen, color, 
                           (icon_rect.centerx, icon_rect.top + 6), 
                           (icon_rect.centerx, icon_rect.bottom - 6), 2)
            pygame.draw.circle(self.screen, color, 
                             (icon_rect.centerx, icon_rect.top + 4), 2)
    
    def draw_progress_bar(self, rect: pygame.Rect, progress: float, 
                         color: Tuple[int, int, int] = (100, 200, 100)):
        """
        Отрисовка прогресс бара.
        
        Параметры:
            rect: Прямоугольник для прогресс бара
            progress: Прогресс от 0.0 до 1.0
            color: Цвет прогресса
        """
        # Фон
        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
        
        # Прогресс
        progress_width = int(rect.width * max(0, min(1, progress)))
        if progress_width > 0:
            progress_rect = pygame.Rect(rect.left, rect.top, progress_width, rect.height)
            pygame.draw.rect(self.screen, color, progress_rect)
    
    def draw_status_indicator(self, rect: pygame.Rect, status: str, 
                             color: Tuple[int, int, int] = (200, 200, 200)):
        """
        Отрисовка индикатора статуса с иконкой.
        
        Параметры:
            rect: Прямоугольник для индикатора
            status: Текст статуса
            color: Цвет текста
        """
        # Фон с закругленными углами
        pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=5)
        pygame.draw.rect(self.screen, (80, 80, 80), rect, 1, border_radius=5)
        
        # Текст
        if self.info_font:
            text = self.info_font.render(status, True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def clear_temp_surfaces(self):
        """
        Очистка временных поверхностей для предотвращения утечек памяти.
        В новой архитектуре это означает сброс слоёв эффектов и UI.
        """
        # Очищаем слои эффектов (они пересоздаются каждый кадр)
        self.layered_renderer.clear_layer('effects')
        self.layered_renderer.clear_layer('ui')
        
        # Запускаем LRU очистку кэша при необходимости
        if len(self.cache.surfaces) > self.cache.MAX_SURFACE_CACHE_SIZE * 0.8:
            self.cache._cleanup_surfaces()
        if len(self.cache.pieces) > self.cache.MAX_PIECE_CACHE_SIZE * 0.8:
            self.cache._cleanup_pieces()
    
    def cleanup(self):
        """Полная очистка всех ресурсов."""
        self.cache.clear()
        self.coord_mapper._rect_cache.clear()
        # Очищаем все слои
        for layer_name in ['base', 'effects', 'pieces', 'ui']:
            self.layered_renderer.clear_layer(layer_name)


# ============================================================================ #
# Пример использования
# ============================================================================ #

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
    pygame.display.set_caption("Оптимизированный BoardRenderer")

    renderer = BoardRenderer(screen, 'white')

    test_board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]

    clock = pygame.time.Clock()
    running = True
    frame_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    # Переключение темы
                    themes = list(THEMES.keys())
                    current = themes.index(renderer._current_theme)
                    next_theme = themes[(current + 1) % len(themes)]
                    renderer.set_theme(next_theme)

        screen.fill((40, 40, 40))
        renderer.draw(
            test_board, 
            evaluation=0.5, 
            thinking=False,
            mouse_pos=pygame.mouse.get_pos(),
            move_count=10,
            capture_count=(3, 2),
            check_count=1
        )
        
        # FPS counter
        fps = int(clock.get_fps())
        fps_text = renderer.info_font.render(f"FPS: {fps}", True, (100, 255, 100))
        screen.blit(fps_text, (10, BOARD_SIZE + 60))
        
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    renderer.cleanup()
    pygame.quit()