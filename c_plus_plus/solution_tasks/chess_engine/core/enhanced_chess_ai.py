#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Chess AI with Advanced Evaluation Function
Features:
- Multi-layer position evaluation
- Tactical pattern recognition
- Material and positional assessment
- King safety evaluation
- Mobility analysis
"""

from typing import List, Tuple, Dict
import math
import json

class EnhancedChessAI:
    """Advanced chess AI with sophisticated evaluation"""
    
    def __init__(self, search_depth: int = 4):
        self.search_depth = search_depth
        self.transposition_table = {}
        self.history_table = {}
        self.initialize_evaluation_weights()
        
    def initialize_evaluation_weights(self):
        """Initialize evaluation weights for different factors"""
        self.weights = {
            # Material values
            'material': 1.0,
            'piece_square': 0.1,
            'mobility': 0.1,
            'pawn_structure': 0.15,
            'king_safety': 0.2,
            'center_control': 0.1,
            'development': 0.05,
            'tempo': 0.05
        }
        
        # Piece values
        self.piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
        
        # Piece-square tables (simplified)
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
        
        # Mirror tables for black pieces
        for piece in ['P', 'N', 'B', 'R', 'Q', 'K']:
            white_table = self.piece_square_tables[piece]
            black_table = white_table[::-1]  # Reverse for black
            self.piece_square_tables[piece.lower()] = black_table
    
    def evaluate_position(self, board: List[List[str]]) -> int:
        """Enhanced position evaluation function"""
        score = 0
        
        # 1. Material evaluation
        material_score = self.evaluate_material(board)
        score += self.weights['material'] * material_score
        
        # 2. Piece-square table evaluation
        pst_score = self.evaluate_piece_square_tables(board)
        score += self.weights['piece_square'] * pst_score
        
        # 3. Mobility evaluation
        mobility_score = self.evaluate_mobility(board)
        score += self.weights['mobility'] * mobility_score
        
        # 4. Pawn structure evaluation
        pawn_score = self.evaluate_pawn_structure(board)
        score += self.weights['pawn_structure'] * pawn_score
        
        # 5. King safety evaluation
        king_safety_score = self.evaluate_king_safety(board)
        score += self.weights['king_safety'] * king_safety_score
        
        # 6. Center control evaluation
        center_score = self.evaluate_center_control(board)
        score += self.weights['center_control'] * center_score
        
        # 7. Development evaluation (early game)
        development_score = self.evaluate_development(board)
        score += self.weights['development'] * development_score
        
        return int(score)
    
    def evaluate_material(self, board: List[List[str]]) -> int:
        """Evaluate material balance"""
        material = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    material += self.piece_values.get(piece, 0)
        return material
    
    def evaluate_piece_square_tables(self, board: List[List[str]]) -> int:
        """Evaluate piece positions using piece-square tables"""
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
        """Evaluate piece mobility"""
        from optimized_move_generator import BitboardMoveGenerator
        generator = BitboardMoveGenerator()
        
        white_moves = len(generator.generate_legal_moves(board, True))
        black_moves = len(generator.generate_legal_moves(board, False))
        
        return (white_moves - black_moves) * 5  # Mobility bonus
    
    def evaluate_pawn_structure(self, board: List[List[str]]) -> int:
        """Evaluate pawn structure"""
        score = 0
        
        # Check for doubled pawns
        for col in range(8):
            white_pawns = 0
            black_pawns = 0
            for row in range(8):
                if board[row][col] == 'P':
                    white_pawns += 1
                elif board[row][col] == 'p':
                    black_pawns += 1
            
            if white_pawns > 1:
                score -= (white_pawns - 1) * 10  # Penalty for doubled pawns
            if black_pawns > 1:
                score += (black_pawns - 1) * 10  # Bonus for opponent's doubled pawns
        
        # Check for isolated pawns
        score += self.evaluate_isolated_pawns(board)
        
        return score
    
    def evaluate_isolated_pawns(self, board: List[List[str]]) -> int:
        """Evaluate isolated pawns"""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.lower() == 'p':
                    is_isolated = True
                    # Check adjacent columns
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
                            score -= 15  # Penalty for isolated white pawn
                        else:
                            score += 15  # Bonus for isolated black pawn
        
        return score
    
    def evaluate_king_safety(self, board: List[List[str]]) -> int:
        """Evaluate king safety"""
        score = 0
        
        # Find kings
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
        """Evaluate safety around the king"""
        king_row, king_col = king_pos
        score = 0
        enemy_color = 'black' if is_white else 'white'
        
        # Check king zone (3x3 area around king)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = king_row + dr, king_col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board[new_row][new_col]
                    if piece != '.':
                        # Friendly pieces near king are good
                        if (piece.isupper() and is_white) or (piece.islower() and not is_white):
                            score += 5
                        # Enemy pieces near king are bad
                        else:
                            score -= 10
        
        return score
    
    def evaluate_center_control(self, board: List[List[str]]) -> int:
        """Evaluate center control"""
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        score = 0
        
        for row, col in center_squares:
            piece = board[row][col]
            if piece != '.':
                if piece.isupper():  # White piece
                    score += 10
                else:  # Black piece
                    score -= 10
        
        return score
    
    def evaluate_development(self, board: List[List[str]]) -> int:
        """Evaluate piece development (early game)"""
        score = 0
        
        # Knights developed from starting position
        if board[7][1] == '.' and board[6][0] == 'N':  # White knight
            score += 20
        if board[7][6] == '.' and board[6][7] == 'N':  # White knight
            score += 20
        if board[0][1] == '.' and board[1][0] == 'n':  # Black knight
            score -= 20
        if board[0][6] == '.' and board[1][7] == 'n':  # Black knight
            score -= 20
        
        # Bishops developed
        if board[7][2] == '.' and board[6][1] == 'B':  # White bishop
            score += 15
        if board[7][5] == '.' and board[6][6] == 'B':  # White bishop
            score += 15
        if board[0][2] == '.' and board[1][1] == 'b':  # Black bishop
            score -= 15
        if board[0][5] == '.' and board[1][6] == 'b':  # Black bishop
            score -= 15
        
        return score
    
    def minimax(self, board: List[List[str]], depth: int, alpha: float, beta: float, 
                maximizing_player: bool) -> Tuple[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Minimax algorithm with alpha-beta pruning"""
        
        # Terminal conditions
        if depth == 0:
            return self.evaluate_position(board), None
        
        # Generate legal moves
        from optimized_move_generator import BitboardMoveGenerator
        generator = BitboardMoveGenerator()
        moves = generator.generate_legal_moves(board, maximizing_player)
        
        if not moves:
            # Check for checkmate or stalemate
            if self.is_in_check(board, maximizing_player):
                return -100000 if maximizing_player else 100000, None
            else:
                return 0, None  # Stalemate
        
        best_move = None
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval, best_move
    
    def make_move(self, board: List[List[str]], move: Tuple[Tuple[int, int], Tuple[int, int]]) -> List[List[str]]:
        """Make a move on the board (returns new board)"""
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Create copy of board
        new_board = [row[:] for row in board]
        
        # Make move
        piece = new_board[from_row][from_col]
        new_board[to_row][to_col] = piece
        new_board[from_row][from_col] = '.'
        
        return new_board
    
    def is_in_check(self, board: List[List[str]], is_white: bool) -> bool:
        """Check if the king is in check"""
        # Find king position
        king_char = 'K' if is_white else 'k'
        king_pos = None
        
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_char:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Check if any opponent piece attacks the king
        opponent_color = not is_white
        from optimized_move_generator import BitboardMoveGenerator
        generator = BitboardMoveGenerator()
        opponent_moves = generator.generate_legal_moves(board, opponent_color)
        
        for move in opponent_moves:
            _, to_pos = move
            if to_pos == king_pos:
                return True
        
        return False
    
    def get_best_move(self, board: List[List[str]], color: bool) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get the best move for the given position"""
        _, best_move = self.minimax(board, self.search_depth, float('-inf'), float('inf'), color)
        return best_move

# Test the enhanced AI
def test_enhanced_ai():
    """Test the enhanced AI performance"""
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
    
    ai = EnhancedChessAI(search_depth=3)
    
    print("🤖 Testing Enhanced Chess AI")
    print("=" * 40)
    
    # Test position evaluation
    start_time = time.perf_counter()
    score = ai.evaluate_position(test_board)
    eval_time = time.perf_counter() - start_time
    
    print(f"Position evaluation: {score}")
    print(f"Evaluation time: {eval_time*1000:.4f} ms")
    
    # Test move generation
    start_time = time.perf_counter()
    best_move = ai.get_best_move(test_board, True)
    move_time = time.perf_counter() - start_time
    
    print(f"Best move found: {best_move}")
    print(f"Move calculation time: {move_time:.4f} s")
    
    return score, best_move, move_time

if __name__ == "__main__":
    test_enhanced_ai()