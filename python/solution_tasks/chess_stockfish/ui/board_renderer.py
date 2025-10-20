# ============================================================================
# ui/board_renderer.py
# ============================================================================

"""
Модуль: ui/board_renderer.py

Описание:
    Содержит класс BoardRenderer для визуализации шахматной доски в Pygame.
    Отвечает за отображение:
    - Клеток доски с правильной раскраской
    - Фигур с использованием Unicode символов
    - Выделений (выбранная клетка, последний ход, шах)
    - Координат (a-h, 1-8)
    - Информации позиции
    
Особенности:
    - Поддержка ориентации (белые снизу/чёрные снизу)
    - Правильное преобразование координат
    - Плавная анимация и отзывчивость
"""

import pygame
from typing import Optional, Tuple, List

BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

# Цветовая схема доски
LIGHT_SQUARE = (240, 217, 181)      # Светлые клетки (слоновая кость)
DARK_SQUARE = (181, 136, 99)        # Тёмные клетки (красное дерево)
HIGHLIGHT_COLOR = (124, 252, 0, 180)  # Зелёный - выбранная клетка
LAST_MOVE_COLOR = (205, 210, 106, 150)  # Жёлтый - последний ход
CHECK_COLOR = (255, 0, 0, 180)      # Красный - шах
MOVE_HINT_COLOR = (0, 0, 255, 100)  # Синий - возможные ходы

# Initialize fonts after pygame.init() is called
FONT = None
SMALL_FONT = None
MOVE_HINT_FONT = None

def init_fonts():
    """Initialize fonts after pygame is initialized."""
    global FONT, SMALL_FONT, MOVE_HINT_FONT
    try:
        FONT = pygame.font.SysFont('Segoe UI Symbol', SQUARE_SIZE - 10)
        SMALL_FONT = pygame.font.SysFont('Arial', 14)
        MOVE_HINT_FONT = pygame.font.SysFont('Arial', 10)
    except Exception:
        FONT = pygame.font.SysFont('Arial', SQUARE_SIZE - 10)
        SMALL_FONT = pygame.font.SysFont('Arial', 14)
        MOVE_HINT_FONT = pygame.font.SysFont('Arial', 10)

# Unicode символы фигур
PIECE_UNICODE = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',  # Белые
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'   # Чёрные
}

# Pre-create highlight surfaces for better performance
HIGHLIGHT_SURFACES = {}


def get_highlight_surface(color, size=SQUARE_SIZE):
    """Create or retrieve a cached highlight surface for better performance."""
    key = (color, size)
    if key not in HIGHLIGHT_SURFACES:
        highlight = pygame.Surface((size, size), pygame.SRCALPHA)
        highlight.fill(color)
        HIGHLIGHT_SURFACES[key] = highlight
    return HIGHLIGHT_SURFACES[key]


