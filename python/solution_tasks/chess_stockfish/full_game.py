#!/usr/bin/env python3
"""
chess_stockfish — Полнофункциональная шахматная игра со Stockfish

Описание:
    Интерактивная шахматная игра с использованием движка Stockfish.
    Игрок может выбрать сторону (белые/чёрные) и уровень сложности (0-20).
    Все компоненты интегрированы в один файл для простоты развёртывания.
    
Требования:
    - pygame: Визуализация и UI
    - stockfish: Шахматный движок
    
Установка зависимостей:
    pip install pygame stockfish
    
Установка Stockfish:
    Windows: https://stockfishchess.org/download/
    Linux: sudo apt-get install stockfish
    macOS: brew install stockfish
    
Запуск:
    python main.py

Автор: Maestro7IT Education
Лицензия: MIT
"""

import pygame
from typing import Optional, Tuple, List
import time
import os
from stockfish import Stockfish


# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

# Цветовая схема доски
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_COLOR = (124, 252, 0, 180)
LAST_MOVE_COLOR = (205, 210, 106, 150)
CHECK_COLOR = (255, 0, 0, 180)

# Initialize fonts after pygame.init() is called
FONT = None
SMALL_FONT = None

def init_fonts():
    """Initialize fonts after pygame is initialized."""
    global FONT, SMALL_FONT
    try:
        FONT = pygame.font.SysFont('Segoe UI Symbol', SQUARE_SIZE - 10)
        SMALL_FONT = pygame.font.SysFont('Arial', 14)
    except Exception:
        FONT = pygame.font.SysFont('Arial', SQUARE_SIZE - 10)
        SMALL_FONT = pygame.font.SysFont('Arial', 14)

# Unicode символы фигур
PIECE_UNICODE = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}


# ============================================================================
# engine/stockfish_wrapper.py
# ============================================================================

"""
Модуль: engine/stockfish_wrapper.py

Описание:
    Содержит класс StockfishWrapper для удобной работы с шахматным движком Stockfish.
    Обеспечивает функции для:
    - Получения ходов и лучших ходов
    - Проверки корректности ходов
    - Анализа позиций и оценки
    - Управления уровнем сложности
    - Обработки исключений и ошибок
"""


