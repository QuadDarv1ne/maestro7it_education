#!/usr/bin/env python3
"""
Продвинутый искусственный интеллект для шахматного движка
Реализует минимакс с альфа-бета отсечением и транспозиционными таблицами
"""

import time
import random
from typing import List, Tuple, Optional, Dict
from collections import namedtuple

# Константы для оценки
PAWN_VALUE = 100
KNIGHT_VALUE = 320
BISHOP_VALUE = 330
ROOK_VALUE = 500
QUEEN_VALUE = 900
KING_VALUE = 20000

# Позиционные бонусы
PAWN_POSITION_BONUS = [
    0,  0,  0,  0,  0,  0,  0,  0,
   50, 50, 50, 50, 50, 50, 50, 50,
   10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_POSITION_BONUS = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_POSITION_BONUS = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_POSITION_BONUS = [
  0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_POSITION_BONUS = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20
]

KING_POSITION_BONUS = [
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20
]

class TranspositionEntry:
    """Запись в транспозиционной таблице"""
    def __init__(self, depth: int, score: int, flag: int, best_move: Optional[Tuple[int, int]] = None):
        self.depth = depth
        self.score = score
        self.flag = flag  # 0 = exact, 1 = lower bound, 2 = upper bound
        self.best_move = best_move

class AdvancedChessAI:
    """Продвинутый шахматный ИИ с минимаксом и альфа-бета отсечением"""
    
    def __init__(self, search_depth: int = 4, time_limit: int = 5000):
        self.search_depth = search_depth
        self.time_limit = time_limit
        self.nodes_searched = 0
        self.tt_hits = 0
        self.transposition_table: Dict[int, TranspositionEntry] = {}
        self.start_time = 0
        self.piece_values = {
            'p': PAWN_VALUE, 'n': KNIGHT_VALUE, 'b': BISHOP_VALUE,
            'r': ROOK_VALUE, 'q': QUEEN_VALUE, 'k': KING_VALUE,
            'P': PAWN_VALUE, 'N': KNIGHT_VALUE, 'B': BISHOP_VALUE,
            'R': ROOK_VALUE, 'Q': QUEEN_VALUE, 'K': KING_VALUE
        }
        self.position_bonuses = {
            'p': PAWN_POSITION_BONUS, 'n': KNIGHT_POSITION_BONUS, 'b': BISHOP_POSITION_BONUS,
            'r': ROOK_POSITION_BONUS, 'q': QUEEN_POSITION_BONUS, 'k': KING_POSITION_BONUS,
            'P': PAWN_POSITION_BONUS, 'N': KNIGHT_POSITION_BONUS, 'B': BISHOP_POSITION_BONUS,
            'R': ROOK_POSITION_BONUS, 'Q': QUEEN_POSITION_BONUS, 'K': KING_POSITION_BONUS
        }
    
    def get_best_move(self, board: List[List[str]], is_white: bool) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Получение лучшего хода"""
        self.nodes_searched = 0
        self.tt_hits = 0
        self.start_time = time.time()
        
        try:
            best_score = float('-inf') if is_white else float('inf')
            best_move = None
            
            # Генерируем все возможные ходы
            moves = self._generate_all_moves(board, is_white)
            
            if not moves:
                return None
            
            # Упорядочиваем ходы для лучшей производительности
            ordered_moves = self._order_moves(board, moves, is_white)
            
            alpha = float('-inf')
            beta = float('inf')
            
            for move in ordered_moves:
                if time.time() - self.start_time > self.time_limit / 1000:
                    break
                
                # Делаем ход
                from_pos, to_pos = move
                piece = board[from_pos[0]][from_pos[1]]
                captured = board[to_pos[0]][to_pos[1]]
                
                board[to_pos[0]][to_pos[1]] = piece
                board[from_pos[0]][from_pos[1]] = '.'
                
                # Оценка позиции
                score = self._minimax(board, self.search_depth - 1, not is_white, alpha, beta)
                
                # Возвращаем доску в исходное состояние
                board[from_pos[0]][from_pos[1]] = piece
                board[to_pos[0]][to_pos[1]] = captured
                
                # Обновляем лучший ход
                if is_white:
                    if score > best_score:
                        best_score = score
                        best_move = move
                        alpha = max(alpha, score)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move
                        beta = min(beta, score)
            
            return best_move
            
        except Exception as e:
            print(f"Ошибка в AI: {e}")
            # Возвращаем случайный ход в случае ошибки
            moves = self._generate_all_moves(board, is_white)
            return random.choice(moves) if moves else None
    
    def _minimax(self, board: List[List[str]], depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        """Алгоритм минимакс с альфа-бета отсечением"""
        self.nodes_searched += 1
        
        # Проверяем транспозиционную таблицу
        board_hash = self._hash_board(board)
        tt_entry = self.transposition_table.get(board_hash)
        
        if tt_entry and tt_entry.depth >= depth:
            self.tt_hits += 1
            if tt_entry.flag == 0:  # exact
                return tt_entry.score
            elif tt_entry.flag == 1 and tt_entry.score >= beta:  # lower bound
                return tt_entry.score
            elif tt_entry.flag == 2 and tt_entry.score <= alpha:  # upper bound
                return tt_entry.score
        
        # Базовый случай
        if depth == 0 or time.time() - self.start_time > self.time_limit / 1000:
            return self._evaluate_position(board)
        
        # Генерируем ходы
        is_white = is_maximizing
        moves = self._generate_all_moves(board, is_white)
        
        if not moves:
            # Проверяем мат/пат
            if self._is_in_check(board, is_white):
                return float('-inf') if is_white else float('inf')  # Мат
            else:
                return 0  # Пат
        
        # Упорядочиваем ходы
        ordered_moves = self._order_moves(board, moves, is_white)
        
        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            
            for move in ordered_moves:
                from_pos, to_pos = move
                piece = board[from_pos[0]][from_pos[1]]
                captured = board[to_pos[0]][to_pos[1]]
                
                # Делаем ход
                board[to_pos[0]][to_pos[1]] = piece
                board[from_pos[0]][from_pos[1]] = '.'
                
                eval_score = self._minimax(board, depth - 1, False, alpha, beta)
                
                # Возвращаем доску
                board[from_pos[0]][from_pos[1]] = piece
                board[to_pos[0]][to_pos[1]] = captured
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            # Сохраняем в транспозиционную таблицу
            flag = 0 if alpha >= max_eval else 1  # exact or lower bound
            self.transposition_table[board_hash] = TranspositionEntry(depth, max_eval, flag, best_move)
            
            return max_eval
        else:
            min_eval = float('inf')
            best_move = None
            
            for move in ordered_moves:
                from_pos, to_pos = move
                piece = board[from_pos[0]][from_pos[1]]
                captured = board[to_pos[0]][to_pos[1]]
                
                # Делаем ход
                board[to_pos[0]][to_pos[1]] = piece
                board[from_pos[0]][from_pos[1]] = '.'
                
                eval_score = self._minimax(board, depth - 1, True, alpha, beta)
                
                # Возвращаем доску
                board[from_pos[0]][from_pos[1]] = piece
                board[to_pos[0]][to_pos[1]] = captured
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            # Сохраняем в транспозиционную таблицу
            flag = 0 if beta <= min_eval else 2  # exact or upper bound
            self.transposition_table[board_hash] = TranspositionEntry(depth, min_eval, flag, best_move)
            
            return min_eval
    
    def _generate_all_moves(self, board: List[List[str]], is_white: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Генерация всех допустимых ходов"""
        moves = []
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.' and ((piece.isupper() and is_white) or (piece.islower() and not is_white)):
                    # Генерируем ходы для этой фигуры
                    piece_moves = self._get_piece_moves(board, (row, col))
                    moves.extend([((row, col), move) for move in piece_moves])
        
        return moves
    
    def _get_piece_moves(self, board: List[List[str]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Получение допустимых ходов для конкретной фигуры"""
        row, col = pos
        piece = board[row][col]
        moves = []
        
        # Здесь должна быть логика движения фигур
        # Для демонстрации возвращаем несколько случайных ходов
        for to_row in range(8):
            for to_col in range(8):
                if self._is_valid_move(board, pos, (to_row, to_col)):
                    moves.append((to_row, to_col))
        
        return moves
    
    def _is_valid_move(self, board: List[List[str]], from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка допустимости хода"""
        # Упрощенная проверка для демонстрации
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if from_pos == to_pos:
            return False
        
        piece = board[from_row][from_col]
        target = board[to_row][to_col]
        
        # Проверка цвета
        is_white_piece = piece.isupper()
        is_white_target = target.isupper() if target != '.' else None
        
        if target != '.' and is_white_piece == is_white_target:
            return False
        
        return True
    
    def _order_moves(self, board: List[List[str]], moves: List[Tuple[Tuple[int, int], Tuple[int, int]]], 
                     is_white: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Упорядочивание ходов для лучшей производительности"""
        # MVV/LVA ordering (Most Valuable Victim / Least Valuable Attacker)
        def move_priority(move):
            from_pos, to_pos = move
            attacker = board[from_pos[0]][from_pos[1]]
            victim = board[to_pos[0]][to_pos[1]]
            
            if victim == '.':
                return 0
            
            # Приоритет захватам
            victim_value = self.piece_values.get(victim.lower(), 0)
            attacker_value = self.piece_values.get(attacker.lower(), 0)
            
            return victim_value * 1000 - attacker_value  # MVV/LVA
        
        return sorted(moves, key=move_priority, reverse=True)
    
    def _evaluate_position(self, board: List[List[str]]) -> float:
        """Оценка позиции"""
        material_score = 0
        positional_score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    # Материальная оценка
                    value = self.piece_values[piece]
                    material_score += value if piece.isupper() else -value
                    
                    # Позиционная оценка
                    square_index = row * 8 + col
                    bonus = self.position_bonuses[piece][square_index]
                    positional_score += bonus if piece.isupper() else -bonus
        
        return material_score + positional_score * 0.1
    
    def _hash_board(self, board: List[List[str]]) -> int:
        """Генерация хэша доски"""
        board_str = ''.join(''.join(row) for row in board)
        return hash(board_str)
    
    def _is_in_check(self, board: List[List[str]], is_white_king: bool) -> bool:
        """Проверка, находится ли король под шахом"""
        # Упрощенная реализация
        return False
    
    def get_statistics(self) -> Dict[str, int]:
        """Получение статистики поиска"""
        return {
            'nodes_searched': self.nodes_searched,
            'tt_hits': self.tt_hits,
            'tt_size': len(self.transposition_table)
        }

# Демонстрационная программа
class AIDemonstration:
    def __init__(self):
        self.ai = AdvancedChessAI(search_depth=3, time_limit=2000)
    
    def run_demo(self):
        print("=== ДЕМОНСТРАЦИЯ ПРОДВИНУТОГО ШАХМАТНОГО ИИ ===\n")
        
        # Тестовая позиция
        test_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        print("Начальная позиция:")
        self._print_board(test_board)
        
        print("\nПоиск лучшего хода для белых...")
        best_move = self.ai.get_best_move(test_board, True)
        
        if best_move:
            from_pos, to_pos = best_move
            print(f"Лучший ход: {self._pos_to_notation(from_pos)} -> {self._pos_to_notation(to_pos)}")
        else:
            print("Нет допустимых ходов")
        
        stats = self.ai.get_statistics()
        print(f"\nСтатистика поиска:")
        print(f"  Узлов рассмотрено: {stats['nodes_searched']:,}")
        print(f"  Попаданий в TT: {stats['tt_hits']}")
        print(f"  Размер TT: {stats['tt_size']} записей")
        
        print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")
    
    def _print_board(self, board: List[List[str]]):
        """Вывод доски"""
        print("  a b c d e f g h")
        print(" +-----------------+")
        for i, row in enumerate(board):
            print(f"{8-i}| {' '.join(row)} |{8-i}")
        print(" +-----------------+")
        print("  a b c d e f g h")
    
    def _pos_to_notation(self, pos: Tuple[int, int]) -> str:
        """Преобразование позиции в шахматную нотацию"""
        row, col = pos
        letter = chr(ord('a') + col)
        number = 8 - row
        return f"{letter}{number}"

if __name__ == "__main__":
    try:
        demo = AIDemonstration()
        demo.run_demo()
    except Exception as e:
        print(f"Ошибка: {e}")