class BoardRenderer:
    """
    Класс для отображения шахматной доски и элементов интерфейса.
    
    Атрибуты:
        screen (pygame.Surface): Поверхность для отрисовки
        player_color (str): Сторона, за которую играет игрок ('white' или 'black')
        selected_square (Tuple): Выбранная клетка (ряд, колонна)
        last_move (Tuple): Последний выполненный ход (from_sq, to_sq)
        check_square (Tuple): Клетка короля в шахе
        move_hints (List): Подсказки возможных ходов
    """
    
    def __init__(self, screen: pygame.Surface, player_color: str = 'white'):
        """
        Инициализация рендерера доски.
        
        Параметры:
            screen (pygame.Surface): Поверхность Pygame для отрисовки
            player_color (str): Сторона игрока ('white' или 'black')
        """
        self.screen = screen
        self.player_color = player_color
        self.selected_square = None
        self.last_move = None
        self.check_square = None
        self.show_coords = True
        self.move_hints = []  # Список возможных ходов для отображения подсказок
        
        # Initialize fonts if not already done
        if FONT is None or SMALL_FONT is None:
            init_fonts()
    
    def set_selected(self, square: Tuple[int, int]):
        """Установить выбранную клетку."""
        self.selected_square = square
    
    def clear_selected(self):
        """Очистить выбранную клетку."""
        self.selected_square = None
    
    def set_last_move(self, from_sq: Tuple[int, int], to_sq: Tuple[int, int]):
        """Установить последний сделанный ход для выделения."""
        self.last_move = (from_sq, to_sq)
    
    def set_check(self, square: Optional[Tuple[int, int]]):
        """Установить клетку короля в шахе для выделения красным."""
        self.check_square = square
    
    def set_move_hints(self, hints: List[Tuple[int, int]]):
        """Установить подсказки возможных ходов."""
        self.move_hints = hints
    
    def clear_move_hints(self):
        """Очистить подсказки возможных ходов."""
        self.move_hints = []
    
    def _fen_to_display(self, row: int, col: int) -> Tuple[int, int]:
        """
        Преобразует FEN-координаты в экранные координаты с учётом стороны игрока.
        
        Параметры:
            row (int): Ряд в FEN (0-7, сверху вниз)
            col (int): Колонна в FEN (0-7, слева направо)
            
        Возвращает:
            Tuple[int, int]: (display_row, display_col) - экранные координаты
        """
        if self.player_color == 'black':
            return 7 - row, 7 - col
        return row, col
    
    def _display_to_fen(self, disp_row: int, disp_col: int) -> Tuple[int, int]:
        """
        Обратное преобразование: экранные координаты в FEN координаты.
        
        Параметры:
            disp_row (int): Ряд на экране
            disp_col (int): Колонна на экране
            
        Возвращает:
            Tuple[int, int]: (fen_row, fen_col) - координаты в FEN
        """
        if self.player_color == 'black':
            return 7 - disp_row, 7 - disp_col
        return disp_row, disp_col
    
    def draw(self, board_state: List[List[Optional[str]]], 
             evaluation: Optional[float] = None, 
             thinking: bool = False):
        """
        Отрисовка шахматной доски и всех элементов интерфейса.
        
        Параметры:
            board_state (List): 2D массив состояния доски
            evaluation (float): Текущая оценка позиции для отображения
            thinking (bool): Показать, что компьютер думает
        """
        # Pre-calculate display positions for better performance
        display_positions = {}
        for row in range(8):
            for col in range(8):
                display_positions[(row, col)] = self._fen_to_display(row, col)
        
        # Отрисовка клеток доски
        for row in range(8):
            for col in range(8):
                disp_row, disp_col = display_positions[(row, col)]
                
                # Базовый цвет клетки
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(disp_col * SQUARE_SIZE, disp_row * SQUARE_SIZE, 
                                   SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Выделение последнего хода (жёлтая подсветка)
                if self.last_move:
                    if (row, col) in self.last_move:
                        highlight = get_highlight_surface(LAST_MOVE_COLOR)
                        self.screen.blit(highlight, rect.topleft)
                
                # Выделение выбранной клетки (зелёная подсветка)
                if self.selected_square == (row, col):
                    highlight = get_highlight_surface(HIGHLIGHT_COLOR)
                    self.screen.blit(highlight, rect.topleft)
                
                # Выделение шаха (красная подсветка)
                if self.check_square == (row, col):
                    highlight = get_highlight_surface(CHECK_COLOR)
                    self.screen.blit(highlight, rect.topleft)
                
                # Подсказки возможных ходов (синие кружки)
                if (row, col) in self.move_hints:
                    highlight = get_highlight_surface(MOVE_HINT_COLOR)
                    self.screen.blit(highlight, rect.topleft)
                    # Рисуем кружок в центре клетки
                    center_x = rect.centerx
                    center_y = rect.centery
                    pygame.draw.circle(self.screen, (0, 0, 255, 200), (center_x, center_y), 8)
                
                # Отрисовка фигур с Unicode символами
                piece = board_state[row][col]
                if piece and FONT is not None:
                    text_color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
                    try:
                        text = FONT.render(PIECE_UNICODE[piece], True, text_color)
                    except KeyError:
                        text = FONT.render(piece, True, text_color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                
                # Отрисовка координат (буквы и цифры) - только по краям
                if self.show_coords and SMALL_FONT is not None:
                    if disp_col == 0:  # Левая граница - номера рядов
                        rank_text = SMALL_FONT.render(str(8 - row), True, (100, 100, 100))
                        self.screen.blit(rank_text, (disp_col * SQUARE_SIZE + 2, 
                                                     disp_row * SQUARE_SIZE + 2))
                    if disp_row == 7:  # Нижняя граница - буквы файлов
                        file_text = SMALL_FONT.render(chr(97 + col), True, (100, 100, 100))
                        self.screen.blit(file_text, (disp_col * SQUARE_SIZE + SQUARE_SIZE - 12, 
                                                     disp_row * SQUARE_SIZE + SQUARE_SIZE - 14))
        
        # Отрисовка дополнительной информации
        if evaluation is not None and SMALL_FONT is not None:
            eval_text = f"Оценка: {evaluation:+.1f}"
            color = (100, 255, 100) if evaluation > 0 else (255, 100, 100)
            text_surface = SMALL_FONT.render(eval_text, True, color)
            self.screen.blit(text_surface, (10, 10))
        
        if thinking and SMALL_FONT is not None:
            thinking_text = SMALL_FONT.render("⟳ Компьютер думает...", True, (255, 200, 0))
            self.screen.blit(thinking_text, (BOARD_SIZE - 200, 10))