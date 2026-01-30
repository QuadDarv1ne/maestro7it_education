#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Улучшенный шахматный ИИ с продвинутой функцией оценки
Возможности:
- Многоуровневая оценка позиции
- Распознавание тактических паттернов
- Оценка материала и позиции
- Оценка безопасности короля
- Анализ мобильности
"""

from typing import List, Tuple, Dict
import math
import json

class EnhancedChessAI:
    """Продвинутый шахматный ИИ с утонченной оценкой"""
    
    def __init__(self, search_depth: int = 4):
        self.search_depth = search_depth
        self.transposition_table = {}
        self.history_table = {}
        self.killer_moves = [[None, None] for _ in range(64)]  # Две killer moves на каждую глубину
        self.nodes_searched = 0
        self.tt_hits = 0
        self.max_tt_size = 1000000  # Максимум 1 миллион позиций в TT
        
        # Переиспользуем генератор ходов
        from core.optimized_move_generator import BitboardMoveGenerator
        self.move_gen = BitboardMoveGenerator()
        
        # Zobrist hashing для быстрых хэшей позиций
        self.zobrist_keys = self.initialize_zobrist_keys()
        
        self.initialize_evaluation_weights()
    
    def initialize_zobrist_keys(self) -> dict:
        """Инициализация Zobrist ключей для быстрого хэширования позиций"""
        import random
        random.seed(42)  # Фиксированный seed для воспроизводимости
        
        keys = {
            'pieces': {},  # [piece][square]
            'turn': random.getrandbits(64),  # Ключ для очереди хода
        }
        
        # Генерируем ключи для каждой фигуры на каждой клетке
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            keys['pieces'][piece] = [random.getrandbits(64) for _ in range(64)]
        
        return keys
    
    def initialize_evaluation_weights(self):
        """Инициализация весов оценки для различных факторов"""
        self.weights = {
            # Значения материала
            'material': 1.0,
            'piece_square': 0.1,
            'mobility': 0.1,
            'pawn_structure': 0.15,
            'king_safety': 0.2,
            'center_control': 0.1,
            'development': 0.05,
            'tempo': 0.05
        }
        
        # Ценность фигур
        self.piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
        
        # Таблицы позиций фигур (упрощенные)
        self.piece_square_tables = {
            'P': [
                0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5,  10, 25, 25, 10,  5,  5,
                0,  0,  0,  20, 20,  0,  0,  0,
                5, -5, -10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ],
            'N': [
                -50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50
            ],
            'B': [
                -20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20
            ],
            'R': [
                0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0
            ],
            'Q': [
                -20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                -5,  0,  5,  5,  5,  5,  0, -5,
                0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20
            ],
            'K': [
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20
            ]
        }
        
        # Зеркальные таблицы для черных фигур
        for piece in ['P', 'N', 'B', 'R', 'Q', 'K']:
            white_table = self.piece_square_tables[piece]
            black_table = white_table[::-1]  # Разворот для черных
            self.piece_square_tables[piece.lower()] = black_table
    
    def evaluate_position(self, board: List[List[str]]) -> int:
        """Улучшенная функция оценки позиции"""
        score = 0
        
        # 1. Оценка материала
        material_score = self.evaluate_material(board)
        score += self.weights['material'] * material_score
        
        # 2. Оценка по таблицам позиций
        pst_score = self.evaluate_piece_square_tables(board)
        score += self.weights['piece_square'] * pst_score
        
        # 3. Оценка мобильности
        mobility_score = self.evaluate_mobility(board)
        score += self.weights['mobility'] * mobility_score
        
        # 4. Оценка пешечной структуры
        pawn_score = self.evaluate_pawn_structure(board)
        score += self.weights['pawn_structure'] * pawn_score
        
        # 5. Оценка безопасности короля
        king_safety_score = self.evaluate_king_safety(board)
        score += self.weights['king_safety'] * king_safety_score
        
        # 6. Оценка контроля центра
        center_score = self.evaluate_center_control(board)
        score += self.weights['center_control'] * center_score
        
        # 7. Оценка развития (ранняя игра)
        development_score = self.evaluate_development(board)
        score += self.weights['development'] * development_score
        
        return int(score)
    
    def evaluate_material(self, board: List[List[str]]) -> int:
        """Оценка материального баланса"""
        material = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    material += self.piece_values.get(piece, 0)
        return material
    
    def evaluate_piece_square_tables(self, board: List[List[str]]) -> int:
        """Оценка позиций фигур с использованием таблиц"""
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    square_index = row * 8 + col
                    piece_table = self.piece_square_tables.get(piece)
                    if piece_table:
                        score += piece_table[square_index]
        return score
    
    def evaluate_mobility(self, board: List[List[str]]) -> int:
        """Оценка мобильности фигур"""
        white_moves = len(self.move_gen.generate_legal_moves(board, True))
        black_moves = len(self.move_gen.generate_legal_moves(board, False))
        
        return (white_moves - black_moves) * 5  # Бонус за мобильность
    
    def evaluate_pawn_structure(self, board: List[List[str]]) -> int:
        """Оценка пешечной структуры"""
        score = 0
        
        # Проверка сдвоенных пешек
        for col in range(8):
            white_pawns = 0
            black_pawns = 0
            for row in range(8):
                if board[row][col] == 'P':
                    white_pawns += 1
                elif board[row][col] == 'p':
                    black_pawns += 1
            
            if white_pawns > 1:
                score -= (white_pawns - 1) * 10  # Штраф за сдвоенные пешки
            if black_pawns > 1:
                score += (black_pawns - 1) * 10  # Бонус за сдвоенные пешки противника
        
        # Проверка изолированных пешек
        score += self.evaluate_isolated_pawns(board)
        
        return score
    
    def evaluate_isolated_pawns(self, board: List[List[str]]) -> int:
        """Оценка изолированных пешек"""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.lower() == 'p':
                    is_isolated = True
                    # Проверка соседних вертикалей
                    for adj_col in [col-1, col+1]:
                        if 0 <= adj_col < 8:
                            for adj_row in range(8):
                                adj_piece = board[adj_row][adj_col]
                                if adj_piece.lower() == 'p' and adj_piece.isupper() == piece.isupper():
                                    is_isolated = False
                                    break
                        if not is_isolated:
                            break
                    
                    if is_isolated:
                        if piece.isupper():
                            score -= 15  # Штраф за изолированную белую пешку
                        else:
                            score += 15  # Бонус за изолированную черную пешку
        
        return score
    
    def evaluate_king_safety(self, board: List[List[str]]) -> int:
        """Оценка безопасности короля"""
        score = 0
        
        # Поиск королей
        white_king_pos = None
        black_king_pos = None
        
        for row in range(8):
            for col in range(8):
                if board[row][col] == 'K':
                    white_king_pos = (row, col)
                elif board[row][col] == 'k':
                    black_king_pos = (row, col)
        
        if white_king_pos:
            score += self.evaluate_king_zone_safety(board, white_king_pos, True)
        if black_king_pos:
            score += self.evaluate_king_zone_safety(board, black_king_pos, False)
        
        return score
    
    def evaluate_king_zone_safety(self, board: List[List[str]], king_pos: Tuple[int, int], is_white: bool) -> int:
        """Оценка безопасности зоны вокруг короля"""
        king_row, king_col = king_pos
        score = 0
        enemy_color = 'black' if is_white else 'white'
        
        # Проверка зоны короля (3x3 область вокруг короля)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = king_row + dr, king_col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board[new_row][new_col]
                    if piece != '.':
                        # Свои фигуры рядом с королем - хорошо
                        if (piece.isupper() and is_white) or (piece.islower() and not is_white):
                            score += 5
                        # Вражеские фигуры рядом с королем - плохо
                        else:
                            score -= 10
        
        return score
    
    def evaluate_center_control(self, board: List[List[str]]) -> int:
        """Оценка контроля центра"""
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        score = 0
        
        for row, col in center_squares:
            piece = board[row][col]
            if piece != '.':
                if piece.isupper():  # Белая фигура
                    score += 10
                else:  # Черная фигура
                    score -= 10
        
        return score
    
    def evaluate_development(self, board: List[List[str]]) -> int:
        """Оценка развития фигур (ранняя игра)"""
        score = 0
        
        # Кони, развитые с начальной позиции
        if board[7][1] == '.' and board[6][0] == 'N':  # Белый конь
            score += 20
        if board[7][6] == '.' and board[6][7] == 'N':  # Белый конь
            score += 20
        if board[0][1] == '.' and board[1][0] == 'n':  # Черный конь
            score -= 20
        if board[0][6] == '.' and board[1][7] == 'n':  # Черный конь
            score -= 20
        
        # Развитые слоны
        if board[7][2] == '.' and board[6][1] == 'B':  # Белый слон
            score += 15
        if board[7][5] == '.' and board[6][6] == 'B':  # Белый слон
            score += 15
        if board[0][2] == '.' and board[1][1] == 'b':  # Черный слон
            score -= 15
        if board[0][5] == '.' and board[1][6] == 'b':  # Черный слон
            score -= 15
        
        return score
    
    def minimax(self, board: List[List[str]], depth: int, alpha: float, beta: float, 
                maximizing_player: bool, allow_null_move: bool = True) -> Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Алгоритм минимакс с альфа-бета отсечением, упорядочиванием ходов и транспозиционной таблицей"""
        self.nodes_searched += 1
        
        # Проверка времени (каждые 1024 узла)
        if self.nodes_searched & 1023 == 0:
            import time
            if time.time() - self.start_time > self.time_limit:
                # Возвращаем текущую оценку, если время истекло
                return self.evaluate_position(board), None

        # Null Move Pruning - пропускаем ход для проверки угрозы
        if allow_null_move and depth >= 3 and not self.is_in_check(board, maximizing_player):
            # Делаем "пустой" ход (меняем только очередь)
            R = 2  # Reduction factor
            null_eval, _ = self.minimax(board, depth - 1 - R, -beta, -beta + 1, not maximizing_player, False)
            null_eval = -null_eval
            
            if null_eval >= beta:
                # Null move вызвало beta cutoff - позиция слишком хороша
                return beta, None

        # Поиск в транспозиционной таблице
        board_hash = self.get_board_hash(board, maximizing_player)
        if board_hash in self.transposition_table:
            entry = self.transposition_table[board_hash]
            if entry['depth'] >= depth:
                self.tt_hits += 1
                return entry['score'], entry['move']
        
        # Терминальные условия
        if depth == 0:
            return self.quiescence_search(board, alpha, beta, maximizing_player), None
        
        # Генерация легальных ходов
        moves = self.move_gen.generate_legal_moves(board, maximizing_player)
        
        if not moves:
            # Проверка на мат или пат
            if self.is_in_check(board, maximizing_player):
                return -100000 - depth if maximizing_player else 100000 + depth, None
            else:
                return 0, None  # Пат
        
        # Упорядочивание ходов
        ordered_moves = self.order_moves(board, moves, maximizing_player, depth)
        
        best_move = None
        moves_searched = 0
        
        if maximizing_player:
            max_eval = float('-inf')
            for i, move in enumerate(ordered_moves):
                new_board = self.make_move(board, move)
                
                # Principal Variation Search (PVS)
                if i == 0:
                    # Первый ход - полный поиск
                    eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                else:
                    # Late Move Reduction (LMR)
                    reduction = 0
                    if moves_searched >= 3 and depth >= 3:
                        target = board[move[1][0]][move[1][1]]
                        if target == '.':
                            reduction = 1
                    
                    # PVS: узкое окно поиска
                    eval_score, _ = self.minimax(new_board, depth - 1 - reduction, alpha, alpha + 1, False, allow_null_move)
                    
                    # Пере-поиск, если результат лучше alpha
                    if alpha < eval_score < beta:
                        eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                    elif reduction > 0 and eval_score > alpha:
                        # Пере-поиск с полной глубиной
                        eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    # Эвристика истории: записываем успешное отсечение
                    self.update_history(move, depth)
                    # Обновляем killer moves для тихих ходов
                    target = board[move[1][0]][move[1][1]]
                    if target == '.':
                        self.update_killer_moves(move, depth)
                    break  # Бета-отсечение
                
                moves_searched += 1
            
            # Сохраняем в транспозиционной таблице с управлением памятью
            self.store_in_tt(board_hash, max_eval, best_move, depth)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            moves_searched = 0
            for i, move in enumerate(ordered_moves):
                new_board = self.make_move(board, move)
                
                # Principal Variation Search (PVS)
                if i == 0:
                    eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                else:
                    # Late Move Reduction
                    reduction = 0
                    if moves_searched >= 3 and depth >= 3:
                        target = board[move[1][0]][move[1][1]]
                        if target == '.':
                            reduction = 1
                    
                    # PVS: узкое окно
                    eval_score, _ = self.minimax(new_board, depth - 1 - reduction, beta - 1, beta, True, allow_null_move)
                    
                    # Пере-поиск
                    if alpha < eval_score < beta:
                        eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                    elif reduction > 0 and eval_score < beta:
                        eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.update_history(move, depth)
                    target = board[move[1][0]][move[1][1]]
                    if target == '.':
                        self.update_killer_moves(move, depth)
                    break  # Альфа-отсечение
                
                moves_searched += 1
            
            # Сохраняем с управлением памятью
            self.store_in_tt(board_hash, min_eval, best_move, depth)
            return min_eval, best_move
    
    def store_in_tt(self, board_hash: int, score: int, move: Tuple, depth: int):
        """Сохранение в транспозиционной таблице с управлением памятью"""
        # Если таблица переполнена, удаляем менее важные записи
        if len(self.transposition_table) >= self.max_tt_size:
            # Удаляем записи с наименьшей глубиной (replacement strategy)
            min_depth_key = min(self.transposition_table.keys(), 
                               key=lambda k: self.transposition_table[k]['depth'])
            del self.transposition_table[min_depth_key]
        
        # Заменяем только если новая запись имеет большую глубину
        if board_hash not in self.transposition_table or \
           self.transposition_table[board_hash]['depth'] <= depth:
            self.transposition_table[board_hash] = {
                'score': score,
                'move': move,
                'depth': depth
            }
    
    def quiescence_search(self, board: List[List[str]], alpha: float, beta: float, 
                           maximizing_player: bool, qs_depth: int = 0) -> int:
        """Поиск только взятий для избежания эффекта горизонта"""
        # Ограничение глубины quiescence search
        max_qs_depth = 8
        if qs_depth >= max_qs_depth:
            return self.evaluate_position(board)
        
        stand_pat = self.evaluate_position(board)
        
        if maximizing_player:
            if stand_pat >= beta:
                return beta
            alpha = max(alpha, stand_pat)
            
            # Рассматриваем только взятия
            moves = self.move_gen.generate_legal_moves(board, maximizing_player)
            captures = [m for m in moves if board[m[1][0]][m[1][1]] != '.']
            ordered_captures = self.order_moves(board, captures, maximizing_player, 0)
            
            for move in ordered_captures:
                new_board = self.make_move(board, move)
                score = self.quiescence_search(new_board, alpha, beta, False, qs_depth + 1)
                if score >= beta:
                    return beta
                alpha = max(alpha, score)
            return alpha
        else:
            if stand_pat <= alpha:
                return alpha
            beta = min(beta, stand_pat)
            
            moves = self.move_gen.generate_legal_moves(board, maximizing_player)
            captures = [m for m in moves if board[m[1][0]][m[1][1]] != '.']
            ordered_captures = self.order_moves(board, captures, maximizing_player, 0)
            
            for move in ordered_captures:
                new_board = self.make_move(board, move)
                score = self.quiescence_search(new_board, alpha, beta, True, qs_depth + 1)
                if score <= alpha:
                    return alpha
                beta = min(beta, score)
            return beta

    def order_moves(self, board: List[List[str]], moves: List, is_white: bool, depth: int = 0) -> List:
        """Сортировка ходов для улучшения производительности альфа-бета отсечения"""
        move_scores = []
        for move in moves:
            score = 0
            from_pos, to_pos = move
            piece = board[from_pos[0]][from_pos[1]]
            target = board[to_pos[0]][to_pos[1]]
            
            # Пропускаем некорректные ходы
            if piece == '.' or piece not in self.piece_values:
                continue
            
            # 1. Killer moves - очень высокий приоритет
            if depth < len(self.killer_moves):
                if move == self.killer_moves[depth][0]:
                    score += 9000
                elif move == self.killer_moves[depth][1]:
                    score += 8900
            
            # 2. MVV-LVA (Самая ценная жертва - Наименее ценный агрессор)
            if target != '.' and target in self.piece_values:
                score += 10000 + 10 * abs(self.piece_values[target]) - abs(self.piece_values[piece]) // 10
            
            # 3. Эвристика истории
            score += self.history_table.get(move, 0)
            
            # 4. Превращения пешек хороши
            if piece.lower() == 'p' and (to_pos[0] == 0 or to_pos[0] == 7):
                score += 8000
            
            # 5. Ходы к центру лучше
            to_center_dist = abs(to_pos[0] - 3.5) + abs(to_pos[1] - 3.5)
            score -= int(to_center_dist * 10)
            
            move_scores.append((score, move))
        
        # Сортировка по убыванию оценки
        move_scores.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in move_scores]

    def update_history(self, move: Tuple, depth: int):
        """Обновление таблицы истории для упорядочивания ходов"""
        self.history_table[move] = self.history_table.get(move, 0) + depth * depth
    
    def update_killer_moves(self, move: Tuple, depth: int):
        """Обновление killer moves для данной глубины"""
        if depth < len(self.killer_moves):
            # Если этот ход уже не первый killer move
            if self.killer_moves[depth][0] != move:
                # Сдвигаем второй killer move
                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                # Добавляем новый как первый
                self.killer_moves[depth][0] = move

    def get_board_hash(self, board: List[List[str]], turn: bool) -> int:
        """Создание хэша состояния доски для транспозиционной таблицы (Zobrist hashing)"""
        hash_value = 0
        
        # XOR всех фигур на доске
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    square = row * 8 + col
                    hash_value ^= self.zobrist_keys['pieces'][piece][square]
        
        # XOR ключа очереди хода
        if turn:
            hash_value ^= self.zobrist_keys['turn']
        
        return hash_value

    def make_move(self, board: List[List[str]], move: Tuple[Tuple[int, int], Tuple[int, int]]) -> List[List[str]]:
        """Выполнение хода на доске (возвращает новую доску)"""
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Создаем копию доски
        new_board = [row[:] for row in board]
        
        # Выполняем ход
        piece = new_board[from_row][from_col]
        new_board[to_row][to_col] = piece
        new_board[from_row][from_col] = '.'
        
        return new_board

    def is_in_check(self, board: List[List[str]], is_white: bool) -> bool:
        """Проверка шаха королю с использованием эффективного определения атак"""
        king_char = 'K' if is_white else 'k'
        king_square = -1
        
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_char:
                    king_square = row * 8 + col
                    break
            if king_square != -1:
                break
        
        if king_square == -1:
            return False
            
        return self.move_gen.is_square_attacked(board, king_square, not is_white)

    def get_best_move(self, board: List[List[str]], color: bool, time_limit: float = 3.0) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Получение лучшего хода с использованием итеративного углубления и aspiration windows"""
        import time
        self.nodes_searched = 0
        self.tt_hits = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        
        # Очищаем killer moves в начале поиска
        self.killer_moves = [[None, None] for _ in range(64)]
        
        best_overall_move = None
        prev_eval = 0
        
        # Итеративное углубление с aspiration windows
        for current_depth in range(1, self.search_depth + 1):
            # Aspiration window для ускорения поиска
            if current_depth >= 3 and prev_eval is not None:
                window = 50  # Размер окна
                alpha = prev_eval - window
                beta = prev_eval + window
                
                # Попытка поиска в узком окне
                eval_score, move = self.minimax(board, current_depth, alpha, beta, color)
                
                # Если вышли за пределы окна, повторяем с полным окном
                if eval_score <= alpha or eval_score >= beta:
                    eval_score, move = self.minimax(board, current_depth, float('-inf'), float('inf'), color)
            else:
                # Для первых глубин используем полное окно
                eval_score, move = self.minimax(board, current_depth, float('-inf'), float('inf'), color)
            
            if move:
                best_overall_move = move
                prev_eval = eval_score
            
            # Проверка, нужно ли прекратить углубление поиска
            if time.time() - self.start_time > self.time_limit:
                break
                
        print(f"Глубина поиска ИИ: {current_depth}")
        print(f"Узлов проверено: {self.nodes_searched}, Попаданий в TT: {self.tt_hits}")
        if prev_eval is not None:
            print(f"Оценка позиции: {prev_eval/100:.2f}")
        return best_overall_move

# Тестирование улучшенного ИИ
def test_enhanced_ai():
    """Тестирование производительности улучшенного ИИ"""
    import time
    
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
    
    ai = EnhancedChessAI(search_depth=3)
    
    print("🤖 Тестирование улучшенного шахматного ИИ")
    print("=" * 40)
    
    # Тест оценки позиции
    start_time = time.perf_counter()
    score = ai.evaluate_position(test_board)
    eval_time = time.perf_counter() - start_time
    
    print(f"Оценка позиции: {score}")
    print(f"Время оценки: {eval_time*1000:.4f} мс")
    
    # Тест генерации хода
    start_time = time.perf_counter()
    best_move = ai.get_best_move(test_board, True)
    move_time = time.perf_counter() - start_time
    
    print(f"Лучший ход найден: {best_move}")
    print(f"Время расчета хода: {move_time:.4f} с")
    
    return score, best_move, move_time

if __name__ == "__main__":
    test_enhanced_ai()