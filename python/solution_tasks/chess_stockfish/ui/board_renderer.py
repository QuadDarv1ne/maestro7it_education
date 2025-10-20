"""
Модуль: ui/board_renderer.py (Улучшенная версия — исправленная)

Исправления и улучшения:
- get_highlight_surface поддерживает произвольный размер (width, height)
- Надёжная работа с цветами RGB и RGBA (альфа необязательна)
- Подсветка (fill/border/glow) рисуется на временной поверхности с SRCALPHA для корректной альфа-композиции
- draw_move_hint_dot использует временную поверхность и градиент через alpha
- Использование кэша шрифтов для всех текстов (eval, coords и т.д.)
- Мелкие улучшения: назначение _current_theme в конструкторе, логирование ошибок, безопасное получение unicode фигур
- Улучшена совместимость с Pygame 2.x (border_radius, SRCALPHA)
"""

import pygame
from typing import Optional, Tuple, List, Dict, Set, Union
from dataclasses import dataclass
from enum import Enum
import logging
import math
import time

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
    'contrast': BoardTheme(
        light_square=(255, 255, 255),
        dark_square=(0, 0, 0),
        white_piece=(200, 0, 0),
        black_piece=(200, 200, 0)
    )
}


class HighlightStyle(Enum):
    """Стили выделения клеток."""
    FILL = "fill"
    BORDER = "border"
    GLOW = "glow"


# ============================================================================ #
# Вспомогательные классы
# ============================================================================ #


class ResourceCache:
    """Кэш для pygame ресурсов (шрифты, поверхности, рендеренные фигуры)."""

    def __init__(self):
        # key: (name, size, bold)
        self.fonts: Dict[Tuple[str, int, bool], pygame.font.Font] = {}
        # key: (color_tuple, (width,height))
        self.surfaces: Dict[Tuple[Tuple[int, ...], Tuple[int, int]], pygame.Surface] = {}
        # key: (piece_char, color_tuple, font_id)
        self.pieces: Dict[Tuple[str, Tuple[int, ...], int], pygame.Surface] = {}

    def _normalize_color(self, color: Union[Tuple[int, ...], List[int]]) -> Tuple[int, ...]:
        """Возвращает цвет как хешируемый tuple; дополняет альфу если нужно."""
        col = tuple(color)
        if len(col) == 3:
            return col
        return col  # may be 4-tuple

    def get_font(self, name: str, size: int, bold: bool = False) -> pygame.font.Font:
        """Получить или создать шрифт."""
        key = (name, size, bold)
        if key not in self.fonts:
            try:
                self.fonts[key] = pygame.font.SysFont(name, size, bold=bold)
            except Exception as e:
                logging.warning(f"ResourceCache: Failed to load font {name}: {e}. Using default font.")
                self.fonts[key] = pygame.font.Font(None, size)
        return self.fonts[key]

    def get_highlight_surface(self, color: Union[Tuple[int, ...], List[int]],
                              size: Tuple[int, int]) -> pygame.Surface:
        """
        Возвращает поверхность с указанным цветом и размером (width, height).
        Цвет может быть RGB или RGBA.
        """
        color_t = self._normalize_color(color)
        key = (color_t, (int(size[0]), int(size[1])))
        if key not in self.surfaces:
            surf = pygame.Surface((key[1][0], key[1][1]), pygame.SRCALPHA)
            # fill with RGBA if provided, else add full alpha
            if len(color_t) == 4:
                surf.fill(color_t)
            else:
                surf.fill((color_t[0], color_t[1], color_t[2], 255))
            self.surfaces[key] = surf
        return self.surfaces[key]

    def get_piece_surface(self, piece: str, color: Tuple[int, int, int],
                          font: pygame.font.Font) -> Optional[pygame.Surface]:
        """Получить или создать отрендеренную фигуру (unicode)."""
        try:
            key = (piece, tuple(color), id(font))
        except Exception:
            # safety fallback
            key = (piece, (color[0], color[1], color[2]), id(font))

        if key not in self.pieces:
            if piece not in PIECE_UNICODE:
                return None
            try:
                # рендерим на прозрачной поверхности
                surf = font.render(PIECE_UNICODE[piece], True, color)
            except Exception as e:
                logging.warning(f"ResourceCache: Failed to render piece '{piece}': {e}")
                return None
            self.pieces[key] = surf
        return self.pieces[key]

    def clear(self):
        """Очистить весь кэш."""
        self.fonts.clear()
        self.surfaces.clear()
        self.pieces.clear()


