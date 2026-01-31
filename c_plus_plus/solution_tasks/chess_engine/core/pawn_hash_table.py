#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pawn Hash Table Implementation
Efficiently caches pawn structure evaluations for performance improvement
"""

from typing import List, Dict, Optional, Tuple
import hashlib
import struct

class PawnHashTable:
    """Specialized hash table for pawn structure caching"""
    
    def __init__(self, size_mb: int = 32):
        """
        Initialize pawn hash table
        
        Args:
            size_mb: Size of hash table in megabytes
        """
        self.entries_per_mb = 1024 * 1024 // 24  # Approximate entry size
        self.table_size = size_mb * self.entries_per_mb
        self.table = [None] * self.table_size
        self.hits = 0
        self.misses = 0
        
        print(f"♟️ Pawn hash table initialized: {size_mb}MB ({self.table_size:,} entries)")
    
    def _get_pawn_key(self, board: List[List[str]]) -> int:
        """
        Generate hash key specifically for pawn positions
        Only considers pawns for faster computation and better cache locality
        """
        # Create compact representation of pawn positions
        pawn_positions = []
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.lower() == 'p':  # Only pawns
                    # Encode piece type, color, and position
                    is_white = 1 if piece.isupper() else 0
                    position_key = (row << 3) | col  # 6 bits for position
                    pawn_key = (is_white << 7) | position_key
                    pawn_positions.append(pawn_key)
        
        # Sort for position independence
        pawn_positions.sort()
        
        # Create hash from sorted pawn positions
        if not pawn_positions:
            return 0
            
        # Convert to bytes for hashing
        pawn_bytes = struct.pack(f'{len(pawn_positions)}H', *pawn_positions)
        hash_object = hashlib.md5(pawn_bytes)
        hash_value = int.from_bytes(hash_object.digest()[:8], byteorder='little')
        
        return hash_value % self.table_size
    
    def store_pawn_evaluation(self, board: List[List[str]], score: int, 
                             passed_pawns_w: int, passed_pawns_b: int,
                             pawn_shield_w: int, pawn_shield_b: int,
                             isolated_pawns_w: int, isolated_pawns_b: int):
        """
        Store pawn structure evaluation in hash table
        
        Args:
            board: Current board state
            score: Pawn structure evaluation score
            passed_pawns_w: Number of white passed pawns
            passed_pawns_b: Number of black passed pawns
            pawn_shield_w: White king pawn shield quality
            pawn_shield_b: Black king pawn shield quality
            isolated_pawns_w: Number of white isolated pawns
            isolated_pawns_b: Number of black isolated pawns
        """
        key = self._get_pawn_key(board)
        
        entry = {
            'score': score,
            'passed_pawns_w': passed_pawns_w,
            'passed_pawns_b': passed_pawns_b,
            'pawn_shield_w': pawn_shield_w,
            'pawn_shield_b': pawn_shield_b,
            'isolated_pawns_w': isolated_pawns_w,
            'isolated_pawns_b': isolated_pawns_b
        }
        
        self.table[key] = entry
    
    def probe_pawn_evaluation(self, board: List[List[str]]) -> Optional[Dict]:
        """
        Probe pawn hash table for cached evaluation
        
        Args:
            board: Current board state
            
        Returns:
            Cached evaluation data or None if not found
        """
        key = self._get_pawn_key(board)
        entry = self.table[key]
        
        if entry is not None:
            self.hits += 1
            return entry.copy()  # Return copy to prevent external modification
        else:
            self.misses += 1
            return None
    
    def get_hit_rate(self) -> float:
        """Get cache hit rate as percentage"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0
    
    def clear(self):
        """Clear the hash table"""
        self.table = [None] * self.table_size
        self.hits = 0
        self.misses = 0
    
    def get_statistics(self) -> Dict[str, any]:
        """Get detailed statistics"""
        total_probes = self.hits + self.misses
        occupancy = sum(1 for entry in self.table if entry is not None)
        
        return {
            'size_mb': len(self.table) * 24 // (1024 * 1024),
            'entries': len(self.table),
            'occupancy': occupancy,
            'occupancy_rate': occupancy / len(self.table) * 100,
            'hits': self.hits,
            'misses': self.misses,
            'total_probes': total_probes,
            'hit_rate': self.get_hit_rate()
        }

