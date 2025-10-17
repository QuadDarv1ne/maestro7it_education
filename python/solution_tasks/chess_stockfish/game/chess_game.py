# ============================================================================
# game/chess_game.py
# ============================================================================

"""
Модуль: game/chess_game.py

Описание:
    Содержит главный класс ChessGame, который управляет игровым процессом.
    Отвечает за:
    - Управление взаимодействием игрока и ИИ
    - Обработку кликов и ввода
    - Управление состоянием игры
    - Отображение информации
    
Возможности:
    - Поддержка игры за белых и чёрных
    - Разные уровни сложности Stockfish (0-20)
    - Отслеживание истории ходов
    - Отображение оценки позиции в реальном времени
    - Информационный интерфейс с количеством ходов
"""

import pygame
from typing import Optional, Tuple, List
import time
import sys

# Import our modules
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer

# Constants from board_renderer
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

# Fonts from board_renderer
try:
    FONT = pygame.font.SysFont('Segoe UI Symbol', SQUARE_SIZE - 10)
    SMALL_FONT = pygame.font.SysFont('Arial', 14)
except Exception:
    FONT = pygame.font.SysFont('Arial', SQUARE_SIZE - 10)
    SMALL_FONT = pygame.font.SysFont('Arial', 14)


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
    
    def __init__(self, player_color: str = 'white', skill_level: int = 5):
        """
        Инициализация новой игры.
        
        Параметры:
            player_color (str): Выбранная сторона ('white' или 'black')
            skill_level (int): Уровень сложности Stockfish (0-20)
            
        Исключения:
            RuntimeError: Если не удалось инициализировать Stockfish
        """
        self.player_color = player_color
        self.ai_color = 'black' if player_color == 'white' else 'white'
        self.skill_level = skill_level
        
        try:
            self.engine = StockfishWrapper(skill_level=skill_level)
        except RuntimeError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось инициализировать игру: {e}")
        
        # Инициализация Pygame UI
        try:
            self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
            pygame.display.set_caption(f"♟️  chess_stockfish — Maestro7IT (уровень {skill_level})")
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось инициализировать графический интерфейс: {e}")
        
        self.renderer = BoardRenderer(self.screen, player_color)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Состояние игры
        self.move_history = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.ai_move_delay = 0.7  # Задержка перед ходом ИИ для реалистичности
    
    def _coord_to_fen_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """
        Преобразует экранные координаты клика в FEN координаты.
        
        Параметры:
            x (int): X координата клика
            y (int): Y координата клика
            
        Возвращает:
            Tuple: (row, col) в FEN или None если клик вне доски
        """
        if y > BOARD_SIZE:
            return None
        disp_row = y // SQUARE_SIZE
        disp_col = x // SQUARE_SIZE
        if disp_row >= 8 or disp_col >= 8:
            return None
        row, col = self.renderer._display_to_fen(disp_row, disp_col)
        return (row, col)
    
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
            return
        
        row, col = coords
        try:
            board = self.engine.get_board_state()
        except Exception as e:
            print(f"⚠️  Ошибка при получении состояния доски: {e}")
            return
        
        piece = board[row][col]
        
        # Выбор фигуры
        if self._is_player_piece(piece):
            self.renderer.set_selected((row, col))
        # Перемещение выбранной фигуры
        elif self.renderer.selected_square:
            from_sq = self.renderer.selected_square
            to_sq = (row, col)
            
            uci_move = (self._fen_square_to_uci(*from_sq) + 
                       self._fen_square_to_uci(*to_sq))
            
            try:
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
            except Exception as e:
                print(f"⚠️  Ошибка при обработке хода: {e}")
                self.renderer.clear_selected()
    
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
            ai_move = self.engine.get_best_move(depth=self.skill_level + 10)
            if ai_move:
                if self.engine.make_move(ai_move):
                    self.move_history.append(ai_move)
                    
                    # Преобразование UCI хода в координаты для выделения
                    from_col = ord(ai_move[0]) - ord('a')
                    from_row = 8 - int(ai_move[1])
                    to_col = ord(ai_move[2]) - ord('a')
                    to_row = 8 - int(ai_move[3])
                    self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
                    self.last_move_time = time.time()
                else:
                    print("⚠️  Не удалось выполнить ход компьютера")
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
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
                return True
        except Exception as e:
            print(f"⚠️  Ошибка при проверке состояния игры: {e}")
        return False
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса (информационная полоса внизу)."""
        try:
            # Информационная панель внизу экрана
            info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
            pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
            pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), (BOARD_SIZE, BOARD_SIZE), 2)
            
            if self.game_over:
                # Экран окончания игры
                if self.game_over_reason:
                    text = SMALL_FONT.render(self.game_over_reason, True, (255, 100, 100))
                    self.screen.blit(text, (20, BOARD_SIZE + 15))
                restart_text = SMALL_FONT.render("Нажмите 'R' для новой игры", True, (200, 200, 200))
                self.screen.blit(restart_text, (20, BOARD_SIZE + 50))
            else:
                # Статус хода
                if self._is_player_turn():
                    status = "🎮 Ваш ход"
                    status_color = (100, 255, 100)
                else:
                    status = "🤖 Ход компьютера"
                    status_color = (100, 150, 255)
                
                text = SMALL_FONT.render(status, True, status_color)
                self.screen.blit(text, (20, BOARD_SIZE + 15))
                
                # Информация о ходах
                moves_text = SMALL_FONT.render(f"Ходов: {len(self.move_history)}", True, (200, 200, 200))
                self.screen.blit(moves_text, (20, BOARD_SIZE + 50))
                
                # Уровень сложности
                level_text = SMALL_FONT.render(f"Уровень: {self.skill_level}/20", True, (200, 200, 200))
                self.screen.blit(level_text, (BOARD_SIZE - 150, BOARD_SIZE + 15))
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
                            print("🔄 Новая игра...")
                            self.__init__(self.player_color, self.skill_level)
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                
                # Отрисовка
                self.screen.fill((0, 0, 0))
                try:
                    board = self.engine.get_board_state()
                    evaluation = self.engine.get_evaluation()
                    self.renderer.draw(board, evaluation, self.thinking)
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
                self.running = False
        
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
            self.engine.quit()
        except Exception as e:
            print(f"⚠️  Ошибка при завершении движка: {e}")
        pygame.quit()