class CoordinateMapper:
    """Преобразование координат между FEN и экраном."""

    def __init__(self, player_color: str = 'white'):
        self.player_color = player_color
        self._display_cache = self._build_display_cache()

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
        """Пиксельные координаты → клетка доски (FEN)."""
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return None
        disp_row, disp_col = y // SQUARE_SIZE, x // SQUARE_SIZE
        if self.player_color == 'black':
            return (7 - disp_row, 7 - disp_col)
        return (disp_row, disp_col)


class EffectRenderer:
    """Рендеринг визуальных эффектов (подсветки, тени, анимации)."""

    def __init__(self, screen: pygame.Surface, theme: BoardTheme, cache: ResourceCache):
        self.screen = screen
        self.theme = theme
        self.cache = cache

    @staticmethod
    def _ensure_rgba(color: Union[Tuple[int, ...], List[int]]) -> Tuple[int, int, int, int]:
        """Возвращает RGBA-цвет, дополняя альфу до 255 при необходимости."""
        c = tuple(color)
        if len(c) == 4:
            return c  # type: ignore
        return (c[0], c[1], c[2], 255)  # type: ignore

    def draw_rounded_rect(self, rect: pygame.Rect, color: Tuple[int, int, int],
                          corner_radius: int = 5):
        """Прямоугольник со скруглёнными углами (без альфа)."""
        corner_radius = max(0, min(corner_radius, min(rect.width, rect.height) // 2))
        # Draw filled rounded rect on the main surface
        try:
            # Pygame >=2 supports border_radius param
            pygame.draw.rect(self.screen, color,
                             rect, 0, border_radius=corner_radius)
            # Add subtle border
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 1, border_radius=corner_radius)
        except TypeError:
            # fallback if older pygame without border_radius positional arg
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def draw_highlight(self, rect: pygame.Rect, color: Union[Tuple[int, ...], List[int]],
                       style: HighlightStyle, border_width: int = 3):
        """Отрисовка различных стилей подсветки с поддержкой альфа."""
        rgba = self._ensure_rgba(color)
        # Используем временную поверхность, чтобы корректно смешать альфу
        surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        if style == HighlightStyle.FILL:
            # fill whole rect with color
            fill_surf = self.cache.get_highlight_surface(rgba, (rect.width, rect.height))
            surf.blit(fill_surf, (0, 0))
            self.screen.blit(surf, rect.topleft)

        elif style == HighlightStyle.BORDER:
            # draw border on surf then blit
            inner_rect = pygame.Rect(0, 0, rect.width, rect.height)
            try:
                pygame.draw.rect(surf, rgba, inner_rect, border_width, border_radius=5)
            except TypeError:
                pygame.draw.rect(surf, rgba, inner_rect, border_width)
            self.screen.blit(surf, rect.topleft)

        elif style == HighlightStyle.GLOW:
            # multi-layer glow
            glow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            base_alpha = rgba[3]
            for i in range(5):
                a = max(0, base_alpha - i * (base_alpha // 5 + 5))
                inset = i * 3
                rr = pygame.Rect(inset, inset, rect.width - inset * 2, rect.height - inset * 2)
                if rr.width <= 0 or rr.height <= 0:
                    continue
                glow_color = (rgba[0], rgba[1], rgba[2], a)
                try:
                    pygame.draw.rect(glow_surf, glow_color, rr, border_radius=5)
                except TypeError:
                    pygame.draw.rect(glow_surf, glow_color, rr)
            self.screen.blit(glow_surf, rect.topleft)

    def draw_piece_with_shadow(self, piece: str, rect: pygame.Rect,
                               color: Tuple[int, int, int], font: pygame.font.Font):
        """Фигура с тенью (рендерunicode через кэш). Улучшенная 3D визуализация."""
        piece_surface = self.cache.get_piece_surface(piece, color, font)
        if not piece_surface:
            return

        # Create a more realistic 3D effect with gradient shadows and highlights
        # Bottom layer (darkest shadow with blur effect)
        shadow_offset = 4
        shadow_color = (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50))
        
        # Create a blurred shadow effect
        shadow_surface = pygame.Surface((piece_surface.get_width() + 8, piece_surface.get_height() + 8), pygame.SRCALPHA)
        shadow_rect = pygame.Rect(0, 0, shadow_surface.get_width(), shadow_surface.get_height())
        
        # Draw multiple layers of shadow with decreasing alpha for blur effect
        for i in range(3):
            alpha = max(0, 80 - i * 30)
            temp_color = (shadow_color[0], shadow_color[1], shadow_color[2], alpha)
            temp_rect = pygame.Rect(
                shadow_offset - 1 + i, 
                shadow_offset - 1 + i, 
                shadow_rect.width - 2*i, 
                shadow_rect.height - 2*i
            )
            if temp_rect.width > 0 and temp_rect.height > 0:
                pygame.draw.ellipse(shadow_surface, temp_color, temp_rect)
        
        # Position the shadow
        shadow_position = (rect.centerx - shadow_surface.get_width()//2 + shadow_offset, 
                          rect.centery - shadow_surface.get_height()//2 + shadow_offset)
        self.screen.blit(shadow_surface, shadow_position)

        # Middle layer (medium shadow)
        mid_shadow_offset = 2
        mid_shadow_color = (max(0, color[0] - 25), max(0, color[1] - 25), max(0, color[2] - 25))
        mid_shadow_surface = self.cache.get_piece_surface(piece, mid_shadow_color, font)
        
        if mid_shadow_surface:
            mid_shadow_rect = mid_shadow_surface.get_rect(center=(rect.centerx + mid_shadow_offset, rect.centery + mid_shadow_offset))
            self.screen.blit(mid_shadow_surface, mid_shadow_rect)

        # Main piece (top layer, brightest)
        piece_rect = piece_surface.get_rect(center=rect.center)
        self.screen.blit(piece_surface, piece_rect)
        
        # Add realistic highlight for 3D effect
        highlight_offset = 1
        highlight_color = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
        
        # Create a highlight surface with gradient
        highlight_surface = pygame.Surface((piece_surface.get_width() // 2, piece_surface.get_height() // 2), pygame.SRCALPHA)
        highlight_radius = min(highlight_surface.get_width(), highlight_surface.get_height()) // 2
        
        # Draw gradient highlight
        for i in range(highlight_radius, 0, -1):
            alpha = int(150 * (i / highlight_radius))
            temp_color = (highlight_color[0], highlight_color[1], highlight_color[2], alpha)
            pygame.draw.circle(highlight_surface, temp_color, (highlight_surface.get_width() // 2, highlight_surface.get_height() // 3), i)
        
        # Position the highlight on the top-left of the piece
        highlight_position = (piece_rect.left + piece_rect.width // 4 - highlight_offset,
                             piece_rect.top + piece_rect.height // 6 - highlight_offset)
        self.screen.blit(highlight_surface, highlight_position)
        
        # Add secondary highlight for more depth
        secondary_highlight_color = (min(255, color[0] + 20), min(255, color[1] + 20), min(255, color[2] + 20), 100)
        secondary_highlight = pygame.Surface((piece_surface.get_width() // 4, piece_surface.get_height() // 4), pygame.SRCALPHA)
        pygame.draw.ellipse(secondary_highlight, secondary_highlight_color, secondary_highlight.get_rect())
        secondary_position = (piece_rect.right - piece_rect.width // 3, piece_rect.top + piece_rect.height // 4)
        self.screen.blit(secondary_highlight, secondary_position)

    def draw_check_indicator(self, rect: pygame.Rect):
        """
        Рисует индикатор шаха вокруг короля. Улучшенная анимация.
        
        Параметры:
            rect: Прямоугольник клетки с королем под шахом
        """
        # Рисуем пульсирующий красный круг вокруг короля с анимацией
        center_x = rect.centerx
        center_y = rect.centery
        base_radius = min(rect.width, rect.height) // 2 + 8
        
        # Создаем поверхность для пульсации с анимацией
        pulse_surface = pygame.Surface((base_radius * 3, base_radius * 3), pygame.SRCALPHA)
        
        # Получаем время для анимации пульсации
        current_time = time.time()
        
        # Анимация пульсации
        pulse_phase = (current_time * 3) % (2 * math.pi)
        pulse_multiplier = 1 + 0.3 * abs(math.sin(pulse_phase))
        
        # Рисуем несколько концентрических кругов для эффекта пульсации
        for i in range(5):
            pulse_radius = int((base_radius - i * 3) * pulse_multiplier)
            if pulse_radius > 0:
                # Создаем градиентный эффект
                alpha = max(0, 220 - i * 40)
                color = (255, 50, 50, alpha)  # Более насыщенный красный
                pygame.draw.circle(pulse_surface, color, (base_radius * 3 // 2, base_radius * 3 // 2), pulse_radius, 3)
        
        # Добавляем внутренний круг для большего эффекта
        inner_radius = int(base_radius * 0.6 * pulse_multiplier)
        pygame.draw.circle(pulse_surface, (255, 100, 100, 150), (base_radius * 3 // 2, base_radius * 3 // 2), inner_radius, 2)
        
        # Добавляем эффект свечения
        glow_surface = pygame.Surface((base_radius * 4, base_radius * 4), pygame.SRCALPHA)
        glow_radius = int(base_radius * 1.5 * pulse_multiplier)
        for i in range(3):
            glow_alpha = max(0, 80 - i * 30)
            glow_color = (255, 0, 0, glow_alpha)
            pygame.draw.circle(glow_surface, glow_color, (base_radius * 2, base_radius * 2), glow_radius - i * 2)
        
        # Рисуем свечение позади пульсации
        self.screen.blit(glow_surface, (center_x - base_radius * 2, center_y - base_radius * 2))
        
        # Рисуем пульсацию
        self.screen.blit(pulse_surface, (center_x - base_radius * 3 // 2, center_y - base_radius * 3 // 2))

    def draw_move_hint_dot(self, rect: pygame.Rect):
        """Точка-подсказка для возможного хода (с градиентом альфа)."""
        w, h = rect.width, rect.height
        hint_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        cx, cy = w // 2, h // 2
        max_radius = min(w, h) // 6
        for i in range(max_radius, 0, -1):
            alpha = int(180 * (i / max_radius))
            pygame.draw.circle(hint_surf, (0, 100, 255, alpha), (cx, cy), i)
        # white ring
        try:
            pygame.draw.circle(hint_surf, (255, 255, 255), (cx, cy), max_radius, 2)
        except Exception:
            pass
        self.screen.blit(hint_surf, rect.topleft)

    def draw_evaluation_bar(self, rect: pygame.Rect, evaluation: float):
        """Отрисовка полосы оценки позиции (использует кэшированные шрифты)."""
        # background
        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

        clamped_eval = max(-10.0, min(10.0, evaluation))
        white_advantage = (clamped_eval + 10.0) / 20.0
        white_width = int(rect.width * white_advantage)
        white_rect = pygame.Rect(rect.left, rect.top, white_width, rect.height)
        pygame.draw.rect(self.screen, (255, 255, 255), white_rect)

        center_x = rect.left + rect.width // 2
        pygame.draw.line(self.screen, (200, 200, 200), (center_x, rect.top), (center_x, rect.bottom), 1)

        if abs(evaluation) > 0.1:
            font = self.cache.get_font('Arial', 12, bold=True)
            eval_text = f"{evaluation:+.1f}"
            text_color = (100, 255, 100) if evaluation > 0 else (255, 100, 100) if evaluation < 0 else (200, 200, 200)
            text_surface = font.render(eval_text, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)


# ============================================================================ #
# Главный класс рендерера
# ============================================================================ #


class BoardRenderer:
    """
    Улучшенный рендерер шахматной доски.
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
        self.effect_renderer = EffectRenderer(screen, self.theme, self.cache)

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

    def _init_fonts(self):
        """Инициализация шрифтов через кэш."""
        # Подбираем размер шрифта для фигур чуть меньше квадрата
        self.piece_font = self.cache.get_font('Segoe UI Symbol', max(10, SQUARE_SIZE - 8))
        self.coord_font = self.cache.get_font('Arial', 14, bold=True)
        self.info_font = self.cache.get_font('Arial', 16)

    def set_player_color(self, color: str):
        """Изменить ориентацию доски."""
        if color != self.player_color:
            self.player_color = color
            self.coord_mapper = CoordinateMapper(color)
            self._mark_all_dirty()

    def set_theme(self, theme_name: str):
        """Изменить цветовую тему доски."""
        if theme_name in THEMES:
            self.theme = THEMES[theme_name]
            self.effect_renderer.theme = self.theme
            self._current_theme = theme_name
            self._mark_all_dirty()
        else:
            logging.warning(f"BoardRenderer.set_theme: unknown theme '{theme_name}'")

    def set_selected(self, square: Optional[Tuple[int, int]]):
        """Установить выбранную клетку."""
        if self.selected_square != square:
            if self.selected_square:
                self._dirty_squares.add(self.selected_square)
            self.selected_square = square
            if square:
                self._dirty_squares.add(square)

    def set_last_move(self, from_sq: Tuple[int, int], to_sq: Tuple[int, int]):
        """Установить последний ход."""
        if self.last_move:
            self._dirty_squares.update(self.last_move)
        self.last_move = (from_sq, to_sq)
        self._dirty_squares.update([from_sq, to_sq])

    def set_check(self, square: Optional[Tuple[int, int]]):
        """Установить клетку короля под шахом."""
        if self.check_square:
            self._dirty_squares.add(self.check_square)
        self.check_square = square
        if square:
            self._dirty_squares.add(square)

    def set_move_hints(self, hints: List[Tuple[int, int]]):
        """Установить подсказки ходов."""
        self._dirty_squares.update(self.move_hints)
        self.move_hints = hints
        self._dirty_squares.update(hints)

    def update_hover(self, mouse_pos: Optional[Tuple[int, int]]):
        """Обновить hover-клетку."""
        new_hover = None
        if mouse_pos:
            new_hover = self.coord_mapper.pixel_to_square(*mouse_pos)

        if new_hover != self.hover_square:
            if self.hover_square:
                self._dirty_squares.add(self.hover_square)
            self.hover_square = new_hover
            if new_hover:
                self._dirty_squares.add(new_hover)

    def _mark_all_dirty(self):
        """Пометить все клетки для перерисовки."""
        self._dirty_squares = {(r, c) for r in range(8) for c in range(8)}

    def _get_square_rect(self, row: int, col: int) -> pygame.Rect:
        """Получить прямоугольник клетки (экранные координаты)."""
        disp_row, disp_col = self.coord_mapper.fen_to_display(row, col)
        return pygame.Rect(disp_col * SQUARE_SIZE, disp_row * SQUARE_SIZE,
                           SQUARE_SIZE, SQUARE_SIZE)

    def _draw_square_base(self, row: int, col: int):
        """Отрисовка базовой клетки."""
        color = (self.theme.light_square if (row + col) % 2 == 0
                 else self.theme.dark_square)
        rect = self._get_square_rect(row, col)
        # draw rounded square
        self.effect_renderer.draw_rounded_rect(rect, color, corner_radius=6)

    def _draw_square_effects(self, row: int, col: int):
        """Отрисовка эффектов на клетке."""
        rect = self._get_square_rect(row, col)
        square = (row, col)

        # Hover
        if square == self.hover_square and square != self.selected_square:
            self.effect_renderer.draw_highlight(rect, self.theme.hover, HighlightStyle.GLOW)

        # Последний ход
        if self.last_move and square in self.last_move:
            self.effect_renderer.draw_highlight(rect, self.theme.last_move, HighlightStyle.BORDER, 3)

        # Выбранная клетка
        if square == self.selected_square:
            self.effect_renderer.draw_highlight(rect, self.theme.highlight, HighlightStyle.BORDER, 4)

        # Шах
        if square == self.check_square:
            self.effect_renderer.draw_highlight(rect, self.theme.check, HighlightStyle.GLOW)
            # Дополнительно рисуем индикатор шаха
            self.effect_renderer.draw_check_indicator(rect)

        # Подсказки
        if square in self.move_hints:
            self.effect_renderer.draw_highlight(rect, self.theme.move_hint, HighlightStyle.FILL)
            self.effect_renderer.draw_move_hint_dot(rect)

    def _draw_piece(self, row: int, col: int, piece: str):
        """Отрисовка фигуры."""
        rect = self._get_square_rect(row, col)
        color = (self.theme.white_piece if piece.isupper()
                 else self.theme.black_piece)
        self.effect_renderer.draw_piece_with_shadow(piece, rect, color, self.piece_font)

    def _draw_coordinates(self, row: int, col: int):
        """Отрисовка координат (номера рядов и буквы колонок)."""
        if not self.show_coords:
            return

        disp_row, disp_col = self.coord_mapper.fen_to_display(row, col)

        # Номера рядов (слева)
        if disp_col == 0:
            # Для белых: ряд 0 -> 8, для чёрных: ряд 0 -> 1
            rank_num = row + 1 if self.player_color == 'black' else 8 - row
            rank_text = self.coord_font.render(str(rank_num), True, (100, 100, 100))
            self.screen.blit(rank_text,
                             (disp_col * SQUARE_SIZE + 5,
                              disp_row * SQUARE_SIZE + 4))

        # Буквы колонок (снизу)
        if disp_row == 7:
            file_char = chr(97 + 7 - col) if self.player_color == 'black' else chr(97 + col)
            file_text = self.coord_font.render(file_char, True, (100, 100, 100))
            self.screen.blit(file_text,
                             (disp_col * SQUARE_SIZE + SQUARE_SIZE - 16,
                              disp_row * SQUARE_SIZE + SQUARE_SIZE - 20))

    def draw(self, board_state: List[List[Optional[str]]],
             evaluation: Optional[float] = None,
             thinking: bool = False,
             mouse_pos: Optional[Tuple[int, int]] = None,
             move_count: int = 0,
             capture_count: Tuple[int, int] = (0, 0),
             check_count: int = 0):
        """
        Главный метод отрисовки.

        Рисуем только dirty squares (и инфо-панель).
        Добавлены дополнительные визуальные индикаторы.
        """
        # Обновим hover (и пометим нужные клетки)
        self.update_hover(mouse_pos)

        # Если первый рендер — пометим всё
        if self._last_board_state is None:
            self._mark_all_dirty()
        else:
            # сравним состояния и пометим отличающиеся клетки
            for row in range(8):
                for col in range(8):
                    if board_state[row][col] != self._last_board_state[row][col]:
                        self._dirty_squares.add((row, col))

        # Рисуем все помеченные клетки
        for row, col in list(self._dirty_squares):
            try:
                self._draw_square_base(row, col)
                self._draw_square_effects(row, col)

                piece = board_state[row][col]
                if piece:
                    self._draw_piece(row, col, piece)

                self._draw_coordinates(row, col)
            except Exception as e:
                logging.exception(f"BoardRenderer.draw: error drawing square {(row, col)}: {e}")

        # очистим пометки
        self._dirty_squares.clear()
        # сохраним копию состояния доски
        self._last_board_state = [row[:] for row in board_state]

        # Информационная панель (рисуется полностью)
        self._draw_info_panel(evaluation, thinking)
        
        # Дополнительные визуальные индикаторы
        self._draw_additional_indicators(move_count, capture_count, check_count)
        
    def _draw_additional_indicators(self, move_count: int, capture_count: Tuple[int, int], check_count: int):
        """
        Отрисовка дополнительных визуальных индикаторов.
        
        Параметры:
            move_count: Количество сделанных ходов
            capture_count: Кортеж (взятия игрока, взятия ИИ)
            check_count: Количество шахов
        """
        try:
            # Индикатор количества ходов
            if move_count > 0:
                moves_rect = pygame.Rect(220, BOARD_SIZE + 10, 100, 20)
                moves_text = f"Ходы: {move_count}"
                moves_surface = self.info_font.render(moves_text, True, (200, 200, 100))
                self.screen.blit(moves_surface, moves_rect)
            
            # Индикатор взятий
            player_captures, ai_captures = capture_count
            if player_captures > 0 or ai_captures > 0:
                captures_rect = pygame.Rect(220, BOARD_SIZE + 35, 150, 20)
                captures_text = f"Взятия: {player_captures} vs {ai_captures}"
                captures_color = (100, 200, 100) if player_captures >= ai_captures else (200, 100, 100)
                captures_surface = self.info_font.render(captures_text, True, captures_color)
                self.screen.blit(captures_surface, captures_rect)
            
            # Индикатор шахов
            if check_count > 0:
                checks_rect = pygame.Rect(380, BOARD_SIZE + 10, 100, 20)
                checks_text = f"Шахи: {check_count}"
                checks_surface = self.info_font.render(checks_text, True, (255, 100, 100))
                self.screen.blit(checks_surface, checks_rect)
                
        except Exception as e:
            logging.warning(f"Ошибка при отрисовке дополнительных индикаторов: {e}")

    def _draw_info_panel(self, evaluation: Optional[float], thinking: bool):
        """Отрисовка информационной панели внизу."""
        # Draw evaluation bar
        if evaluation is not None:
            eval_bar_rect = pygame.Rect(10, BOARD_SIZE + 10, 200, 20)
            self.effect_renderer.draw_evaluation_bar(eval_bar_rect, evaluation)

        # Draw thinking indicator
        if thinking:
            thinking_text = self.info_font.render("⟳ Думаю...", True, (255, 200, 0))
            self.screen.blit(thinking_text, (BOARD_SIZE - 150, BOARD_SIZE + 10))

        # Draw theme indicator
        theme_text = self.info_font.render(f"Тема: {getattr(self, '_current_theme', 'classic')}", True, (200, 200, 200))
        self.screen.blit(theme_text, (BOARD_SIZE - 150, BOARD_SIZE + 35))
        
    def _draw_progress_bar(self, rect: pygame.Rect, progress: float, color: Tuple[int, int, int] = (100, 200, 100)):
        """
        Отрисовка прогресс бара.
        
        Параметры:
            rect: Прямоугольник для прогресс бара
            progress: Прогресс от 0.0 до 1.0
            color: Цвет прогресса
        """
        # Отрисовка фона
        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
        
        # Отрисовка прогресса
        progress_width = int(rect.width * max(0, min(1, progress)))
        if progress_width > 0:
            progress_rect = pygame.Rect(rect.left, rect.top, progress_width, rect.height)
            pygame.draw.rect(self.screen, color, progress_rect)
            
            # Добавляем градиентный эффект
            for i in range(0, progress_width, 2):
                alpha = int(100 * (1 - i / progress_width))
                highlight_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50), alpha)
                # Создаем временную поверхность для градиента
                highlight_surf = pygame.Surface((2, rect.height), pygame.SRCALPHA)
                highlight_surf.fill(highlight_color)
                self.screen.blit(highlight_surf, (rect.left + i, rect.top))
                
    def _draw_status_indicator(self, rect: pygame.Rect, status: str, color: Tuple[int, int, int] = (200, 200, 200)):
        """
        Отрисовка индикатора статуса с иконкой.
        
        Параметры:
            rect: Прямоугольник для индикатора
            status: Текст статуса
            color: Цвет текста
        """
        # Отрисовка фона с закругленными углами
        pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=5)
        pygame.draw.rect(self.screen, (80, 80, 80), rect, 1, border_radius=5)
        
        # Отрисовка текста
        if self.info_font:
            text = self.info_font.render(status, True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
    def _draw_enhanced_feedback(self, feedback: str, rect: pygame.Rect, feedback_type: str = "info"):
        """
        Отрисовка улучшенной обратной связи с визуальными эффектами.
        
        Параметры:
            feedback: Текст обратной связи
            rect: Прямоугольник для отрисовки
            feedback_type: Тип обратной связи ("info", "warning", "success", "error")
        """
        # Определяем цвета в зависимости от типа обратной связи
        colors = {
            "info": (100, 200, 255),      # Голубой
            "warning": (255, 200, 100),   # Желтый
            "success": (100, 255, 100),   # Зеленый
            "error": (255, 100, 100)      # Красный
        }
        
        color = colors.get(feedback_type, colors["info"])
        
        # Отрисовка фона с градиентом
        pygame.draw.rect(self.screen, (30, 30, 30), rect, border_radius=8)
        pygame.draw.rect(self.screen, color, rect, 2, border_radius=8)
        
        # Добавляем внутреннюю тень
        inner_rect = pygame.Rect(rect.left + 2, rect.top + 2, rect.width - 4, rect.height - 4)
        pygame.draw.rect(self.screen, (20, 20, 20), inner_rect, border_radius=6)
        
        # Отрисовка текста с тенью
        if self.info_font:
            # Тень
            shadow_text = self.info_font.render(feedback, True, (0, 0, 0))
            self.screen.blit(shadow_text, (rect.left + 15, rect.top + 10))
            
            # Основной текст
            text = self.info_font.render(feedback, True, color)
            self.screen.blit(text, (rect.left + 13, rect.top + 8))
            
        # Добавляем иконку в зависимости от типа обратной связи
        icon_rect = pygame.Rect(rect.right - 25, rect.top + 5, 20, 20)
        if feedback_type == "success":
            # Зеленая галочка
            pygame.draw.line(self.screen, color, (icon_rect.left + 5, icon_rect.centery), 
                           (icon_rect.centerx - 2, icon_rect.bottom - 5), 3)
            pygame.draw.line(self.screen, color, (icon_rect.centerx - 2, icon_rect.bottom - 5), 
                           (icon_rect.right - 5, icon_rect.top + 5), 3)
        elif feedback_type == "warning":
            # Желтый восклицательный знак
            pygame.draw.circle(self.screen, color, (icon_rect.centerx, icon_rect.top + 5), 3)
            pygame.draw.line(self.screen, color, (icon_rect.centerx, icon_rect.top + 10), 
                           (icon_rect.centerx, icon_rect.bottom - 5), 3)
        elif feedback_type == "error":
            # Красный крестик
            pygame.draw.line(self.screen, color, (icon_rect.left + 5, icon_rect.top + 5), 
                           (icon_rect.right - 5, icon_rect.bottom - 5), 3)
            pygame.draw.line(self.screen, color, (icon_rect.right - 5, icon_rect.top + 5), 
                           (icon_rect.left + 5, icon_rect.bottom - 5), 3)
        else:  # info
            # Синий кружок с i
            pygame.draw.circle(self.screen, color, icon_rect.center, 8, 2)
            pygame.draw.line(self.screen, color, (icon_rect.centerx, icon_rect.top + 6), 
                           (icon_rect.centerx, icon_rect.bottom - 6), 2)
            pygame.draw.circle(self.screen, color, (icon_rect.centerx, icon_rect.top + 4), 2)

    def cleanup(self):
        """Очистка ресурсов (кэш)."""
        self.cache.clear()
    
    def clear_temp_surfaces(self):
        """Очистка временных поверхностей для предотвращения утечек памяти."""
        # Очищаем только временные поверхности, оставляя кэш шрифтов и фигур
        temp_surfaces = {}
        for key, surface in self.cache.surfaces.items():
            # Сохраняем поверхности подсветки, которые могут быть переиспользованы
            if key[0][3] < 200:  # alpha < 200 indicates temporary highlight surfaces
                temp_surfaces[key] = surface
        self.cache.surfaces = temp_surfaces


# ============================================================================ #
# Пример использования (если запускается как скрипт)
# ============================================================================ #

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 50))
    pygame.display.set_caption("Улучшенный BoardRenderer (исправленная версия)")

    # Создание рендерера с тёмной темой
    dark_theme = BoardTheme(
        light_square=(100, 100, 120),
        dark_square=(60, 60, 80)
    )
    renderer = BoardRenderer(screen, 'white', dark_theme)
    renderer._current_theme = 'dark'  # метка

    # Тестовая позиция
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

    # initial dirty so draws everything first loop
    renderer._mark_all_dirty()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True,
                      mouse_pos=pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(60)

    renderer.cleanup()
    pygame.quit()