class EnhancedPawnEvaluator:
    """Enhanced pawn structure evaluator with caching"""
    
    def __init__(self, cache_size_mb: int = 64):
        self.pawn_hash = PawnHashTable(cache_size_mb)
        self.piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
        }
    
    def evaluate_pawn_structure(self, board: List[List[str]]) -> int:
        """
        Comprehensive pawn structure evaluation with caching
        """
        # Check cache first
        cached = self.pawn_hash.probe_pawn_evaluation(board)
        if cached:
            return cached['score']
        
        # Calculate pawn structure factors
        white_pawns = self._get_pawn_positions(board, True)
        black_pawns = self._get_pawn_positions(board, False)
        
        # 1. Passed pawns
        passed_w = self._count_passed_pawns(white_pawns, black_pawns, True)
        passed_b = self._count_passed_pawns(black_pawns, white_pawns, False)
        
        # 2. Isolated pawns
        isolated_w = self._count_isolated_pawns(white_pawns)
        isolated_b = self._count_isolated_pawns(black_pawns)
        
        # 3. Doubled pawns
        doubled_w = self._count_doubled_pawns(white_pawns)
        doubled_b = self._count_doubled_pawns(black_pawns)
        
        # 4. Pawn chains and connectivity
        chain_w = self._evaluate_pawn_chains(white_pawns)
        chain_b = self._evaluate_pawn_chains(black_pawns)
        
        # 5. King pawn shield
        shield_w = self._evaluate_king_shield(board, white_pawns, True)
        shield_b = self._evaluate_king_shield(board, black_pawns, False)
        
        # Calculate total score
        score = 0
        
        # Passed pawn bonus (very important)
        score += passed_w * 25  # Base passed pawn value
        score -= passed_b * 25
        
        # Isolated pawn penalty
        score -= isolated_w * 15
        score += isolated_b * 15
        
        # Doubled pawn penalty
        score -= doubled_w * 10
        score += doubled_b * 10
        
        # Chain bonus
        score += chain_w * 5
        score -= chain_b * 5
        
        # King shield bonus
        score += shield_w * 8
        score -= shield_b * 8
        
        # Store in cache
        self.pawn_hash.store_pawn_evaluation(
            board, score, passed_w, passed_b, shield_w, shield_b, isolated_w, isolated_b
        )
        
        return score
    
    def _get_pawn_positions(self, board: List[List[str]], is_white: bool) -> List[Tuple[int, int]]:
        """Get positions of all pawns of specified color"""
        pawn_char = 'P' if is_white else 'p'
        positions = []
        
        for row in range(8):
            for col in range(8):
                if board[row][col] == pawn_char:
                    positions.append((row, col))
        
        return positions
    
    def _count_passed_pawns(self, own_pawns: List[Tuple[int, int]], 
                           enemy_pawns: List[Tuple[int, int]], is_white: bool) -> int:
        """Count passed pawns for given color"""
        passed_count = 0
        direction = -1 if is_white else 1  # White moves up, black moves down
        
        for pawn_row, pawn_col in own_pawns:
            is_passed = True
            
            # Check if any enemy pawn can capture or block this pawn
            for enemy_row, enemy_col in enemy_pawns:
                # Same column or adjacent columns
                if abs(enemy_col - pawn_col) <= 1:
                    # Enemy pawn is ahead of our pawn
                    if (is_white and enemy_row < pawn_row) or (not is_white and enemy_row > pawn_row):
                        is_passed = False
                        break
            
            if is_passed:
                passed_count += 1
        
        return passed_count
    
    def _count_isolated_pawns(self, pawns: List[Tuple[int, int]]) -> int:
        """Count isolated pawns (no friendly pawns on adjacent files)"""
        isolated_count = 0
        
        for pawn_row, pawn_col in pawns:
            is_isolated = True
            
            # Check adjacent files
            for other_row, other_col in pawns:
                if other_col != pawn_col and abs(other_col - pawn_col) == 1:
                    is_isolated = False
                    break
            
            if is_isolated:
                isolated_count += 1
        
        return isolated_count
    
    def _count_doubled_pawns(self, pawns: List[Tuple[int, int]]) -> int:
        """Count doubled pawns (multiple pawns on same file)"""
        file_counts = [0] * 8
        doubled_count = 0
        
        # Count pawns per file
        for _, col in pawns:
            file_counts[col] += 1
        
        # Count files with more than one pawn
        for count in file_counts:
            if count > 1:
                doubled_count += (count - 1)  # Each extra pawn beyond first
        
        return doubled_count
    
    def _evaluate_pawn_chains(self, pawns: List[Tuple[int, int]]) -> int:
        """Evaluate pawn chain formation"""
        chain_score = 0
        
        for pawn_row, pawn_col in pawns:
            # Check for supporting pawns diagonally behind
            supporting_positions = [
                (pawn_row + 1, pawn_col - 1),  # Bottom-left
                (pawn_row + 1, pawn_col + 1),  # Bottom-right
            ]
            
            for supp_row, supp_col in supporting_positions:
                if 0 <= supp_row < 8 and 0 <= supp_col < 8:
                    if (supp_row, supp_col) in pawns:
                        chain_score += 1
        
        return chain_score
    
    def _evaluate_king_shield(self, board: List[List[str]], 
                             pawns: List[Tuple[int, int]], is_white: bool) -> int:
        """Evaluate pawn shield around the king"""
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
            return 0
        
        king_row, king_col = king_pos
        shield_score = 0
        
        # Define shield area around king
        shield_positions = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row = king_row + dr
                new_col = king_col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    shield_positions.append((new_row, new_col))
        
        # Count friendly pawns in shield area
        for pawn_row, pawn_col in pawns:
            if (pawn_row, pawn_col) in shield_positions:
                shield_score += 1
        
        return shield_score

