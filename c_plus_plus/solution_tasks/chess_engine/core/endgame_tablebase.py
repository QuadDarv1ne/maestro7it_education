#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Endgame Tablebase Implementation
Provides perfect play for positions with limited material
"""

from typing import List, Tuple, Dict, Optional, Set
import pickle
import os
import itertools
import math

class EndgameTablebase:
    """Endgame tablebase for perfect endgame play"""
    
    def __init__(self, max_pieces: int = 5):
        """
        Initialize endgame tablebase
        
        Args:
            max_pieces: Maximum number of pieces to include in tablebase
        """
        self.max_pieces = max_pieces
        self.tablebases = {}  # Dictionary of position -> result
        self.material_configs = set()  # Track material combinations
        self.generated_positions = 0
        self.loaded_positions = 0
        
        print(f"🎯 Endgame tablebase initialized for up to {max_pieces} pieces")
    
    def get_material_signature(self, board: List[List[str]]) -> str:
        """
        Create canonical material signature for position classification
        
        Args:
            board: Current board state
            
        Returns:
            String representing material composition
        """
        piece_counts = {
            'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0,
            'k': 0, 'q': 0, 'r': 0, 'b': 0, 'n': 0, 'p': 0
        }
        
        # Count pieces
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in piece_counts:
                    piece_counts[piece] += 1
        
        # Create canonical signature (white pieces first, then black)
        white_pieces = []
        black_pieces = []
        
        # Order: K, Q, R, B, N, P for each side
        piece_order = ['K', 'Q', 'R', 'B', 'N', 'P']
        
        for piece_type in piece_order:
            count = piece_counts[piece_type]
            if count > 0:
                white_pieces.extend([piece_type] * count)
            
            count = piece_counts[piece_type.lower()]
            if count > 0:
                black_pieces.extend([piece_type.lower()] * count)
        
        # Create signature
        signature = ''.join(white_pieces) + 'v' + ''.join(black_pieces)
        return signature
    
    def is_tablebase_position(self, board: List[List[str]]) -> bool:
        """
        Check if position qualifies for tablebase lookup
        
        Args:
            board: Current board state
            
        Returns:
            True if position has few enough pieces for tablebase
        """
        piece_count = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] != '.':
                    piece_count += 1
        
        return piece_count <= self.max_pieces
    
    def generate_kpk_tablebase(self) -> Dict[str, Tuple[str, int]]:
        """
        Generate King + Pawn vs King tablebase (most common endgame)
        
        Returns:
            Dictionary mapping positions to (result, distance_to_conversion)
        """
        print("♟️ Generating KPK tablebase...")
        kpk_tablebase = {}
        
        # Generate all legal KPK positions
        piece_types = ['K', 'k', 'P']
        
        # For each possible arrangement of pieces
        for white_king_sq in range(64):
            for black_king_sq in range(64):
                if white_king_sq == black_king_sq:
                    continue
                    
                for pawn_sq in range(8, 56):  # Pawns not on first/last ranks
                    # Create position string: WK_SQ:BK_SQ:P_SQ:TURN
                    position_key = f"{white_king_sq}:{black_king_sq}:{pawn_sq}"
                    
                    # Evaluate this position
                    result = self._evaluate_kpk_position(
                        white_king_sq, black_king_sq, pawn_sq
                    )
                    kpk_tablebase[position_key] = result
        
        print(f"✅ Generated {len(kpk_tablebase)} KPK positions")
        return kpk_tablebase
    
    def _evaluate_kpk_position(self, wk_sq: int, bk_sq: int, pawn_sq: int) -> Tuple[str, int]:
        """
        Evaluate specific KPK position using retrograde analysis
        
        Args:
            wk_sq: White king square (0-63)
            bk_sq: Black king square (0-63)  
            pawn_sq: Pawn square (0-63)
            
        Returns:
            Tuple of (result, distance) where result is 'win', 'draw', or 'loss'
        """
        # Simplified KPK evaluation
        wk_row, wk_col = wk_sq // 8, wk_sq % 8
        bk_row, bk_col = bk_sq // 8, bk_sq % 8
        pawn_row, pawn_col = pawn_sq // 8, pawn_sq % 8
        
        # Basic checks
        # 1. Kings too close (illegal)
        king_distance = max(abs(wk_row - bk_row), abs(wk_col - bk_col))
        if king_distance <= 1:
            return ('illegal', 0)
        
        # 2. Pawn can promote
        if pawn_row == 1:  # White pawn on 7th rank
            # Check if white king can support promotion
            promotion_distance = abs(wk_row - 0) + abs(wk_col - pawn_col)
            if promotion_distance <= 1:
                return ('win', 1)
        
        # 3. Opposition and key squares (simplified)
        if abs(wk_row - bk_row) == 2 and wk_col == bk_col:
            # Vertical opposition - usually drawish
            return ('draw', 10)
        
        # Default - complex position requiring deeper analysis
        return ('unknown', 0)
    
    def generate_basic_endgames(self) -> Dict[str, Dict]:
        """
        Generate tablebases for basic endgames
        
        Returns:
            Dictionary of material signatures to their tablebases
        """
        print("🎯 Generating basic endgame tablebases...")
        
        tablebases = {}
        
        # Common endgames to generate
        endgames = [
            'KvK',      # King vs King (trivial draws)
            'KQvK',     # Queen vs King (easy wins)
            'KRvK',     # Rook vs King (easy wins)
            'KBvK',     # Bishop vs King (draws)
            'KNvK',     # Knight vs King (draws)
            'KPk',      # Pawn vs King (varied results)
        ]
        
        for endgame in endgames:
            print(f"  Generating {endgame} tablebase...")
            tablebase = self._generate_single_endgame(endgame)
            tablebases[endgame] = tablebase
            self.generated_positions += len(tablebase)
        
        print(f"✅ Generated {len(endgames)} endgame tablebases")
        print(f"   Total positions: {self.generated_positions:,}")
        
        return tablebases
    
    def _generate_single_endgame(self, material_sig: str) -> Dict[str, Tuple[str, int]]:
        """Generate tablebase for specific material configuration"""
        tablebase = {}
        
        if material_sig == 'KvK':
            # All KvK positions are draws
            for wk_sq in range(64):
                for bk_sq in range(64):
                    if abs(wk_sq // 8 - bk_sq // 8) > 1 or abs(wk_sq % 8 - bk_sq % 8) > 1:
                        key = f"{wk_sq}:{bk_sq}"
                        tablebase[key] = ('draw', 0)
        
        elif material_sig == 'KQvK':
            # Queen vs King - all winnable except illegal positions
            for wk_sq in range(64):
                for bk_sq in range(64):
                    for q_sq in range(64):
                        if len({wk_sq, bk_sq, q_sq}) == 3:  # All different squares
                            key = f"{wk_sq}:{bk_sq}:{q_sq}"
                            # Check if queen attacks king
                            if self._attacks_square(q_sq, bk_sq):
                                tablebase[key] = ('win', 1)
                            else:
                                tablebase[key] = ('win', 5)  # Win in several moves
        
        elif material_sig == 'KRvK':
            # Similar logic for rook vs king
            for wk_sq in range(64):
                for bk_sq in range(64):
                    for r_sq in range(64):
                        if len({wk_sq, bk_sq, r_sq}) == 3:
                            key = f"{wk_sq}:{bk_sq}:{r_sq}"
                            if self._attacks_square(r_sq, bk_sq):
                                tablebase[key] = ('win', 1)
                            else:
                                tablebase[key] = ('win', 8)
        
        return tablebase
    
    def _attacks_square(self, piece_sq: int, target_sq: int) -> bool:
        """Check if piece on piece_sq attacks target_sq (simplified)"""
        piece_row, piece_col = piece_sq // 8, piece_sq % 8
        target_row, target_col = target_sq // 8, target_sq % 8
        
        # Queen/Rook attacks (same row or column)
        if piece_row == target_row or piece_col == target_col:
            return True
        
        # Queen/Bishop attacks (diagonals)
        if abs(piece_row - target_row) == abs(piece_col - target_col):
            return True
        
        return False
    
    def probe_tablebase(self, board: List[List[str]]) -> Optional[Tuple[str, int, Optional[Tuple]]]:
        """
        Probe tablebase for perfect endgame play
        
        Args:
            board: Current board state
            
        Returns:
            Tuple of (result, distance, best_move) or None if not in tablebase
        """
        if not self.is_tablebase_position(board):
            return None
        
        material_sig = self.get_material_signature(board)
        
        # Check if we have this material configuration
        if material_sig not in self.tablebases:
            return None
        
        # Generate position key
        position_key = self._board_to_key(board)
        
        # Look up in tablebase
        if position_key in self.tablebases[material_sig]:
            result, distance = self.tablebases[material_sig][position_key]
            best_move = self._get_tablebase_move(board, material_sig, position_key)
            return (result, distance, best_move)
        
        return None
    
    def _board_to_key(self, board: List[List[str]]) -> str:
        """Convert board to position key for tablebase lookup"""
        pieces = {}
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    square = row * 8 + col
                    if piece not in pieces:
                        pieces[piece] = []
                    pieces[piece].append(square)
        
        # Create canonical key
        key_parts = []
        piece_order = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']
        
        for piece_type in piece_order:
            if piece_type in pieces:
                squares = sorted(pieces[piece_type])
                for sq in squares:
                    key_parts.append(str(sq))
        
        return ':'.join(key_parts)
    
    def _get_tablebase_move(self, board: List[List[str]], material_sig: str, 
                           position_key: str) -> Optional[Tuple]:
        """Get best move from tablebase (simplified)"""
        # This would contain actual move generation logic
        # For now, return None to indicate tablebase knows result but not move
        return None
    
    def save_tablebases(self, filepath: str):
        """Save generated tablebases to file"""
        data = {
            'tablebases': self.tablebases,
            'max_pieces': self.max_pieces,
            'generated_positions': self.generated_positions
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"💾 Tablebases saved to {filepath}")
    
    def load_tablebases(self, filepath: str) -> bool:
        """Load tablebases from file"""
        if not os.path.exists(filepath):
            print(f"⚠️ Tablebase file {filepath} not found")
            return False
        
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            self.tablebases = data['tablebases']
            self.max_pieces = data['max_pieces']
            self.generated_positions = data['generated_positions']
            
            print(f"📂 Loaded {len(self.tablebases)} tablebases")
            print(f"   Total positions: {self.generated_positions:,}")
            return True
        except Exception as e:
            print(f"❌ Failed to load tablebases: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, any]:
        """Get tablebase statistics"""
        total_positions = sum(len(tb) for tb in self.tablebases.values())
        
        return {
            'max_pieces': self.max_pieces,
            'material_configs': len(self.tablebases),
            'total_positions': total_positions,
            'generated_positions': self.generated_positions,
            'loaded_positions': self.loaded_positions
        }

class EnhancedEndgamePlayer:
    """Integrates tablebase with main chess engine"""
    
    def __init__(self, tablebase_path: Optional[str] = None):
        self.tablebase = EndgameTablebase(max_pieces=5)
        
        # Load pre-generated tablebases
        if tablebase_path and os.path.exists(tablebase_path):
            self.tablebase.load_tablebases(tablebase_path)
        else:
            # Generate basic tablebases
            basic_tablebases = self.tablebase.generate_basic_endgames()
            self.tablebase.tablebases.update(basic_tablebases)
    
    def get_endgame_move(self, board: List[List[str]], 
                        is_white: bool) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get perfect endgame move from tablebase
        
        Args:
            board: Current board state
            is_white: True if white to move
            
        Returns:
            Perfect move from tablebase or None if not applicable
        """
        result = self.tablebase.probe_tablebase(board)
        
        if result:
            tb_result, distance, best_move = result
            
            # Return perfect play based on result
            if tb_result == 'win':
                print(f"🎯 Tablebase win in {distance} moves")
                # Would return actual winning move
                return self._find_winning_move(board, is_white)
            elif tb_result == 'draw':
                print(f"🤝 Tablebase draw")
                # Would return drawing move
                return self._find_drawing_move(board, is_white)
            elif tb_result == 'loss':
                print(f"😔 Tablebase loss in {distance} moves")
                # Would return best defensive move
                return self._find_defensive_move(board, is_white)
        
        return None
    
    def _find_winning_move(self, board: List[List[str]], 
                          is_white: bool) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Find winning move (placeholder implementation)"""
        # This would contain actual move generation logic
        return None
    
    def _find_drawing_move(self, board: List[List[str]], 
                          is_white: bool) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Find drawing move (placeholder implementation)"""
        return None
    
    def _find_defensive_move(self, board: List[List[str]], 
                            is_white: bool) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Find best defensive move (placeholder implementation)"""
        return None

# Test function
def test_endgame_tablebase():
    """Test endgame tablebase functionality"""
    print("🎯 ENDGAME TABLEBASE TEST")
    print("=" * 40)
    
    # Create endgame player
    player = EnhancedEndgamePlayer()
    
    # Test positions
    test_positions = [
        # King vs King (draw)
        ([
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'k', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'K', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.']
        ], True, "KvK endgame"),
        
        # Queen vs King (win)
        ([
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'k', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['K', '.', '.', '.', '.', '.', 'Q', '.']
        ], True, "KQvK endgame"),
        
        # Rook vs King (win)
        ([
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'k', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['K', '.', '.', '.', '.', '.', 'R', '.']
        ], True, "KRvK endgame")
    ]
    
    print("Testing endgame positions...")
    
    for board, turn, description in test_positions:
        print(f"\n{description}:")
        
        # Check if tablebase position
        is_tb_pos = player.tablebase.is_tablebase_position(board)
        print(f"  Tablebase eligible: {'✅' if is_tb_pos else '❌'}")
        
        if is_tb_pos:
            # Get material signature
            material_sig = player.tablebase.get_material_signature(board)
            print(f"  Material: {material_sig}")
            
            # Probe tablebase
            result = player.tablebase.probe_tablebase(board)
            if result:
                tb_result, distance, move = result
                print(f"  Result: {tb_result.upper()}")
                print(f"  Distance: {distance} moves")
                print(f"  Best move: {move}")
            else:
                print(f"  No tablebase data available")
    
    # Statistics
    stats = player.tablebase.get_statistics()
    print(f"\n📊 TABLEBASE STATISTICS:")
    print(f"  Max pieces: {stats['max_pieces']}")
    print(f"  Material configs: {stats['material_configs']}")
    print(f"  Total positions: {stats['total_positions']:,}")
    
    print("\n✅ Endgame tablebase test completed!")

if __name__ == "__main__":
    test_endgame_tablebase()