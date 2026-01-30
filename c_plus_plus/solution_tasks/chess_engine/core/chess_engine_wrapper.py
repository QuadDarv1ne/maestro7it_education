#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import os
import sys
from typing import Tuple, List, Optional

class ChessEngineWrapper:
    """Python wrapper для С++ шахматного движка"""
    
    def __init__(self):
        self.lib = None
        self.board_state = self.get_initial_board()
        self.current_turn = True  # True = белые, False = черные
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.game_stats = {'moves_count': 0, 'captures_count': 0, 'check_count': 0}
        self.game_active = True
        self.selected_square = None
        self.valid_moves = []
        
        # Рокировка и специальные ходы
        self.castling_rights = {
            'white_kingside': True,
            'white_queenside': True,
            'black_kingside': True,
            'black_queenside': True
        }
        self.king_moved = {'white': False, 'black': False}
        self.rook_moved = {
            'white_kingside': False,
            'white_queenside': False,
            'black_kingside': False,
            'black_queenside': False
        }
        self.en_passant_target = None
        
        # Интеграция оптимизированных компонентов
        # ВРЕМЕННО ОТКЛЮЧЕНО: BitboardMoveGenerator вызывает проблемы с валидацией
        # try:
        #     from core.optimized_move_generator import BitboardMoveGenerator
        #     self.move_gen = BitboardMoveGenerator()
        # except ImportError:
        #     try:
        #         from .optimized_move_generator import BitboardMoveGenerator
        #         self.move_gen = BitboardMoveGenerator()
        #     except ImportError:
        #         self.move_gen = None
        self.move_gen = None  # Используем только Python валидацию
            
        # ВРЕМЕННО ОТКЛЮЧЕНО: EnhancedChessAI вызывает циклическую зависимость
        # try:
        #     from core.enhanced_chess_ai import EnhancedChessAI
        #     self.ai = EnhancedChessAI(search_depth=4)
        # except ImportError:
        #     try:
        #         from .enhanced_chess_ai import EnhancedChessAI
        #         self.ai = EnhancedChessAI(search_depth=4)
        #     except ImportError:
        #         self.ai = None
        self.ai = None  # Используем базовый AI
        
    def initialize_engine(self) -> bool:
        """Инициализация С++ библиотеки движка"""
        try:
            # Попытка загрузить скомпилированную библиотеку
            if os.name == 'nt':  # Windows
                lib_name = 'chess_engine.dll'
            else:  # Linux/Mac
                lib_name = 'libchess_engine.so'
            
            lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'build_gui', lib_name)
            if os.path.exists(lib_path):
                self.lib = ctypes.CDLL(lib_path)
                print("С++ движок успешно загружен")
                return True
            else:
                print("Библиотека движка не найдена, используем Python реализацию")
                return False
        except Exception as e:
            print(f"Ошибка загрузки движка: {e}")
            return False
    
    def get_initial_board(self) -> List[List[str]]:
        """Начальная позиция шахматной доски"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def get_game_statistics(self) -> dict:
        """Получение статистики текущей игры"""
        stats = self.game_stats.copy()
        if self.ai:
            stats['ai_nodes'] = self.nodes_searched = getattr(self.ai, 'nodes_searched', 0)
            stats['ai_tt_hits'] = getattr(self.ai, 'tt_hits', 0)
        return stats
    
    def is_checkmate(self, is_white: bool) -> bool:
        """Эффективная проверка мата"""
        # Если нет шаха, то и мата нет
        if not self.is_king_in_check(is_white):
            return False
        
        # Проверяем, есть ли хоть один легальный ход
        if self.move_gen:
            legal_moves = self.move_gen.generate_legal_moves(self.board_state, is_white)
            return len(legal_moves) == 0
        
        return False
    
    def is_stalemate(self, is_white: bool) -> bool:
        """Эффективная проверка пата"""
        # Если есть шах, то пата нет
        if self.is_king_in_check(is_white):
            return False
        
        # Проверяем, есть ли хоть один легальный ход
        if self.move_gen:
            legal_moves = self.move_gen.generate_legal_moves(self.board_state, is_white)
            return len(legal_moves) == 0
        
        return False
    
    def get_game_status(self) -> str:
        """Получение статуса игры (продолжается, мат, пат, ничья)"""
        current_color = self.current_turn
        
        # Проверка мата
        if self.is_checkmate(current_color):
            winner = "Черные" if current_color else "Белые"
            return f"Мат! Победа: {winner}"
        
        # Проверка пата
        if self.is_stalemate(current_color):
            return "Пат! Ничья"
        
        # Проверка шаха
        if self.is_king_in_check(current_color):
            return "Шах!"
        
        return "Игра продолжается"
    
    def board_to_fen(self) -> str:
        """Преобразование доски в FEN нотацию"""
        fen = ""
        for row in self.board_state:
            empty_count = 0
            for piece in row:
                if piece == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += piece
            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"
        fen = fen[:-1]  # Убираем последний слеш
        
        # Добавляем информацию о ходе
        fen += " w " if self.current_turn else " b "
        fen += "KQkq - 0 1"  # Права рокировки, en passant, счетчики
        return fen
    
    def get_evaluation(self) -> int:
        """Получение численной оценки текущей позиции"""
        if self.ai:
            return self.ai.evaluate_position(self.board_state)
        return 0

    def save_game(self, filename: str) -> bool:
        """Сохранение игры в JSON файл"""
        try:
            import json
            data = {
                'board_state': self.board_state,
                'current_turn': self.current_turn,
                'move_history': self.move_history,
                'captured_pieces': self.captured_pieces,
                'game_stats': self.game_stats
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False

    def load_game(self, filename: str) -> bool:
        """Загрузка игры из JSON файла"""
        try:
            import json
            if not os.path.exists(filename):
                return False
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.board_state = data['board_state']
            self.current_turn = data['current_turn']
            self.move_history = data.get('move_history', [])
            self.captured_pieces = data.get('captured_pieces', {'white': [], 'black': []})
            self.game_stats = data.get('game_stats', {'moves_count': 0, 'captures_count': 0, 'check_count': 0})
            
            # Сброс временных состояний
            self.selected_square = None
            self.valid_moves = []
            
            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False

    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка допустимости хода через оптимизированный движок, С++ или Python"""
        # Сначала пробуем BitboardMoveGenerator
        if self.move_gen:
            try:
                # Bitboard generator usually returns all legal moves, 
                # but we can use it to check a specific move
                legal_moves = self.move_gen.generate_legal_moves(self.board_state, self.current_turn)
                return (from_pos, to_pos) in legal_moves
            except Exception as e:
                print(f"Ошибка Bitboard MoveGen: {e}")
        
        # Резервные варианты
        try:
            return self.is_valid_move_cpp(from_pos, to_pos)
        except:
            return self.is_valid_move_python(from_pos, to_pos)
    
    def is_valid_move_cpp(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка хода через С++ движок"""
        if self.lib is None:
            raise Exception("С++ библиотека не загружена")
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        result = self.lib.is_valid_move(
            self.engine_ptr,
            from_row, from_col,
            to_row, to_col
        )
        return bool(result)
    
    def is_valid_move_python(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], debug: bool = False) -> bool:
        """Python реализация проверки хода с отладкой"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        target_piece = self.board_state[to_row][to_col]
        
        if debug:
            print(f"Проверка хода: {piece} с ({from_row},{from_col}) на ({to_row},{to_col})")
            print(f"Целевая клетка: '{target_piece}'")
        
        # Проверка цвета фигуры
        is_white_piece = piece.isupper()
        if debug:
            print(f"Белая фигура: {is_white_piece}, Очередь белых: {self.current_turn}")
        
        if (is_white_piece and not self.current_turn) or (not is_white_piece and self.current_turn):
            if debug:
                print("Неправильная очередь хода!")
            return False
            
        # Проверка выхода за границы
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            if debug:
                print("Выход за границы доски!")
            return False
            
        # Проверка на то же поле
        if from_pos == to_pos:
            if debug:
                print("Нельзя ходить на ту же клетку!")
            return False
            
        # Проверка, что нельзя съесть свою фигуру
        if target_piece != '.' and ((target_piece.isupper() and is_white_piece) or 
                                   (target_piece.islower() and not is_white_piece)):
            if debug:
                print("Нельзя съесть свою фигуру!")
            return False
            
        # Проверка, что нельзя съесть короля
        if target_piece.lower() == 'k':
            if debug:
                print("Нельзя съесть короля!")
            return False
            
        piece_type = piece.lower()
        if debug:
            print(f"Тип фигуры: {piece_type}")
        
        # Логика для пешки
        if piece_type == 'p':
            direction = -1 if is_white_piece else 1
            start_row = 6 if is_white_piece else 1
            if debug:
                print(f"Пешка: направление={direction}, начальная строка={start_row}")
            
            # Ход вперед на одну клетку
            if from_col == to_col and to_row == from_row + direction and target_piece == '.':
                if debug:
                    print("Допустимый ход пешки вперед")
                return True
                
            # Двойной ход с начальной позиции
            if (from_row == start_row and from_col == to_col and 
                to_row == from_row + 2 * direction and 
                target_piece == '.' and self.board_state[from_row + direction][from_col] == '.'):
                if debug:
                    print("Допустимый двойной ход пешки")
                return True
                
            # Взятие по диагонали
            if (abs(from_col - to_col) == 1 and to_row == from_row + direction and 
                target_piece != '.' and target_piece.isupper() != is_white_piece):
                if debug:
                    print("Допустимое взятие пешкой")
                return True
                
        # Логика для ладьи
        elif piece_type == 'r':
            result = self.is_straight_move(from_pos, to_pos)
            if debug:
                print(f"Ладья: прямой ход = {result}")
            return result
            
        # Логика для слона
        elif piece_type == 'b':
            result = self.is_diagonal_move(from_pos, to_pos)
            if debug:
                print(f"Слон: диагональный ход = {result}")
            return result
            
        # Логика для ферзя
        elif piece_type == 'q':
            straight = self.is_straight_move(from_pos, to_pos)
            diagonal = self.is_diagonal_move(from_pos, to_pos)
            result = straight or diagonal
            if debug:
                print(f"Ферзь: прямой={straight}, диагональный={diagonal}, результат={result}")
            return result
            
        # Логика для короля
        elif piece_type == 'k':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            if debug:
                print(f"Король: разница строк={row_diff}, столбцов={col_diff}")
            
            # Проверка рокировки
            if row_diff == 0 and col_diff == 2:
                return self.is_castling_valid(from_pos, to_pos, is_white_piece)
            
            # Король может ходить только на одну клетку
            if row_diff <= 1 and col_diff <= 1:
                # Проверяем, не попадает ли под атаку
                attacked = self.would_king_be_attacked(from_pos, to_pos, is_white_piece)
                if debug:
                    print(f"Король под атакой после хода: {attacked}")
                return not attacked
            
        # Логика для коня
        elif piece_type == 'n':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            result = (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
            if debug:
                print(f"Конь: разница строк={row_diff}, столбцов={col_diff}, результат={result}")
            return result
            
        if debug:
            print("Ход не соответствует правилам!")
        return False
    
    def is_straight_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка прямого хода (ладья, ферзь)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверка прямой линии
        if from_row != to_row and from_col != to_col:
            return False
        
        # Проверка пути
        if from_row == to_row:  # Горизонталь
            step = 1 if from_col < to_col else -1
            for col in range(from_col + step, to_col, step):
                if self.board_state[from_row][col] != '.':
                    return False
        else:  # Вертикаль
            step = 1 if from_row < to_row else -1
            for row in range(from_row + step, to_row, step):
                if self.board_state[row][from_col] != '.':
                    return False
        
        return True
    
    def is_diagonal_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка диагонального хода (слон, ферзь)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверка диагонали
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        
        # Проверка пути
        row_step = 1 if from_row < to_row else -1
        col_step = 1 if from_col < to_col else -1
        
        row, col = from_row + row_step, from_col + col_step
        while row != to_row and col != to_col:
            if self.board_state[row][col] != '.':
                return False
            row += row_step
            col += col_step
        
        return True
    
    def is_castling_valid(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool) -> bool:
        """Проверка возможности рокировки"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Определяем тип рокировки
        kingside = to_col > from_col
        color = 'white' if is_white else 'black'
        
        # Проверка прав на рокировку
        if kingside:
            if not self.castling_rights[f'{color}_kingside']:
                return False
            rook_col = 7
        else:
            if not self.castling_rights[f'{color}_queenside']:
                return False
            rook_col = 0
        
        # Проверка что король не под шахом
        if self.is_king_in_check(is_white):
            return False
        
        # Проверка пути (должен быть свободен)
        step = 1 if kingside else -1
        for col in range(from_col + step, to_col + step, step):
            if self.board_state[from_row][col] != '.':
                return False
            
            # Проверяем что король не проходит через атакованное поле
            if col != to_col + step:  # Не проверяем поле за королем
                if self.is_square_under_attack((from_row, col), not is_white):
                    return False
        
        # Проверка наличия ладьи
        rook_piece = 'R' if is_white else 'r'
        if self.board_state[from_row][rook_col] != rook_piece:
            return False
        
        return True
    
    def is_square_under_attack(self, square: Tuple[int, int], by_white: bool) -> bool:
        """Проверка атаки клетки"""
        target_row, target_col = square
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.isupper() == by_white:
                    # Проверяем может ли фигура атаковать клетку
                    if self.can_piece_attack((row, col), square, piece):
                        return True
        return False
    
    def can_piece_attack(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], piece: str) -> bool:
        """Проверяет может ли фигура атаковать клетку"""
        piece_type = piece.lower()
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if piece_type == 'p':
            direction = -1 if piece.isupper() else 1
            return abs(from_col - to_col) == 1 and to_row == from_row + direction
        elif piece_type == 'n':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        elif piece_type == 'b':
            return self.is_diagonal_move(from_pos, to_pos)
        elif piece_type == 'r':
            return self.is_straight_move(from_pos, to_pos)
        elif piece_type == 'q':
            return self.is_straight_move(from_pos, to_pos) or self.is_diagonal_move(from_pos, to_pos)
        elif piece_type == 'k':
            return abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1
        return False
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Выполнение хода с отладкой"""
        print(f"\n=== ПОПЫТКА ХОДА ===")
        print(f"Из: {from_pos}, В: {to_pos}")
        print(f"Очередь белых: {self.current_turn}")
        
        if not self.is_valid_move(from_pos, to_pos):
            print("Ход НЕДОПУСТИМ!")
            return False
        
        print("Ход ДОПУСТИМ!")
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board_state[from_row][from_col]
        captured = self.board_state[to_row][to_col]
        
        print(f"Фигура: {piece}, Захват: '{captured}'")
        
        # Запись в историю
        move_notation = f"{piece}{chr(97+from_col)}{8-from_row}-{chr(97+to_col)}{8-to_row}"
        if captured != '.':
            move_notation += f"x{captured}"
            self.captured_pieces['white' if captured.isupper() else 'black'].append(captured)
            self.game_stats['captures_count'] += 1
        
        # Проверяем наличие move_history
        if not hasattr(self, 'move_history'):
            self.move_history = []
        self.move_history.append(move_notation)
        print(f"Ход записан: {move_notation}")
        
        # Выполнение хода
        print("Выполняю ход...")
        # Используем Python реализацию вместо С++
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        print("Ход выполнен успешно!")
        
        # Проверка шаха
        if self.is_king_in_check(not self.current_turn):
            self.game_stats['check_count'] += 1
            print("ШАХ!")
        
        # Смена очереди
        self.current_turn = not self.current_turn
        print(f"Очередь перешла: {'белым' if self.current_turn else 'черным'}")
        
        # Сброс выбора
        self.selected_square = None
        self.valid_moves = []
        
        # Проверка окончания игры
        if self.is_checkmate(self.current_turn):
            self.game_active = False
            winner = "Черные" if self.current_turn else "Белые"
            print(f"МАТ! Победили {winner}")
        elif self.is_stalemate(self.current_turn):
            self.game_active = False
            print("ПАТ! Ничья")
        
        print("=== ХОД ЗАВЕРШЕН ===\n")
        return True
    
    def get_best_move(self, depth: int = 3) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Получение лучшего хода для AI (использует Enhanced AI если доступен)"""
        if self.ai:
            try:
                self.ai.search_depth = depth
                return self.ai.get_best_move(self.board_state, self.current_turn)
            except Exception as e:
                print(f"Ошибка Enhanced AI: {e}")
        
        # Резервный вариант из старой реализации
        try:
            # Импортируем продвинутый ИИ
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
            
            try:
                from advanced_ai import AdvancedChessAI
                ai = AdvancedChessAI(search_depth=depth, time_limit=3000)
                
                # Преобразуем доску в формат AI
                ai_board = [[cell for cell in row] for row in self.board_state]
                
                # Получаем лучший ход
                best_move = ai.get_best_move(ai_board, not self.current_turn)  # AI играет за черных
                
                if best_move:
                    stats = ai.get_statistics()
                    print(f"AI: Рассмотрено {stats['nodes_searched']:,} узлов, TT hits: {stats['tt_hits']}")
                    return best_move
                
            except ImportError:
                print("Продвинутый ИИ не доступен, используем улучшенный базовый")
                pass
            
            # Улучшенный резервный вариант - с приоритетом взятий
            possible_moves = []
            capture_moves = []
            
            # AI играет за черных (если current_turn=False)
            ai_is_white = not self.current_turn
            
            for row in range(8):
                for col in range(8):
                    piece = self.board_state[row][col]
                    if piece == '.':
                        continue
                    
                    # Проверяем, что это фигура AI
                    piece_is_white = piece.isupper()
                    if piece_is_white != ai_is_white:
                        continue
                    
                    # Генерируем ходы только для фигур AI
                    for to_row in range(8):
                        for to_col in range(8):
                            if (row, col) == (to_row, to_col):
                                continue
                            
                            # Быстрая предварительная проверка
                            target = self.board_state[to_row][to_col]
                            if target != '.' and (target.isupper() == piece_is_white):
                                continue  # Не можем съесть свою фигуру
                            
                            # Временно меняем очередь для проверки
                            original_turn = self.current_turn
                            self.current_turn = ai_is_white
                            
                            if self.is_valid_move_python((row, col), (to_row, to_col)):
                                move = ((row, col), (to_row, to_col))
                                if target != '.':
                                    capture_moves.append(move)  # Приоритет взятиям
                                else:
                                    possible_moves.append(move)
                            
                            self.current_turn = original_turn
            
            # Приоритет взятиям, потом обычным ходам
            all_moves = capture_moves + possible_moves
            
            if not all_moves:
                return None
            
            # Выбираем первый ход (лучше взятие если есть)
            import random
            if capture_moves:
                return capture_moves[0]  # Берем первое взятие
            else:
                return random.choice(possible_moves)  # Случайный ход
            
        except Exception as e:
            print(f"Ошибка в get_best_move: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def is_king_in_check(self, king_color: bool) -> bool:
        """Проверка, находится ли король под шахом"""
        # Находим положение короля
        king_piece = 'K' if king_color else 'k'
        king_pos = None
        
        for row in range(8):
            for col in range(8):
                if self.board_state[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
            
        # Проверяем, может ли какая-либо вражеская фигура атаковать короля
        opponent_color = not king_color
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and ((piece.isupper() and not king_color) or 
                                   (piece.islower() and king_color)):
                    # Временно меняем очередь хода для проверки
                    original_turn = self.current_turn
                    self.current_turn = opponent_color
                    if self.is_valid_attack((row, col), king_pos):
                        self.current_turn = original_turn
                        return True
                    self.current_turn = original_turn
        
        return False
    
    def would_still_be_in_check(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], king_color: bool) -> bool:
        """Проверка, будет ли король все еще под шахом после хода"""
        # Сохраняем текущее состояние
        original_board = [row[:] for row in self.board_state]
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Делаем временный ход
        piece = self.board_state[from_row][from_col]
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        # Проверяем шах
        in_check = self.is_king_in_check(king_color)
        
        # Восстанавливаем доску
        self.board_state = original_board
        
        return in_check
    
    def would_king_be_attacked(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], king_color: bool) -> bool:
        """Проверка, будет ли король атакован после хода"""
        # Сохраняем текущее состояние
        original_board = [row[:] for row in self.board_state]
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Делаем временный ход
        piece = self.board_state[from_row][from_col]
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        # Находим положение короля
        king_piece = 'K' if king_color else 'k'
        king_pos = None
        for row in range(8):
            for col in range(8):
                if self.board_state[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            # Восстанавливаем доску
            self.board_state = original_board
            return False
        
        # Проверяем, может ли какая-либо вражеская фигура атаковать короля
        opponent_color = not king_color
        attacked = False
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and ((piece.isupper() and not king_color) or 
                                   (piece.islower() and king_color)):
                    # Временно меняем очередь хода для проверки
                    original_turn = self.current_turn
                    self.current_turn = opponent_color
                    if self.is_valid_attack((row, col), king_pos):
                        attacked = True
                        self.current_turn = original_turn
                        break
                    self.current_turn = original_turn
            if attacked:
                break
        
        # Восстанавливаем доску
        self.board_state = original_board
        return attacked
        """Проверка, может ли фигура атаковать позицию (без проверки цвета)"""
    def is_valid_attack(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка, может ли фигура атаковать позицию (без проверки цвета)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        piece_type = piece.lower()
        
        # Не может атаковать саму себя или пустую клетку
        if from_pos == to_pos:
            return False
            
        # Логика атаки для разных фигур
        if piece_type == 'p':  # Пешка
            direction = -1 if piece.isupper() else 1
            return (abs(from_col - to_col) == 1 and to_row == from_row + direction)
            
        elif piece_type == 'r':  # Ладья
            return self.is_straight_move(from_pos, to_pos)
            
        elif piece_type == 'b':  # Слон
            return self.is_diagonal_move(from_pos, to_pos)
            
        elif piece_type == 'q':  # Ферзь
            return self.is_straight_move(from_pos, to_pos) or self.is_diagonal_move(from_pos, to_pos)
            
        elif piece_type == 'k':  # Король
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return row_diff <= 1 and col_diff <= 1
            
        elif piece_type == 'n':  # Конь
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
            
        return False
    
    def is_straight_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка прямого хода (ладья, ферзь)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Движение по горизонтали
        if from_row == to_row:
            start_col = min(from_col, to_col)
            end_col = max(from_col, to_col)
            for col in range(start_col + 1, end_col):
                if self.board_state[from_row][col] != '.':
                    return False
            return True
        
        # Движение по вертикали
        elif from_col == to_col:
            start_row = min(from_row, to_row)
            end_row = max(from_row, to_row)
            for row in range(start_row + 1, end_row):
                if self.board_state[row][from_col] != '.':
                    return False
            return True
        
        return False
    
    def is_diagonal_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка диагонального хода (слон, ферзь)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        # Должно быть равное количество шагов по строкам и столбцам
        if row_diff != col_diff:
            return False
        
        # Проверяем путь
        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1
        
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while current_row != to_row and current_col != to_col:
            if self.board_state[current_row][current_col] != '.':
                return False
            current_row += row_step
            current_col += col_step
        
        return True
    
    def get_best_move_python(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Python реализация поиска лучшего хода (резервный вариант)"""
        # Простой алгоритм: найти случайный допустимый ход для черных
        import random
        
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.islower():  # Черная фигура
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move_python((row, col), (to_row, to_col)):
                                possible_moves.append(((row, col), (to_row, to_col)))
        
        return random.choice(possible_moves) if possible_moves else None


class OptimizedChessEngine:
    """Оптимизированный шахматный движок"""
    
    def __init__(self):
        self.board_state = self.get_initial_board()
        self.current_turn = True  # True = белые, False = черные
        self.move_history = []
        self.captured_pieces = []
        
        # Оптимизация: кэширование
        self.move_cache = {}  # Кэш допустимых ходов
        self.attack_cache = {}  # Кэш атак
        self.position_hash = None  # Хэш позиции для быстрого сравнения
        self.update_position_hash()
    
    def get_initial_board(self):
        """Начальная позиция шахматной доски"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def update_position_hash(self):
        """Обновление хэша позиции для быстрого сравнения"""
        board_str = ''.join(''.join(row) for row in self.board_state)
        self.position_hash = hash(board_str + str(self.current_turn))
    
    def get_cached_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Получение кэшированных допустимых ходов"""
        cache_key = (pos, self.position_hash)
        if cache_key in self.move_cache:
            return self.move_cache[cache_key]
        
        # Вычисляем и кэшируем
        moves = self.calculate_valid_moves(pos)
        self.move_cache[cache_key] = moves
        return moves
    
    def calculate_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Вычисление допустимых ходов без кэширования"""
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(pos, (row, col)):
                    valid_moves.append((row, col))
        return valid_moves
    
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Оптимизированная проверка допустимости хода"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Быстрая проверка граничных условий
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 
                0 <= to_row < 8 and 0 <= to_col < 8):
            return False
        
        piece = self.board_state[from_row][from_col]
        if piece == '.':
            return False
        
        # Проверка очереди хода
        is_white = piece.isupper()
        if (is_white and not self.current_turn) or (not is_white and self.current_turn):
            return False
        
        target = self.board_state[to_row][to_col]
        
        # Проверка на то же поле
        if from_pos == to_pos:
            return False
        
        # Проверка своей фигуры
        if target != '.' and ((target.isupper() and is_white) or 
                             (target.islower() and not is_white)):
            return False
        
        # Проверка короля
        if target.lower() == 'k':
            return False
        
        # Оптимизированная проверка фигур
        return self.check_piece_movement(piece, from_pos, to_pos)
    
    def check_piece_movement(self, piece: str, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Оптимизированная проверка движения конкретной фигуры"""
        piece_type = piece.lower()
        
        if piece_type == 'p':  # Пешка
            return self.is_valid_pawn_move(from_pos, to_pos, piece.isupper())
        elif piece_type == 'r':  # Ладья
            return self.is_straight_move(from_pos, to_pos)
        elif piece_type == 'b':  # Слон
            return self.is_diagonal_move(from_pos, to_pos)
        elif piece_type == 'q':  # Ферзь
            return self.is_straight_move(from_pos, to_pos) or self.is_diagonal_move(from_pos, to_pos)
        elif piece_type == 'k':  # Король
            row_diff = abs(to_pos[0] - from_pos[0])
            col_diff = abs(to_pos[1] - from_pos[1])
            return row_diff <= 1 and col_diff <= 1
        elif piece_type == 'n':  # Конь
            row_diff = abs(to_pos[0] - from_pos[0])
            col_diff = abs(to_pos[1] - from_pos[1])
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        
        return False
    
    def is_valid_pawn_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool) -> bool:
        """Оптимизированная проверка хода пешки"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        
        target = self.board_state[to_row][to_col]
        
        # Ход вперед
        if from_col == to_col:
            if to_row == from_row + direction and target == '.':
                return True
            # Двойной ход
            if (from_row == start_row and to_row == from_row + 2 * direction and 
                target == '.' and self.board_state[from_row + direction][from_col] == '.'):
                return True
        
        # Взятие
        elif abs(from_col - to_col) == 1 and to_row == from_row + direction:
            return target != '.' and target.isupper() != is_white
        
        return False
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Оптимизированное выполнение хода"""
        if not self.is_valid_move(from_pos, to_pos):
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Выполнение хода
        piece = self.board_state[from_row][from_col]
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        # Обновление состояния
        self.current_turn = not self.current_turn
        self.move_history.append((from_pos, to_pos))
        
        # Очистка кэша (позиция изменилась)
        self.move_cache.clear()
        self.attack_cache.clear()
        self.update_position_hash()
        
        return True
    
    def get_best_move(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Оптимизированный поиск лучшего хода"""
        # Приоритетизация ходов для производительности
        priority_moves = []
        regular_moves = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.islower():  # Черные фигуры
                    moves = self.get_cached_valid_moves((row, col))
                    for move in moves:
                        # Приоритет взятий
                        if self.board_state[move[0]][move[1]] != '.':
                            priority_moves.append(((row, col), move))
                        else:
                            regular_moves.append(((row, col), move))
        
        # Сначала проверяем приоритетные ходы
        all_moves = priority_moves + regular_moves
        return all_moves[0] if all_moves else None


class AdvancedChessEngine(OptimizedChessEngine):
    """Продвинутый шахматный движок с полными правилами"""
    
    def __init__(self):
        super().__init__()
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.king_positions = {'K': (7, 4), 'k': (0, 4)}
    
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Расширенная проверка допустимости хода с особыми правилами"""
        if not super().is_valid_move(from_pos, to_pos):
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board_state[from_row][from_col]
        piece_type = piece.lower()
        
        # Проверка рокировки
        if piece_type == 'k' and abs(from_col - to_col) == 2:
            return self.is_valid_castling(from_pos, to_pos, piece.isupper())
        
        # Проверка взятия на проходе
        if piece_type == 'p' and from_col != to_col and self.board_state[to_row][to_col] == '.':
            return self.is_valid_en_passant(from_pos, to_pos, piece.isupper())
        
        # Проверка пешки на последней горизонтали (промоция)
        if piece_type == 'p' and (to_row == 0 or to_row == 7):
            return self.is_valid_pawn_promotion(from_pos, to_pos, piece.isupper())
        
        return True
    
    def is_valid_castling(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool) -> bool:
        """Проверка допустимости рокировки"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Определение типа рокировки
        king_side = to_col > from_col
        rights_key = 'K' if is_white else 'k' if king_side else 'Q' if is_white else 'q'
        
        # Проверка прав на рокировку
        if not self.castling_rights[rights_key]:
            return False
        
        # Проверка, что король не под шахом
        if self.is_king_in_check(is_white):
            return False
        
        # Проверка пути (должен быть свободен)
        step = 1 if king_side else -1
        for col in range(from_col + step, to_col, step):
            if self.board_state[from_row][col] != '.':
                return False
            # Проверка, что король не проходит через атакованное поле
            if self.is_square_attacked((from_row, col), not is_white):
                return False
        
        return True
    
    def is_valid_en_passant(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool) -> bool:
        """Проверка допустимости взятия на проходе"""
        if not self.en_passant_target:
            return False
        
        return to_pos == self.en_passant_target
    
    def is_valid_pawn_promotion(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool) -> bool:
        """Проверка допустимости промоции пешки"""
        # Пешка может превратиться в любую фигуру кроме короля
        return True  # В данной реализации разрешаем любую промоцию
    
    def is_square_attacked(self, square: Tuple[int, int], by_white: bool) -> bool:
        """Проверка, атакована ли клетка"""
        target_row, target_col = square
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.isupper() == by_white:
                    # Временно меняем очередь для проверки атаки
                    original_turn = self.current_turn
                    self.current_turn = by_white
                    if self.check_piece_movement(piece, (row, col), square):
                        self.current_turn = original_turn
                        return True
                    self.current_turn = original_turn
        
        return False
    
    def is_king_in_check(self, king_color: bool) -> bool:
        """Проверка шаха королю"""
        king_piece = 'K' if king_color else 'k'
        king_pos = self.king_positions[king_piece]
        return self.is_square_attacked(king_pos, not king_color)
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Расширенное выполнение хода с особыми правилами"""
        if not self.is_valid_move(from_pos, to_pos):
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board_state[from_row][from_col]
        piece_type = piece.lower()
        captured = self.board_state[to_row][to_col]
        
        # Обновление позиции короля
        if piece_type == 'k':
            self.king_positions[piece] = to_pos
        
        # Выполнение рокировки
        if piece_type == 'k' and abs(from_col - to_col) == 2:
            self.perform_castling(from_pos, to_pos, piece.isupper())
        # Выполнение взятия на проходе
        elif piece_type == 'p' and from_col != to_col and captured == '.':
            self.perform_en_passant(from_pos, to_pos, piece.isupper())
        # Обычный ход
        else:
            self.board_state[to_row][to_col] = piece
            self.board_state[from_row][from_col] = '.'
            
            # Обновление прав на рокировку
            self.update_castling_rights(piece, from_pos)
            
            # Установка цели для взятия на проходе
            if piece_type == 'p' and abs(from_row - to_row) == 2:
                self.en_passant_target = ((from_row + to_row) // 2, from_col)
            else:
                self.en_passant_target = None
        
        # Обновление состояния игры
        self.current_turn = not self.current_turn
        self.move_history.append((from_pos, to_pos))
        self.fullmove_number += 1 if not self.current_turn else 0
        
        # Очистка кэша
        self.move_cache.clear()
        self.attack_cache.clear()
        self.update_position_hash()
        
        return True
    
    def perform_castling(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool):
        """Выполнение рокировки"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        king_side = to_col > from_col
        
        # Перемещение короля
        self.board_state[to_row][to_col] = self.board_state[from_row][from_col]
        self.board_state[from_row][from_col] = '.'
        
        # Перемещение ладьи
        rook_from_col = 7 if king_side else 0
        rook_to_col = to_col - 1 if king_side else to_col + 1
        rook_piece = 'R' if is_white else 'r'
        
        self.board_state[to_row][rook_to_col] = self.board_state[to_row][rook_from_col]
        self.board_state[to_row][rook_from_col] = '.'
        
        # Обновление позиции короля
        king_piece = 'K' if is_white else 'k'
        self.king_positions[king_piece] = to_pos
    
    def perform_en_passant(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool):
        """Выполнение взятия на проходе"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Перемещение пешки
        self.board_state[to_row][to_col] = self.board_state[from_row][from_col]
        self.board_state[from_row][from_col] = '.'
        
        # Удаление захваченной пешки
        captured_row = from_row
        self.board_state[captured_row][to_col] = '.'
    
    def update_castling_rights(self, piece: str, pos: Tuple[int, int]):
        """Обновление прав на рокировку"""
        row, col = pos
        piece_type = piece.lower()
        
        if piece_type == 'k':
            self.castling_rights['K' if piece.isupper() else 'k'] = False
            self.castling_rights['Q' if piece.isupper() else 'q'] = False
        elif piece_type == 'r':
            if row == 0:  # Черные ладьи
                if col == 0:
                    self.castling_rights['q'] = False
                elif col == 7:
                    self.castling_rights['k'] = False
            elif row == 7:  # Белые ладьи
                if col == 0:
                    self.castling_rights['Q'] = False
                elif col == 7:
                    self.castling_rights['K'] = False

# Глобальный продвинутый экземпляр
advanced_engine = AdvancedChessEngine()

# Глобальный оптимизированный экземпляр
optimized_engine = OptimizedChessEngine()

# Глобальный экземпляр движка
chess_engine = ChessEngineWrapper()