# Test function
def test_pawn_hash():
    """Test pawn hash table functionality"""
    print("♟️ PAWN HASH TABLE TEST")
    print("=" * 40)
    
    # Create evaluator
    evaluator = EnhancedPawnEvaluator(cache_size_mb=16)
    
    # Test positions
    test_positions = [
        # Starting position
        [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ],
        # Advanced pawn position
        [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['.', 'p', 'p', '.', '.', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['p', '.', '.', 'p', 'p', '.', '.', '.'],
            ['.', '.', '.', 'P', 'P', '.', '.', '.'],
            ['.', '.', 'P', '.', '.', '.', '.', '.'],
            ['P', 'P', '.', '.', '.', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    ]
    
    print("Testing pawn structure evaluation...")
    
    for i, position in enumerate(test_positions):
        print(f"\nPosition {i + 1}:")
        
        # First evaluation (uncached)
        score1 = evaluator.evaluate_pawn_structure(position)
        stats1 = evaluator.pawn_hash.get_statistics()
        print(f"  First eval: {score1}")
        print(f"  Cache hit rate: {stats1['hit_rate']:.1f}%")
        
        # Second evaluation (cached)
        score2 = evaluator.evaluate_pawn_structure(position)
        stats2 = evaluator.pawn_hash.get_statistics()
        print(f"  Second eval: {score2}")
        print(f"  Cache hit rate: {stats2['hit_rate']:.1f}%")
        
        # Verify caching works
        assert score1 == score2, "Cached evaluation should match original"
        assert stats2['hits'] > stats1['hits'], "Second call should hit cache"
    
    # Final statistics
    final_stats = evaluator.pawn_hash.get_statistics()
    print(f"\n📊 FINAL STATISTICS:")
    print(f"  Cache size: {final_stats['size_mb']}MB")
    print(f"  Entries: {final_stats['entries']:,}")
    print(f"  Occupancy: {final_stats['occupancy']:,} ({final_stats['occupancy_rate']:.1f}%)")
    print(f"  Total probes: {final_stats['total_probes']:,}")
    print(f"  Hit rate: {final_stats['hit_rate']:.1f}%")
    
    print("\n✅ Pawn hash table test completed successfully!")

if __name__ == "__main__":
    test_pawn_hash()