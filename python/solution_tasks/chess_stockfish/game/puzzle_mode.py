# ============================================================================
# game/puzzle_mode.py
# ============================================================================

"""
Модуль: game/puzzle_mode.py

Описание:
    Реализация режима головоломок для шахматной игры chess_stockfish.
    Предоставляет интерактивные шахматные головоломки для обучения и тренировки.

Возможности:
    - Решение шахматных головоломок различной сложности
    - Система подсказок и объяснений решений
    - Отслеживание прогресса и статистики
    - Рейтинговая система для оценки навыков
"""

import pygame
import time
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer
from utils.educational import ChessEducator
from utils.sound_manager import SoundManager


@dataclass
class Puzzle:
    """Класс для представления шахматной головоломки."""
    id: str
    name: str
    fen: str
    solution: str
    description: str
    difficulty: str  # 'beginner', 'intermediate', 'advanced', 'expert'
    category: str    # 'checkmate', 'tactics', 'endgame', 'openings'
    hints: List[str]
    explanation: str
    points: int


# База шахматных головоломок
PUZZLE_DATABASE = [
    Puzzle(
        id="mate1_1",
        name="Мат в 1 ход",
        fen="r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
        solution="f3g5",
        description="Белые ставят мат в один ход",
        difficulty="beginner",
        category="checkmate",
        hints=["Ищите ход, который атакует короля черных и не имеет защиты", "Конь с f3 может пойти на g5"],
        explanation="Конь с f3 идет на g5, ставя шах королю на e7. Король не может уйти, и нет фигуры, которая может защитить e7.",
        points=10
    ),
    Puzzle(
        id="fork1_1",
        name="Вилка конем",
        fen="r1bq1rk1/pp2bppp/2n2n2/2pp4/4P3/2PB1N2/PP3PPP/RNBQ1RK1 w - - 0 1",
        solution="d3h7",
        description="Белые создают вилку конем, атакуя короля и ладью",
        difficulty="intermediate",
        category="tactics",
        hints=["Ищите ход, который атакует две фигуры одновременно", "Конь может атаковать короля и ладью"],
        explanation="Конь с d3 идет на h7, атакуя короля на g8 и ладью на f8 одновременно. Черные не могут защитить обе фигуры.",
        points=20
    ),
    Puzzle(
        id="pin1_1",
        name="Связка",
        fen="r1bq1rk1/pp2bppp/2n2n2/2pp4/4P3/2PB1N2/PP3PPP/RNBQ1RK1 b - - 0 1",
        solution="c8g4",
        description="Черные связывают коня, атакуя ферзя и коня",
        difficulty="intermediate",
        category="tactics",
        hints=["Ищите ход, который атакует две фигуры на одной линии", "Слон может атаковать ферзя и коня"],
        explanation="Слон с c8 идет на g4, атакуя ферзя на d1 и коня на f3. Конь не может уйти, так как это откроет шах королю.",
        points=20
    ),
    Puzzle(
        id="endgame1_1",
        name="Простой эндшпиль",
        fen="8/8/8/8/8/8/4k3/K4Q1P w - - 0 1",
        solution="f1e1",
        description="Белые выигрывают в простом эндшпиле ферзь против короля",
        difficulty="beginner",
        category="endgame",
        hints=["Используйте ферзя для ограничения движения короля черных", "Постепенно сужайте пространство для короля черных"],
        explanation="Ферзь с f1 идет на e1, ограничивая движение короля черных. Постепенно ферзь будет сужать пространство до мата.",
        points=15
    ),
    Puzzle(
        id="checkmate2_1",
        name="Мат в 2 хода",
        fen="r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
        solution="d1h5",
        description="Белые начинают комбинацию для мата в 2 хода",
        difficulty="advanced",
        category="checkmate",
        hints=["Ищите ход, который создает угрозу мата", "Ферзь может создать угрозу на h7"],
        explanation="Ферзь с d1 идет на h5, угрожая матом на f7. Черные должны защитить f7, но тогда белые могут поставить мат следующим ходом.",
        points=30
    )
]


