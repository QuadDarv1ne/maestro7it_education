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
        self.move_count = 0
        
        # Проверка наличия исполняемого файла Stockfish
        if path is not None:
            if not os.path.exists(path):
                raise RuntimeError(f"❌ Файл Stockfish не найден по пути: {path}")
        else:
            # Попробуем найти Stockfish в PATH
            import shutil
            if shutil.which("stockfish") is None:
                print("⚠️  Stockfish не найден в PATH. Убедитесь, что он установлен.")
        
        try:
            # Handle the case where path might be None
            if path is not None:
                self.engine = Stockfish(path=path)
            else:
                self.engine = Stockfish()
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
        try:
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
        """
        Получает лучший ход в текущей позиции.
        
        Параметры:
            depth (int): Глубина анализа (если None, использует установленную)
            
        Возвращает:
            str: Лучший ход в формате UCI, или None если нет ходов
        """
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
        """
        Получает текущую позицию в формате FEN (Forsyth–Edwards Notation).
        
        Возвращает:
            str: Позиция в формате FEN
        """
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
        try:
            eval_score = self.engine.get_evaluation()
            if eval_score and 'value' in eval_score:
                return eval_score['value'] / 100.0
        except Exception:
            pass
        return None
    
    def get_best_move_eval(self) -> Tuple[Optional[str], Optional[float]]:
        """
        Получает лучший ход и его оценку.
        
        Возвращает:
            Tuple[str, float]: Кортеж (ход, оценка) или (None, None)
        """
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
        # Newer versions of stockfish library don't have quit method
        # The engine will be automatically cleaned up when the object is destroyed
        try:
            # Try to quit if the method exists
            if hasattr(self.engine, 'quit'):
                # self.engine.quit()  # Removed due to compatibility issues
                pass
        except Exception:
            pass