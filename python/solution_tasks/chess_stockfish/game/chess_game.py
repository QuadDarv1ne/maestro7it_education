#!/usr/bin/env python3
# ============================================================================
# game/chess_game.py (Обновлённая версия)
# ============================================================================

"""
Модуль: game/chess_game.py

Описание:
    Содержит главный класс ChessGame, который управляет игровым процессом.
    
Изменения в этой версии:
    - Удалён импорт и вызов init_fonts() (инициализация теперь в BoardRenderer)
    - Обновлены методы для работы с новым API BoardRenderer
    - Улучшена обработка ошибок
"""

import pygame
from typing import Optional, Tuple, List
import time
import sys
import random

# Import our modules
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer  # Убран init_fonts
from utils.educational import ChessEducator

# Constants from board_renderer
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8


class ChessGame:
    """
    Главный класс для управления ходом игры.
    
    Атрибуты:
        player_color (str): Сторона, за которую играет игрок
        ai_color (str): Сторона, за которую играет компьютер
        engine (StockfishWrapper): Экземпляр шахматного движка
        move_history (List): История всех сделанных ходов
        game_over (bool): Флаг окончания игры
        renderer (BoardRenderer): Рендерер для отображения доски
        educator (ChessEducator): Образовательный компонент для подсказок
    """
    
    def __init__(self, player_color: str = 'white', skill_level: int = 5, theme: str = 'classic'):
        """
        Инициализация новой игры.
        
        Параметры:
            player_color (str): Выбранная сторона ('white' или 'black')
            skill_level (int): Уровень сложности Stockfish (0-20)
            theme (str): Цветовая тема доски
            
        Исключения:
            RuntimeError: Если не удалось инициализировать Stockfish
        """
        self.player_color = player_color
        self.ai_color = 'black' if player_color == 'white' else 'white'
        self.skill_level = skill_level
        self.theme = theme
        
        try:
            self.engine = StockfishWrapper(skill_level=skill_level)
        except RuntimeError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось инициализировать игру: {e}")
        
        # Инициализация Pygame UI
        try:
            # Инициализируем pygame если ещё не инициализирован
            if not pygame.get_init():
                pygame.init()
            
            self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
            pygame.display.set_caption(f"♟️  chess_stockfish — Maestro7IT (уровень {skill_level})")
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось инициализировать графический интерфейс: {e}")
        
        # Создаём рендерер (шрифты инициализируются автоматически)
        self.renderer = BoardRenderer(self.screen, player_color)
        self.renderer.set_theme(theme)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Инициализируем шрифты для UI панели
        self._init_ui_fonts()
        
        # Образовательные компоненты
        self.educator = ChessEducator()
        
        # Состояние игры
        self.move_history = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.ai_move_delay = 0.7  # Задержка перед ходом ИИ для реалистичности
        self.move_feedback = ""  # Feedback message for the player
        self.move_feedback_time = 0
        self.frame_count = 0  # Счетчик кадров для очистки временных поверхностей
        self.highlight_hint = None  # For T key hint highlighting
        
        # Улучшенная система кэширования
        self._cache = {
            'board_state': None,
            'board_fen': None,
            'valid_moves': {},  # Кэш для допустимых ходов
            'uci_conversions': {},  # Кэш для преобразований координат
            'last_evaluation': None,
            'last_eval_fen': None
        }
        
        # Оптимизация рендеринга
        self.last_ui_update = 0
        self.ui_update_interval = 1.0/30  # 30 FPS для UI
    
    def _init_ui_fonts(self):
        """Инициализация шрифтов для UI элементов."""
        try:
            self.ui_font = pygame.font.SysFont('Arial', 14)
            self.ui_font_small = pygame.font.SysFont('Arial', 12)
        except Exception as e:
            print(f"⚠️  Не удалось загрузить шрифты UI: {e}")
            self.ui_font = pygame.font.Font(None, 14)
            self.ui_font_small = pygame.font.Font(None, 12)
    
    def _coord_to_fen_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """
        Преобразует экранные координаты клика в FEN координаты.
        Использует новый метод coord_mapper из BoardRenderer.
        
        Параметры:
            x (int): X координата клика
            y (int): Y координата клика
            
        Возвращает:
            Tuple: (row, col) в FEN или None если клик вне доски
        """
        return self.renderer.coord_mapper.pixel_to_square(x, y)
    
    def _fen_square_to_uci(self, row: int, col: int) -> str:
        """
        Преобразует FEN координаты в UCI формат с кэшированием.
        
        Параметры:
            row (int): Ряд (0-7)
            col (int): Колонна (0-7)
            
        Возвращает:
            str: Координата в UCI формате (например, 'e4')
        """
        # Кэширование для улучшения производительности
        if not hasattr(self, '_uci_cache'):
            self._uci_cache = {}
        
        cache_key = (row, col)
        if cache_key in self._uci_cache:
            return self._uci_cache[cache_key]
        
        uci = chr(ord('a') + col) + str(8 - row)
        self._uci_cache[cache_key] = uci
        return uci
    
    def get_board_state(self):
        """
        Получение состояния доски с кэшированием.
        
        Возвращает:
            List[List[Optional[str]]]: Состояние доски
        """
        try:
            current_fen = self.engine.get_fen()
            if self._cache['board_fen'] == current_fen and self._cache['board_state'] is not None:
                return self._cache['board_state']
                
            board = self.engine.get_board_state()
            self._cache['board_state'] = board
            self._cache['board_fen'] = current_fen
            return board
        except Exception:
            # Возвращаем пустую доску в случае ошибки
            return [[None for _ in range(8)] for _ in range(8)]
    
    def get_cached_evaluation(self):
        """
        Получение кэшированной оценки позиции.
        
        Возвращает:
            float: Оценка позиции
        """
        try:
            current_fen = self.engine.get_fen()
            if self._cache['last_eval_fen'] == current_fen and self._cache['last_evaluation'] is not None:
                return self._cache['last_evaluation']
                
            evaluation = self.engine.get_evaluation()
            self._cache['last_evaluation'] = evaluation
            self._cache['last_eval_fen'] = current_fen
            return evaluation
        except Exception:
            return None
    
    def _get_pawn_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для пешки."""
        moves = []
        is_white = piece.isupper()
        
        # Направление движения
        direction = -1 if is_white else 1
        
        # Ход вперед на одну клетку
        new_row = row + direction
        if 0 <= new_row < 8 and board[new_row][col] is None:
            moves.append((new_row, col))
            
            # Ход вперед на две клетки с начальной позиции
            start_row = 6 if is_white else 1
            if row == start_row:
                new_row_2 = row + 2 * direction
                if 0 <= new_row_2 < 8 and board[new_row][col] is None and board[new_row_2][col] is None:
                    moves.append((new_row_2, col))
        
        # Взятие по диагонали
        for dc in [-1, 1]:
            new_col = col + dc
            new_row = row + direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is not None and ((is_white and target.islower()) or (not is_white and target.isupper())):
                    moves.append((new_row, new_col))
                    
        return moves

    def _get_knight_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для коня."""
        moves = []
        is_white = piece.isupper()
        
        # Все возможные ходы коня
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or ((is_white and target.islower()) or (not is_white and target.isupper())):
                    moves.append((new_row, new_col))
                    
        return moves

    def _get_bishop_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для слона."""
        moves = []
        is_white = piece.isupper()
        
        # Диагональные направления
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                else:
                    if (is_white and target.islower()) or (not is_white and target.isupper()):
                        moves.append((new_row, new_col))
                    break
                new_row += dr
                new_col += dc
                    
        return moves

    def _get_rook_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для ладьи."""
        moves = []
        is_white = piece.isupper()
        
        # Горизонтальные и вертикальные направления
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                else:
                    if (is_white and target.islower()) or (not is_white and target.isupper()):
                        moves.append((new_row, new_col))
                    break
                new_row += dr
                new_col += dc
                    
        return moves

    def _get_queen_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для ферзя."""
        # Ферзь = слон + ладья
        bishop_moves = self._get_bishop_moves(row, col, piece, board)
        rook_moves = self._get_rook_moves(row, col, piece, board)
        return bishop_moves + rook_moves

    def _get_king_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для короля."""
        moves = []
        is_white = piece.isupper()
        
        # Все направления для короля
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or ((is_white and target.islower()) or (not is_white and target.isupper())):
                    moves.append((new_row, new_col))
                    
        return moves

    def _get_valid_moves(self, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """
        Получить список допустимых ходов для фигуры на заданной позиции.
        Оптимизированная версия с использованием правил движения фигур.
        
        Параметры:
            from_row (int): Ряд фигуры
            from_col (int): Колонна фигуры
            
        Возвращает:
            List[Tuple[int, int]]: Список допустимых позиций для хода
        """
        valid_moves = []
        from_uci = self._fen_square_to_uci(from_row, from_col)
        
        try:
            board_state = self.get_board_state()
            # Ensure board_state is of the correct type
            if not isinstance(board_state, list) or len(board_state) != 8:
                # Fallback to engine's board state if our cache has issues
                board_state = self.engine.get_board_state()
            
            # Convert to proper type if needed
            if isinstance(board_state, list) and len(board_state) == 8:
                # Ensure each row is properly typed
                typed_board: List[List[Optional[str]]] = []
                for row in board_state:
                    if isinstance(row, list) and len(row) == 8:
                        typed_row: List[Optional[str]] = []
                        for cell in row:
                            if cell is None or isinstance(cell, str):
                                typed_row.append(cell)
                            else:
                                typed_row.append(None)
                        typed_board.append(typed_row)
                    else:
                        # Fallback to engine's board state if there are issues
                        board_state = self.engine.get_board_state()
                        typed_board = board_state
                        break
            else:
                # Fallback to engine's board state if there are issues
                board_state = self.engine.get_board_state()
                typed_board = board_state
            
            piece = typed_board[from_row][from_col]
            if not piece:
                return valid_moves
                
            piece_lower = piece.lower()
            
            # Оптимизация: генерируем только возможные ходы для каждой фигуры
            if piece_lower == 'p':  # Пешка
                candidate_moves = self._get_pawn_moves(from_row, from_col, piece, typed_board)
            elif piece_lower == 'n':  # Конь
                candidate_moves = self._get_knight_moves(from_row, from_col, piece, typed_board)
            elif piece_lower == 'b':  # Слон
                candidate_moves = self._get_bishop_moves(from_row, from_col, piece, typed_board)
            elif piece_lower == 'r':  # Ладья
                candidate_moves = self._get_rook_moves(from_row, from_col, piece, typed_board)
            elif piece_lower == 'q':  # Ферзь
                candidate_moves = self._get_queen_moves(from_row, from_col, piece, typed_board)
            elif piece_lower == 'k':  # Король
                candidate_moves = self._get_king_moves(from_row, from_col, piece, typed_board)
            else:
                candidate_moves = []
                
            # Проверяем допустимость ходов через движок
            for to_row, to_col in candidate_moves:
                to_uci = self._fen_square_to_uci(to_row, to_col)
                uci_move = from_uci + to_uci
                if self.engine.is_move_correct(uci_move):
                    valid_moves.append((to_row, to_col))
                    
        except Exception as e:
            print(f"Ошибка при расчете допустимых ходов: {e}")
            
        return valid_moves

    def _is_path_blocked(self, from_row: int, from_col: int, to_row: int, to_col: int, board: List[List[Optional[str]]]) -> bool:
        """
        Проверить, заблокирован ли путь между двумя клетками.
        
        Параметры:
            from_row (int): Исходный ряд
            from_col (int): Исходная колонна
            to_row (int): Целевой ряд
            to_col (int): Целевая колонна
            board (List[List[Optional[str]]]): Состояние доски
            
        Возвращает:
            bool: True если путь заблокирован, False если свободен
        """
        # Determine direction
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        # Check each square along the path (excluding start and end)
        current_row, current_col = from_row + row_step, from_col + col_step
        while current_row != to_row or current_col != to_col:
            if board[current_row][current_col] is not None:
                return True  # Path is blocked
            current_row += row_step
            current_col += col_step
        
        return False  # Path is clear
    
    def _get_move_hint(self, from_row: int, from_col: int, to_row: int, to_col: int) -> str:
        """
        Получить подсказку о причине недопустимости хода.
        
        Параметры:
            from_row (int): Исходный ряд
            from_col (int): Исходная колонна
            to_row (int): Целевой ряд
            to_col (int): Целевая колонна
            
        Возвращает:
            str: Подсказка о причине недопустимости хода
        """
        try:
            # Оптимизация: кэшируем доску, чтобы не запрашивать её несколько раз
            if not hasattr(self, '_cached_board'):
                self._cached_board = self.engine.get_board_state()
            board = self._cached_board
            
            piece = board[from_row][from_col]
            
            if not piece:
                return "Нет фигуры на этой клетке"
            
            # Оптимизация: кэшируем имена фигур
            if not hasattr(self, '_piece_name_cache'):
                self._piece_name_cache = {
                    'P': 'белая пешка', 'N': 'белый конь', 'B': 'белый слон', 
                    'R': 'белая ладья', 'Q': 'белый ферзь', 'K': 'белый король',
                    'p': 'чёрная пешка', 'n': 'чёрный конь', 'b': 'чёрный слон', 
                    'r': 'чёрная ладья', 'q': 'чёрный ферзь', 'k': 'чёрный король'
                }
            piece_name = self._piece_name_cache.get(piece, piece)
            
            # Special hints for pawns
            piece_lower = piece.lower()
            if piece_lower == 'p':
                # Check if it's a pawn trying to move two squares from non-starting position
                if abs(from_row - to_row) == 2:
                    # White pawn starting position is row 6 in FEN (rank 2)
                    # Black pawn starting position is row 1 in FEN (rank 7)
                    is_white = piece.isupper()
                    is_starting_position = (is_white and from_row == 6) or (not is_white and from_row == 1)
                    
                    if not is_starting_position:
                        return f"{piece_name} может двигаться на две клетки только со стартовой позиции"
                
                # Check if moving backward
                is_white = piece.isupper()
                moving_forward = (is_white and to_row < from_row) or (not is_white and to_row > from_row)
                
                if not moving_forward:
                    return f"{piece_name} может двигаться только вперёд"
                
                # Check if trying to capture forward (pawns capture diagonally)
                if from_col == to_col and board[to_row][to_col] is not None:
                    return f"{piece_name} не может взять фигуру, двигаясь вперёд. Пешки берут по диагонали!"
                
                # Check if trying to move diagonally without capturing
                if from_col != to_col and board[to_row][to_col] is None:
                    return f"{piece_name} может двигаться по диагонали только для взятия фигуры"
            
            # Special hints for other pieces
            elif piece_lower == 'n':  # Knight
                # Knights move in L-shape, check if the move is valid for a knight
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
                    return f"{piece_name} ходит буквой Г (две клетки в одном направлении и одна в перпендикулярном)"
            
            elif piece_lower == 'b':  # Bishop
                # Bishops move diagonally, check if the move is diagonal
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if row_diff != col_diff:
                    return f"{piece_name} ходит только по диагонали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'r':  # Rook
                # Rooks move horizontally or vertically
                if from_row != to_row and from_col != to_col:
                    return f"{piece_name} ходит только по горизонтали или вертикали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'q':  # Queen
                # Queens move like bishops or rooks
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                
                # Not diagonal, horizontal, or vertical
                if not ((from_row == to_row) or (from_col == to_col) or (row_diff == col_diff)):
                    return f"{piece_name} ходит по горизонтали, вертикали или диагонали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'k':  # King
                # Kings move one square in any direction
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if row_diff > 1 or col_diff > 1:
                    return f"{piece_name} ходит только на одну клетку в любом направлении"
                
                # Special hint for castling
                if row_diff == 0 and col_diff == 2:
                    return f"Рокировка возможна только из начальной позиции и при определённых условиях"
            
            # Check if trying to capture own piece
            target_piece = board[to_row][to_col]
            if target_piece and ((piece.isupper() and target_piece.isupper()) or 
                               (piece.islower() and target_piece.islower())):
                return f"{piece_name} не может взять свою же фигуру"
            
            return f"Недопустимый ход для {piece_name}"
        except Exception as e:
            print(f"Ошибка при получении подсказки: {e}")
            return "Недопустимый ход"

    def _is_player_turn(self) -> bool:
        """
        Проверяет, является ли текущий ход ходом игрока.
        
        Возвращает:
            bool: True если ход игрока, False если ход компьютера
        """
        try:
            side = self.engine.get_side_to_move()
            return (
                (self.player_color == 'white' and side == 'w') or
                (self.player_color == 'black' and side == 'b')
            )
        except Exception:
            # Если не удалось получить сторону, предполагаем, что ход игрока
            return True
    
    def _is_player_piece(self, piece: Optional[str]) -> bool:
        """
        Проверяет, принадлежит ли фигура игроку.
        
        Параметры:
            piece (str): Символ фигуры
            
        Возвращает:
            bool: True если фигура принадлежит игроку
        """
        if not piece:
            return False
        is_white = piece.isupper()
        return (self.player_color == 'white') == is_white

    def handle_click(self, x: int, y: int):
        """
        Обработка клика по доске для выбора и перемещения фигур.
        
        Параметры:
            x (int): X координата клика
            y (int): Y координата клика
        """
        if self.game_over or self.thinking or not self._is_player_turn():
            return
        
        coords = self._coord_to_fen_square(x, y)
        if coords is None:
            # Клик вне доски - очищаем выделение и подсказки
            self.renderer.set_selected(None)
            self.renderer.set_move_hints([])
            return
        
        row, col = coords
        # Очистка кэша доски перед получением нового состояния
        if hasattr(self, '_cached_board'):
            delattr(self, '_cached_board')
        try:
            board = self.engine.get_board_state()
        except Exception as e:
            print(f"⚠️  Ошибка при получении состояния доски: {e}")
            return
        
        piece = board[row][col]
        
        # Выбор фигуры
        if self._is_player_piece(piece) and piece is not None:
            self.renderer.set_selected((row, col))
            # Показываем подсказки возможных ходов
            valid_moves = self._get_valid_moves(row, col)
            self.renderer.set_move_hints(valid_moves)
            # Provide feedback about the selected piece
            piece_name = {
                'P': 'пешка', 'N': 'конь', 'B': 'слон', 'R': 'ладья', 
                'Q': 'ферзь', 'K': 'король', 'p': 'пешка', 'n': 'конь', 
                'b': 'слон', 'r': 'ладья', 'q': 'ферзь', 'k': 'король'
            }.get(piece, piece)
            self.move_feedback = f"Выбрана {piece_name}"
            self.move_feedback_time = time.time()
            
            # Add educational hint about the piece
            piece_hint = self.educator.get_piece_hint(piece_name)
            self.move_feedback += f" | {piece_hint}"
        # Перемещение выбранной фигуры
        elif self.renderer.selected_square:
            from_sq = self.renderer.selected_square
            to_sq = (row, col)
            
            from_uci = self._fen_square_to_uci(*from_sq)
            to_uci = self._fen_square_to_uci(*to_sq)
            uci_move = from_uci + to_uci
            
            print(f"Попытка хода: {uci_move} (из {from_sq} в {to_sq})")
            
            try:
                # Validate the move using our improved method
                if self.engine.is_move_correct(uci_move):
                    # Make the move and verify it was successful
                    if self.engine.make_move(uci_move):
                        self.move_history.append(uci_move)
                        self.renderer.set_last_move(from_sq, to_sq)
                        self.renderer.set_selected(None)
                        self.renderer.set_move_hints([])
                        self.last_move_time = time.time()
                        print(f"Ход выполнен: {uci_move}")
                        self.move_feedback = f"Ход {uci_move} выполнен"
                        self.move_feedback_time = time.time()
                        
                        # Add educational feedback
                        educational_tip = self.educator.get_educational_feedback(
                            len(self.move_history), time.time())
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = time.time()
                    else:
                        print("❌ Не удалось выполнить ход")
                        self.renderer.set_selected(None)
                        self.renderer.set_move_hints([])
                        self.move_feedback = "Не удалось выполнить ход"
                        self.move_feedback_time = time.time()
                else:
                    print(f"❌ Некорректный ход: {uci_move}")
                    self.renderer.set_selected(None)
                    self.renderer.set_move_hints([])
                    # Provide specific feedback about why the move is invalid
                    hint = self._get_move_hint(from_sq[0], from_sq[1], row, col)
                    self.move_feedback = hint
                    self.move_feedback_time = time.time()
            except Exception as e:
                print(f"⚠️  Ошибка при обработке хода: {e}")
                self.renderer.set_selected(None)
                self.renderer.set_move_hints([])
                self.move_feedback = "Ошибка при выполнении хода"
                self.move_feedback_time = time.time()
        else:
            # Клик по пустой клетке без выбранной фигуры - очищаем выделение
            self.renderer.set_selected(None)
            self.renderer.set_move_hints([])
    
    def handle_ai_move(self):
        """
        Получить и выполнить ход ИИ (Stockfish).
        
        Добавляет реалистичную задержку перед ходом.
        """
        if self._is_player_turn() or self.game_over or self.thinking:
            return
        
        # Задержка для более реалистичной игры
        if time.time() - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        try:
            # Get the best move with appropriate depth based on skill level
            depth = max(1, min(20, self.skill_level + 5))  # Limit depth between 1 and 20
            
            # Try to get multiple move options for better decision making
            ai_move = None
            best_moves = self.engine.get_best_moves(3)
            
            # If we have multiple options, try to choose a more interesting move
            if len(best_moves) > 1 and self.skill_level < 15:
                # For lower skill levels, sometimes choose a suboptimal but more interesting move
                if random.random() < 0.3:  # 30% chance to choose a different move
                    ai_move = best_moves[min(1, len(best_moves) - 1)]  # Choose second best
                else:
                    ai_move = best_moves[0]  # Choose best move
            else:
                # For higher skill levels or when only one move is available
                ai_move = self.engine.get_best_move(depth=depth)
            
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                # Validate the move before making it
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        self.move_history.append(ai_move)
                        
                        # Очистка кэша доски после хода
                        if hasattr(self, '_cached_board'):
                            delattr(self, '_cached_board')
                        
                        # Преобразование UCI хода в координаты для выделения
                        from_col = ord(ai_move[0]) - ord('a')
                        from_row = 8 - int(ai_move[1])
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
                        self.last_move_time = time.time()
                        print(f"Ход компьютера выполнен: {ai_move}")
                        self.move_feedback = f"Ход компьютера: {ai_move}"
                        self.move_feedback_time = time.time()
                        
                        # Add general educational feedback
                        educational_tip = self.educator.get_educational_feedback(
                            len(self.move_history), time.time())
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = time.time()
                        
                        # Add educational feedback for interesting moves
                        if len(best_moves) > 1 and ai_move != best_moves[0]:
                            self.move_feedback += " (интересный выбор!)"
                    else:
                        print("⚠️  Не удалось выполнить ход компьютера")
                        self.move_feedback = "Не удалось выполнить ход компьютера"
                        self.move_feedback_time = time.time()
                else:
                    print("⚠️  Компьютер предложил некорректный ход")
                    self.move_feedback = "Компьютер предложил некорректный ход"
                    self.move_feedback_time = time.time()
            else:
                print("⚠️  Компьютер не смог найти ход")
                self.move_feedback = "Компьютер не смог найти ход"
                self.move_feedback_time = time.time()
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
            self.move_feedback = "Ошибка при получении хода компьютера"
            self.move_feedback_time = time.time()
        finally:
            self.thinking = False
    
    def check_game_state(self) -> bool:
        """
        Проверить текущее состояние игры (мат, пат, конец).
        
        Возвращает:
            bool: True если игра завершена
        """
        try:
            is_over, reason = self.engine.is_game_over()
            if is_over:
                self.game_over = True
                self.game_over_reason = reason
                self.move_feedback = reason
                self.move_feedback_time = time.time()
                return True
            
            # Check for check state for educational purposes
            # Get raw evaluation from engine (not the processed float version)
            try:
                if self.engine.engine is not None:
                    eval_score = self.engine.engine.get_evaluation()
                    if eval_score and isinstance(eval_score, dict) and eval_score.get('type') == 'mate':
                        mate_in = eval_score.get('value', 0)
                        side = self.engine.get_side_to_move()
                        if mate_in > 0:  # Mate in N moves
                            if (side == 'w' and self.player_color == 'white') or (side == 'b' and self.player_color == 'black'):
                                self.move_feedback = f"⚠️  Вам поставлен мат в {mate_in} ходов!"
                            else:
                                self.move_feedback = f"✅  Вы поставили мат в {mate_in} ходов!"
                            self.move_feedback_time = time.time()
                        elif mate_in < 0:  # Mate in N moves for opponent
                            mate_in = abs(mate_in)
                            if (side == 'w' and self.player_color == 'white') or (side == 'b' and self.player_color == 'black'):
                                self.move_feedback = f"✅  Вы поставите мат в {mate_in} ходов!"
                            else:
                                self.move_feedback = f"⚠️  Вам поставят мат в {mate_in} ходов!"
                            self.move_feedback_time = time.time()
            except Exception:
                # Ignore errors in mate detection, it's just for educational purposes
                pass
        except Exception as e:
            print(f"⚠️  Ошибка при проверке состояния игры: {e}")
        return False
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса (информационная полоса внизу)."""
        try:
            # Информационная панель внизу экрана
            info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
            pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
            pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), 
                           (BOARD_SIZE, BOARD_SIZE), 2)
            
            if self.game_over:
                # Экран окончания игры
                if self.game_over_reason:
                    text = self.ui_font.render(self.game_over_reason, True, (255, 100, 100))
                    self.screen.blit(text, (20, BOARD_SIZE + 15))
                restart_text = self.ui_font.render("Нажмите 'R' для новой игры", 
                                                   True, (200, 200, 200))
                self.screen.blit(restart_text, (20, BOARD_SIZE + 50))
            else:
                # Статус хода
                if self._is_player_turn():
                    status = "🎮 Ваш ход"
                    status_color = (100, 255, 100)
                else:
                    status = "🤖 Ход компьютера"
                    status_color = (100, 150, 255)
                
                text = self.ui_font.render(status, True, status_color)
                self.screen.blit(text, (20, BOARD_SIZE + 15))
                
                # Информация о ходах
                moves_text = self.ui_font.render(f"Ходов: {len(self.move_history)}", 
                                                True, (200, 200, 200))
                self.screen.blit(moves_text, (20, BOARD_SIZE + 50))
                
                # Уровень сложности
                level_text = self.ui_font.render(f"Уровень: {self.skill_level}/20", 
                                                True, (200, 200, 200))
                self.screen.blit(level_text, (BOARD_SIZE - 150, BOARD_SIZE + 15))
                
                # Подсказка
                hint_text = self.ui_font_small.render(
                    "Подсказка: Кликните по фигуре для показа возможных ходов | Нажмите 'T' для совета", 
                    True, (150, 150, 150))
                self.screen.blit(hint_text, (20, BOARD_SIZE + 75))
                
                # Move feedback (show for 3 seconds)
                if self.move_feedback and time.time() - self.move_feedback_time < 3:
                    feedback_color = (255, 255, 100)  # Yellow feedback
                    feedback_text = self.ui_font.render(self.move_feedback, True, feedback_color)
                    self.screen.blit(feedback_text, 
                                   (BOARD_SIZE // 2 - feedback_text.get_width() // 2, 
                                    BOARD_SIZE + 30))
        except Exception as e:
            print(f"⚠️  Ошибка при отрисовке интерфейса: {e}")
    
    def get_game_stats(self) -> dict:
        """
        Получить статистику текущей игры.
        
        Возвращает:
            dict: Словарь со статистикой игры
        """
        try:
            return {
                'player_color': self.player_color,
                'ai_color': self.ai_color,
                'skill_level': self.skill_level,
                'total_moves': len(self.move_history),
                'move_history': self.move_history.copy(),
                'fen': self.engine.get_fen(),
                'game_over': self.game_over,
                'game_reason': self.game_over_reason
            }
        except Exception as e:
            print(f"⚠️  Ошибка при получении статистики игры: {e}")
            return {
                'player_color': self.player_color,
                'ai_color': self.ai_color,
                'skill_level': self.skill_level,
                'total_moves': len(self.move_history),
                'move_history': self.move_history.copy(),
                'fen': '',
                'game_over': self.game_over,
                'game_reason': self.game_over_reason
            }
    
    def _clear_caches(self):
        """Очистить кэши для оптимизации памяти."""
        if hasattr(self, '_uci_cache'):
            self._uci_cache.clear()
        if hasattr(self, '_cached_board'):
            delattr(self, '_cached_board')
        if hasattr(self, '_piece_name_cache'):
            self._piece_name_cache.clear()
    
    def reset_game(self):
        """Сбросить игру к начальному состоянию."""
        print("🔄 Новая игра...")
        
        # Reset the engine to initial position
        self.engine.reset_board()
        
        # Reset game state
        self.move_history = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.move_feedback = ""
        self.move_feedback_time = 0
        self.highlight_hint = None
        
        # Reset renderer state
        self.renderer.set_selected(None)
        # For set_last_move, we need to pass valid tuples or avoid calling it with None
        # We'll just reset the last_move attribute directly
        self.renderer.last_move = None
        self.renderer.set_move_hints([])
        self.renderer.set_check(None)
        
        print("[INFO] Игра сброшена до начальной позиции")
    
    def run(self):
        """
        Запустить основной цикл игры.
        
        Обрабатывает события, обновляет состояние и отрисовывает кадры.
        """
        print(f"\n{'='*60}")
        print(f"🎮 Игра началась!")
        print(f"   Вы играете: {self.player_color.upper()}")
        print(f"   Компьютер: {self.ai_color.upper()}")
        print(f"   Уровень: {self.skill_level}/20")
        print(f"   Горячие клавиши: R - новая игра, ESC - выход, T - подсказка")
        print(f"{'='*60}\n")
        
        running = True

        while running:
            # === Обработка событий ===
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # Сброс игры
                    if event.key == pygame.K_r:
                        self.reset_game()
                    # Подсказка (ход Stockfish)
                    elif event.key == pygame.K_t:
                        if not self.game_over and self._is_player_turn():
                            self.thinking = True
                            # Get best move from engine
                            best_move = self.engine.get_best_move()
                            self.thinking = False
                            if best_move:
                                print(f"[ENGINE] Совет: {best_move}")
                                self.highlight_hint = best_move
                                # Show hint for 3 seconds
                                self.move_feedback = f"Подсказка: {best_move}"
                                self.move_feedback_time = time.time()
                                # Highlight the suggested move on the board
                                if len(best_move) >= 4:
                                    try:
                                        # Convert UCI move to board coordinates for highlighting
                                        from_col = ord(best_move[0]) - ord('a')
                                        from_row = 8 - int(best_move[1])
                                        to_col = ord(best_move[2]) - ord('a')
                                        to_row = 8 - int(best_move[3])
                                        # Store the hint move for visual highlighting
                                        self.highlight_hint = ((from_row, from_col), (to_row, to_col))
                                    except Exception as e:
                                        print(f"Ошибка при обработке подсказки: {e}")
                            else:
                                self.move_feedback = "Не удалось получить подсказку"
                                self.move_feedback_time = time.time()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ
                        pos = pygame.mouse.get_pos()
                        self.handle_click(pos[0], pos[1])

            # === Обновление и отрисовка ===
            # Get current board state for rendering
            board_state = self.engine.get_board_state()
            
            # Get evaluation for info panel
            evaluation = self.engine.get_evaluation()
            
            # Update hover square
            mouse_pos = pygame.mouse.get_pos()
            self.renderer.update_hover(mouse_pos)
            
            # Draw the board
            self.renderer.draw(board_state, evaluation=evaluation, thinking=self.thinking, mouse_pos=mouse_pos)
            
            # Draw UI panel at bottom
            self.draw_ui()
            
            # Handle AI moves
            if not self.game_over:
                self.handle_ai_move()
                self.check_game_state()

            # === Очистка кэша для предотвращения утечек памяти ===
            self.frame_count += 1
            if self.frame_count % 3600 == 0:  # Every minute at 60 FPS
                self.renderer.clear_temp_surfaces()
                self._clear_caches()

            # === Обновление экрана ===
            pygame.display.flip()

            # === Ограничение FPS ===
            self.clock.tick(60)

        # === Завершение работы ===
        self.renderer.cleanup()
        pygame.quit()

        # === Возврат статистики ===
        print("[INFO] Игра завершена.")
        return self.get_game_stats()