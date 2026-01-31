#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stockfish NNUE Integration - Enhanced Neural Network Evaluator
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Union
import math
import pickle
import os
import json
from pathlib import Path

class StockfishNNUE:
    """Stockfish-style NNUE (Efficiently Updatable Neural Network) evaluator"""
    
    def __init__(self, feature_set_size: int = 768, hidden_dim: int = 256):
        """
        Initialize Stockfish-style NNUE
        
        Args:
            feature_set_size: Number of HalfKP features (768 = 64 squares × 12 piece types)
            hidden_dim: Size of hidden layer
        """
        self.feature_set_size = feature_set_size
        self.hidden_dim = hidden_dim
        self.output_dim = 1
        
        # Feature transformer weights (input to hidden)
        # Weights for white perspective and black perspective
        self.ft_weights_white = np.random.normal(0, 0.1, (feature_set_size, hidden_dim))
        self.ft_weights_black = np.random.normal(0, 0.1, (feature_set_size, hidden_dim))
        
        # Biases for feature transformer
        self.ft_bias = np.zeros(hidden_dim)
        
        # Output layer weights
        self.output_weights = np.random.normal(0, 0.1, (hidden_dim * 2, self.output_dim))  # *2 for both perspectives
        self.output_bias = np.zeros(self.output_dim)
        
        # Clipping values (NNUE uses clipped ReLU)
        self.ft_clip_min = -127
        self.ft_clip_max = 127
        self.out_clip_min = -32768
        self.out_clip_max = 32767
        
        # Accumulators for incremental updates
        self.accumulator_white = np.zeros(hidden_dim)
        self.accumulator_black = np.zeros(hidden_dim)
        
        # Cache for performance
        self.eval_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
        print(f"🎯 Stockfish NNUE initialized")
        print(f"   Features: {feature_set_size}")
        print(f"   Hidden dim: {hidden_dim}")
        print(f"   Parameters: {(feature_set_size * hidden_dim * 2 + hidden_dim * 2 + 1):,}")
    
    def piece_to_index(self, piece: str, square: int) -> int:
        """Convert piece and square to HalfKP feature index"""
        piece_types = {'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
                      'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11}
        
        if piece not in piece_types:
            return -1
            
        piece_idx = piece_types[piece]
        return square * 12 + piece_idx
    
    def board_to_features(self, board: List[List[str]]) -> Tuple[List[int], List[int]]:
        """
        Convert board to active feature indices for both perspectives
        
        Returns:
            (white_features, black_features) - lists of active feature indices
        """
        white_features = []
        black_features = []
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    square = row * 8 + col
                    feature_idx = self.piece_to_index(piece, square)
                    
                    if feature_idx >= 0:
                        if piece.isupper():  # White piece
                            white_features.append(feature_idx)
                            # For black perspective, mirror the square vertically
                            mirrored_square = (7 - row) * 8 + col
                            black_feature_idx = self.piece_to_index(piece.lower(), mirrored_square)
                            if black_feature_idx >= 0:
                                black_features.append(black_feature_idx)
                        else:  # Black piece
                            black_features.append(feature_idx)
                            # For white perspective, mirror the square vertically
                            mirrored_square = (7 - row) * 8 + col
                            white_feature_idx = self.piece_to_index(piece.upper(), mirrored_square)
                            if white_feature_idx >= 0:
                                white_features.append(white_feature_idx)
        
        return white_features, black_features
    
    def refresh_accumulator(self, board: List[List[str]]):
        """Refresh accumulators from scratch (full calculation)"""
        white_features, black_features = self.board_to_features(board)
        
        # Reset accumulators
        self.accumulator_white = self.ft_bias.copy()
        self.accumulator_black = self.ft_bias.copy()
        
        # Add contributions from active features
        for feat_idx in white_features:
            self.accumulator_white += self.ft_weights_white[feat_idx]
        
        for feat_idx in black_features:
            self.accumulator_black += self.ft_weights_black[feat_idx]
        
        # Apply clipping
        self.accumulator_white = np.clip(self.accumulator_white, self.ft_clip_min, self.ft_clip_max)
        self.accumulator_black = np.clip(self.accumulator_black, self.ft_clip_min, self.ft_clip_max)
    
    def update_accumulator(self, board: List[List[str]], move_history: List):
        """Incrementally update accumulator based on move history"""
        # For simplicity, we'll refresh from scratch
        # In a real implementation, you'd track incremental changes
        self.refresh_accumulator(board)
    
    def evaluate(self, board: List[List[str]], turn: bool = True) -> float:
        """
        Evaluate position using NNUE
        
        Args:
            board: 8x8 board representation
            turn: True for white, False for black
            
        Returns:
            Evaluation score in centipawns
        """
        # Check cache first
        board_tuple = tuple(tuple(row) for row in board)
        cache_key = (board_tuple, turn)
        
        if cache_key in self.eval_cache:
            self.cache_hits += 1
            return self.eval_cache[cache_key]
        
        self.cache_misses += 1
        
        # Refresh accumulators
        self.refresh_accumulator(board)
        
        # Concatenate both perspectives
        combined_hidden = np.concatenate([self.accumulator_white, self.accumulator_black])
        
        # Output layer (clipped linear)
        output = np.dot(combined_hidden, self.output_weights) + self.output_bias
        clipped_output = np.clip(output, self.out_clip_min, self.out_clip_max)
        
        # Convert to centipawns
        score = float(clipped_output[0]) / 100.0  # Scale down from Stockfish's internal scale
        
        # Adjust for side to move
        if not turn:
            score = -score
        
        # Cache result
        self.eval_cache[cache_key] = score
        
        return score
    
    def get_cache_hit_rate(self) -> float:
        """Get cache hit rate percentage"""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    def save_weights(self, filepath: str):
        """Save NNUE weights to file"""
        weights_dict = {
            'ft_weights_white': self.ft_weights_white,
            'ft_weights_black': self.ft_weights_black,
            'ft_bias': self.ft_bias,
            'output_weights': self.output_weights,
            'output_bias': self.output_bias,
            'feature_set_size': self.feature_set_size,
            'hidden_dim': self.hidden_dim
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(weights_dict, f)
        
        print(f"💾 NNUE weights saved to {filepath}")
    
    def load_weights(self, filepath: str) -> bool:
        """Load NNUE weights from file"""
        if not os.path.exists(filepath):
            print(f"⚠️ Weights file {filepath} not found")
            return False
        
        try:
            with open(filepath, 'rb') as f:
                weights_dict = pickle.load(f)
            
            self.ft_weights_white = weights_dict['ft_weights_white']
            self.ft_weights_black = weights_dict['ft_weights_black']
            self.ft_bias = weights_dict['ft_bias']
            self.output_weights = weights_dict['output_weights']
            self.output_bias = weights_dict['output_bias']
            
            print(f"📂 NNUE weights loaded from {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to load weights: {e}")
            return False

class EnhancedNeuralEvaluator:
    """Enhanced neural evaluator combining multiple approaches"""
    
    def __init__(self, model_path: Optional[str] = None):
        # Initialize different evaluation methods
        self.nnue = StockfishNNUE()
        self.simple_nn = None  # Will be initialized if needed
        
        # Load pre-trained model if available
        if model_path and os.path.exists(model_path):
            if model_path.endswith('.pkl') or model_path.endswith('.pickle'):
                self.nnue.load_weights(model_path)
            else:
                print(f"⚠️ Unsupported model format: {model_path}")
        
        # Weight mixing ratios
        self.nnue_weight = 0.8    # 80% NNUE
        self.traditional_weight = 0.2  # 20% traditional
        
        # Piece values for traditional evaluation
        self.piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
        
        print(f"🚀 Enhanced Neural Evaluator initialized")
        print(f"   NNUE weight: {self.nnue_weight*100:.0f}%")
        print(f"   Traditional weight: {self.traditional_weight*100:.0f}%")
    
    def evaluate_position(self, board: List[List[str]], turn: bool = True) -> float:
        """
        Enhanced evaluation combining NNUE and traditional methods
        """
        # NNUE evaluation
        nnue_score = self.nnue.evaluate(board, turn)
        
        # Traditional evaluation
        traditional_score = self._traditional_evaluation(board, turn)
        
        # Combine evaluations
        final_score = (
            self.nnue_weight * nnue_score + 
            self.traditional_weight * traditional_score
        )
        
        return final_score
    
    def _traditional_evaluation(self, board: List[List[str]], turn: bool) -> float:
        """Comprehensive traditional evaluation"""
        # Material evaluation
        material_score = 0
        piece_counts = {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0,
                       'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in self.piece_values:
                    material_score += self.piece_values[piece]
                    if piece != 'K' and piece != 'k':
                        piece_counts[piece] += 1
        
        # Positional evaluation
        positional_score = 0
        
        # Center control
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for row, col in center_squares:
            piece = board[row][col]
            if piece != '.':
                bonus = 10 if piece.isupper() else -10
                positional_score += bonus
        
        # Piece development
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in ['N', 'B', 'n', 'b']:
                    # Bonus for developed minor pieces
                    if 2 <= row <= 5 and 2 <= col <= 5:
                        bonus = 5 if piece.isupper() else -5
                        positional_score += bonus
        
        # Pawn structure
        pawn_score = self._evaluate_pawn_structure(board)
        
        # King safety
        king_score = self._evaluate_king_safety(board)
        
        total_traditional = material_score + positional_score + pawn_score + king_score
        
        # Adjust for side to move
        if not turn:
            total_traditional = -total_traditional
            
        return total_traditional / 100.0  # Convert to pawn units
    
    def _evaluate_pawn_structure(self, board: List[List[str]]) -> int:
        """Evaluate pawn structure"""
        score = 0
        
        # Count pawns per file
        white_pawns_per_file = [0] * 8
        black_pawns_per_file = [0] * 8
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece == 'P':
                    white_pawns_per_file[col] += 1
                elif piece == 'p':
                    black_pawns_per_file[col] += 1
        
        # Doubled pawns penalty
        for file_count in white_pawns_per_file:
            if file_count > 1:
                score -= (file_count - 1) * 15
        
        for file_count in black_pawns_per_file:
            if file_count > 1:
                score += (file_count - 1) * 15
        
        # Passed pawns bonus
        score += self._count_passed_pawns(board, True) * 25
        score -= self._count_passed_pawns(board, False) * 25
        
        return score
    
    def _count_passed_pawns(self, board: List[List[str]], is_white: bool) -> int:
        """Count passed pawns for given side"""
        count = 0
        direction = -1 if is_white else 1  # White pawns move up, black down
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if (is_white and piece == 'P') or (not is_white and piece == 'p'):
                    # Check if pawn is passed (no opposing pawns ahead)
                    is_passed = True
                    
                    # Check squares ahead in same file and adjacent files
                    for r_offset in range(1, 8):
                        check_row = row + direction * r_offset
                        if 0 <= check_row < 8:
                            # Same file
                            if board[check_row][col].lower() == ('p' if is_white else 'P'):
                                is_passed = False
                                break
                            
                            # Adjacent files
                            for c_offset in [-1, 1]:
                                check_col = col + c_offset
                                if 0 <= check_col < 8:
                                    if board[check_row][check_col].lower() == ('p' if is_white else 'P'):
                                        is_passed = False
                                        break
                        if not is_passed:
                            break
                    
                    if is_passed:
                        count += 1
        
        return count
    
    def _evaluate_king_safety(self, board: List[List[str]]) -> int:
        """Evaluate king safety"""
        score = 0
        
        # Find kings
        white_king_pos = None
        black_king_pos = None
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece == 'K':
                    white_king_pos = (row, col)
                elif piece == 'k':
                    black_king_pos = (row, col)
        
        # Evaluate white king safety
        if white_king_pos:
            score += self._evaluate_single_king_safety(board, white_king_pos, True)
        
        # Evaluate black king safety
        if black_king_pos:
            score -= self._evaluate_single_king_safety(board, black_king_pos, False)
        
        return score
    
    def _evaluate_single_king_safety(self, board: List[List[str]], king_pos: Tuple[int, int], is_white: bool) -> int:
        """Evaluate safety for a single king"""
        score = 0
        king_row, king_col = king_pos
        
        # Pawn shield bonus
        shield_bonus = 0
        pawn_char = 'P' if is_white else 'p'
        
        # Check squares in front of and around the king
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = king_row + dr, king_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if board[r][c] == pawn_char:
                        shield_bonus += 10
        
        score += shield_bonus
        
        # Exposure penalty for edge positions
        if king_col in [0, 7]:  # Edge files
            score -= 15
        elif king_col in [1, 6]:  # Near edge
            score -= 5
        
        return max(-50, min(50, score))  # Clamp to reasonable range
    
    def get_cache_hit_rate(self) -> float:
        """Get NNUE cache hit rate"""
        return self.nnue.get_cache_hit_rate()
    
    def clear_cache(self):
        """Clear evaluation cache"""
        self.nnue.eval_cache.clear()
        self.nnue.cache_hits = 0
        self.nnue.cache_misses = 0

# Test function
def test_stockfish_nnue():
    """Test Stockfish NNUE implementation"""
    print("🎯 STOCKFISH NNUE TEST")
    print("=" * 40)
    
    # Create enhanced evaluator
    evaluator = EnhancedNeuralEvaluator()
    
    # Test positions
    test_positions = [
        # Starting position
        ([
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ], True, "Starting position"),
        
        # Italian Game position
        ([
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', '.', '.', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'p', 'p', '.', '.', '.'],
            ['.', '.', '.', 'P', 'P', '.', '.', '.'],
            ['.', '.', '.', '.', '.', 'N', '.', '.'],
            ['P', 'P', 'P', '.', '.', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', '.', 'R']
        ], True, "Italian Game"),
        
        # Endgame position
        ([
            ['.', '.', '.', '.', 'k', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'K', '.', '.', '.']
        ], True, "King vs King endgame")
    ]
    
    print("Testing position evaluations...")
    
    for board, turn, description in test_positions:
        print(f"\n{description}:")
        
        # NNUE evaluation
        nnue_score = evaluator.nnue.evaluate(board, turn)
        print(f"  NNUE Score: {nnue_score:+.2f}")
        
        # Traditional evaluation
        trad_score = evaluator._traditional_evaluation(board, turn)
        print(f"  Traditional: {trad_score:+.2f}")
        
        # Combined evaluation
        combined_score = evaluator.evaluate_position(board, turn)
        print(f"  Combined: {combined_score:+.2f}")
        
        # Cache statistics
        cache_rate = evaluator.get_cache_hit_rate()
        print(f"  Cache hit rate: {cache_rate:.1f}%")
    
    # Performance test
    print(f"\n⚡ Performance test...")
    board, turn, _ = test_positions[0]
    
    import time
    
    # Warm up
    for _ in range(10):
        evaluator.evaluate_position(board, turn)
    
    # Timed evaluation
    start_time = time.perf_counter()
    evaluations = 1000
    
    for _ in range(evaluations):
        evaluator.evaluate_position(board, turn)
    
    elapsed_time = time.perf_counter() - start_time
    avg_time = elapsed_time / evaluations * 1000  # ms
    
    print(f"  {evaluations} evaluations in {elapsed_time:.3f}s")
    print(f"  Average time: {avg_time:.3f}ms per evaluation")
    print(f"  Evaluations/sec: {evaluations/elapsed_time:.0f}")
    
    if avg_time < 1.0:
        print("  ✅ Excellent performance!")
    elif avg_time < 5.0:
        print("  ✅ Good performance")
    else:
        print("  ⚠️ Performance could be improved")
    
    print(f"\n✅ Stockfish NNUE test completed!")

if __name__ == "__main__":
    test_stockfish_nnue()