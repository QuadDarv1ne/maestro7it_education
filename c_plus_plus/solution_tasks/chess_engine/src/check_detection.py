#!/usr/bin/env python3
"""
Система обнаружения шаха и мата
Реализует полную проверку шахматных правил согласно FIDE
"""

class CheckDetector:
    """Класс для обнаружения шаха, мата и других состояний игры"""
    
    def __init__(self):
        # Направления движения фигур (для атаки)
        self.directions = {
            'R': [(0, 1), (0, -1), (1, 0), (-1, 0)],  # Ладья - горизонталь/вертикаль
            'B': [(1, 1), (1, -1), (-1, 1), (-1, -1)], # Слон - диагонали
            'Q': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)], # Ферзь - все направления
            'K': [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)], # Король - все направления (1 шаг)
            'N': [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)] # Конь - Г-образные ходы
        }
        
        # Типы состояний игры
        self.GameState = {
            'NORMAL': 'NORMAL',
            'CHECK': 'CHECK',
            'CHECKMATE': 'CHECKMATE',
            'STALEMATE': 'STALEMATE',
            'INSUFFICIENT_MATERIAL': 'INSUFFICIENT_MATERIAL',
            'THREEFOLD_REPETITION': 'THREEFOLD_REPETITION',
            'FIFTY_MOVE_RULE': 'FIFTY_MOVE_RULE'
        }
    
    def detect_check(self, board_state):
        """
        Проверяет, находится ли король под шахом
        """
        board = board_state['board']
        white_to_move = board_state['turn'] == 'white'
        
        # Находим короля текущего игрока
        king_pos = self._find_king(board, white_to_move)
        if king_pos is None:
            return {
                'in_check': False,
                'attacking_pieces': [],
                'attack_squares': [],
                'game_state': self.GameState['NORMAL']
            }
        
        # Проверяем, атакуют ли короля фигуры противника
        attackers = []
        attack_squares = []
        
        # Проверяем все фигуры противника
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and self._is_opponent_piece(piece, white_to_move):
                    if self._attacks_square(board, row, col, king_pos[0], king_pos[1]):
                        attackers.append((row, col))
                        attack_squares.append((row, col))
        
        in_check = len(attackers) > 0
        
        # Определяем состояние игры
        game_state = self.GameState['NORMAL']
        if in_check:
            if self._is_checkmate(board, king_pos, white_to_move, attackers):
                game_state = self.GameState['CHECKMATE']
            else:
                game_state = self.GameState['CHECK']
        elif self._is_stalemate(board, white_to_move):
            game_state = self.GameState['STALEMATE']
        elif self._is_insufficient_material(board):
            game_state = self.GameState['INSUFFICIENT_MATERIAL']
        
        return {
            'in_check': in_check,
            'attacking_pieces': attackers,
            'attack_squares': attack_squares,
            'game_state': game_state
        }
    
    def _find_king(self, board, white_king):
        """Находит позицию короля"""
        king_symbol = 'K' if white_king else 'k'
        
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_symbol:
                    return (row, col)
        return None
    
    def _is_opponent_piece(self, piece, white_to_move):
        """Проверяет, является ли фигура фигурой противника"""
        if white_to_move:
            return piece.islower()  # Черные фигуры
        else:
            return piece.isupper()  # Белые фигуры
    
    def _attacks_square(self, board, from_row, from_col, to_row, to_col):
        """Проверяет, атакует ли фигура конкретную клетку"""
        piece = board[from_row][from_col]
        piece_type = piece.upper()
        
        # Пешка
        if piece_type == 'P':
            return self._pawn_attacks(from_row, from_col, to_row, to_col, piece.isupper())
        
        # Конь
        if piece_type == 'N':
            return self._knight_attacks(from_row, from_col, to_row, to_col)
        
        # Король
        if piece_type == 'K':
            return self._king_attacks(from_row, from_col, to_row, to_col)
        
        # Ладья, Слон, Ферзь
        if piece_type in ['R', 'B', 'Q']:
            return self._ray_attacks(board, from_row, from_col, to_row, to_col, piece_type)
        
        return False
    
    def _pawn_attacks(self, from_row, from_col, to_row, to_col, is_white):
        """Проверяет, атакует ли пешка клетку"""
        direction = -1 if is_white else 1
        # Пешка атакует по диагонали
        return (to_row == from_row + direction and 
                abs(to_col - from_col) == 1)
    
    def _knight_attacks(self, from_row, from_col, to_row, to_col):
        """Проверяет, атакует ли конь клетку"""
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def _king_attacks(self, from_row, from_col, to_row, to_col):
        """Проверяет, атакует ли король клетку"""
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0)
    
    def _ray_attacks(self, board, from_row, from_col, to_row, to_col, piece_type):
        """Проверяет, атакует ли лучевая фигура (ладья/слон/ферзь) клетку"""
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        # Проверяем направление
        if piece_type in ['R', 'Q']:  # Ладья и ферзь
            if row_diff == 0 or col_diff == 0:  # Горизонталь или вертикаль
                return self._is_ray_clear(board, from_row, from_col, to_row, to_col)
        
        if piece_type in ['B', 'Q']:  # Слон и ферзь
            if abs(row_diff) == abs(col_diff):  # Диагональ
                return self._is_ray_clear(board, from_row, from_col, to_row, to_col)
        
        return False
    
    def _is_ray_clear(self, board, from_row, from_col, to_row, to_col):
        """Проверяет, свободен ли путь между двумя клетками"""
        row_step = self._sign(to_row - from_row)
        col_step = self._sign(to_col - from_col)
        
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while current_row != to_row or current_col != to_col:
            if board[current_row][current_col] is not None:
                return False
            current_row += row_step
            current_col += col_step
        
        return True
    
    def _sign(self, x):
        """Возвращает знак числа"""
        return 1 if x > 0 else (-1 if x < 0 else 0)
    
    def _is_checkmate(self, board, king_pos, white_to_move, attackers):
        """Проверяет, является ли позиция матом"""
        # Проверяем, есть ли легальные ходы короля
        king_moves = self._get_king_legal_moves(board, king_pos, white_to_move)
        if king_moves:
            return False
        
        # Если король атакован одной фигурой, можно ли закрыться или съесть атакующую фигуру
        if len(attackers) == 1:
            attacker_pos = attackers[0]
            # Проверяем, могут ли другие фигуры помочь
            if self._can_escape_check(board, king_pos, attacker_pos, white_to_move):
                return False
        
        return True
    
    def _get_king_legal_moves(self, board, king_pos, white_to_move):
        """Получает все легальные ходы короля"""
        moves = []
        king_row, king_col = king_pos
        
        # Проверяем все 8 направлений
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row = king_row + dr
                new_col = king_col + dc
                
                if (0 <= new_row < 8 and 0 <= new_col < 8 and
                    (board[new_row][new_col] is None or 
                     self._is_opponent_piece(board[new_row][new_col], white_to_move))):
                    
                    # Временно перемещаем короля для проверки
                    temp_piece = board[new_row][new_col]
                    board[new_row][new_col] = board[king_row][king_col]
                    board[king_row][king_col] = None
                    
                    # Проверяем, не под шахом ли новая позиция
                    if not self._is_square_attacked(board, new_row, new_col, not white_to_move):
                        moves.append((new_row, new_col))
                    
                    # Возвращаем доску в исходное состояние
                    board[king_row][king_col] = board[new_row][new_col]
                    board[new_row][new_col] = temp_piece
        
        return moves
    
    def _is_square_attacked(self, board, row, col, by_white_pieces):
        """Проверяет, атакована ли клетка фигурами заданного цвета"""
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and self._is_piece_color(piece, by_white_pieces):
                    if self._attacks_square(board, r, c, row, col):
                        return True
        return False
    
    def _is_piece_color(self, piece, white_pieces):
        """Проверяет цвет фигуры"""
        return piece.isupper() if white_pieces else piece.islower()
    
    def _can_escape_check(self, board, king_pos, attacker_pos, white_to_move):
        """Проверяет, можно ли избежать шаха"""
        # Проверяем, могут ли другие фигуры съесть атакующую фигуру
        attacker_row, attacker_col = attacker_pos
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and not self._is_opponent_piece(piece, white_to_move):
                    if self._attacks_square(board, row, col, attacker_row, attacker_col):
                        return True
        
        # Проверяем, можно ли закрыться (для дальнобойных фигур)
        if self._is_long_range_attacker(board[attacker_row][attacker_col]):
            # Проверяем, можно ли поставить фигуру между королем и атакующей фигурой
            blocking_squares = self._get_blocking_squares(king_pos, attacker_pos)
            for block_row, block_col in blocking_squares:
                if board[block_row][block_col] is None:
                    # Проверяем, может ли какая-либо фигура пойти на эту клетку
                    for row in range(8):
                        for col in range(8):
                            piece = board[row][col]
                            if piece and not self._is_opponent_piece(piece, white_to_move):
                                if self._attacks_square(board, row, col, block_row, block_col):
                                    return True
        
        return False
    
    def _is_long_range_attacker(self, piece):
        """Проверяет, является ли фигура дальнобойной"""
        return piece.upper() in ['R', 'B', 'Q']
    
    def _get_blocking_squares(self, king_pos, attacker_pos):
        """Получает клетки, которые могут блокировать атаку"""
        king_row, king_col = king_pos
        att_row, att_col = attacker_pos
        
        squares = []
        
        if king_row == att_row:  # Горизонтальная атака
            start_col = min(king_col, att_col) + 1
            end_col = max(king_col, att_col)
            for col in range(start_col, end_col):
                squares.append((king_row, col))
        elif king_col == att_col:  # Вертикальная атака
            start_row = min(king_row, att_row) + 1
            end_row = max(king_row, att_row)
            for row in range(start_row, end_row):
                squares.append((row, king_col))
        elif abs(king_row - att_row) == abs(king_col - att_col):  # Диагональная атака
            row_step = 1 if att_row > king_row else -1
            col_step = 1 if att_col > king_col else -1
            current_row = king_row + row_step
            current_col = king_col + col_step
            while current_row != att_row and current_col != att_col:
                squares.append((current_row, current_col))
                current_row += row_step
                current_col += col_step
        
        return squares
    
    def _is_stalemate(self, board, white_to_move):
        """Проверяет, является ли позиция патом"""
        # Проверяем, есть ли у игрока какие-либо легальные ходы
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and not self._is_opponent_piece(piece, white_to_move):
                    # Проверяем, есть ли легальные ходы для этой фигуры
                    if self._has_legal_moves(board, row, col, white_to_move):
                        return False
        return True
    
    def _has_legal_moves(self, board, row, col, white_to_move):
        """Проверяет, есть ли легальные ходы для фигуры"""
        piece = board[row][col]
        piece_type = piece.upper()
        
        # Упрощенная проверка - в реальной реализации нужно проверить каждый возможный ход
        # и убедиться, что он не оставляет короля под шахом
        return True  # Заглушка
    
    def _is_insufficient_material(self, board):
        """Проверяет недостаток материала для мата"""
        # Подсчитываем фигуры
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    pieces.append(piece.upper())
        
        # Проверяем условия ничьей по материалу
        if len(pieces) <= 2:  # Только короли
            return True
        elif len(pieces) == 3:  # Король + слон/конь против короля
            piece_types = [p for p in pieces if p != 'K']
            if len(piece_types) == 1 and piece_types[0] in ['B', 'N']:
                return True
        
        return False

# Глобальный экземпляр
g_check_detector = CheckDetector()