class StockfishWrapper:
    """
    Обёртка для работы со Stockfish с улучшенной обработкой ошибок.
    
    Атрибуты:
        engine (Stockfish): Экземпляр движка Stockfish
        skill_level (int): Уровень сложности (0-20)
        depth (int): Глубина анализа
    """
    
    def __init__(self, skill_level=5, depth=15, path=None):
        """
        Инициализация Stockfish движка.
        
        Параметры:
            skill_level (int): Уровень сложности (0-20), по умолчанию 5
            depth (int): Глубина анализа, по умолчанию 15
            path (str): Путь к исполняемому файлу Stockfish (если None, ищет в PATH)
            
        Исключения:
            RuntimeError: Если не удалось запустить Stockfish
        """
        self.skill_level = max(0, min(20, skill_level))
        self.depth = depth
        self.move_count = 0
        
        try:
            if path is not None:
                self.engine = Stockfish(path=path)
            else:
                self.engine = Stockfish()
            self.engine.set_skill_level(self.skill_level)
            self.engine.set_depth(self.depth)
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось запустить Stockfish: {e}")
    
    def get_board_state(self) -> List[List[Optional[str]]]:
        """
        Возвращает текущее состояние доски (8x8).
        
        Возвращает:
            List[List[Optional[str]]]: 2D массив фигур или None
        """
        fen = self.engine.get_fen_position()
        board_str = fen.split()[0]
        rows = board_str.split('/')
        board = []
        for row in rows:
            new_row = []
            for char in row:
                if char.isdigit():
                    new_row.extend([None] * int(char))
                else:
                    new_row.append(char)
            board.append(new_row)
        return board
    
    def is_move_correct(self, uci_move: str) -> bool:
        """Проверяет, является ли ход корректным в текущей позиции."""
        try:
            return self.engine.is_move_correct(uci_move)
        except Exception:
            return False
    
    def make_move(self, uci_move: str) -> bool:
        """Выполняет ход в текущей позиции."""
        if not self.is_move_correct(uci_move):
            return False
        try:
            self.engine.make_moves_from_current_position([uci_move])
            self.move_count += 1
            return True
        except Exception as e:
            print(f"⚠️  Ошибка при выполнении хода {uci_move}: {e}")
            return False
    
    def get_best_move(self, depth: Optional[int] = None) -> Optional[str]:
        """Получает лучший ход в текущей позиции."""
        try:
            old_depth = None
            if depth:
                old_depth = self.engine.depth
                self.engine.set_depth(depth)
            move = self.engine.get_best_move()
            if depth and old_depth is not None:
                self.engine.set_depth(int(old_depth))
            return move
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода: {e}")
            return None
    
    def get_side_to_move(self) -> str:
        """Получает, чей ход в текущей позиции ('w' или 'b')."""
        return self.engine.get_fen_position().split()[1]
    
    def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """Проверяет, закончена ли игра и причину окончания."""
        try:
            # Use the get_evaluation method to determine game state
            fen = self.engine.get_fen_position()
            board_state = fen.split()[0]
            
            # Check for mate using evaluation
            eval_result = self.engine.get_evaluation()
            if eval_result and eval_result['type'] == 'mate':
                side = self.get_side_to_move()
                winner = "чёрные" if side == 'w' else "белые"
                return True, f"🏆 Шах и мат! Победили {winner}"
            
            # Check for stalemate by seeing if there are any legal moves
            # If evaluation is very low and no legal moves, it's stalemate
            if eval_result and eval_result['type'] == 'cp' and abs(eval_result['value']) < 10000:
                # Try to get a move - if none exists, it's stalemate
                move = self.engine.get_best_move()
                if move is None:
                    return True, "🤝 Пат! Ничья"
            
            # Check for insufficient material
            pieces = [p for p in board_state if p.lower() in 'pnbrqk']
            white_pieces = [p for p in pieces if p.isupper()]
            black_pieces = [p for p in pieces if p.islower()]
            
            # King vs King
            if len(white_pieces) == 1 and len(black_pieces) == 1:
                return True, "🤝 Недостаточно материала для мата. Ничья"
            
            # King + Bishop vs King or King + Knight vs King
            if (len(white_pieces) <= 2 and len(black_pieces) == 1) or (len(white_pieces) == 1 and len(black_pieces) <= 2):
                # Check if the extra pieces are only bishops or knights
                extra_pieces = []
                if len(white_pieces) > 1:
                    extra_pieces.extend([p for p in white_pieces if p.upper() in 'BN'])
                if len(black_pieces) > 1:
                    extra_pieces.extend([p for p in black_pieces if p.upper() in 'BN'])
                
                if len(extra_pieces) <= 1:  # Only one bishop or knight extra
                    return True, "🤝 Недостаточно материала для мата. Ничья"
        except Exception:
            pass
        
        return False, None
    
    def get_fen(self) -> str:
        """Получает текущую позицию в формате FEN."""
        return self.engine.get_fen_position()
    
    def get_evaluation(self) -> Optional[float]:
        """Получает оценку текущей позиции в пешках."""
        try:
            eval_score = self.engine.get_evaluation()
            if eval_score and 'value' in eval_score:
                return eval_score['value'] / 100.0
        except Exception:
            pass
        return None
    
    def reset_board(self):
        """Сбрасывает доску в начальную позицию."""
        try:
            start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            self.engine.set_fen_position(start_fen)
            self.move_count = 0
        except Exception as e:
            print(f"⚠️  Ошибка при сбросе доски: {e}")
    
    def quit(self):
        """Закрывает соединение с Stockfish."""
        # Newer versions of stockfish library don't have quit method
        # The engine will be automatically cleaned up when the object is destroyed
        try:
            # Try to quit if the method exists
            if hasattr(self.engine, 'quit'):
                # self.engine.quit()  # Removed due to compatibility issues
                pass
        except Exception:
            pass


# ============================================================================
# ui/board_renderer.py
# ============================================================================

"""
Модуль: ui/board_renderer.py

Описание:
    Содержит класс BoardRenderer для визуализации шахматной доски в Pygame.
    Отвечает за отображение клеток, фигур, выделений и информации.
"""