class PuzzleMode:
    """
    Класс для управления режимом головоломок.
    """
    
    def __init__(self, screen: pygame.Surface, player_color: str = 'white'):
        """
        Инициализация режима головоломок.
        
        Параметры:
            screen (pygame.Surface): Поверхность для отрисовки
            player_color (str): Цвет игрока ('white' или 'black')
        """
        self.screen = screen
        self.player_color = player_color
        self.engine = StockfishWrapper(skill_level=10)
        self.renderer = BoardRenderer(screen, player_color)
        self.educator = ChessEducator()
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        
        # Состояние головоломки
        self.current_puzzle: Optional[Puzzle] = None
        self.puzzle_solved = False
        self.attempts = 0
        self.hints_used = 0
        self.start_time = 0
        self.solve_time = 0
        self.score = 0
        self.feedback_message = ""
        self.feedback_time = 0
        self.selected_hint = -1
        
        # Статистика
        self.puzzles_solved = 0
        self.total_attempts = 0
        self.total_hints_used = 0
        self.total_time_spent = 0
        
        # История решенных головоломок
        self.solved_puzzles = set()
        
        # Выбор головоломки
        self.select_random_puzzle()
    
    def select_random_puzzle(self):
        """Выбрать случайную головоломку из базы."""
        if PUZZLE_DATABASE:
            # Выбираем головоломку, которую еще не решали
            unsolved_puzzles = [p for p in PUZZLE_DATABASE if p.id not in self.solved_puzzles]
            if unsolved_puzzles:
                self.current_puzzle = random.choice(unsolved_puzzles)
            else:
                # Если все решены, выбираем любую
                self.current_puzzle = random.choice(PUZZLE_DATABASE)
            
            # Устанавливаем позицию головоломки
            self.engine.set_fen(self.current_puzzle.fen)
            self.puzzle_solved = False
            self.attempts = 0
            self.hints_used = 0
            self.start_time = time.time()
            self.feedback_message = f"Головоломка: {self.current_puzzle.name}"
            self.feedback_time = time.time()
            self.selected_hint = -1
        else:
            self.current_puzzle = None
            self.feedback_message = "Нет доступных головоломок"
            self.feedback_time = time.time()
    
    def check_solution(self, move: str) -> bool:
        """
        Проверить решение головоломки.
        
        Параметры:
            move (str): Ход игрока в формате UCI
            
        Возвращает:
            bool: True если решение верное
        """
        if not self.current_puzzle or self.puzzle_solved:
            return False
            
        self.attempts += 1
        self.total_attempts += 1
        
        is_correct = move == self.current_puzzle.solution
        if is_correct:
            self.puzzle_solved = True
            self.solve_time = time.time() - self.start_time
            self.total_time_spent += self.solve_time
            self.solved_puzzles.add(self.current_puzzle.id)
            self.puzzles_solved += 1
            
            # Начисляем очки
            base_points = self.current_puzzle.points
            time_bonus = max(0, 30 - int(self.solve_time))  # Бонус за быстрое решение
            hint_penalty = self.hints_used * 2  # Штраф за использование подсказок
            self.score += max(1, base_points + time_bonus - hint_penalty)
            
            self.feedback_message = "✅ Правильное решение! Отличная работа!"
            self.feedback_time = time.time()
            
            # Проигрываем звук успеха
            if self.sound_manager:
                self.sound_manager.play_sound("capture")
        else:
            self.feedback_message = "❌ Неправильное решение. Попробуйте еще раз!"
            self.feedback_time = time.time()
            
            # Проигрываем звук ошибки
            if self.sound_manager:
                self.sound_manager.play_sound("button")
        
        return is_correct
    
    def get_hint(self) -> str:
        """
        Получить подсказку для текущей головоломки.
        
        Возвращает:
            str: Подсказка
        """
        if not self.current_puzzle or self.puzzle_solved:
            return "Нет доступных подсказок"
            
        self.hints_used += 1
        self.total_hints_used += 1
        
        if self.hints_used <= len(self.current_puzzle.hints):
            hint = self.current_puzzle.hints[self.hints_used - 1]
            self.feedback_message = f"💡 Подсказка: {hint}"
        else:
            self.feedback_message = f"💡 Решение: {self.current_puzzle.solution}"
            
        self.feedback_time = time.time()
        return self.feedback_message
    
    def get_explanation(self) -> str:
        """
        Получить объяснение решения головоломки.
        
        Возвращает:
            str: Объяснение решения
        """
        if not self.current_puzzle:
            return "Нет объяснения"
            
        return self.current_puzzle.explanation
    
    def get_statistics(self) -> Dict:
        """
        Получить статистику по решенным головоломкам.
        
        Возвращает:
            Dict: Словарь со статистикой
        """
        return {
            'puzzles_solved': self.puzzles_solved,
            'total_attempts': self.total_attempts,
            'total_hints_used': self.total_hints_used,
            'total_time_spent': self.total_time_spent,
            'current_score': self.score,
            'accuracy': (self.puzzles_solved / max(1, self.total_attempts)) * 100 if self.total_attempts > 0 else 0,
            'average_time': self.total_time_spent / max(1, self.puzzles_solved) if self.puzzles_solved > 0 else 0
        }
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса режима головоломок."""
        BOARD_SIZE = 512
        
        # Информационная панель
        info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
        pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), 
                        (BOARD_SIZE, BOARD_SIZE), 2)
        
        if self.current_puzzle:
            # Название головоломки
            font = pygame.font.SysFont('Arial', 16, bold=True)
            name_text = font.render(self.current_puzzle.name, True, (255, 255, 255))
            self.screen.blit(name_text, (20, BOARD_SIZE + 10))
            
            # Описание
            font = pygame.font.SysFont('Arial', 14)
            desc_text = font.render(self.current_puzzle.description, True, (200, 200, 200))
            self.screen.blit(desc_text, (20, BOARD_SIZE + 35))
            
            # Сложность и категория
            diff_text = font.render(f"Сложность: {self.current_puzzle.difficulty} | Категория: {self.current_puzzle.category}", 
                                   True, (180, 180, 100))
            self.screen.blit(diff_text, (20, BOARD_SIZE + 55))
            
            # Статистика
            stats_text = font.render(f"Попытки: {self.attempts} | Подсказки: {self.hints_used} | Очки: {self.score}", 
                                    True, (100, 200, 255))
            self.screen.blit(stats_text, (BOARD_SIZE - 250, BOARD_SIZE + 10))
            
            # Таймер
            if not self.puzzle_solved and self.start_time > 0:
                elapsed = int(time.time() - self.start_time)
                timer_text = font.render(f"Время: {elapsed}с", True, (255, 200, 100))
                self.screen.blit(timer_text, (BOARD_SIZE - 100, BOARD_SIZE + 35))
        
        # Обратная связь
        if self.feedback_message and time.time() - self.feedback_time < 5:
            font = pygame.font.SysFont('Arial', 14)
            feedback_color = (100, 255, 100) if "Правильное" in self.feedback_message else (255, 100, 100)
            feedback_text = font.render(self.feedback_message, True, feedback_color)
            self.screen.blit(feedback_text, (BOARD_SIZE // 2 - feedback_text.get_width() // 2, BOARD_SIZE + 75))
        
        # Кнопки управления
        button_font = pygame.font.SysFont('Arial', 12)
        
        # Кнопка "Следующая головоломка"
        next_rect = pygame.Rect(BOARD_SIZE - 150, BOARD_SIZE + 60, 140, 25)
        pygame.draw.rect(self.screen, (70, 70, 150), next_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 200), next_rect, 2, border_radius=5)
        next_text = button_font.render("Следующая головоломка", True, (255, 255, 255))
        self.screen.blit(next_text, (next_rect.centerx - next_text.get_width() // 2, 
                                    next_rect.centery - next_text.get_height() // 2))
        
        # Кнопка "Подсказка"
        hint_rect = pygame.Rect(20, BOARD_SIZE + 60, 80, 25)
        pygame.draw.rect(self.screen, (70, 150, 70), hint_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 200, 100), hint_rect, 2, border_radius=5)
        hint_text = button_font.render("Подсказка", True, (255, 255, 255))
        self.screen.blit(hint_text, (hint_rect.centerx - hint_text.get_width() // 2, 
                                    hint_rect.centery - hint_text.get_height() // 2))
        
        # Кнопка "Объяснение"
        expl_rect = pygame.Rect(110, BOARD_SIZE + 60, 100, 25)
        pygame.draw.rect(self.screen, (150, 70, 70), expl_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 100, 100), expl_rect, 2, border_radius=5)
        expl_text = button_font.render("Объяснение", True, (255, 255, 255))
        self.screen.blit(expl_text, (expl_rect.centerx - expl_text.get_width() // 2, 
                                    expl_rect.centery - expl_text.get_height() // 2))
    
    def handle_click(self, x: int, y: int) -> str:
        """
        Обработка клика мыши.
        
        Параметры:
            x (int): Координата X клика
            y (int): Координата Y клика
            
        Возвращает:
            str: Действие, которое нужно выполнить ('next_puzzle', 'hint', 'explanation', 'none')
        """
        BOARD_SIZE = 512
        
        # Проверяем клик по кнопкам
        if BOARD_SIZE <= y <= BOARD_SIZE + 100:
            # Кнопка "Следующая головоломка"
            if BOARD_SIZE - 150 <= x <= BOARD_SIZE - 10 and BOARD_SIZE + 60 <= y <= BOARD_SIZE + 85:
                return 'next_puzzle'
            # Кнопка "Подсказка"
            elif 20 <= x <= 100 and BOARD_SIZE + 60 <= y <= BOARD_SIZE + 85:
                return 'hint'
            # Кнопка "Объяснение"
            elif 110 <= x <= 210 and BOARD_SIZE + 60 <= y <= BOARD_SIZE + 85:
                return 'explanation'
        
        return 'none'
    
    def draw(self):
        """Отрисовка режима головоломок."""
        # Получаем состояние доски
        board_state = self.engine.get_board_state()
        
        # Отрисовываем доску
        self.renderer.draw(board_state)
        
        # Отрисовываем UI
        self.draw_ui()
    
    def next_puzzle(self):
        """Перейти к следующей головоломке."""
        self.select_random_puzzle()
    
    def cleanup(self):
        """Очистка ресурсов."""
        if self.engine:
            self.engine.quit()
        if self.sound_manager:
            self.sound_manager.cleanup()

