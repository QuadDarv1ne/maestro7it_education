#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Оптимизированный генератор шахматных ходов на основе битбордов
Использует 64-битные целые числа для представления позиций для максимальной производительности
"""

from typing import List, Tuple, Set
import numpy as np

class BitboardMoveGenerator:
    """Высокопроизводительный генератор ходов с использованием битбордов"""
    
    def __init__(self):
        # Предвычисленные таблицы атак для скользящих фигур
        self.initialize_attack_tables()
        
        # Таблицы позиций фигур для оценки
        self.piece_square_tables = self.initialize_piece_square_tables()
        
    def initialize_attack_tables(self):
        """Инициализация предвычисленных таблиц атак для более быстрой генерации ходов"""
        # Векторы направлений для скользящих фигур
        self.directions = {
            'rook': [(0, 1), (0, -1), (1, 0), (-1, 0)],      # Горизонталь/Вертикаль
            'bishop': [(1, 1), (1, -1), (-1, 1), (-1, -1)],  # Диагонали
            'queen': [(0, 1), (0, -1), (1, 0), (-1, 0),      # Все направления
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }
        
        # Предвычисление лучей для каждой клетки и направления
        self.rays = {}
        for square in range(64):
            self.rays[square] = {}
            row, col = square // 8, square % 8
            
            # Лучи ладьи
            self.rays[square]['rook'] = self.compute_ray(row, col, self.directions['rook'])
            
            # Лучи слона
            self.rays[square]['bishop'] = self.compute_ray(row, col, self.directions['bishop'])
            
            # Лучи ферзя (комбинация)
            self.rays[square]['queen'] = self.compute_ray(row, col, self.directions['queen'])
        
        # Ходы коня предвычислены
        self.knight_moves = self.compute_knight_moves()
        
        # Ходы короля предвычислены
        self.king_moves = self.compute_king_moves()
        
    def compute_ray(self, row: int, col: int, directions: List[Tuple[int, int]]) -> dict:
        """Вычисление атак лучами для фигуры с заданной позиции"""
        rays = {}
        for dr, dc in directions:
            mask = 0
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                mask |= (1 << (r * 8 + c))
                r += dr
                c += dc
            rays[(dr, dc)] = mask
        return rays
    
    def compute_knight_moves(self) -> dict:
        """Предвычисление всех возможных ходов коня"""
        knight_moves = {}
        knight_offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for square in range(64):
            row, col = square // 8, square % 8
            moves = 0
            for dr, dc in knight_offsets:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    moves |= (1 << (new_row * 8 + new_col))
            knight_moves[square] = moves
        return knight_moves
    
    def compute_king_moves(self) -> dict:
        """Предвычисление всех возможных ходов короля"""
        king_moves = {}
        king_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for square in range(64):
            row, col = square // 8, square % 8
            moves = 0
            for dr, dc in king_offsets:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    moves |= (1 << (new_row * 8 + new_col))
            king_moves[square] = moves
        return king_moves
    
    def initialize_piece_square_tables(self) -> dict:
        """Инициализация таблиц позиций фигур для оценки позиции"""
        # Упрощенные значения PST (бонусы за контроль центра)
        pst = {
            'pawn': [
                0,  0,  0,  0,  0,  0,  0,  0,
                5,  5,  5,  5,  5,  5,  5,  5,
                1,  1,  2,  3,  3,  2,  1,  1,
                0,  0,  1,  2,  2,  1,  0,  0,
                0,  0,  1,  2,  2,  1,  0,  0,
                1,  1,  2,  3,  3,  2,  1,  1,
                5,  5,  5,  5,  5,  5,  5,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ],
            'knight': [
                -5, -4, -3, -3, -3, -3, -4, -5,
                -4, -2,  0,  0,  0,  0, -2, -4,
                -3,  0,  1,  1,  1,  1,  0, -3,
                -3,  0,  1,  2,  2,  1,  0, -3,
                -3,  0,  1,  2,  2,  1,  0, -3,
                -3,  0,  1,  1,  1,  1,  0, -3,
                -4, -2,  0,  0,  0,  0, -2, -4,
                -5, -4, -3, -3, -3, -3, -4, -5
            ],
            'bishop': [
                -2, -1, -1, -1, -1, -1, -1, -2,
                -1,  0,  0,  0,  0,  0,  0, -1,
                -1,  0,  1,  1,  1,  1,  0, -1,
                -1,  0,  1,  2,  2,  1,  0, -1,
                -1,  0,  1,  2,  2,  1,  0, -1,
                -1,  0,  1,  1,  1,  1,  0, -1,
                -1,  0,  0,  0,  0,  0,  0, -1,
                -2, -1, -1, -1, -1, -1, -1, -2
            ]
        }
        return pst
    
    def board_to_bitboards(self, board: List[List[str]]) -> dict:
        """Преобразование стандартного представления доски в битборды"""
        bitboards = {
            'white_pawns': 0, 'white_knights': 0, 'white_bishops': 0,
            'white_rooks': 0, 'white_queens': 0, 'white_king': 0,
            'black_pawns': 0, 'black_knights': 0, 'black_bishops': 0,
            'black_rooks': 0, 'black_queens': 0, 'black_king': 0,
            'occupied': 0, 'white_occupied': 0, 'black_occupied': 0
        }
        
        for row in range(8):
            for col in range(8):
                square = row * 8 + col
                piece = board[row][col]
                
                if piece != '.':
                    bitboards['occupied'] |= (1 << square)
                    
                    if piece.isupper():
                        bitboards['white_occupied'] |= (1 << square)
                        piece_key = f"white_{self.piece_to_type(piece)}"
                    else:
                        bitboards['black_occupied'] |= (1 << square)
                        piece_key = f"black_{self.piece_to_type(piece)}"
                    
                    bitboards[piece_key] |= (1 << square)
        
        return bitboards
    
    def piece_to_type(self, piece: str) -> str:
        """Преобразование символа фигуры в имя типа"""
        piece_map = {
            'P': 'pawns', 'N': 'knights', 'B': 'bishops',
            'R': 'rooks', 'Q': 'queens', 'K': 'king',
            'p': 'pawns', 'n': 'knights', 'b': 'bishops',
            'r': 'rooks', 'q': 'queens', 'k': 'king'
        }
        return piece_map.get(piece.upper(), 'pawns')
    
    def is_square_attacked(self, board: List[List[str]], square: int, by_white: bool) -> bool:
        """Эффективная проверка, атакована ли клетка заданным цветом"""
        bitboards = self.board_to_bitboards(board)
        row, col = square // 8, square % 8
        
        # 1. Атаки пешек
        pawn_bb = bitboards['white_pawns' if by_white else 'black_pawns']
        if by_white:
            # Белые пешки атакуют снизу (больший индекс строки для черного короля)
            if col > 0 and (row < 7) and (board[row+1][col-1] == 'P'): return True
            if col < 7 and (row < 7) and (board[row+1][col+1] == 'P'): return True
        else:
            # Черные пешки атакуют сверху (меньший индекс строки для белого короля)
            if col > 0 and (row > 0) and (board[row-1][col-1] == 'p'): return True
            if col < 7 and (row > 0) and (board[row-1][col+1] == 'p'): return True
            
        # 2. Атаки коня
        knight_bb = bitboards['white_knights' if by_white else 'black_knights']
        if self.knight_moves[square] & knight_bb:
            return True
            
        # 3. Скользящие атаки (Ладья/Ферзь)
        rook_queen_bb = bitboards['white_rooks' if by_white else 'black_rooks'] | \
                        bitboards['white_queens' if by_white else 'black_queens']
        if self.compute_sliding_attacks(square, bitboards['occupied'], 'rook') & rook_queen_bb:
            return True
            
        # 4. Скользящие атаки (Слон/Ферзь)
        bishop_queen_bb = bitboards['white_bishops' if by_white else 'black_bishops'] | \
                          bitboards['white_queens' if by_white else 'black_queens']
        if self.compute_sliding_attacks(square, bitboards['occupied'], 'bishop') & bishop_queen_bb:
            return True
            
        # 5. Атаки короля
        king_bb = bitboards['white_king' if by_white else 'black_king']
        if self.king_moves[square] & king_bb:
            return True
            
        return False

    def generate_legal_moves(self, board: List[List[str]], color: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Генерация всех легальных ходов для заданного цвета с использованием битбордов"""
        bitboards = self.board_to_bitboards(board)
        moves = []
        
        if color:  # Ход белых
            piece_bb_prefix = 'white_'
            occupied_bb = bitboards['white_occupied']
            opponent_bb = bitboards['black_occupied']
        else:  # Ход черных
            piece_bb_prefix = 'black_'
            occupied_bb = bitboards['black_occupied']
            opponent_bb = bitboards['white_occupied']
        
        # Генерация ходов для каждого типа фигур
        moves.extend(self.generate_pawn_moves(bitboards, color, occupied_bb, opponent_bb))
        moves.extend(self.generate_knight_moves(bitboards, piece_bb_prefix, occupied_bb, opponent_bb))
        moves.extend(self.generate_bishop_moves(bitboards, piece_bb_prefix, occupied_bb, opponent_bb))
        moves.extend(self.generate_rook_moves(bitboards, piece_bb_prefix, occupied_bb, opponent_bb))
        moves.extend(self.generate_queen_moves(bitboards, piece_bb_prefix, occupied_bb, opponent_bb))
        moves.extend(self.generate_king_moves(bitboards, piece_bb_prefix, occupied_bb, opponent_bb))
        
        return moves
    
    def generate_pawn_moves(self, bitboards: dict, is_white: bool, occupied_bb: int, opponent_bb: int) -> List:
        """Generate pawn moves using bitboard operations"""
        moves = []
        direction = -1 if is_white else 1
        start_rank = 6 if is_white else 1
        promotion_rank = 0 if is_white else 7
        
        pawn_bb = bitboards[f"{'white' if is_white else 'black'}_pawns"]
        
        # Single pawn pushes
        single_push = (pawn_bb << 8) if is_white else (pawn_bb >> 8)
        single_push &= ~occupied_bb  # Remove occupied squares
        
        # Double pawn pushes (from starting position)
        double_push = (single_push << 8) if is_white else (single_push >> 8)
        rank_mask = 0xFF << (start_rank * 8) if is_white else 0xFF << (start_rank * 8)
        double_push &= ~occupied_bb & rank_mask
        
        # Captures
        capture_left = ((pawn_bb & 0xFEFEFEFEFEFEFEFE) << 7) if is_white else ((pawn_bb & 0xFEFEFEFEFEFEFEFE) >> 9)
        capture_right = ((pawn_bb & 0x7F7F7F7F7F7F7F7F) << 9) if is_white else ((pawn_bb & 0x7F7F7F7F7F7F7F7F) >> 7)
        captures = (capture_left | capture_right) & opponent_bb
        
        # Convert bitboard moves to coordinate moves
        moves.extend(self.bitboard_to_moves(single_push, direction, 'push'))
        moves.extend(self.bitboard_to_moves(double_push, direction * 2, 'double_push'))
        moves.extend(self.bitboard_to_captures(captures, direction, is_white))
        
        return moves
    
    def generate_knight_moves(self, bitboards: dict, piece_prefix: str, occupied_bb: int, opponent_bb: int) -> List:
        """Generate knight moves using precomputed attack tables"""
        moves = []
        knight_bb = bitboards[f"{piece_prefix}knights"]
        
        square = 0
        while knight_bb:
            if knight_bb & 1:
                attack_mask = self.knight_moves[square]
                # Legal moves = attacks - own pieces
                legal_moves = attack_mask & ~occupied_bb
                # Captures = attacks on opponent pieces
                captures = attack_mask & opponent_bb
                
                moves.extend(self.square_moves_to_coords(square, legal_moves, 'move'))
                moves.extend(self.square_moves_to_coords(square, captures, 'capture'))
            
            knight_bb >>= 1
            square += 1
        
        return moves
    
    def generate_bishop_moves(self, bitboards: dict, piece_prefix: str, occupied_bb: int, opponent_bb: int) -> List:
        """Generate bishop moves using ray attacks"""
        moves = []
        bishop_bb = bitboards[f"{piece_prefix}bishops"]
        
        square = 0
        while bishop_bb:
            if bishop_bb & 1:
                attack_mask = self.compute_sliding_attacks(square, occupied_bb, 'bishop')
                legal_moves = attack_mask & ~occupied_bb
                captures = attack_mask & opponent_bb
                
                moves.extend(self.square_moves_to_coords(square, legal_moves, 'move'))
                moves.extend(self.square_moves_to_coords(square, captures, 'capture'))
            
            bishop_bb >>= 1
            square += 1
        
        return moves
    
    def generate_rook_moves(self, bitboards: dict, piece_prefix: str, occupied_bb: int, opponent_bb: int) -> List:
        """Generate rook moves using ray attacks"""
        moves = []
        rook_bb = bitboards[f"{piece_prefix}rooks"]
        
        square = 0
        while rook_bb:
            if rook_bb & 1:
                attack_mask = self.compute_sliding_attacks(square, occupied_bb, 'rook')
                legal_moves = attack_mask & ~occupied_bb
                captures = attack_mask & opponent_bb
                
                moves.extend(self.square_moves_to_coords(square, legal_moves, 'move'))
                moves.extend(self.square_moves_to_coords(square, captures, 'capture'))
            
            rook_bb >>= 1
            square += 1
        
        return moves
    
    def generate_queen_moves(self, bitboards: dict, piece_prefix: str, occupied_bb: int, opponent_bb: int) -> List:
        """Generate queen moves (combination of rook and bishop)"""
        moves = []
        queen_bb = bitboards[f"{piece_prefix}queens"]
        
        square = 0
        while queen_bb:
            if queen_bb & 1:
                attack_mask = self.compute_sliding_attacks(square, occupied_bb, 'queen')
                legal_moves = attack_mask & ~occupied_bb
                captures = attack_mask & opponent_bb
                
                moves.extend(self.square_moves_to_coords(square, legal_moves, 'move'))
                moves.extend(self.square_moves_to_coords(square, captures, 'capture'))
            
            queen_bb >>= 1
            square += 1
        
        return moves
    
    def generate_king_moves(self, bitboards: dict, piece_prefix: str, occupied_bb: int, opponent_bb: int) -> List:
        """Generate king moves using precomputed attack table"""
        moves = []
        king_bb = bitboards[f"{piece_prefix}king"]
        
        if king_bb:
            square = 0
            while not (king_bb & 1):
                king_bb >>= 1
                square += 1
            
            attack_mask = self.king_moves[square]
            legal_moves = attack_mask & ~occupied_bb
            captures = attack_mask & opponent_bb
            
            moves.extend(self.square_moves_to_coords(square, legal_moves, 'move'))
            moves.extend(self.square_moves_to_coords(square, captures, 'capture'))
        
        return moves
    
    def compute_sliding_attacks(self, square: int, occupied_bb: int, piece_type: str) -> int:
        """Compute sliding piece attacks using occupancy information"""
        attack_mask = 0
        row, col = square // 8, square % 8
        
        for dr, dc in self.directions[piece_type]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_square = r * 8 + c
                attack_mask |= (1 << target_square)
                
                # Stop if blocked by any piece
                if occupied_bb & (1 << target_square):
                    break
                    
                r += dr
                c += dc
        
        return attack_mask
    
    def bitboard_to_moves(self, move_bb: int, direction: int, move_type: str) -> List:
        """Convert bitboard moves to coordinate format"""
        moves = []
        square = 0
        while move_bb:
            if move_bb & 1:
                from_row, from_col = square // 8, square % 8
                to_row, to_col = from_row + direction, from_col
                moves.append(((from_row, from_col), (to_row, to_col)))
            move_bb >>= 1
            square += 1
        return moves
    
    def bitboard_to_captures(self, capture_bb: int, direction: int, is_white: bool) -> List:
        """Convert bitboard captures to coordinate format"""
        moves = []
        square = 0
        while capture_bb:
            if capture_bb & 1:
                from_row, from_col = square // 8, square % 8
                # Calculate capture direction (diagonal)
                col_offset = 1 if (square % 8) < 4 else -1
                to_row, to_col = from_row + direction, from_col + col_offset
                moves.append(((from_row, from_col), (to_row, to_col)))
            capture_bb >>= 1
            square += 1
        return moves
    
    def square_moves_to_coords(self, from_square: int, move_bb: int, move_type: str) -> List:
        """Convert moves from a square to coordinate format"""
        moves = []
        from_row, from_col = from_square // 8, from_square % 8
        
        square = 0
        while move_bb:
            if move_bb & 1:
                to_row, to_col = square // 8, square % 8
                moves.append(((from_row, from_col), (to_row, to_col)))
            move_bb >>= 1
            square += 1
        
        return moves

# Performance test function
def test_bitboard_performance():
    """Test the performance of bitboard move generator"""
    import time
    
    # Test position
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
    
    generator = BitboardMoveGenerator()
    
    # Warm up
    for _ in range(100):
        generator.generate_legal_moves(test_board, True)
    
    # Measure performance
    start_time = time.perf_counter()
    iterations = 1000
    
    for _ in range(iterations):
        moves = generator.generate_legal_moves(test_board, True)
    
    end_time = time.perf_counter()
    
    avg_time = (end_time - start_time) / iterations
    moves_per_second = iterations / (end_time - start_time)
    
    print(f"Bitboard Performance Test Results:")
    print(f"Average time per move generation: {avg_time*1000:.4f} ms")
    print(f"Moves generated per second: {moves_per_second:.0f}")
    print(f"Generated {len(moves)} legal moves")
    
    return avg_time, moves_per_second

if __name__ == "__main__":
    test_bitboard_performance()