class BoardRenderer:
    """
    Класс для отображения шахматной доски и элементов интерфейса.
    
    Атрибуты:
        screen (pygame.Surface): Поверхность для отрисовки
        player_color (str): Сторона, за которую играет игрок
        selected_square (Tuple): Выбранная клетка
        last_move (Tuple): Последний выполненный ход
    """
    
    def __init__(self, screen: pygame.Surface, player_color: str = 'white'):
        """Инициализация рендерера доски."""
        self.screen = screen
        self.player_color = player_color
        self.selected_square = None
        self.last_move = None
        self.check_square = None
        self.show_coords = True
    
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
        """Установить клетку короля в шахе."""
        self.check_square = square
    
    def _fen_to_display(self, row: int, col: int) -> Tuple[int, int]:
        """Преобразует FEN-координаты в экранные координаты."""
        if self.player_color == 'black':
            return 7 - row, 7 - col
        return row, col
    
    def _display_to_fen(self, disp_row: int, disp_col: int) -> Tuple[int, int]:
        """Обратное преобразование: экранные координаты в FEN."""
        if self.player_color == 'black':
            return 7 - disp_row, 7 - disp_col
        return disp_row, disp_col
    
    def draw(self, board_state: List[List[Optional[str]]], 
             evaluation: Optional[float] = None, 
             thinking: bool = False):
        """Отрисовка шахматной доски и всех элементов."""
        for row in range(8):
            for col in range(8):
                disp_row, disp_col = self._fen_to_display(row, col)
                
                # Базовый цвет клетки
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(disp_col * SQUARE_SIZE, disp_row * SQUARE_SIZE, 
                                   SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Выделение последнего хода (жёлтая подсветка)
                if self.last_move:
                    if (row, col) in self.last_move:
                        highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        highlight.fill(LAST_MOVE_COLOR)
                        self.screen.blit(highlight, rect.topleft)
                
                # Выделение выбранной клетки (зелёная подсветка)
                if self.selected_square == (row, col):
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(HIGHLIGHT_COLOR)
                    self.screen.blit(highlight, rect.topleft)
                
                # Выделение шаха (красная подсветка)
                if self.check_square == (row, col):
                    highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight.fill(CHECK_COLOR)
                    self.screen.blit(highlight, rect.topleft)
                
                # Отрисовка фигур
                piece = board_state[row][col]
                if piece and FONT is not None:
                    text_color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
                    try:
                        text = FONT.render(PIECE_UNICODE[piece], True, text_color)
                    except KeyError:
                        text = FONT.render(piece, True, text_color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                
                # Отрисовка координат
                if self.show_coords and SMALL_FONT is not None:
                    if disp_col == 0:
                        rank_text = SMALL_FONT.render(str(8 - row), True, (100, 100, 100))
                        self.screen.blit(rank_text, (disp_col * SQUARE_SIZE + 2, 
                                                     disp_row * SQUARE_SIZE + 2))
                    if disp_row == 7:
                        file_text = SMALL_FONT.render(chr(97 + col), True, (100, 100, 100))
                        self.screen.blit(file_text, (disp_col * SQUARE_SIZE + SQUARE_SIZE - 12, 
                                                     disp_row * SQUARE_SIZE + SQUARE_SIZE - 14))
        
        # Отрисовка информации
        if evaluation is not None and SMALL_FONT is not None:
            eval_text = f"Оценка: {evaluation:+.1f}"
            color = (100, 255, 100) if evaluation > 0 else (255, 100, 100)
            text_surface = SMALL_FONT.render(eval_text, True, color)
            self.screen.blit(text_surface, (10, 10))
        
        if thinking and SMALL_FONT is not None:
            thinking_text = SMALL_FONT.render("⟳ Компьютер думает...", True, (255, 200, 0))
            self.screen.blit(thinking_text, (BOARD_SIZE - 200, 10))


# ============================================================================
# game/chess_game.py
# ============================================================================

"""
Модуль: game/chess_game.py

Описание:
    Содержит главный класс ChessGame, который управляет игровым процессом.
"""


class ChessGame:
    """Главный класс для управления ходом игры."""
    
    def __init__(self, player_color: str = 'white', skill_level: int = 5):
        """Инициализация новой игры."""
        self.player_color = player_color
        self.ai_color = 'black' if player_color == 'white' else 'white'
        self.skill_level = skill_level
        
        try:
            self.engine = StockfishWrapper(skill_level=skill_level)
        except RuntimeError as e:
            raise e
        
        # Инициализация Pygame UI
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
        pygame.display.set_caption(f"♟️  chess_stockfish — Maestro7IT (уровень {skill_level})")
        
        self.renderer = BoardRenderer(self.screen, player_color)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Состояние игры
        self.move_history = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.ai_move_delay = 0.7
    
    def _coord_to_fen_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Преобразует экранные координаты клика в FEN координаты."""
        if y > BOARD_SIZE:
            return None
        disp_row = y // SQUARE_SIZE
        disp_col = x // SQUARE_SIZE
        if disp_row >= 8 or disp_col >= 8:
            return None
        row, col = self.renderer._display_to_fen(disp_row, disp_col)
        return (row, col)
    
    def _fen_square_to_uci(self, row: int, col: int) -> str:
        """Преобразует FEN координаты в UCI формат."""
        return chr(ord('a') + col) + str(8 - row)
    
    def _is_player_turn(self) -> bool:
        """Проверяет, является ли текущий ход ходом игрока."""
        side = self.engine.get_side_to_move()
        return (
            (self.player_color == 'white' and side == 'w') or
            (self.player_color == 'black' and side == 'b')
        )
    
    def _is_player_piece(self, piece: Optional[str]) -> bool:
        """Проверяет, принадлежит ли фигура игроку."""
        if not piece:
            return False
        is_white = piece.isupper()
        return (self.player_color == 'white') == is_white
    
    def handle_click(self, x: int, y: int):
        """Обработка клика по доске."""
        if self.game_over or self.thinking or not self._is_player_turn():
            return
        
        coords = self._coord_to_fen_square(x, y)
        if coords is None:
            return
        
        row, col = coords
        board = self.engine.get_board_state()
        piece = board[row][col]
        
        if self._is_player_piece(piece):
            self.renderer.set_selected((row, col))
        elif self.renderer.selected_square:
            from_sq = self.renderer.selected_square
            to_sq = (row, col)
            
            uci_move = (self._fen_square_to_uci(*from_sq) + 
                       self._fen_square_to_uci(*to_sq))
            
            if self.engine.is_move_correct(uci_move):
                if self.engine.make_move(uci_move):
                    self.move_history.append(uci_move)
                    self.renderer.set_last_move(from_sq, to_sq)
                    self.renderer.clear_selected()
                    self.last_move_time = time.time()
                else:
                    print("❌ Не удалось выполнить ход")
            else:
                self.renderer.clear_selected()
    
    def handle_ai_move(self):
        """Получить и выполнить ход ИИ."""
        if self._is_player_turn() or self.game_over or self.thinking:
            return
        
        if time.time() - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        ai_move = self.engine.get_best_move(depth=self.skill_level + 10)
        self.thinking = False
        
        if ai_move:
            self.engine.make_move(ai_move)
            self.move_history.append(ai_move)
            
            from_col = ord(ai_move[0]) - ord('a')
            from_row = 8 - int(ai_move[1])
            to_col = ord(ai_move[2]) - ord('a')
            to_row = 8 - int(ai_move[3])
            self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
            self.last_move_time = time.time()
    
    def check_game_state(self) -> bool:
        """Проверить текущее состояние игры."""
        is_over, reason = self.engine.is_game_over()
        if is_over:
            self.game_over = True
            self.game_over_reason = reason
            return True
        return False
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса."""
        info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
        pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), (BOARD_SIZE, BOARD_SIZE), 2)
        
        if SMALL_FONT is not None:
            if self.game_over:
                text = SMALL_FONT.render(self.game_over_reason, True, (255, 100, 100))
                self.screen.blit(text, (20, BOARD_SIZE + 15))
                restart_text = SMALL_FONT.render("Нажмите 'R' для новой игры", True, (200, 200, 200))
                self.screen.blit(restart_text, (20, BOARD_SIZE + 50))
            else:
                if self._is_player_turn():
                    status = "🎮 Ваш ход"
                    status_color = (100, 255, 100)
                else:
                    status = "🤖 Ход компьютера"
                    status_color = (100, 150, 255)
                
                text = SMALL_FONT.render(status, True, status_color)
                self.screen.blit(text, (20, BOARD_SIZE + 15))
                
                moves_text = SMALL_FONT.render(f"Ходов: {len(self.move_history)}", True, (200, 200, 200))
                self.screen.blit(moves_text, (20, BOARD_SIZE + 50))
                
                level_text = SMALL_FONT.render(f"Уровень: {self.skill_level}/20", True, (200, 200, 200))
                self.screen.blit(level_text, (BOARD_SIZE - 150, BOARD_SIZE + 15))
    
    def get_game_stats(self) -> dict:
        """Получить статистику текущей игры."""
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
    
    def run(self):
        """Запустить основной цикл игры."""
        print(f"\n{'='*60}")
        print(f"🎮 Игра началась!")
        print(f"   Вы играете: {self.player_color.upper()}")
        print(f"   Компьютер: {self.ai_color.upper()}")
        print(f"   Уровень: {self.skill_level}/20")
        print(f"   Горячие клавиши: R - новая игра, ESC - выход")
        print(f"{'='*60}\n")
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    self.handle_click(x, y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print("🔄 Новая игра...")
                        self.__init__(self.player_color, self.skill_level)
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.screen.fill((0, 0, 0))
            board = self.engine.get_board_state()
            evaluation = self.engine.get_evaluation()
            self.renderer.draw(board, evaluation, self.thinking)
            self.draw_ui()
            pygame.display.flip()
            
            if not self.game_over:
                self.check_game_state()
                self.handle_ai_move()
            
            self.clock.tick(60)
        
        stats = self.get_game_stats()
        print(f"\n{'='*60}")
        print("📊 Статистика игры:")
        print(f"   Всего ходов: {stats['total_moves']}")
        print(f"   Результат: {stats['game_reason']}")
        print(f"{'='*60}\n")
        
        self.engine.quit()


# ============================================================================
# game/menu.py
# ============================================================================

"""
Модуль: game/menu.py

Описание:
    Содержит функции для интерактивного меню выбора параметров игры.
"""


def show_difficulty_guide():
    """Показать справку по уровням сложности Stockfish."""
    print("\n📚 Уровни сложности Stockfish:")
    print("   0-5   : Любитель (начинающий может победить)")
    print("   6-10  : Средний (опытный любитель)")
    print("   11-15 : Сильный (мастер)")
    print("   16-20 : Гроссмейстер (чемпион)")
    print()


def main_menu() -> Tuple[str, int]:
    """Главное меню выбора параметров игры."""
    print("\n" + "="*70)
    print("♟️  chess_stockfish — УЛУЧШЕННАЯ ВЕРСИЯ — Maestro7IT Education")
    print("="*70)
    print("\n🎯 Добро пожаловать в шахматный тренер со Stockfish!\n")
    print("✨ Новые возможности улучшенной версии:")
    print("   ✓ Оценка позиции в реальном времени")
    print("   ✓ Выделение последних ходов")
    print("   ✓ Информационная панель с подробной статистикой")
    print("   ✓ Поддержка обеих сторон (белые/чёрные)")
    print("   ✓ Разные уровни сложности (0-20)")
    print("   ✓ История ходов и позиций")
    print("   ✓ Оптимизированная производительность\n")
    
    show_difficulty_guide()
    
    # Выбор стороны
    while True:
        side_input = input("Выберите сторону (white/w, black/b): ").strip().lower()
        if side_input in ('white', 'w'):
            player_color = 'white'
            break
        elif side_input in ('black', 'b'):
            player_color = 'black'
            break
        else:
            print("❌ Неверный ввод! Введите 'white' (или 'w') или 'black' (или 'b')")
    
    # Выбор уровня сложности
    while True:
        try:
            level_input = input("\nУровень Stockfish (0-20, рекомендуется 5-10): ").strip()
            if level_input == '':
                level = 5
                break
            level = int(level_input)
            if 0 <= level <= 20:
                break
            else:
                print("❌ Уровень должен быть от 0 до 20")
        except ValueError:
            print("❌ Пожалуйста, введите число от 0 до 20")
    
    print(f"\n✅ Игра начинается:")
    print(f"   Вы: {player_color.upper()}")
    print(f"   ПК: {('BLACK' if player_color == 'white' else 'WHITE')}")
    print(f"   Уровень: {level}/20")
    print(f"\n{'='*70}\n")
    
    return player_color, level


# ============================================================================
# main.py
# ============================================================================

"""
Модуль: main.py

Описание:
    Точка входа в приложение chess_stockfish.
    Инициализирует Pygame, запускает меню и начинает игру.
"""


def main():
    """
    Главная функция - точка входа в приложение.
    
    Инициализирует Pygame, показывает меню и запускает игру.
    Обрабатывает исключения и выводит полезные сообщения об ошибках.
    """
    pygame.init()
    
    # Initialize fonts
    init_fonts()
    
    try:
        player_color, skill_level = main_menu()
        game = ChessGame(player_color=player_color, skill_level=skill_level)
        game.run()
        
        # Сохранить статистику игры
        # stats = GameStatistics()
        # stats.save_game(game.get_game_stats())
        
    except RuntimeError as e:
        print(f"\n❌ Ошибка: {e}")
        print("\n💡 РЕШЕНИЕ: Убедитесь, что Stockfish установлен на вашу систему:")
        print("\n   Windows:")
        print("      1. Скачайте с https://stockfishchess.org/download/")
        print("      2. Разархивируйте stockfish.exe в C:\\Program Files\\stockfish\\")
        print("      3. Добавьте в PATH или укажите полный путь в коде\n")
        print("   Linux/macOS:")
        print("      Linux:  sudo apt-get install stockfish")
        print("      macOS:  brew install stockfish\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Игра прервана пользователем")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        pygame.quit()
        print("✅ Приложение закрыто\n")


if __name__ == "__main__":
    main()