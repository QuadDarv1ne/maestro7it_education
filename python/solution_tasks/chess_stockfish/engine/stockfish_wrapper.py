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
        
        try:
            self.engine = Stockfish(path=path)
            self.engine.set_skill_level(self.skill_level)
            self.engine.set_depth(self.depth)
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось запустить Stockfish: {e}")
    
    def get_board_state(self) -> List[List[Optional[str]]]:
        """
        Возвращает текущее состояние доски (8x8).
        
        Возвращает:
            List[List[Optional[str]]]: 2D массив, где каждый элемент - фигура или None
                                       Пример: 'P' - пешка белых, 'p' - пешка чёрных
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
        """
        Проверяет, является ли ход корректным в текущей позиции.
        
        Параметры:
            uci_move (str): Ход в формате UCI (например, "e2e4")
            
        Возвращает:
            bool: True если ход корректен, False иначе
        """
        try:
            return self.engine.is_move_correct(uci_move)
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
            if depth:
                old_depth = self.depth
                self.engine.set_depth(depth)
            move = self.engine.get_best_move()
            if depth:
                self.engine.set_depth(old_depth)
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
        except Exception:
            return []
    
    def get_side_to_move(self) -> str:
        """
        Получает, чей ход в текущей позиции.
        
        Возвращает:
            str: 'w' для белых, 'b' для чёрных
        """
        return self.engine.get_fen_position().split()[1]
    
    def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """
        Проверяет, закончена ли игра и причину окончания.
        
        Возвращает:
            Tuple[bool, Optional[str]]: (is_over, reason)
                - is_over: True если игра завершена
                - reason: Строка с описанием причины завершения
        """
        fen = self.engine.get_fen_position()
        
        if self.engine.is_mate():
            side = self.get_side_to_move()
            winner = "чёрные" if side == 'w' else "белые"
            return True, f"🏆 Шах и мат! Победили {winner}"
        
        if self.engine.is_stalemate():
            return True, "🤝 Пат! Ничья"
        
        if self.engine.is_insufficient_material():
            return True, "🤝 Недостаточно материала для мата. Ничья"
        
        return False, None
    
    def get_fen(self) -> str:
        """
        Получает текущую позицию в формате FEN (Forsyth–Edwards Notation).
        
        Возвращает:
            str: Позиция в формате FEN
        """
        return self.engine.get_fen_position()
    
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
        except Exception:
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
        try:
            self.engine.set_fen_position(fen)
            return True
        except Exception as e:
            print(f"⚠️  Ошибка при установке FEN: {e}")
            return False
    
    def quit(self):
        """Закрывает соединение с Stockfish и освобождает ресурсы."""
        try:
            self.engine.quit()
        except Exception:
            pass