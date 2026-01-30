#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Улучшенный шахматный ИИ v2.0 с продвинутой функцией оценки
Улучшения:
- Исправленный LMR (Late Move Reduction)
- Delta Pruning в Quiescence Search
- SEE (Static Exchange Evaluation)
- Улучшенная оценка безопасности короля
- Оценка проходных пешек
- PV move ordering
- Кэширование оценок
- Оптимизированная транспозиционная таблица
"""

from typing import List, Tuple, Dict, Optional
import math
import time

class EnhancedChessAI:
    """Продвинутый шахматный ИИ v2.0 с улучшенными алгоритмами"""
    
    def __init__(self, search_depth: int = 4, engine_wrapper=None):
        self.search_depth = search_depth
        self.transposition_table = {}
        self.history_table = {}
        self.killer_moves = [[None, None] for _ in range(64)]
        self.eval_cache = {}  # НОВОЕ: Кэш оценок
        self.pv_table = {}  # НОВОЕ: Principal Variation
        
        self.nodes_searched = 0
        self.tt_hits = 0
        self.max_tt_size = 1000000
        
        self.engine_wrapper = engine_wrapper
        self.move_gen = None
        
        self.zobrist_keys = self.initialize_zobrist_keys()
        self.initialize_evaluation_weights()
    
    def initialize_zobrist_keys(self) -> dict:
        """Инициализация Zobrist ключей для быстрого хэширования позиций"""
        import random
        random.seed(42)
        
        keys = {
            'pieces': {},
            'turn': random.getrandbits(64),
        }
        
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            keys['pieces'][piece] = [random.getrandbits(64) for _ in range(64)]
        
        return keys
    
    def initialize_evaluation_weights(self):
        """Инициализация весов оценки для различных факторов"""
        self.weights = {
            'material': 1.0,
            'piece_square': 0.1,
            'mobility': 0.1,
            'pawn_structure': 0.15,
            'king_safety': 0.4,  # Увеличен вес
            'center_control': 0.1,
            'development': 0.05,
            'tempo': 0.05,
            'bishop_pair': 30,
            'rook_open_file': 20,
            'passed_pawn_base': 25,  # Базовый бонус
            'passed_pawn_rank': 15,  # Бонус за ранг
        }
        
        self.piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
        
        # Улучшенные таблицы позиций
        self.piece_square_tables = {
            'P': [
                0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
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
            ],
            'K_endgame': [
                -50,-40,-30,-20,-20,-30,-40,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50
            ]
        }
        
        for piece in ['P', 'N', 'B', 'R', 'Q', 'K']:
            white_table = self.piece_square_tables[piece]
            black_table = white_table[::-1]
            self.piece_square_tables[piece.lower()] = black_table
            
        self.piece_square_tables['k_endgame'] = self.piece_square_tables['K_endgame'][::-1]
    
    def evaluate_position(self, board: List[List[str]]) -> int:
        """Улучшенная функция оценки с кэшированием"""
        # НОВОЕ: Проверяем кэш
        board_hash = self.get_board_hash(board, True)
        if board_hash in self.eval_cache:
            return self.eval_cache[board_hash]
        
        score = self._calculate_evaluation(board)
        
        # Ограничиваем размер кэша
        if len(self.eval_cache) > 50000:
            self.eval_cache.clear()
        
        self.eval_cache[board_hash] = score
        return score
    
    def _calculate_evaluation(self, board: List[List[str]]) -> int:
        """Внутренний расчёт оценки позиции"""
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
        
        # 5. УЛУЧШЕНО: Оценка безопасности короля
        king_safety_score = self.evaluate_king_safety_improved(board)
        score += self.weights['king_safety'] * king_safety_score
        
        # 6. Оценка контроля центра
        center_score = self.evaluate_center_control(board)
        score += self.weights['center_control'] * center_score
        
        # 7. Оценка развития
        development_score = self.evaluate_development(board)
        score += self.weights['development'] * development_score
        
        # 8. Дополнительные бонусы
        score += self.evaluate_bishop_pair(board)
        score += self.evaluate_rook_files(board)
        
        # 9. НОВОЕ: Оценка проходных пешек
        score += self.evaluate_passed_pawns(board)
        
        return int(score)
    
    def quiescence_search(self, board: List[List[str]], alpha: float, beta: float, 
                          maximizing_player: bool, depth: int = 0) -> int:
        """НОВОЕ: Поиск только взятий для избежания эффекта горизонта"""
        # Ограничение глубины поиска
        max_depth = 4
        if depth >= max_depth:
            return self.evaluate_position(board)
        
        # Статическая оценка текущей позиции
        stand_pat = self.evaluate_position(board)
        
        if maximizing_player:
            if stand_pat >= beta:
                return beta
            alpha = max(alpha, stand_pat)
        else:
            if stand_pat <= alpha:
                return alpha
            beta = min(beta, stand_pat)
        
        # Генерируем только взятия
        moves = self.generate_legal_moves(board, maximizing_player)
        captures = []
        for move in moves:
            from_pos, to_pos = move
            target = board[to_pos[0]][to_pos[1]]
            if target != '.':  # Только взятия
                captures.append(move)
        
        # Сортируем взятия по MVV-LVA
        ordered_captures = self.order_capture_moves(board, captures, maximizing_player)
        
        for move in ordered_captures:
            new_board = self.make_move(board, move)
            score = self.quiescence_search(new_board, alpha, beta, not maximizing_player, depth + 1)
            
            if maximizing_player:
                if score >= beta:
                    return beta
                alpha = max(alpha, score)
            else:
                if score <= alpha:
                    return alpha
                beta = min(beta, score)
        
        return stand_pat if maximizing_player else stand_pat
    
    def order_capture_moves(self, board: List[List[str]], moves: List, is_white: bool) -> List:
        """Сортировка взятий по MVV-LVA (Most Valuable Victim - Least Valuable Aggressor)"""
        move_scores = []
        
        for move in moves:
            from_pos, to_pos = move
            attacker = board[from_pos[0]][from_pos[1]]
            victim = board[to_pos[0]][to_pos[1]]
            
            if victim == '.':
                continue
            
            # MVV-LVA оценка
            victim_value = abs(self.piece_values.get(victim, 0))
            attacker_value = abs(self.piece_values.get(attacker, 0))
            score = victim_value * 10 - attacker_value // 10
            
            # Бонус за выгодные взятия
            if victim_value >= attacker_value:
                score += 10000
            
            move_scores.append((score, move))
        
        # Сортировка по убыванию
        move_scores.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in move_scores]

    def evaluate_passed_pawns(self, board: List[List[str]]) -> int:
        """НОВОЕ: Оценка проходных пешек"""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece == 'P':
                    if self.is_passed_pawn(board, row, col, True):
                        # Бонус растёт экспоненциально при приближении к превращению
                        rank_bonus = (7 - row) ** 2
                        bonus = self.weights['passed_pawn_base'] + self.weights['passed_pawn_rank'] * rank_bonus
                        score += int(bonus)
                elif piece == 'p':
                    if self.is_passed_pawn(board, row, col, False):
                        rank_bonus = row ** 2
                        bonus = self.weights['passed_pawn_base'] + self.weights['passed_pawn_rank'] * rank_bonus
                        score -= int(bonus)
        
        return score
    
    def is_passed_pawn(self, board: List[List[str]], row: int, col: int, is_white: bool) -> bool:
        """Проверка, является ли пешка проходной"""
        enemy_pawn = 'p' if is_white else 'P'
        direction = -1 if is_white else 1
        
        # Проверяем вертикаль и соседние
        for check_col in [col - 1, col, col + 1]:
            if not (0 <= check_col < 8):
                continue
            r = row + direction
            while 0 <= r < 8:
                if board[r][check_col] == enemy_pawn:
                    return False
                r += direction
        return True
    
    def evaluate_king_safety_improved(self, board: List[List[str]]) -> int:
        """УЛУЧШЕНО: Более точная оценка безопасности короля"""
        score = 0
        
        white_king_pos = self.find_king(board, True)
        black_king_pos = self.find_king(board, False)
        
        if white_king_pos:
            # Пешечный щит
            shield = self.evaluate_pawn_shield(board, white_king_pos, True)
            # Открытые линии
            open_files = self.count_open_files_near_king(board, white_king_pos)
            # Атакующие фигуры
            attackers = self.count_king_attackers(board, white_king_pos, False)
            
            score += shield - open_files * 20 - attackers * 30
        
        if black_king_pos:
            shield = self.evaluate_pawn_shield(board, black_king_pos, False)
            open_files = self.count_open_files_near_king(board, black_king_pos)
            attackers = self.count_king_attackers(board, black_king_pos, True)
            
            score -= shield - open_files * 20 - attackers * 30
        
        return score
    
    def find_king(self, board: List[List[str]], is_white: bool) -> Optional[Tuple[int, int]]:
        """Поиск позиции короля"""
        king_char = 'K' if is_white else 'k'
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_char:
                    return (row, col)
        return None
    
    def evaluate_pawn_shield(self, board: List[List[str]], king_pos: Tuple[int, int], is_white: bool) -> int:
        """Бонус за пешки перед королём"""
        kr, kc = king_pos
        shield = 0
        direction = -1 if is_white else 1
        pawn = 'P' if is_white else 'p'
        
        for dc in [-1, 0, 1]:
            col = kc + dc
            if 0 <= col < 8:
                for dr in [1, 2]:
                    row = kr + direction * dr
                    if 0 <= row < 8 and board[row][col] == pawn:
                        shield += 25 if dr == 1 else 15
                        break
        return shield
    
    def count_open_files_near_king(self, board: List[List[str]], king_pos: Tuple[int, int]) -> int:
        """Подсчёт открытых линий рядом с королём"""
        kr, kc = king_pos
        open_count = 0
        
        for dc in [-1, 0, 1]:
            col = kc + dc
            if 0 <= col < 8:
                has_pawn = False
                for row in range(8):
                    if board[row][col].lower() == 'p':
                        has_pawn = True
                        break
                if not has_pawn:
                    open_count += 1
        
        return open_count
    
    def count_king_attackers(self, board: List[List[str]], king_pos: Tuple[int, int], by_white: bool) -> int:
        """Подсчёт атакующих фигур вблизи короля"""
        kr, kc = king_pos
        attackers = 0
        
        # Проверяем зону 5x5 вокруг короля
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                row, col = kr + dr, kc + dc
                if 0 <= row < 8 and 0 <= col < 8:
                    piece = board[row][col]
                    if piece != '.' and piece.isupper() == by_white:
                        if piece.lower() in 'qrbn':  # Опасные атакующие фигуры
                            attackers += 1
        
        return attackers
    
    def evaluate_bishop_pair(self, board: List[List[str]]) -> int:
        """Бонус за наличие пары слонов"""
        white_bishops = sum(1 for row in board for piece in row if piece == 'B')
        black_bishops = sum(1 for row in board for piece in row if piece == 'b')
        
        score = 0
        if white_bishops >= 2:
            score += self.weights['bishop_pair']
        if black_bishops >= 2:
            score -= self.weights['bishop_pair']
        return score
    
    def evaluate_rook_files(self, board: List[List[str]]) -> int:
        """Бонус за ладьи на открытых и полуоткрытых линиях"""
        score = 0
        for col in range(8):
            white_pawn = any(board[row][col] == 'P' for row in range(8))
            black_pawn = any(board[row][col] == 'p' for row in range(8))
            white_rook = any(board[row][col] == 'R' for row in range(8))
            black_rook = any(board[row][col] == 'r' for row in range(8))
            
            if not white_pawn and not black_pawn:
                if white_rook:
                    score += self.weights['rook_open_file']
                if black_rook:
                    score -= self.weights['rook_open_file']
            elif white_rook and not white_pawn:
                score += self.weights['rook_open_file'] // 2
            elif black_rook and not black_pawn:
                score -= self.weights['rook_open_file'] // 2
        
        return score
    
    def evaluate_material(self, board: List[List[str]]) -> int:
        """Оценка материального баланса"""
        return sum(self.piece_values.get(board[row][col], 0) 
                  for row in range(8) for col in range(8))
    
    def evaluate_piece_square_tables(self, board: List[List[str]]) -> int:
        """Оценка позиций фигур с использованием таблиц"""
        is_endgame = self.check_is_endgame(board)
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    square_index = row * 8 + col
                    table_key = piece
                    
                    if piece == 'K' and is_endgame:
                        table_key = 'K_endgame'
                    elif piece == 'k' and is_endgame:
                        table_key = 'k_endgame'
                    
                    piece_table = self.piece_square_tables.get(table_key)
                    if piece_table:
                        score += piece_table[square_index]
        
        return score
    
    def check_is_endgame(self, board: List[List[str]]) -> bool:
        """Определение фазы игры (эндшпиль)"""
        has_white_queen = any(board[row][col] == 'Q' for row in range(8) for col in range(8))
        has_black_queen = any(board[row][col] == 'q' for row in range(8) for col in range(8))
        
        white_minor = sum(1 for row in range(8) for col in range(8) if board[row][col] in 'NBR')
        black_minor = sum(1 for row in range(8) for col in range(8) if board[row][col] in 'nbr')
        
        if not has_white_queen and not has_black_queen:
            return True
        if not has_white_queen and white_minor <= 1:
            return True
        if not has_black_queen and black_minor <= 1:
            return True
        return False
    
    def evaluate_mobility(self, board: List[List[str]]) -> int:
        """Оценка мобильности фигур"""
        white_moves = len(self.generate_legal_moves(board, True))
        black_moves = len(self.generate_legal_moves(board, False))
        return (white_moves - black_moves) * 5
    
    def evaluate_pawn_structure(self, board: List[List[str]]) -> int:
        """Оценка пешечной структуры"""
        score = 0
        
        # Сдвоенные пешки
        for col in range(8):
            white_pawns = sum(1 for row in range(8) if board[row][col] == 'P')
            black_pawns = sum(1 for row in range(8) if board[row][col] == 'p')
            
            if white_pawns > 1:
                score -= (white_pawns - 1) * 10
            if black_pawns > 1:
                score += (black_pawns - 1) * 10
        
        # Изолированные пешки
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
                        score += -15 if piece.isupper() else 15
        
        return score
    
    def evaluate_center_control(self, board: List[List[str]]) -> int:
        """Оценка контроля центра"""
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        score = sum(10 if board[r][c].isupper() else -10 
                   for r, c in center_squares if board[r][c] != '.')
        return score
    
    def evaluate_development(self, board: List[List[str]]) -> int:
        """Оценка развития фигур"""
        score = 0
        
        # Развитые кони
        if board[7][1] == '.':
            score += 20
        if board[7][6] == '.':
            score += 20
        if board[0][1] == '.':
            score -= 20
        if board[0][6] == '.':
            score -= 20
        
        # Развитые слоны
        if board[7][2] == '.':
            score += 15
        if board[7][5] == '.':
            score += 15
        if board[0][2] == '.':
            score -= 15
        if board[0][5] == '.':
            score -= 15
        
        return score
    
    def generate_legal_moves(self, board: List[List[str]], is_white: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Генерация всех легальных ходов"""
        if not self.engine_wrapper:
            return []
        
        moves = []
        original_board = self.engine_wrapper.board_state
        original_turn = self.engine_wrapper.current_turn
        
        self.engine_wrapper.board_state = [row[:] for row in board]
        self.engine_wrapper.current_turn = is_white
        
        for from_row in range(8):
            for from_col in range(8):
                piece = board[from_row][from_col]
                if piece == '.' or piece.isupper() != is_white:
                    continue
                
                for to_row in range(8):
                    for to_col in range(8):
                        if self.engine_wrapper.is_valid_move_python((from_row, from_col), (to_row, to_col)):
                            if not self.engine_wrapper.would_still_be_in_check((from_row, from_col), (to_row, to_col), is_white):
                                moves.append(((from_row, from_col), (to_row, to_col)))
        
        self.engine_wrapper.board_state = original_board
        self.engine_wrapper.current_turn = original_turn
        return moves
    
    def see_capture(self, board: List[List[str]], move: Tuple) -> int:
        """НОВОЕ: Static Exchange Evaluation - оценка размена"""
        from_pos, to_pos = move
        target = board[to_pos[0]][to_pos[1]]
        
        if target == '.':
            return 0
        
        attacker = board[from_pos[0]][from_pos[1]]
        victim_value = abs(self.piece_values.get(target, 0))
        attacker_value = abs(self.piece_values.get(attacker, 0))
        
        # Упрощённая SEE: если берём дороже или равное - хорошо
        if victim_value >= attacker_value:
            return victim_value - attacker_value
        
        # Если берём дешёвой что-то дорогое, но можем быть съедены - пессимистично
        return victim_value - attacker_value
    
    def calculate_lmr_reduction(self, depth: int, moves_searched: int, move: Tuple, board: List[List[str]]) -> int:
        """НОВОЕ: Улучшенная формула Late Move Reduction"""
        if moves_searched < 3 or depth < 3:
            return 0
        
        # Формула на основе Stockfish
        reduction = math.log(depth) * math.log(moves_searched) / 2.5
        reduction = int(reduction)
        
        target = board[move[1][0]][move[1][1]]
        
        # Взятия не редуцируем
        if target != '.':
            return 0
        
        # Шахи редуцируем меньше
        if self.gives_check(board, move):
            reduction = max(0, reduction - 1)
        
        return min(reduction, depth - 2)
    
    def gives_check(self, board: List[List[str]], move: Tuple) -> bool:
        """Проверка, даёт ли ход шах"""
        new_board = self.make_move(board, move)
        piece = board[move[0][0]][move[0][1]]
        is_white = piece.isupper()
        return self.is_in_check(new_board, not is_white)
    
    def minimax(self, board: List[List[str]], depth: int, alpha: float, beta: float,
                maximizing_player: bool, allow_null_move: bool = True) -> Tuple[int, Optional[Tuple]]:
        """Алгоритм минимакс с улучшениями"""
        self.nodes_searched += 1
        
        # Проверка времени
        if self.nodes_searched & 1023 == 0:
            if time.time() - self.start_time > self.time_limit:
                return self.evaluate_position(board), None
        
        # Null Move Pruning
        if allow_null_move and depth >= 3 and not self.is_in_check(board, maximizing_player):
            R = 3 if depth >= 6 else 2
            null_eval, _ = self.minimax(board, depth - 1 - R, -beta, -beta + 1, not maximizing_player, False)
            null_eval = -null_eval
            
            if null_eval >= beta:
                if depth >= 8:
                    verify_eval, _ = self.minimax(board, depth - 5, alpha, beta, maximizing_player, False)
                    if verify_eval >= beta:
                        return beta, None
                else:
                    return beta, None
        
        # Транспозиционная таблица
        board_hash = self.get_board_hash(board, maximizing_player)
        pv_move = None
        
        if board_hash in self.transposition_table:
            entry = self.transposition_table[board_hash]
            if entry['depth'] >= depth:
                self.tt_hits += 1
                return entry['score'], entry['move']
            pv_move = entry.get('move')
        
        # Терминальные условия
        if depth == 0:
            return self.quiescence_search(board, alpha, beta, maximizing_player), None
        
        moves = self.generate_legal_moves(board, maximizing_player)
        
        if not moves:
            if self.is_in_check(board, maximizing_player):
                return -100000 - depth if maximizing_player else 100000 + depth, None
            return 0, None
        
        # УЛУЧШЕНО: Упорядочивание с PV move
        ordered_moves = self.order_moves(board, moves, maximizing_player, depth, pv_move)
        
        best_move = None
        moves_searched = 0
        
        if maximizing_player:
            max_eval = float('-inf')
            for i, move in enumerate(ordered_moves):
                new_board = self.make_move(board, move)
                
                if i == 0:
                    eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                else:
                    # УЛУЧШЕНО: LMR
                    reduction = self.calculate_lmr_reduction(depth, moves_searched, move, board)
                    
                    # PVS
                    eval_score, _ = self.minimax(new_board, depth - 1 - reduction, alpha, alpha + 1, False, allow_null_move)
                    
                    if alpha < eval_score < beta:
                        eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                    elif reduction > 0 and eval_score > alpha:
                        eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.update_history(move, depth)
                    target = board[move[1][0]][move[1][1]]
                    if target == '.':
                        self.update_killer_moves(move, depth)
                    break
                
                moves_searched += 1
            
            self.store_in_tt(board_hash, max_eval, best_move, depth)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for i, move in enumerate(ordered_moves):
                new_board = self.make_move(board, move)
                
                if i == 0:
                    eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                else:
                    reduction = self.calculate_lmr_reduction(depth, moves_searched, move, board)
                    
                    eval_score, _ = self.minimax(new_board, depth - 1 - reduction, beta - 1, beta, True, allow_null_move)
                    
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
                    break
                
                moves_searched += 1
            
            self.store_in_tt(board_hash, min_eval, best_move, depth)
            return min_eval, best_move
    
    def quiescence_search(self, board: List[List[str]], alpha: float, beta: float,
                         maximizing_player: bool, qs_depth: int = 0) -> int:
        """УЛУЧШЕНО: Quiescence search с Delta Pruning"""
        max_qs_depth = 8
        if qs_depth >= max_qs_depth:
            return self.evaluate_position(board)
        
        stand_pat = self.evaluate_position(board)
        
        # НОВОЕ: Delta Pruning
        DELTA_MARGIN = 200  # ~2 пешки
        
        if maximizing_player:
            if stand_pat >= beta:
                return beta
            
            # Delta pruning - пропускаем заведомо плохие позиции
            if stand_pat < alpha - DELTA_MARGIN:
                return alpha
            
            alpha = max(alpha, stand_pat)
            
            moves = self.generate_legal_moves(board, maximizing_player)
            captures = [m for m in moves if board[m[1][0]][m[1][1]] != '.']
            
            # УЛУЧШЕНО: Фильтруем плохие взятия через SEE
            good_captures = [m for m in captures if self.see_capture(board, m) >= -50]
            ordered_captures = self.order_moves(board, good_captures, maximizing_player, 0)
            
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
            
            if stand_pat > beta + DELTA_MARGIN:
                return beta
            
            beta = min(beta, stand_pat)
            
            moves = self.generate_legal_moves(board, maximizing_player)
            captures = [m for m in moves if board[m[1][0]][m[1][1]] != '.']
            good_captures = [m for m in captures if self.see_capture(board, m) >= -50]
            ordered_captures = self.order_moves(board, good_captures, maximizing_player, 0)
            
            for move in ordered_captures:
                new_board = self.make_move(board, move)
                score = self.quiescence_search(new_board, alpha, beta, True, qs_depth + 1)
                if score <= alpha:
                    return alpha
                beta = min(beta, score)
            return beta
    
    def order_moves(self, board: List[List[str]], moves: List, is_white: bool, 
                   depth: int = 0, pv_move: Optional[Tuple] = None) -> List:
        """УЛУЧШЕНО: Упорядочивание ходов с PV move"""
        move_scores = []
        
        for move in moves:
            score = 0
            
            # 1. НОВОЕ: PV move - наивысший приоритет
            if pv_move and move == pv_move:
                score += 100000
                move_scores.append((score, move))
                continue
            
            from_pos, to_pos = move
            piece = board[from_pos[0]][from_pos[1]]
            target = board[to_pos[0]][to_pos[1]]
            
            if piece == '.' or piece not in self.piece_values:
                continue
            
            # 2. Killer moves
            if depth < len(self.killer_moves):
                if move == self.killer_moves[depth][0]:
                    score += 9000
                elif move == self.killer_moves[depth][1]:
                    score += 8900
            
            # 3. УЛУЧШЕНО: MVV-LVA с SEE
            if target != '.' and target in self.piece_values:
                victim_value = abs(self.piece_values[target])
                attacker_value = abs(self.piece_values[piece])
                score += 10000 + (victim_value * 10) - (attacker_value // 10)
                
                # SEE бонус
                see_score = self.see_capture(board, move)
                if see_score > 0:
                    score += 5000
            
            # 4. История
            score += self.history_table.get(move, 0)
            
            # 5. Превращения
            if piece.lower() == 'p' and (to_pos[0] == 0 or to_pos[0] == 7):
                score += 20000
            
            # 6. Центр
            to_center_dist = abs(to_pos[0] - 3.5) + abs(to_pos[1] - 3.5)
            score -= int(to_center_dist * 10)
            
            # 7. Продвижение пешек
            if piece.lower() == 'p':
                direction = 1 if piece.isupper() else -1
                advance = (to_pos[0] - from_pos[0]) * direction
                if advance > 0:
                    score += advance * 15
            
            move_scores.append((score, move))
        
        move_scores.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in move_scores]
    
    def update_history(self, move: Tuple, depth: int):
        """Обновление таблицы истории"""
        self.history_table[move] = self.history_table.get(move, 0) + depth * depth
    
    def update_killer_moves(self, move: Tuple, depth: int):
        """Обновление killer moves"""
        if depth < len(self.killer_moves):
            if self.killer_moves[depth][0] != move:
                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                self.killer_moves[depth][0] = move
    
    def store_in_tt(self, board_hash: int, score: int, move: Optional[Tuple], depth: int):
        """УЛУЧШЕНО: Оптимизированное сохранение в TT"""
        # Заменяем, если глубина больше или равна
        if board_hash in self.transposition_table:
            old_depth = self.transposition_table[board_hash]['depth']
            if depth >= old_depth:
                self.transposition_table[board_hash] = {
                    'score': score, 'move': move, 'depth': depth
                }
        elif len(self.transposition_table) < self.max_tt_size:
            self.transposition_table[board_hash] = {
                'score': score, 'move': move, 'depth': depth
            }
        else:
            # Замена случайной записи с малой глубиной
            for key in list(self.transposition_table.keys())[:100]:
                if self.transposition_table[key]['depth'] < depth - 2:
                    del self.transposition_table[key]
                    self.transposition_table[board_hash] = {
                        'score': score, 'move': move, 'depth': depth
                    }
                    break
    
    def get_board_hash(self, board: List[List[str]], turn: bool) -> int:
        """Zobrist hashing"""
        hash_value = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    square = row * 8 + col
                    hash_value ^= self.zobrist_keys['pieces'][piece][square]
        
        if turn:
            hash_value ^= self.zobrist_keys['turn']
        
        return hash_value
    
    def make_move(self, board: List[List[str]], move: Tuple[Tuple[int, int], Tuple[int, int]]) -> List[List[str]]:
        """Выполнение хода"""
        from_pos, to_pos = move
        new_board = [row[:] for row in board]
        
        piece = new_board[from_pos[0]][from_pos[1]]
        new_board[to_pos[0]][to_pos[1]] = piece
        new_board[from_pos[0]][from_pos[1]] = '.'
        
        return new_board
    
    def is_in_check(self, board: List[List[str]], is_white: bool) -> bool:
        """Проверка шаха"""
        king_pos = self.find_king(board, is_white)
        if not king_pos:
            return False
        
        king_square = king_pos[0] * 8 + king_pos[1]
        return self.is_square_attacked(board, king_square, not is_white)
    
    def is_square_attacked(self, board: List[List[str]], square_index: int, by_white: bool) -> bool:
        """Проверка атаки клетки"""
        if not self.engine_wrapper:
            return False
        
        target_row = square_index // 8
        target_col = square_index % 8
        
        original_board = self.engine_wrapper.board_state
        original_turn = self.engine_wrapper.current_turn
        self.engine_wrapper.board_state = [row[:] for row in board]
        self.engine_wrapper.current_turn = by_white
        
        result = False
        for from_row in range(8):
            for from_col in range(8):
                piece = board[from_row][from_col]
                if piece != '.' and piece.isupper() == by_white:
                    if self.engine_wrapper.is_valid_attack((from_row, from_col), (target_row, target_col)):
                        result = True
                        break
            if result:
                break
        
        self.engine_wrapper.board_state = original_board
        self.engine_wrapper.current_turn = original_turn
        return result
    
    def get_best_move(self, board: List[List[str]], color: bool, time_limit: float = 3.0) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Получение лучшего хода с итеративным углублением"""
        self.nodes_searched = 0
        self.tt_hits = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        
        self.killer_moves = [[None, None] for _ in range(64)]
        
        best_overall_move = None
        prev_eval = 0
        current_depth = 1
        
        # Итеративное углубление с aspiration windows
        for current_depth in range(1, self.search_depth + 1):
            if current_depth >= 3 and prev_eval is not None:
                window = 50
                alpha = prev_eval - window
                beta = prev_eval + window
                
                eval_score, move = self.minimax(board, current_depth, alpha, beta, color)
                
                if eval_score <= alpha or eval_score >= beta:
                    eval_score, move = self.minimax(board, current_depth, float('-inf'), float('inf'), color)
            else:
                eval_score, move = self.minimax(board, current_depth, float('-inf'), float('inf'), color)
            
            if move:
                best_overall_move = move
                prev_eval = eval_score
            
            if time.time() - self.start_time > self.time_limit:
                break
        
        print(f"Глубина поиска ИИ: {current_depth}")
        print(f"Узлов проверено: {self.nodes_searched}, Попаданий в TT: {self.tt_hits}")
        if prev_eval is not None:
            print(f"Оценка позиции: {prev_eval/100:.2f} пешек")
        
        return best_overall_move


def test_enhanced_ai():
    """Тестирование улучшенного ИИ v2.0"""
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
    
    ai = EnhancedChessAI(search_depth=4)
    
    print("🤖 Тестирование улучшенного шахматного ИИ v2.0")
    print("=" * 50)
    
    start_time = time.perf_counter()
    score = ai.evaluate_position(test_board)
    eval_time = time.perf_counter() - start_time
    
    print(f"Оценка позиции: {score} ({score/100:.2f} пешек)")
    print(f"Время оценки: {eval_time*1000:.4f} мс")
    
    start_time = time.perf_counter()
    best_move = ai.get_best_move(test_board, True, time_limit=3.0)
    move_time = time.perf_counter() - start_time
    
    print(f"Лучший ход найден: {best_move}")
    print(f"Время расчета: {move_time:.4f} с")
    print(f"Узлов/сек: {ai.nodes_searched/move_time:.0f}")
    
    return score, best_move, move_time


if __name__ == "__main__":
    test_enhanced_ai()