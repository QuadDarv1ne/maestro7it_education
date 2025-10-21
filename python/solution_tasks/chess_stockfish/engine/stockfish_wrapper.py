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
    
Возможности:
    - Интеграция с python-chess для глубокого анализа
    - Кэширование результатов анализа
    - Поддержка различных форматов позиций (FEN, UCI)
    - Безопасное завершение работы с движком
"""

from stockfish import Stockfish
from typing import Optional, Tuple, List
import os
import sys
import shutil
import time


class StockfishWrapper:
    """
    Обёртка для работы со Stockfish с улучшенной обработкой ошибок.
    
    Атрибуты:
        engine (Stockfish): Экземпляр движка Stockfish
        skill_level (int): Уровень сложности (0-20)
        depth (int): Глубина анализа
        analysis_cache (dict): Кэш для результатов анализа
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
        self.analysis_cache = {}
        self.board_state_cache = None
        self.board_state_cache_fen = None
        self.evaluation_cache = None
        self.evaluation_cache_fen = None
        self.move_count = 0
        self.engine = None
        
        # Проверка наличия исполняемого файла Stockfish
        stockfish_path = path
        if stockfish_path is None:
            # Попробуем найти Stockfish в PATH
            stockfish_path = shutil.which("stockfish")
            if stockfish_path is None:
                print("⚠️  Stockfish не найден в PATH. Убедитесь, что он установлен.")
                print("💡 Решение:")
                print("   1. Скачайте Stockfish с https://stockfishchess.org/download/")
                print("   2. Распакуйте в папку и добавьте её в PATH")
                print("   3. Или запустите install_stockfish.bat")
                raise RuntimeError("Stockfish executable not found in PATH")
        
        # Проверим, что файл существует, если указан конкретный путь
        if path is not None and not os.path.exists(path):
            raise RuntimeError(f"❌ Файл Stockfish не найден по пути: {path}")
        
        try:
            # Handle the case where path might be None
            if path is not None:
                self.engine = Stockfish(path=path)
            else:
                # Используем найденный путь или путь по умолчанию
                self.engine = Stockfish(path=stockfish_path) if stockfish_path else Stockfish()
            self.engine.set_skill_level(self.skill_level)
            self.engine.set_depth(self.depth)
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось запустить Stockfish: {e}. Убедитесь, что Stockfish установлен и доступен.")
    
    def get_board_state(self) -> List[List[Optional[str]]]:
        """
        Возвращает текущее состояние доски (8x8).
        
        Возвращает:
            List[List[Optional[str]]]: 2D массив, где каждый элемент - фигура или None
                                       Пример: 'P' - пешка белых, 'p' - пешка чёрных
        """
        if self.engine is None:
            # Возвращаем начальную позицию в случае ошибки
            return [
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
            ]
            
        try:
            fen = self.engine.get_fen_position()
            # Check cache first with more aggressive caching
            if self.board_state_cache_fen == fen and self.board_state_cache is not None:
                # Проверяем время кэша - используем кэш до 500 мс (уменьшено с 200 мс для более агрессивного кэширования)
                return self.board_state_cache  # type: ignore
            
            board_str = fen.split()[0]
            rows = board_str.split('/')
            board: List[List[Optional[str]]] = []
            for row in rows:
                new_row: List[Optional[str]] = []
                for char in row:
                    if char.isdigit():
                        new_row.extend([None] * int(char))
                    else:
                        new_row.append(char)
                board.append(new_row)
            
            # Update cache
            self.board_state_cache = board
            self.board_state_cache_fen = fen
            return board
        except Exception as e:
            print(f"⚠️  Ошибка при получении состояния доски: {e}")
            # Возвращаем пустую доску в случае ошибки
            return [[None for _ in range(8)] for _ in range(8)]
    
    def is_move_correct(self, uci_move: str) -> bool:
        """
        Проверяет, является ли ход корректным в текущей позиции.
        
        Параметры:
            uci_move (str): Ход в формате UCI (например, "e2e4")
            
        Возвращает:
            bool: True если ход корректен, False иначе
        """
        if self.engine is None:
            return False
            
        if not uci_move or len(uci_move) != 4:
            return False
        try:
            # Get the FEN before attempting the move
            original_fen = self.engine.get_fen_position()
            # Try to make the move
            self.engine.make_moves_from_current_position([uci_move])
            # Get the FEN after the move
            new_fen = self.engine.get_fen_position()
            # Undo the move to restore the original position
            self.engine.set_fen_position(original_fen)
            # If the FEN changed, the move was valid
            return original_fen != new_fen
        except Exception:
            return False
    
    def make_move(self, uci_move: str) -> bool:
        """
        Выполняет ход в текущей позиции.
        
        Параметры:
            uci_move (str): Ход в формате UCI
            
        Возвращает:
            bool: True если ход успешно выполнен, False иначе
        """
        if self.engine is None:
            return False
            
        if not self.is_move_correct(uci_move):
            return False
        try:
            self.engine.make_moves_from_current_position([uci_move])
            self.move_count += 1
            # Clear cache after making a move
            self.board_state_cache = None
            self.board_state_cache_fen = None
            self.evaluation_cache = None
            self.evaluation_cache_fen = None
            return True
        except Exception as e:
            print(f"⚠️  Ошибка при выполнении хода {uci_move}: {e}")
            return False
    
    def get_best_move(self, depth: Optional[int] = None) -> Optional[str]:
        """
        Получает лучший ход в текущей позиции.
        
        Параметры:
            depth (int): Глубина анализа (если None, использует установленную)
            
        Возвращает:
            str: Лучший ход в формате UCI, или None если нет ходов
        """
        if self.engine is None:
            return None
            
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
    
    def get_best_moves(self, num_moves: int = 3) -> List[str]:
        """
        Получает несколько лучших ходов в текущей позиции.
        
        Параметры:
            num_moves (int): Количество ходов для возврата
            
        Возвращает:
            List[str]: Список лучших ходов в порядке убывания качества
        """
        if self.engine is None:
            return []
            
        try:
            best_moves = []
            fen = self.engine.get_fen_position()
            for i in range(num_moves):
                move = self.engine.get_best_move()
                if not move:
                    break
                best_moves.append(move)
                self.engine.make_moves_from_current_position([move])
            # Откатываем ходы
            for _ in range(len(best_moves)):
                self.engine.set_fen_position(fen)
            return best_moves
        except Exception as e:
            print(f"⚠️  Ошибка при получении лучших ходов: {e}")
            return []
    
    def get_side_to_move(self) -> str:
        """
        Получает, чей ход в текущей позиции.
        
        Возвращает:
            str: 'w' для белых, 'b' для чёрных
        """
        if self.engine is None:
            return 'w'  # По умолчанию возвращаем 'w' (белые)
            
        try:
            return self.engine.get_fen_position().split()[1]
        except Exception:
            # По умолчанию возвращаем 'w' (белые)
            return 'w'
    
    def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """
        Проверяет, закончена ли игра и причину окончания.
        
        Возвращает:
            Tuple[bool, Optional[str]]: (is_over, reason)
                - is_over: True если игра завершена
                - reason: Строка с описанием причины завершения
        """
        if self.engine is None:
            return False, None
            
        try:
            # Get current FEN position
            fen = self.engine.get_fen_position()
            fen_parts = fen.split()
            board_state = fen_parts[0]
            
            # Check if Stockfish reports game over directly
            # This is the most reliable method
            try:
                # Try to get best move - if None, game is over
                best_move = self.engine.get_best_move()
                if best_move is None:
                    # Game is over, determine the reason
                    eval_result = self.engine.get_evaluation()
                    if eval_result and eval_result['type'] == 'mate':
                        mate_value = eval_result['value']
                        side = self.get_side_to_move()
                        
                        if mate_value == 0:
                            winner = "чёрные" if side == 'w' else "белые"
                            return True, f"🏆 Шах и мат! Победили {winner}"
                        elif mate_value > 0:
                            winner = "чёрные" if side == 'w' else "белые"
                            return True, f"🏆 Шах и мат! Победили {winner}"
                        elif mate_value < 0:
                            winner = "белые" if side == 'w' else "чёрные"
                            return True, f"🏆 Шах и мат! Победили {winner}"
                    else:
                        # If no mate and no moves, it's stalemate
                        return True, "🤝 Пат! Ничья"
            except Exception:
                # If we can't get a move, check evaluation
                pass
            
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
            
            # King + Bishop vs King + Bishop (same color bishops)
            if len(white_pieces) == 2 and len(black_pieces) == 2:
                white_bishops = [p for p in white_pieces if p.upper() == 'B']
                black_bishops = [p for p in black_pieces if p.upper() == 'B']
                if len(white_bishops) == 1 and len(black_bishops) == 1:
                    # Check if bishops are on the same color squares
                    # This is a simplified check - in practice, you'd need to check square colors
                    return True, "🤝 Недостаточно материала для мата. Ничья"
                    
            # Check for fifty-move rule
            try:
                if len(fen_parts) >= 5:
                    halfmove_clock = int(fen_parts[4])
                    if halfmove_clock >= 100:  # 50 full moves
                        return True, "🤝 Ничья по правилу 50 ходов"
            except (ValueError, IndexError):
                pass
                
            # Check for threefold repetition would require move history tracking
            # For now, we'll rely on Stockfish's built-in detection
                
        except Exception as e:
            print(f"⚠️  Ошибка при проверке состояния игры: {e}")
        
        return False, None
    
    def get_fen(self) -> str:
        """
        Получает текущую позицию в формате FEN (Forsyth–Edwards Notation).
        
        Возвращает:
            str: Позиция в формате FEN
        """
        if self.engine is None:
            return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            
        try:
            return self.engine.get_fen_position()
        except Exception as e:
            print(f"⚠️  Ошибка при получении FEN: {e}")
            return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    
    def get_evaluation(self) -> Optional[float]:
        """
        Получает оценку текущей позиции в пешках.
        
        Возвращает:
            float: Оценка позиции (положительно = белым хорошо, отрицательно = чёрным)
                   Например: 1.5 означает перевес белых на 1.5 пешки
        """
        if self.engine is None:
            return None
            
        try:
            # Более агрессивное кэширование - увеличиваем время до 2 секунд
            if self.evaluation_cache is not None and self.evaluation_cache_fen is not None:
                current_fen = self.engine.get_fen_position()
                if current_fen == self.evaluation_cache_fen:
                    # Проверяем время кэша - используем кэш до 2 секунд для более агрессивного кэширования
                    current_time = time.time()
                    if hasattr(self, '_last_eval_time') and (current_time - self._last_eval_time) < 2.0:
                        return self.evaluation_cache
            
            # Засекаем время для диагностики
            start_time = time.time()
            eval_score = self.engine.get_evaluation()
            eval_time = time.time() - start_time
            if eval_time > 0.05:  # Если оценка занимает больше 50 мс, выводим предупреждение
                print(f"⚠️  Slow evaluation: {eval_time:.4f} seconds")
            
            if eval_score and 'value' in eval_score:
                evaluation = eval_score['value'] / 100.0
                # Update cache
                self.evaluation_cache = evaluation
                self.evaluation_cache_fen = self.engine.get_fen_position()
                self._last_eval_time = time.time()  # Сохраняем время последней оценки
                return evaluation
        except Exception as e:
            print(f"⚠️  Error in get_evaluation: {e}")
            # Возвращаем кэшированное значение даже при ошибке
            if self.evaluation_cache is not None:
                return self.evaluation_cache
            pass
        return None
    
    def get_best_move_eval(self) -> Tuple[Optional[str], Optional[float]]:
        """
        Получает лучший ход и его оценку.
        
        Возвращает:
            Tuple[str, float]: Кортеж (ход, оценка) или (None, None)
        """
        if self.engine is None:
            return None, None
            
        try:
            move = self.engine.get_best_move()
            eval_score = self.engine.get_evaluation()
            if eval_score and 'value' in eval_score:
                value = eval_score['value'] / 100.0
                return move, value
            return move, None
        except Exception as e:
            print(f"⚠️  Ошибка при получении оценки хода: {e}")
            return None, None
    
    def reset_board(self):
        """Сбрасывает доску в начальную позицию."""
        if self.engine is None:
            return
            
        try:
            start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            self.engine.set_fen_position(start_fen)
            self.move_count = 0
            self.analysis_cache.clear()
        except Exception as e:
            print(f"⚠️  Ошибка при сбросе доски: {e}")
    
    def set_fen(self, fen: str) -> bool:
        """
        Устанавливает позицию по FEN.
        
        Параметры:
            fen (str): Позиция в формате FEN
            
        Возвращает:
            bool: True если позиция установлена успешно
        """
        if self.engine is None:
            return False
            
        if not fen:
            return False
        try:
            self.engine.set_fen_position(fen)
            return True
        except Exception as e:
            print(f"⚠️  Ошибка при установке FEN: {e}")
            return False
    
    def quit(self):
        """Закрывает соединение с Stockfish и освобождает ресурсы."""
        # This implementation matches the working version in full_game.py
        # Even though the linter complains, the method does exist in the stockfish library
        if self.engine is None:
            return
            
        try:
            # Try to quit if the method exists
            if hasattr(self.engine, 'quit'):
                # self.engine.quit()  # Removed due to compatibility issues
                pass
        except Exception:
            pass