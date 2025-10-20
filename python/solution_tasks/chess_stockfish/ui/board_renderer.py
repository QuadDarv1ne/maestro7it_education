"""
Модуль: ui/board_renderer.py (Улучшенная версия)

Улучшения:
- Кэширование ресурсов для повышения производительности
- Лучшая архитектура с разделением ответственности
- Поддержка анимаций и тем
- Улучшенная обработка ошибок
- Оптимизация рендеринга (dirty rectangles)
"""

import pygame
from typing import Optional, Tuple, List, Dict, Set
from dataclasses import dataclass
from enum import Enum
import logging

# ============================================================================
# Константы и конфигурация
# ============================================================================

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


class HighlightStyle(Enum):
    """Стили выделения клеток."""
    FILL = "fill"
    BORDER = "border"
    GLOW = "glow"


# ============================================================================
# Вспомогательные классы
# ============================================================================

class ResourceCache:
    """Кэш для pygame ресурсов (шрифты, поверхности)."""
    
    def __init__(self):
        self.fonts: Dict[Tuple[str, int], pygame.font.Font] = {}
        self.surfaces: Dict[Tuple, pygame.Surface] = {}
        self.pieces: Dict[Tuple[str, Tuple], pygame.Surface] = {}
    
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
    
    def get_highlight_surface(self, color: Tuple, size: int) -> pygame.Surface:
        """Получить или создать поверхность подсветки."""
        key = (color, size)
        if key not in self.surfaces:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            surface.fill(color)
            self.surfaces[key] = surface
        return self.surfaces[key]
    
    def get_piece_surface(self, piece: str, color: Tuple[int, int, int], 
                         font: pygame.font.Font) -> Optional[pygame.Surface]:
        """Получить или создать отрендеренную фигуру."""
        key = (piece, color, id(font))
        if key not in self.pieces:
            if piece not in PIECE_UNICODE:
                return None
            self.pieces[key] = font.render(PIECE_UNICODE[piece], True, color)
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
        """Предвычислить все преобразования координат."""
        cache = {}
        for row in range(8):
            for col in range(8):
                if self.player_color == 'black':
                    cache[(row, col)] = (7 - row, 7 - col)
                else:
                    cache[(row, col)] = (row, col)
        return cache
    
    def fen_to_display(self, row: int, col: int) -> Tuple[int, int]:
        """FEN координаты → экранные координаты."""
        return self._display_cache[(row, col)]
    
    def display_to_fen(self, disp_row: int, disp_col: int) -> Tuple[int, int]:
        """Экранные координаты → FEN координаты."""
        if self.player_color == 'black':
            return (7 - disp_row, 7 - disp_col)
        return (disp_row, disp_col)
    
    def pixel_to_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Пиксельные координаты → клетка доски (FEN)."""
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return None
        disp_row, disp_col = y // SQUARE_SIZE, x // SQUARE_SIZE
        return self.display_to_fen(disp_row, disp_col)


class EffectRenderer:
    """Рендеринг визуальных эффектов (подсветки, тени, анимации)."""
    
    def __init__(self, screen: pygame.Surface, theme: BoardTheme, cache: ResourceCache):
        self.screen = screen
        self.theme = theme
        self.cache = cache
    
    def draw_rounded_rect(self, rect: pygame.Rect, color: Tuple[int, int, int], 
                         corner_radius: int = 5):
        """Прямоугольник со скруглёнными углами."""
        corner_radius = max(0, min(corner_radius, min(rect.width, rect.height) // 2))
        
        # Основные прямоугольники
        pygame.draw.rect(self.screen, color, 
                        (rect.left + corner_radius, rect.top, 
                         rect.width - 2 * corner_radius, rect.height))
        pygame.draw.rect(self.screen, color, 
                        (rect.left, rect.top + corner_radius, 
                         rect.width, rect.height - 2 * corner_radius))
        
        # Углы
        corners = [
            (rect.left + corner_radius, rect.top + corner_radius),
            (rect.right - corner_radius, rect.top + corner_radius),
            (rect.left + corner_radius, rect.bottom - corner_radius),
            (rect.right - corner_radius, rect.bottom - corner_radius)
        ]
        for corner in corners:
            pygame.draw.circle(self.screen, color, corner, corner_radius)
    
    def draw_highlight(self, rect: pygame.Rect, color: Tuple[int, int, int, int], 
                      style: HighlightStyle, border_width: int = 3):
        """Отрисовка различных стилей подсветки."""
        if style == HighlightStyle.FILL:
            highlight = self.cache.get_highlight_surface(color, rect.width)
            self.screen.blit(highlight, rect.topleft)
        
        elif style == HighlightStyle.BORDER:
            pygame.draw.rect(self.screen, color, rect, border_width, border_radius=5)
        
        elif style == HighlightStyle.GLOW:
            glow_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            for i in range(5):
                alpha = max(0, color[3] - i * 30)
                glow_color = (color[0], color[1], color[2], alpha)
                pygame.draw.rect(glow_surface, glow_color, 
                               (i, i, rect.width - 2*i, rect.height - 2*i), 
                               border_radius=5)
            self.screen.blit(glow_surface, rect.topleft)
    
    def draw_piece_with_shadow(self, piece: str, rect: pygame.Rect, 
                              color: Tuple[int, int, int], font: pygame.font.Font):
        """Фигура с тенью."""
        piece_surface = self.cache.get_piece_surface(piece, color, font)
        if not piece_surface:
            return
        
        # Тень
        shadow_surface = self.cache.get_piece_surface(piece, (50, 50, 50), font)
        if shadow_surface:
            shadow_rect = shadow_surface.get_rect(
                center=(rect.centerx + 2, rect.centery + 2)
            )
            self.screen.blit(shadow_surface, shadow_rect)
        
        # Основная фигура
        piece_rect = piece_surface.get_rect(center=rect.center)
        self.screen.blit(piece_surface, piece_rect)
    
    def draw_move_hint_dot(self, rect: pygame.Rect):
        """Точка-подсказка для возможного хода."""
        center = rect.center
        # Draw a more visible hint with gradient effect
        for i in range(5):
            alpha = max(0, 200 - i * 30)
            radius = max(1, 8 - i)
            pygame.draw.circle(self.screen, (0, 0, 255, alpha), center, radius)
        pygame.draw.circle(self.screen, (255, 255, 255), center, 8, 2)


# ============================================================================
# Главный класс рендерера
# ============================================================================

class BoardRenderer:
    """
    Улучшенный рендерер шахматной доски.
    
    Особенности:
    - Кэширование ресурсов
    - Оптимизация через dirty rectangles
    - Модульная архитектура
    - Поддержка тем и анимаций
    """
    
    def __init__(self, screen: pygame.Surface, player_color: str = 'white',
                 theme: Optional[BoardTheme] = None):
        self.screen = screen
        self.player_color = player_color
        self.theme = theme or BoardTheme()
        
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
        self.piece_font = self.cache.get_font('Segoe UI Symbol', SQUARE_SIZE - 10)
        self.coord_font = self.cache.get_font('Arial', 12, bold=True)
        self.info_font = self.cache.get_font('Arial', 14)
    
    def set_player_color(self, color: str):
        """Изменить ориентацию доски."""
        if color != self.player_color:
            self.player_color = color
            self.coord_mapper = CoordinateMapper(color)
            self._mark_all_dirty()
    
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
        """Получить прямоугольник клетки."""
        disp_row, disp_col = self.coord_mapper.fen_to_display(row, col)
        return pygame.Rect(disp_col * SQUARE_SIZE, disp_row * SQUARE_SIZE,
                          SQUARE_SIZE, SQUARE_SIZE)
    
    def _draw_square_base(self, row: int, col: int):
        """Отрисовка базовой клетки."""
        color = (self.theme.light_square if (row + col) % 2 == 0 
                else self.theme.dark_square)
        rect = self._get_square_rect(row, col)
        self.effect_renderer.draw_rounded_rect(rect, color)
        pygame.draw.rect(self.screen, (100, 100, 100), rect, 1, border_radius=5)
    
    def _draw_square_effects(self, row: int, col: int):
        """Отрисовка эффектов на клетке."""
        rect = self._get_square_rect(row, col)
        square = (row, col)
        
        # Hover
        if square == self.hover_square and square != self.selected_square:
            self.effect_renderer.draw_highlight(rect, self.theme.hover, 
                                               HighlightStyle.GLOW)
        
        # Последний ход
        if self.last_move and square in self.last_move:
            self.effect_renderer.draw_highlight(rect, self.theme.last_move, 
                                               HighlightStyle.BORDER, 3)
        
        # Выбранная клетка
        if square == self.selected_square:
            self.effect_renderer.draw_highlight(rect, self.theme.highlight, 
                                               HighlightStyle.BORDER, 4)
        
        # Шах
        if square == self.check_square:
            self.effect_renderer.draw_highlight(rect, self.theme.check, 
                                               HighlightStyle.GLOW)
        
        # Подсказки
        if square in self.move_hints:
            self.effect_renderer.draw_highlight(rect, self.theme.move_hint, 
                                               HighlightStyle.FILL)
            self.effect_renderer.draw_move_hint_dot(rect)
    
    def _draw_piece(self, row: int, col: int, piece: str):
        """Отрисовка фигуры."""
        rect = self._get_square_rect(row, col)
        color = (self.theme.white_piece if piece.isupper() 
                else self.theme.black_piece)
        self.effect_renderer.draw_piece_with_shadow(piece, rect, color, 
                                                    self.piece_font)
    
    def _draw_coordinates(self, row: int, col: int):
        """Отрисовка координат."""
        if not self.show_coords:
            return
        
        disp_row, disp_col = self.coord_mapper.fen_to_display(row, col)
        
        # Номера рядов (слева)
        if disp_col == 0:
            rank_text = self.coord_font.render(str(8 - row), True, (100, 100, 100))
            self.screen.blit(rank_text, 
                           (disp_col * SQUARE_SIZE + 5, 
                            disp_row * SQUARE_SIZE + 5))
        
        # Буквы колонок (снизу)
        if disp_row == 7:
            file_text = self.coord_font.render(chr(97 + col), True, (100, 100, 100))
            self.screen.blit(file_text, 
                           (disp_col * SQUARE_SIZE + SQUARE_SIZE - 15,
                            disp_row * SQUARE_SIZE + SQUARE_SIZE - 20))
    
    def draw(self, board_state: List[List[Optional[str]]], 
             evaluation: Optional[float] = None,
             thinking: bool = False,
             mouse_pos: Optional[Tuple[int, int]] = None):
        """
        Главный метод отрисовки.
        
        Оптимизация: перерисовываются только изменённые клетки.
        """
        self.update_hover(mouse_pos)
        
        # Определить, что изменилось
        if self._last_board_state is None:
            self._mark_all_dirty()
        else:
            for row in range(8):
                for col in range(8):
                    if board_state[row][col] != self._last_board_state[row][col]:
                        self._dirty_squares.add((row, col))
        
        # Отрисовка dirty squares
        for row, col in self._dirty_squares:
            self._draw_square_base(row, col)
            self._draw_square_effects(row, col)
            
            piece = board_state[row][col]
            if piece:
                self._draw_piece(row, col, piece)
            
            self._draw_coordinates(row, col)
        
        self._dirty_squares.clear()
        self._last_board_state = [row[:] for row in board_state]
        
        # Информационная панель
        self._draw_info_panel(evaluation, thinking)
    
    def _draw_info_panel(self, evaluation: Optional[float], thinking: bool):
        """Отрисовка информационной панели."""
        if evaluation is not None:
            eval_text = f"Оценка: {evaluation:+.1f}"
            color = (100, 255, 100) if evaluation > 0 else (255, 100, 100)
            text_surface = self.info_font.render(eval_text, True, color)
            self.screen.blit(text_surface, (10, BOARD_SIZE + 10))
        
        if thinking:
            thinking_text = self.info_font.render("⟳ Думаю...", True, (255, 200, 0))
            self.screen.blit(thinking_text, (BOARD_SIZE - 150, BOARD_SIZE + 10))
    
    def cleanup(self):
        """Очистка ресурсов."""
        self.cache.clear()


# ============================================================================
# Пример использования
# ============================================================================

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 50))
    pygame.display.set_caption("Улучшенный BoardRenderer")
    
    # Создание рендерера с тёмной темой
    dark_theme = BoardTheme(
        light_square=(100, 100, 120),
        dark_square=(60, 60, 80)
    )
    renderer = BoardRenderer(screen, 'white', dark_theme)
    
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