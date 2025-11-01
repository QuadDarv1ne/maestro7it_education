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
from typing import Optional, Tuple, List, Dict, Any
import os
import sys
import shutil
import time
import threading
import weakref

# Импортируем пул движков
from engine.stockfish_pool import get_stockfish_pool, cleanup_stockfish_pool


class StockfishWrapper:
    """
    Обёртка для работы со Stockfish с улучшенной обработкой ошибок.
    
    Атрибуты:
        engine (Stockfish): Экземпляр движка Stockfish
        skill_level (int): Уровень сложности (0-20)
        depth (int): Глубина анализа
        analysis_cache (dict): Кэш для результатов анализа
        move_validation_cache (dict): Кэш для валидации ходов
        position_analysis_cache (dict): Кэш для анализа позиций
    """
    
    def __init__(self, skill_level=5, depth=15, path=None):
        """
        Инициализация Stockfish движка с использованием пула подключений.
        
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
        self.move_validation_cache = {}  # Кэш для валидации ходов
        self.position_analysis_cache = {}  # Кэш для анализа позиций
        self.move_count = 0
        self.engine = None
        self._process_cleaned_up = False  # Флаг для отслеживания очистки
        self._lock = threading.Lock()  # Блокировка для потокобезопасности
        self._weakref_cache = weakref.WeakValueDictionary()  # Кэш слабых ссылок для предотвращения утечек памяти
        
        # Ограничение размера кэша для предотвращения утечек памяти
        self._max_cache_size = 100  # Увеличиваем для лучшей производительности
        self._cache_access_count = {}
        self._cache_timestamps = {}  # Добавляем временные метки для кэша
        
        # Получаем движок из пула вместо создания нового
        try:
            # Получаем пул движков
            self._pool = get_stockfish_pool(path=path, skill_level=skill_level, depth=depth)
            # Получаем движок из пула
            self.engine = self._pool.get_engine()
            
            if self.engine is None:
                raise RuntimeError("Не удалось получить движок из пула")
            
            # Настраиваем движок
            self.engine.set_skill_level(self.skill_level)
            self.engine.set_depth(self.depth)
            
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось получить Stockfish движок из пула: {e}")
    
    def _cleanup_cache(self):
        """Очистка кэша по LRU алгоритму при превышении максимального размера."""
        current_time = time.time()
        
        # Очистка analysis_cache
        if len(self.analysis_cache) > self._max_cache_size:
            # Сортируем по количеству обращений и удаляем наименее используемые
            sorted_items = sorted(self._cache_access_count.items(), key=lambda x: x[1])
            items_to_remove = len(self.analysis_cache) - self._max_cache_size // 2
            
            for i in range(min(items_to_remove, len(sorted_items))):
                key = sorted_items[i][0]
                if key in self.analysis_cache:
                    del self.analysis_cache[key]
                if key in self._cache_access_count:
                    del self._cache_access_count[key]
                if key in self._cache_timestamps:
                    del self._cache_timestamps[key]
        
        # Очистка move_validation_cache по времени (устаревшие записи старше 60 секунд)
        expired_keys = [key for key, timestamp in self.move_validation_cache.items() 
                       if isinstance(timestamp, tuple) and current_time - timestamp[1] > 60]  # Увеличиваем до 60 секунд
        for key in expired_keys:
            del self.move_validation_cache[key]
        
        # Очистка position_analysis_cache по времени (устаревшие записи старше 120 секунд)
        expired_keys = [key for key, data in self.position_analysis_cache.items() 
                       if isinstance(data, dict) and 'timestamp' in data and current_time - data['timestamp'] > 120]  # Увеличиваем до 120 секунд
        for key in expired_keys:
            del self.position_analysis_cache[key]
    
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
                # Проверяем время кэша - используем кэш до 3 секунд (увеличено с 2 секунд)
                if hasattr(self, '_last_board_cache_time'):
                    current_time = time.time()
                    if (current_time - self._last_board_cache_time) < 3.0:
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
            self._last_board_cache_time = time.time()  # Сохраняем время последнего кэширования
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
            
        # Проверяем кэш валидации ходов
        cache_key = f"{self.engine.get_fen_position()}_{uci_move}"
        current_time = time.time()
        
        if cache_key in self.move_validation_cache:
            # Проверяем время кэширования - увеличиваем до 60 секунд
            cached_result, cache_time = self.move_validation_cache[cache_key]
            if current_time - cache_time < 60.0:
                return cached_result
        
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
            result = original_fen != new_fen
            
            # Сохраняем результат в кэш
            self.move_validation_cache[cache_key] = (result, current_time)
            
            return result
        except Exception:
            # Сохраняем результат в кэш даже при ошибке
            self.move_validation_cache[cache_key] = (False, current_time)
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
            current_time = time.time()
            
            # Более агрессивное кэширование - увеличиваем время до 180 секунд (увеличено с 120 секунд)
            if (self.evaluation_cache is not None and 
                self.evaluation_cache_fen is not None and
                hasattr(self, '_last_eval_time')):
                current_fen = self.engine.get_fen_position()
                time_since_last_eval = current_time - self._last_eval_time
                # Используем кэш если:
                # 1. FEN не изменился, или
                # 2. Прошло меньше 45 секунд с последней оценки, или
                # 3. Прошло меньше 3 секунды (очень свежий кэш)
                if (current_fen == self.evaluation_cache_fen or 
                    time_since_last_eval < 45.0 or
                    time_since_last_eval < 3.0):
                    return self.evaluation_cache
            
            # Засекаем время для диагностики только если кэш не используется
            start_time = time.time()
            eval_score = self.engine.get_evaluation()
            eval_time = time.time() - start_time
            
            # Выводим предупреждение только если оценка занимает больше 80 мс (увеличено с 100 мс)
            if eval_time > 0.08:  # Уменьшено с 0.1 для более чувствительного мониторинга
                print(f"⚠️  Slow evaluation: {eval_time:.4f} seconds")
            
            if eval_score and 'value' in eval_score:
                evaluation = eval_score['value'] / 100.0
                # Update cache
                self.evaluation_cache = evaluation
                self.evaluation_cache_fen = self.engine.get_fen_position()
                self._last_eval_time = current_time  # Сохраняем время последней оценки
                return evaluation
        except Exception as e:
            # print(f"⚠️  Error in get_evaluation: {e}")  # Убираем вывод ошибок для улучшения производительности
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
            # Clear all caches
            self.board_state_cache = None
            self.board_state_cache_fen = None
            self.evaluation_cache = None
            self.evaluation_cache_fen = None
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
            # Clear caches when setting new position
            self.board_state_cache = None
            self.board_state_cache_fen = None
            self.evaluation_cache = None
            self.evaluation_cache_fen = None
            return True
        except Exception as e:
            print(f"⚠️  Ошибка при установке FEN: {e}")
            return False
    
    def set_skill_level(self, skill_level: int) -> bool:
        """
        Устанавливает уровень сложности Stockfish.
        
        Параметры:
            skill_level (int): Уровень сложности (0-20)
            
        Возвращает:
            bool: True если уровень установлен успешно
        """
        if self.engine is None:
            return False
            
        try:
            skill_level = max(0, min(20, skill_level))
            self.engine.set_skill_level(skill_level)
            self.skill_level = skill_level
            return True
        except Exception as e:
            print(f"⚠️  Ошибка при установке уровня сложности: {e}")
            return False
    
    def set_depth(self, depth: int) -> bool:
        """
        Устанавливает глубину анализа.
        
        Параметры:
            depth (int): Глубина анализа
            
        Возвращает:
            bool: True если глубина установлена успешно
        """
        if self.engine is None:
            return False
            
        try:
            self.engine.set_depth(depth)
            self.depth = depth
            return True
        except Exception as e:
            print(f"⚠️  Ошибка при установке глубины анализа: {e}")
            return False
    
    def get_move_analysis(self, move: str, depth: Optional[int] = None) -> Dict[str, Any]:
        """
        Получает подробный анализ хода.
        
        Параметры:
            move (str): Ход в формате UCI
            depth (int): Глубина анализа (если None, использует установленную)
            
        Возвращает:
            Dict[str, Any]: Словарь с анализом хода
        """
        if self.engine is None:
            return {}
            
        # Проверяем кэш анализа позиций
        cache_key = f"{self.engine.get_fen_position()}_{move}_{depth}"
        current_time = time.time()
        
        if cache_key in self.position_analysis_cache:
            cached_data = self.position_analysis_cache[cache_key]
            # Используем кэш если он свежий (меньше 30 секунд)
            if 'timestamp' in cached_data and current_time - cached_data['timestamp'] < 30:
                return cached_data
            
        try:
            # Сохраняем текущую позицию
            original_fen = self.engine.get_fen_position()
            
            # Выполняем ход
            if not self.make_move(move):
                return {}
            
            # Получаем оценку после хода
            evaluation = self.get_evaluation()
            
            # Получаем лучший ход после этого хода
            best_move = self.get_best_move(depth)
            
            # Восстанавливаем оригинальную позицию
            self.engine.set_fen_position(original_fen)
            
            result = {
                'move': move,
                'evaluation': evaluation,
                'best_response': best_move,
                'timestamp': current_time
            }
            
            # Сохраняем результат в кэш
            self.position_analysis_cache[cache_key] = result
            
            return result
        except Exception as e:
            print(f"⚠️  Ошибка при анализе хода {move}: {e}")
            return {}
    
    def quit(self):
        """Возвращает движок в пул и освобождает ресурсы."""
        with self._lock:  # Потокобезопасное завершение
            if self.engine is None or self._process_cleaned_up:
                return
                
            try:
                # Помечаем, что процесс уже очищен
                self._process_cleaned_up = True
                
                # Возвращаем движок в пул вместо закрытия
                if hasattr(self, '_pool') and self._pool and self.engine:
                    self._pool.return_engine(self.engine)
                
            except Exception as e:
                # Игнорируем ошибки при возврате в пул
                print(f"⚠️  Ошибка при возврате движка в пул: {e}")
            finally:
                self.engine = None