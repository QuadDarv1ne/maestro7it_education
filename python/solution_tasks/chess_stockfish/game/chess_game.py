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

# Import our modules
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer  # Убран init_fonts

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
        
        # Состояние игры
        self.move_history = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.ai_move_delay = 0.7  # Задержка перед ходом ИИ для реалистичности
        self.move_feedback = ""  # Feedback message for the player
        self.move_feedback_time = 0
    
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
        Преобразует FEN координаты в UCI формат.
        
        Параметры:
            row (int): Ряд (0-7)
            col (int): Колонна (0-7)
            
        Возвращает:
            str: Координата в UCI формате (например, 'e4')
        """
        return chr(ord('a') + col) + str(8 - row)
    
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
    
    def _get_valid_moves(self, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """
        Получить список допустимых ходов для фигуры на заданной позиции.
        
        Параметры:
            from_row (int): Ряд фигуры
            from_col (int): Колонна фигуры
            
        Возвращает:
            List[Tuple[int, int]]: Список допустимых позиций для хода
        """
        valid_moves = []
        from_uci = self._fen_square_to_uci(from_row, from_col)
        
        # Для каждой возможной целевой позиции проверяем допустимость хода
        for to_row in range(8):
            for to_col in range(8):
                to_uci = self._fen_square_to_uci(to_row, to_col)
                uci_move = from_uci + to_uci
                if self.engine.is_move_correct(uci_move):
                    valid_moves.append((to_row, to_col))
        
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
            board = self.engine.get_board_state()
            piece = board[from_row][from_col]
            
            if not piece:
                return "Нет фигуры на этой клетке"
            
            piece_name = {
                'P': 'белая пешка', 'N': 'белый конь', 'B': 'белый слон', 
                'R': 'белая ладья', 'Q': 'белый ферзь', 'K': 'белый король',
                'p': 'чёрная пешка', 'n': 'чёрный конь', 'b': 'чёрный слон', 
                'r': 'чёрная ладья', 'q': 'чёрный ферзь', 'k': 'чёрный король'
            }.get(piece, piece)
            
            # Special hints for pawns
            if piece.lower() == 'p':
                from_uci = self._fen_square_to_uci(from_row, from_col)
                to_uci = self._fen_square_to_uci(to_row, to_col)
                uci_move = from_uci + to_uci
                
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
            elif piece.lower() == 'n':  # Knight
                # Knights move in L-shape, check if the move is valid for a knight
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
                    return f"{piece_name} ходит буквой Г (две клетки в одном направлении и одна в перпендикулярном)"
            
            elif piece.lower() == 'b':  # Bishop
                # Bishops move diagonally, check if the move is diagonal
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if row_diff != col_diff:
                    return f"{piece_name} ходит только по диагонали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece.lower() == 'r':  # Rook
                # Rooks move horizontally or vertically
                if from_row != to_row and from_col != to_col:
                    return f"{piece_name} ходит только по горизонтали или вертикали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece.lower() == 'q':  # Queen
                # Queens move like bishops or rooks
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                
                # Not diagonal, horizontal, or vertical
                if not ((from_row == to_row) or (from_col == to_col) or (row_diff == col_diff)):
                    return f"{piece_name} ходит по горизонтали, вертикали или диагонали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece.lower() == 'k':  # King
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
                import random
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
                    "Подсказка: Кликните по фигуре для показа возможных ходов", 
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
    
    def reset_game(self):
        """Сбросить игру к начальному состоянию."""
        print("🔄 Новая игра...")
        # Сохраняем статистику перед сбросом
        try:
            stats = self.get_game_stats()
            # Здесь можно сохранить статистику, если нужно
        except Exception as e:
            print(f"⚠️  Ошибка при сохранении статистики перед сбросом: {e}")
        
        # Очищаем ресурсы старого рендерера
        if hasattr(self, 'renderer'):
            self.renderer.cleanup()
        
        # Переинициализируем игру с теми же параметрами
        self.__init__(self.player_color, self.skill_level)
    
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
        print(f"   Горячие клавиши: R - новая игра, ESC - выход")
        print(f"{'='*60}\n")
        
        while self.running:
            try:
                mouse_pos = pygame.mouse.get_pos()
                
                # Обработка событий
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        self.handle_click(x, y)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            # Перезагрузка игры
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                
                # Отрисовка
                self.screen.fill((30, 30, 30))  # Dark background for better contrast
                try:
                    board = self.engine.get_board_state()
                    evaluation = self.engine.get_evaluation()
                    self.renderer.draw(board, evaluation, self.thinking, mouse_pos)
                    self.draw_ui()
                    pygame.display.flip()
                except Exception as e:
                    print(f"⚠️  Ошибка при отрисовке: {e}")
                
                # Логика игры
                if not self.game_over:
                    self.check_game_state()
                    self.handle_ai_move()
                
                self.clock.tick(60)
            except Exception as e:
                print(f"⚠️  Критическая ошибка в игровом цикле: {e}")
                # Не завершаем игру полностью, а пытаемся продолжить
                continue
        
        # Очистка при выходе
        try:
            stats = self.get_game_stats()
            print(f"\n{'='*60}")
            print("📊 Статистика игры:")
            print(f"   Всего ходов: {stats['total_moves']}")
            if stats['game_reason']:
                print(f"   Результат: {stats['game_reason']}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"⚠️  Ошибка при выводе статистики: {e}")
        
        try:
            if hasattr(self, 'renderer'):
                self.renderer.cleanup()
            self.engine.quit()
        except Exception as e:
            print(f"⚠️  Ошибка при завершении движка: {e}")
        
        pygame.quit()