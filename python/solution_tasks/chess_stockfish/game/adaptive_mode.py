# ============================================================================
# game/adaptive_mode.py
# ============================================================================

"""
Модуль: game/adaptive_mode.py

Описание:
    Реализация режима адаптивной сложности для шахматной игры chess_stockfish.
    Автоматически подстраивает уровень сложности в зависимости от навыков игрока.

Возможности:
    - Автоматическая настройка уровня сложности Stockfish
    - Отслеживание игровой статистики игрока
    - Адаптация к стилю игры игрока
    - Персонализированные подсказки и обучение
"""

import pygame
import time
import random
from typing import Dict, List, Optional, Tuple

from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer
from utils.educational import ChessEducator
from utils.sound_manager import SoundManager


class AdaptiveMode:
    """
    Класс для управления режимом адаптивной сложности.
    """
    
    def __init__(self, screen: pygame.Surface, player_color: str = 'white'):
        """
        Инициализация режима адаптивной сложности.
        
        Параметры:
            screen (pygame.Surface): Поверхность для отрисовки
            player_color (str): Цвет игрока ('white' или 'black')
        """
        self.screen = screen
        self.player_color = player_color
        
        # Инициализация компонентов
        self.engine = StockfishWrapper(skill_level=5)  # Начинаем со среднего уровня
        self.renderer = BoardRenderer(screen, player_color)
        self.educator = ChessEducator()
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        
        # Адаптивные параметры
        self.current_skill_level = 5  # Текущий уровень сложности (0-20)
        self.player_strength = 0       # Оценка силы игрока (-100 до 100)
        self.adaptation_rate = 0.1     # Скорость адаптации (0.0 - 1.0)
        
        # Статистика игрока
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        self.total_moves = 0
        self.good_moves = 0
        self.mistakes = 0
        self.captures = 0
        self.checks = 0
        
        # Игровое состояние
        self.move_history = []
        self.game_started = False
        self.game_over = False
        self.winner = None
        self.game_over_reason = ""
        self.last_move_time = 0
        self.move_times = []
        
        # Обратная связь и обучение
        self.feedback_message = ""
        self.feedback_time = 0
        self.last_tips = []  # Последние показанные советы
        self.tips_shown = 0
        
        # Цвета для отображения уровня сложности
        self.skill_colors = {
            'beginner': (100, 255, 100),    # Зеленый - новичок
            'intermediate': (255, 255, 100), # Желтый - средний
            'advanced': (255, 165, 0),      # Оранжевый - продвинутый
            'expert': (255, 100, 100)       # Красный - эксперт
        }
    
    def start_game(self):
        """Начать игру в адаптивном режиме."""
        self.game_started = True
        self.last_move_time = time.time()
        self.feedback_message = "Адаптивная игра началась! Уровень сложности будет автоматически подстраиваться."
        self.feedback_time = time.time()
        
        # Проигрываем звук начала игры
        if self.sound_manager:
            self.sound_manager.play_sound("move")
    
    def make_move(self, uci_move: str) -> bool:
        """
        Выполнить ход игрока и адаптировать сложность.
        
        Параметры:
            uci_move (str): Ход игрока в формате UCI
            
        Возвращает:
            bool: True если ход выполнен успешно
        """
        if not self.game_started or self.game_over:
            return False
            
        if not self.engine.is_move_correct(uci_move):
            self.feedback_message = "Недопустимый ход"
            self.feedback_time = time.time()
            if self.sound_manager:
                self.sound_manager.play_sound("button")
            return False
        
        # Засекаем время хода
        move_time = time.time() - self.last_move_time
        self.move_times.append(move_time)
        self.last_move_time = time.time()
        
        # Выполняем ход игрока
        if self.engine.make_move(uci_move):
            self.move_history.append(uci_move)
            self.total_moves += 1
            
            # Оцениваем качество хода
            move_quality = self._evaluate_move_quality(uci_move)
            if move_quality > 0.7:  # Хороший ход
                self.good_moves += 1
                self.feedback_message = "Отличный ход!"
            elif move_quality > 0.4:  # Средний ход
                self.feedback_message = "Хороший ход"
            else:  # Слабый ход
                self.mistakes += 1
                self.feedback_message = "Есть более сильные ходы"
            
            self.feedback_time = time.time()
            
            # Проверяем окончание игры
            is_over, reason = self.engine.is_game_over()
            if is_over:
                self._handle_game_end(reason)
                return True
            
            # Ход компьютера
            self._make_ai_move()
            
            # Адаптируем сложность
            self._adapt_difficulty()
            
            # Проигрываем звук хода
            if self.sound_manager:
                self.sound_manager.play_sound("move")
            
            return True
        else:
            self.feedback_message = "Ошибка при выполнении хода"
            self.feedback_time = time.time()
            if self.sound_manager:
                self.sound_manager.play_sound("button")
            return False
    
    def _evaluate_move_quality(self, player_move: str) -> float:
        """
        Оценить качество хода игрока по сравнению с лучшими ходами.
        
        Параметры:
            player_move (str): Ход игрока
            
        Возвращает:
            float: Качество хода от 0.0 (плохой) до 1.0 (лучший)
        """
        try:
            # Получаем лучшие ходы от Stockfish
            best_moves = self.engine.get_best_moves(3)
            
            if not best_moves:
                return 0.5  # Нейтральная оценка если нет ходов
            
            # Если ход игрока совпадает с лучшим ходом
            if player_move == best_moves[0]:
                return 1.0
            
            # Если ход среди топ-3
            if player_move in best_moves:
                index = best_moves.index(player_move)
                return 0.8 - (index * 0.2)  # 0.8, 0.6 для второго и третьего
            
            # Получаем оценку позиции до и после хода
            original_eval = self.engine.get_evaluation()
            
            # Делаем ход игрока временно
            self.engine.make_move(player_move)
            player_eval = self.engine.get_evaluation()
            
            # Возвращаемся к исходной позиции
            self.engine.reset_board()
            for move in self.move_history:
                self.engine.make_move(move)
            
            # Сравниваем оценки (если доступны)
            if original_eval is not None and player_eval is not None:
                # Для игрока белыми: положительная оценка хороша
                # Для игрока черными: отрицательная оценка хороша
                is_white_player = (self.player_color == 'white')
                
                if is_white_player:
                    # Белые - чем выше оценка, тем лучше
                    improvement = player_eval - original_eval
                    quality = max(0.0, min(1.0, 0.5 + improvement / 2.0))
                else:
                    # Черные - чем ниже оценка, тем лучше
                    improvement = original_eval - player_eval
                    quality = max(0.0, min(1.0, 0.5 + improvement / 2.0))
                
                return quality
            
            return 0.5  # Нейтральная оценка если нет данных
        except Exception as e:
            print(f"Ошибка при оценке качества хода: {e}")
            return 0.5
    
    def _make_ai_move(self):
        """Сделать ход компьютера."""
        try:
            # Получаем лучший ход с текущим уровнем сложности
            ai_move = self.engine.get_best_move()
            
            if ai_move:
                if self.engine.make_move(ai_move):
                    self.move_history.append(ai_move)
                    
                    # Проверяем взятие
                    if 'x' in ai_move:
                        self.captures += 1
                    
                    # Проверяем шах
                    if '+' in ai_move:
                        self.checks += 1
                    
                    # Проверяем окончание игры
                    is_over, reason = self.engine.is_game_over()
                    if is_over:
                        self._handle_game_end(reason)
                    
                    # Проигрываем звук хода компьютера
                    if self.sound_manager:
                        self.sound_manager.play_sound("move")
                else:
                    self.feedback_message = "Ошибка хода компьютера"
                    self.feedback_time = time.time()
            else:
                self.feedback_message = "Компьютер не нашел ход"
                self.feedback_time = time.time()
        except Exception as e:
            print(f"Ошибка хода компьютера: {e}")
            self.feedback_message = "Ошибка хода компьютера"
            self.feedback_time = time.time()
    
    def _handle_game_end(self, reason: Optional[str]):
        """
        Обработать окончание игры.
        
        Параметры:
            reason (str): Причина окончания игры
        """
        self.game_over = True
        self.game_over_reason = reason or "Игра завершена"
        
        # Определяем победителя
        if reason:
            if "мат" in reason.lower():
                # Определяем, кто поставил мат
                side_to_move = self.engine.get_side_to_move()
                if (side_to_move == 'w' and self.player_color == 'black') or \
                   (side_to_move == 'b' and self.player_color == 'white'):
                    self.winner = "player"
                    self.games_won += 1
                    self.feedback_message = "Шах и мат! Вы победили!"
                else:
                    self.winner = "computer"
                    self.games_lost += 1
                    self.feedback_message = "Шах и мат! Компьютер победил!"
            elif "пат" in reason.lower() or "ничья" in reason.lower():
                self.winner = "draw"
                self.feedback_message = "Ничья!"
            else:
                self.feedback_message = reason
        else:
            self.feedback_message = "Игра завершена"
        
        self.feedback_time = time.time()
        self.games_played += 1
        
        # Адаптируем сложность после игры
        self._adapt_difficulty_post_game()
        
        # Проигрываем соответствующий звук
        if self.sound_manager:
            if self.winner == "player":
                self.sound_manager.play_sound("capture")
            elif self.winner == "computer":
                self.sound_manager.play_sound("button")
            else:
                self.sound_manager.play_sound("move")
    
    def _adapt_difficulty(self):
        """Адаптировать уровень сложности во время игры."""
        if self.total_moves < 5:
            return  # Не адаптируем на начальных ходах
        
        # Рассчитываем текущую эффективность игрока
        if self.total_moves > 0:
            accuracy = self.good_moves / max(1, self.total_moves)
            mistake_rate = self.mistakes / max(1, self.total_moves)
        else:
            accuracy = 0.5
            mistake_rate = 0.5
        
        # Адаптируем уровень сложности
        if accuracy > 0.8 and self.current_skill_level < 18:
            # Игрок сильный, увеличиваем сложность
            self.current_skill_level = min(20, self.current_skill_level + 1)
            self.feedback_message = "Уровень сложности повышен!"
        elif mistake_rate > 0.6 and self.current_skill_level > 2:
            # Игрок слабый, уменьшаем сложность
            self.current_skill_level = max(0, self.current_skill_level - 1)
            self.feedback_message = "Уровень сложности понижен для удобства обучения"
        
        # Обновляем уровень сложности движка
        self.engine.set_skill_level(self.current_skill_level)
        self.feedback_time = time.time()
    
    def _adapt_difficulty_post_game(self):
        """Адаптировать уровень сложности после окончания игры."""
        # Рассчитываем общий уровень игрока на основе этой игры
        if self.total_moves > 0:
            game_accuracy = self.good_moves / self.total_moves
        else:
            game_accuracy = 0.5
        
        # Обновляем оценку силы игрока
        strength_change = (game_accuracy - 0.5) * 20  # От -10 до +10
        self.player_strength = self.player_strength * (1 - self.adaptation_rate) + \
                              strength_change * self.adaptation_rate
        
        # Корректируем уровень сложности для следующей игры
        # Преобразуем силу игрока (-100 до 100) в уровень сложности (0-20)
        new_skill_level = max(0, min(20, int(10 + self.player_strength / 10)))
        
        if abs(new_skill_level - self.current_skill_level) > 2:
            # Меняем уровень только если разница значительная
            self.current_skill_level = new_skill_level
            self.engine.set_skill_level(self.current_skill_level)
    
    def get_skill_level_description(self) -> str:
        """
        Получить описание текущего уровня сложности.
        
        Возвращает:
            str: Описание уровня сложности
        """
        if self.current_skill_level <= 5:
            return "Новичок"
        elif self.current_skill_level <= 10:
            return "Любитель"
        elif self.current_skill_level <= 15:
            return "Сильный игрок"
        else:
            return "Эксперт"
    
    def get_skill_color(self) -> Tuple[int, int, int]:
        """
        Получить цвет для отображения текущего уровня сложности.
        
        Возвращает:
            Tuple[int, int, int]: Цвет RGB
        """
        if self.current_skill_level <= 5:
            return self.skill_colors['beginner']
        elif self.current_skill_level <= 10:
            return self.skill_colors['intermediate']
        elif self.current_skill_level <= 15:
            return self.skill_colors['advanced']
        else:
            return self.skill_colors['expert']
    
    def get_player_stats(self) -> Dict:
        """
        Получить статистику игрока.
        
        Возвращает:
            Dict: Словарь со статистикой
        """
        avg_move_time = sum(self.move_times) / max(1, len(self.move_times)) if self.move_times else 0
        
        return {
            'games_played': self.games_played,
            'games_won': self.games_won,
            'games_lost': self.games_lost,
            'win_rate': (self.games_won / max(1, self.games_played)) * 100 if self.games_played > 0 else 0,
            'total_moves': self.total_moves,
            'accuracy': (self.good_moves / max(1, self.total_moves)) * 100 if self.total_moves > 0 else 0,
            'mistakes': self.mistakes,
            'captures': self.captures,
            'checks': self.checks,
            'avg_move_time': avg_move_time,
            'current_skill_level': self.current_skill_level,
            'player_strength': self.player_strength
        }
    
    def get_educational_tip(self) -> str:
        """
        Получить образовательный совет, адаптированный к уровню игрока.
        
        Возвращает:
            str: Образовательный совет
        """
        # Ограничиваем частоту показа советов
        if self.total_moves > 0 and self.total_moves % 7 == 0:
            # Выбираем тип совета в зависимости от уровня игрока
            if self.current_skill_level <= 5:
                # Для новичков - основы
                tips = [
                    self.educator.get_random_tip(),
                    self.educator.get_piece_hint(random.choice(['пешка', 'ладья', 'конь', 'слон', 'ферзь', 'король'])),
                    self.educator.get_term_explanation(random.choice(['шах', 'мат', 'пат', 'рокировка']))
                ]
            elif self.current_skill_level <= 10:
                # Для любителей - тактика
                tips = [
                    self.educator.get_tactical_motiv(),
                    self.educator.get_historical_fact(),
                    self.educator.get_endgame_tip()
                ]
            else:
                # Для сильных игроков - стратегия
                tips = [
                    self.educator.get_endgame_tip(),
                    self.educator.get_historical_fact(),
                    "Попробуйте просчитать ходы на 3-4 полухода вперёд"
                ]
            
            # Выбираем случайный совет, которого не было недавно
            available_tips = [tip for tip in tips if tip not in self.last_tips]
            if not available_tips:
                available_tips = tips
            
            tip = random.choice(available_tips)
            self.last_tips.append(tip)
            if len(self.last_tips) > 3:
                self.last_tips.pop(0)
            
            self.tips_shown += 1
            return tip
        
        return ""
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса адаптивного режима."""
        BOARD_SIZE = 512
        
        # Информационная панель
        info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
        pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), 
                        (BOARD_SIZE, BOARD_SIZE), 2)
        
        # Уровень сложности
        font = pygame.font.SysFont('Arial', 16, bold=True)
        skill_text = font.render(f"Уровень: {self.current_skill_level}/20 ({self.get_skill_level_description()})", 
                                True, self.get_skill_color())
        self.screen.blit(skill_text, (20, BOARD_SIZE + 10))
        
        # Статистика
        stats_font = pygame.font.SysFont('Arial', 14)
        moves_text = stats_font.render(f"Ходы: {self.total_moves} | Точность: {self.get_player_stats()['accuracy']:.1f}%", 
                                      True, (200, 200, 100))
        self.screen.blit(moves_text, (20, BOARD_SIZE + 35))
        
        wins_text = stats_font.render(f"Победы: {self.games_won}/{self.games_played}", 
                                     True, (100, 255, 100) if self.games_won > self.games_lost else (255, 100, 100))
        self.screen.blit(wins_text, (20, BOARD_SIZE + 60))
        
        # Оценка силы игрока
        strength_text = stats_font.render(f"Сила: {self.player_strength:+.1f}", True, (200, 200, 200))
        self.screen.blit(strength_text, (BOARD_SIZE - 150, BOARD_SIZE + 35))
        
        # Статус игры
        status_text = ""
        if not self.game_started:
            status_text = "Ожидание начала игры"
        elif self.game_over:
            status_text = "ИГРА ЗАВЕРШЕНА"
        else:
            side_to_move = self.engine.get_side_to_move()
            player_side = "Ваш ход" if (side_to_move == 'w' and self.player_color == 'white') or \
                                     (side_to_move == 'b' and self.player_color == 'black') else "Ход компьютера"
            status_text = player_side
        
        status_color = (100, 255, 100) if "Ваш" in status_text else (200, 200, 200)
        status_render = stats_font.render(status_text, True, status_color)
        self.screen.blit(status_render, (BOARD_SIZE // 2 - status_render.get_width() // 2, BOARD_SIZE + 10))
        
        # Обратная связь
        if self.feedback_message and time.time() - self.feedback_time < 4:
            feedback_font = pygame.font.SysFont('Arial', 14)
            feedback_color = (100, 255, 100) if "побед" in self.feedback_message.lower() or "Отличн" in self.feedback_message or "Хорош" in self.feedback_message else (255, 255, 100) if "повышен" in self.feedback_message or "понижен" in self.feedback_message else (255, 100, 100)
            feedback_text = feedback_font.render(self.feedback_message, True, feedback_color)
            self.screen.blit(feedback_text, (BOARD_SIZE // 2 - feedback_text.get_width() // 2, BOARD_SIZE + 75))
        
        # Образовательные советы
        tip = self.get_educational_tip()
        if tip and self.tips_shown > 0:
            tip_font = pygame.font.SysFont('Arial', 12)
            tip_text = tip_font.render(f"💡 {tip}", True, (100, 200, 255))
            self.screen.blit(tip_text, (BOARD_SIZE // 2 - tip_text.get_width() // 2, BOARD_SIZE + 60))
    
    def draw(self):
        """Отрисовка режима адаптивной сложности."""
        # Получаем состояние доски
        board_state = self.engine.get_board_state()
        
        # Отрисовываем доску
        self.renderer.draw(board_state)
        
        # Отрисовываем UI
        self.draw_ui()
    
    def reset_game(self):
        """Сбросить игру к начальному состоянию."""
        self.engine.reset_board()
        self.move_history = []
        self.game_started = False
        self.game_over = False
        self.winner = None
        self.game_over_reason = ""
        self.last_move_time = time.time()
        self.move_times = []
        self.feedback_message = "Новая игра! Уровень сложности адаптируется к вашим навыкам."
        self.feedback_time = time.time()
        self.total_moves = 0
        self.good_moves = 0
        self.mistakes = 0
        self.captures = 0
        self.checks = 0
        self.last_tips = []
        
        # Проигрываем звук новой игры
        if self.sound_manager:
            self.sound_manager.play_sound("move")
    
    def cleanup(self):
        """Очистка ресурсов."""
        if self.engine:
            self.engine.quit()
        if self.sound_manager:
            self.sound_manager.cleanup()
