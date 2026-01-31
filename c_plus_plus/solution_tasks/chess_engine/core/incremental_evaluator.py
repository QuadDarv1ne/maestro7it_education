#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Incremental Evaluator - Python wrapper for incremental position evaluation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class IncrementalEvaluator:
    """Python wrapper for incremental position evaluation system"""
    
    def __init__(self, board_state=None):
        """
        Initialize incremental evaluator
        
        Args:
            board_state: Initial board state (8x8 list of strings)
        """
        self.board_state = board_state or self._get_initial_board()
        self.material_score = 0
        self.positional_score = 0
        self.mobility_score = 0
        self.pawn_structure_score = 0
        self.king_safety_score = 0
        
        # Material values (centipawns)
        self.MATERIAL_VALUES = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
        
        # Positional bonuses
        self.POSITIONAL_BONUSES = self._initialize_positional_bonuses()
        self.MOBILITY_BONUSES = {'N': 3, 'B': 3, 'R': 4, 'Q': 5, 'K': 0}
        
        # Initialize scores
        self.full_recalculate()
    
    def _get_initial_board(self):
        """Get initial chess board setup"""
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
    
    def _initialize_positional_bonuses(self):
        """Initialize positional bonus table"""
        bonuses = {}
        for rank in range(8):
            for file in range(8):
                square = rank * 8 + file
                bonus = 0
                
                # Center control bonus
                if 2 <= file <= 5 and 2 <= rank <= 5:
                    bonus += 10
                
                # Development bonus for initial positions
                if rank == 1 or rank == 6:
                    bonus += 5
                    
                bonuses[square] = bonus
        return bonuses
    
    def set_board(self, board_state):
        """Set new board state and recalculate"""
        self.board_state = board_state
        self.full_recalculate()
    
    def full_recalculate(self):
        """Perform full recalculation of all evaluation components"""
        self.material_score = self._calculate_material_score()
        self.positional_score = self._calculate_positional_score()
        self.mobility_score = self._calculate_mobility_score()
        self.pawn_structure_score = self._calculate_pawn_structure_score()
        self.king_safety_score = self._calculate_king_safety_score()
    
    def _calculate_material_score(self):
        """Calculate material score"""
        score = 0
        for rank in range(8):
            for file in range(8):
                piece = self.board_state[rank][file]
                if piece != '.':
                    score += self.MATERIAL_VALUES.get(piece, 0)
        return score
    
    def _calculate_positional_score(self):
        """Calculate positional score"""
        score = 0
        for rank in range(8):
            for file in range(8):
                piece = self.board_state[rank][file]
                if piece != '.':
                    square = rank * 8 + file
                    if piece.isupper():  # White pieces
                        score += self.POSITIONAL_BONUSES[square]
                    else:  # Black pieces
                        score -= self.POSITIONAL_BONUSES[square]
        return score
    
    def _calculate_mobility_score(self):
        """Calculate mobility score (simplified)"""
        score = 0
        # This is a simplified version - in practice would calculate actual legal moves
        piece_counts = {}
        for rank in range(8):
            for file in range(8):
                piece = self.board_state[rank][file]
                if piece in 'PNBRQK':
                    piece_counts[piece] = piece_counts.get(piece, 0) + 1
                elif piece in 'pnbrqk':
                    piece_counts[piece] = piece_counts.get(piece, 0) + 1
        
        # Approximate mobility based on piece counts and positions
        for piece, count in piece_counts.items():
            if piece.upper() in self.MOBILITY_BONUSES:
                bonus = self.MOBILITY_BONUSES[piece.upper()]
                if piece.isupper():
                    score += count * bonus * 2  # White pieces
                else:
                    score -= count * bonus * 2  # Black pieces
                    
        return score
    
    def _calculate_pawn_structure_score(self):
        """Calculate pawn structure score"""
        score = 0
        white_pawns = []
        black_pawns = []
        
        # Collect pawn positions
        for rank in range(8):
            for file in range(8):
                piece = self.board_state[rank][file]
                if piece == 'P':
                    white_pawns.append((rank, file))
                elif piece == 'p':
                    black_pawns.append((rank, file))
        
        # Analyze white pawn structure
        score += self._analyze_pawn_structure(white_pawns, black_pawns, True)
        
        # Analyze black pawn structure (negative)
        score -= self._analyze_pawn_structure(black_pawns, white_pawns, False)
        
        return score
    
    def _analyze_pawn_structure(self, own_pawns, enemy_pawns, is_white):
        """Analyze pawn structure for one side"""
        score = 0
        file_counts = [0] * 8
        
        # Count pawns per file
        for rank, file in own_pawns:
            file_counts[file] += 1
        
        # Check for doubled pawns
        for count in file_counts:
            if count > 1:
                score -= 15 * (count - 1)  # Penalty for doubled pawns
        
        # Check for isolated pawns
        for i, (rank, file) in enumerate(own_pawns):
            isolated = True
            for other_rank, other_file in own_pawns:
                if abs(file - other_file) == 1:  # Adjacent file
                    isolated = False
                    break
            if isolated:
                score -= 20  # Isolated pawn penalty
        
        # Check for passed pawns
        for rank, file in own_pawns:
            passed = True
            if is_white:
                # Check squares ahead for enemy pawns
                for r in range(rank + 1, 8):
                    for f in range(max(0, file - 1), min(8, file + 2)):
                        if (r, f) in [(er, ef) for er, ef in enemy_pawns]:
                            passed = False
                            break
                    if not passed:
                        break
            else:
                # Check squares behind for enemy pawns
                for r in range(rank - 1, -1, -1):
                    for f in range(max(0, file - 1), min(8, file + 2)):
                        if (r, f) in [(er, ef) for er, ef in enemy_pawns]:
                            passed = False
                            break
                    if not passed:
                        break
            
            if passed:
                # Bonus based on advancement
                advancement = rank if is_white else (7 - rank)
                score += 25 + advancement * 5
        
        return max(-100, min(100, score))  # Clamp to reasonable range
    
    def _calculate_king_safety_score(self):
        """Calculate king safety score"""
        score = 0
        
        # Find kings
        white_king_pos = None
        black_king_pos = None
        
        for rank in range(8):
            for file in range(8):
                piece = self.board_state[rank][file]
                if piece == 'K':
                    white_king_pos = (rank, file)
                elif piece == 'k':
                    black_king_pos = (rank, file)
        
        # Evaluate white king safety
        if white_king_pos:
            score += self._evaluate_king_safety(white_king_pos, True)
        
        # Evaluate black king safety (negative)
        if black_king_pos:
            score -= self._evaluate_king_safety(black_king_pos, False)
        
        return score
    
    def _evaluate_king_safety(self, king_pos, is_white):
        """Evaluate safety for a specific king"""
        score = 0
        king_rank, king_file = king_pos
        
        # Pawn shield bonus
        shield_bonus = 0
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                r, f = king_rank + dr, king_file + df
                if 0 <= r < 8 and 0 <= f < 8:
                    piece = self.board_state[r][f]
                    if (is_white and piece == 'P') or (not is_white and piece == 'p'):
                        shield_bonus += 10
        
        score += shield_bonus
        
        # Exposure penalty (simplified)
        # In practice, would check for open files/attacks near king
        if king_file in [0, 1, 6, 7]:  # Edge positions are somewhat exposed
            score -= 5
        
        return max(-50, min(50, score))  # Clamp to reasonable range
    
    def update_on_move(self, from_pos, to_pos, captured_piece=None):
        """
        Incrementally update evaluation after a move
        
        Args:
            from_pos: (rank, file) tuple of source position
            to_pos: (rank, file) tuple of destination position
            captured_piece: Piece that was captured (if any)
        """
        from_rank, from_file = from_pos
        to_rank, to_file = to_pos
        from_square = from_rank * 8 + from_file
        to_square = to_rank * 8 + to_file
        
        moved_piece = self.board_state[to_rank][to_file]  # Piece after move
        
        if moved_piece == '.':
            return  # Invalid move
        
        # Update material score if piece was captured
        if captured_piece:
            captured_value = abs(self.MATERIAL_VALUES.get(captured_piece, 0))
            if moved_piece.isupper():  # White captured
                self.material_score += captured_value
            else:  # Black captured
                self.material_score -= captured_value
        
        # Update positional score
        if moved_piece.isupper():  # White piece
            self.positional_score -= self.POSITIONAL_BONUSES[from_square]
            self.positional_score += self.POSITIONAL_BONUSES[to_square]
        else:  # Black piece
            self.positional_score += self.POSITIONAL_BONUSES[from_square]
            self.positional_score -= self.POSITIONAL_BONUSES[to_square]
        
        # Update pawn structure if pawn moved
        if moved_piece.upper() == 'P':
            # Recalculate pawn structure (could be optimized further)
            old_pawn_score = self.pawn_structure_score
            self.pawn_structure_score = self._calculate_pawn_structure_score()
    
    def evaluate(self):
        """Get total evaluation score"""
        total = (self.material_score + self.positional_score + 
                self.mobility_score + self.pawn_structure_score + 
                self.king_safety_score)
        return total
    
    def get_evaluation_breakdown(self):
        """Get detailed breakdown of evaluation components"""
        return {
            'material': self.material_score,
            'positional': self.positional_score,
            'mobility': self.mobility_score,
            'pawn_structure': self.pawn_structure_score,
            'king_safety': self.king_safety_score,
            'total': self.evaluate()
        }
    
    def print_evaluation(self):
        """Print detailed evaluation breakdown"""
        breakdown = self.get_evaluation_breakdown()
        print("\n=== POSITION EVALUATION BREAKDOWN ===")
        print(f"Material score:      {breakdown['material']:>6}")
        print(f"Positional score:    {breakdown['positional']:>6}")
        print(f"Mobility score:      {breakdown['mobility']:>6}")
        print(f"Pawn structure:      {breakdown['pawn_structure']:>6}")
        print(f"King safety:         {breakdown['king_safety']:>6}")
        print("-" * 35)
        print(f"Total evaluation:    {breakdown['total']:>6}")
        print("=" * 35)
        
        # Interpretation
        if breakdown['total'] > 100:
            print("White has significant advantage")
        elif breakdown['total'] > 50:
            print("White has moderate advantage")
        elif breakdown['total'] > 10:
            print("White has slight advantage")
        elif breakdown['total'] < -100:
            print("Black has significant advantage")
        elif breakdown['total'] < -50:
            print("Black has moderate advantage")
        elif breakdown['total'] < -10:
            print("Black has slight advantage")
        else:
            print("Position is roughly equal")

# Test function
def test_incremental_evaluator():
    """Test the incremental evaluator"""
    print("🔬 TESTING INCREMENTAL EVALUATOR")
    print("=" * 40)
    
    # Create evaluator
    evaluator = IncrementalEvaluator()
    print("✅ Incremental evaluator created")
    
    # Test initial position
    print("\nInitial position evaluation:")
    evaluator.print_evaluation()
    
    # Test after a move
    print("\nAfter 1.e4:")
    # Simulate pawn move from e2 to e4
    evaluator.board_state[6][4] = '.'  # e2
    evaluator.board_state[4][4] = 'P'  # e4
    evaluator.update_on_move((6, 4), (4, 4))
    evaluator.print_evaluation()
    
    # Test after another move
    print("\nAfter 1...e5:")
    # Simulate pawn move from e7 to e5
    evaluator.board_state[1][4] = '.'  # e7
    evaluator.board_state[3][4] = 'p'  # e5
    evaluator.update_on_move((1, 4), (3, 4))
    evaluator.print_evaluation()
    
    print("\n✅ Incremental evaluator test completed!")

if __name__ == "__main__":
    test_incremental_evaluator()