#!/usr/bin/env python3
"""
Standard Algebraic Notation (SAN) Parser
Converts chess moves from SAN format (e.g., Nf3, e4, O-O, Bxe5) to coordinates
"""

import re
from typing import Tuple, Optional, List


class SANParser:
    """Parser for Standard Algebraic Notation chess moves"""
    
    def __init__(self):
        # Piece symbols mapping
        self.piece_map = {
            'K': 'king',
            'Q': 'queen',
            'R': 'rook',
            'B': 'bishop',
            'N': 'knight',
            '': 'pawn'  # No symbol = pawn
        }
        
        # File and rank conversion
        self.files = 'abcdefgh'
        self.ranks = '12345678'
        
    def parse_move(self, san_move: str, board_state: List[List[str]], 
                   current_turn: bool) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], str]]:
        """
        Parse SAN move and return (from_pos, to_pos, special_flags)
        
        Args:
            san_move: Move in SAN format (e.g., "Nf3", "exd5", "O-O")
            board_state: Current board position
            current_turn: True for white, False for black
            
        Returns:
            Tuple of (from_pos, to_pos, flags) or None if invalid
            flags can be: '', 'promotion_q', 'promotion_r', 'promotion_b', 'promotion_n'
        """
        # Remove check/checkmate indicators
        san_move = san_move.rstrip('+#')
        
        # Handle castling
        if san_move in ['O-O', '0-0']:
            return self._parse_kingside_castle(current_turn)
        if san_move in ['O-O-O', '0-0-0']:
            return self._parse_queenside_castle(current_turn)
        
        # Handle pawn promotion
        promotion = ''
        if '=' in san_move:
            san_move, promo_piece = san_move.split('=')
            promotion = f'promotion_{promo_piece.lower()}'
        
        # Parse regular move
        return self._parse_regular_move(san_move, board_state, current_turn, promotion)
    
    def _parse_regular_move(self, san_move: str, board_state: List[List[str]], 
                           current_turn: bool, promotion: str) -> Optional[Tuple]:
        """Parse regular (non-castling) move"""
        
        # Pattern: [Piece][from_file][from_rank][x][to_square]
        # Examples: Nf3, Nbd2, exd5, e4, Bxe5
        
        is_capture = 'x' in san_move
        san_move = san_move.replace('x', '')
        
        # Determine piece type (first uppercase letter or none for pawn)
        piece_type = ''
        if san_move[0].isupper() and san_move[0] in 'KQRBN':
            piece_type = san_move[0]
            san_move = san_move[1:]
        
        # Extract destination square (last 2 characters)
        if len(san_move) < 2:
            return None
        
        to_square = san_move[-2:]
        to_pos = self._algebraic_to_coords(to_square)
        if not to_pos:
            return None
        
        # Extract disambiguation info (file/rank from which piece moves)
        from_hint = san_move[:-2] if len(san_move) > 2 else ''
        
        # Find the piece that can make this move
        from_pos = self._find_piece(piece_type, to_pos, from_hint, 
                                     board_state, current_turn, is_capture)
        
        if not from_pos:
            return None
        
        return (from_pos, to_pos, promotion)
    
    def _find_piece(self, piece_type: str, to_pos: Tuple[int, int], 
                    from_hint: str, board_state: List[List[str]], 
                    current_turn: bool, is_capture: bool) -> Optional[Tuple[int, int]]:
        """Find which piece can make the given move"""
        
        piece_symbol = piece_type if piece_type else 'P'
        if not current_turn:  # Black pieces are lowercase
            piece_symbol = piece_symbol.lower()
        
        # Search for all pieces of this type
        candidates = []
        for r in range(8):
            for c in range(8):
                if board_state[r][c].upper() == piece_symbol.upper():
                    if board_state[r][c].isupper() == current_turn:
                        # Check if this piece matches the hint
                        if self._matches_hint((r, c), from_hint):
                            # Check if this piece can legally move to to_pos
                            if self._can_piece_move(piece_symbol.upper(), (r, c), 
                                                    to_pos, board_state, is_capture):
                                candidates.append((r, c))
        
        # Return unique candidate or None
        return candidates[0] if len(candidates) == 1 else None
    
    def _matches_hint(self, pos: Tuple[int, int], hint: str) -> bool:
        """Check if position matches the disambiguation hint"""
        if not hint:
            return True
        
        r, c = pos
        
        # Check file hint
        if len(hint) == 1 and hint in self.files:
            return c == self.files.index(hint)
        
        # Check rank hint
        if len(hint) == 1 and hint in self.ranks:
            return r == int(hint) - 1
        
        # Check full square hint
        if len(hint) == 2:
            return self._algebraic_to_coords(hint) == pos
        
        return True
    
    def _can_piece_move(self, piece: str, from_pos: Tuple[int, int], 
                       to_pos: Tuple[int, int], board_state: List[List[str]], 
                       is_capture: bool) -> bool:
        """Check if piece can legally move from from_pos to to_pos"""
        
        # Simplified validation - checks basic piece movement patterns
        from_r, from_c = from_pos
        to_r, to_c = to_pos
        
        dr = abs(to_r - from_r)
        dc = abs(to_c - from_c)
        
        if piece == 'P':  # Pawn
            direction = 1 if board_state[from_r][from_c].isupper() else -1
            
            if is_capture:
                return dr == 1 and dc == 1 and (to_r - from_r) * direction > 0
            else:
                if dc != 0:
                    return False
                if dr == 1:
                    return (to_r - from_r) * direction > 0
                if dr == 2:
                    start_rank = 1 if direction == 1 else 6
                    return from_r == start_rank
                return False
        
        elif piece == 'N':  # Knight
            return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)
        
        elif piece == 'B':  # Bishop
            if dr != dc:
                return False
            return self._is_path_clear(from_pos, to_pos, board_state)
        
        elif piece == 'R':  # Rook
            if dr != 0 and dc != 0:
                return False
            return self._is_path_clear(from_pos, to_pos, board_state)
        
        elif piece == 'Q':  # Queen
            if dr != 0 and dc != 0 and dr != dc:
                return False
            return self._is_path_clear(from_pos, to_pos, board_state)
        
        elif piece == 'K':  # King
            return dr <= 1 and dc <= 1
        
        return False
    
    def _is_path_clear(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                      board_state: List[List[str]]) -> bool:
        """Check if path between squares is clear"""
        from_r, from_c = from_pos
        to_r, to_c = to_pos
        
        dr = 0 if to_r == from_r else (1 if to_r > from_r else -1)
        dc = 0 if to_c == from_c else (1 if to_c > from_c else -1)
        
        r, c = from_r + dr, from_c + dc
        while (r, c) != (to_r, to_c):
            if board_state[r][c] != '.':
                return False
            r += dr
            c += dc
        
        return True
    
    def _parse_kingside_castle(self, is_white: bool) -> Tuple:
        """Parse kingside castling (O-O)"""
        rank = 7 if is_white else 0
        return ((rank, 4), (rank, 6), 'castle_kingside')
    
    def _parse_queenside_castle(self, is_white: bool) -> Tuple:
        """Parse queenside castling (O-O-O)"""
        rank = 7 if is_white else 0
        return ((rank, 4), (rank, 2), 'castle_queenside')
    
    def _algebraic_to_coords(self, square: str) -> Optional[Tuple[int, int]]:
        """Convert algebraic notation (e.g., 'e4') to coordinates (3, 4)"""
        if len(square) != 2:
            return None
        
        file = square[0].lower()
        rank = square[1]
        
        if file not in self.files or rank not in self.ranks:
            return None
        
        c = self.files.index(file)
        r = int(rank) - 1
        
        return (r, c)
    
    def coords_to_algebraic(self, pos: Tuple[int, int]) -> str:
        """Convert coordinates to algebraic notation"""
        r, c = pos
        return self.files[c] + str(r + 1)
    
    def move_to_san(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                   piece: str, board_state: List[List[str]], 
                   is_capture: bool = False) -> str:
        """
        Convert coordinate move to SAN notation
        
        Args:
            from_pos: Starting position
            to_pos: Destination position  
            piece: Piece being moved (uppercase)
            board_state: Current board state
            is_capture: Whether move captures a piece
            
        Returns:
            Move in SAN format
        """
        piece_type = piece.upper() if piece != 'P' else ''
        to_square = self.coords_to_algebraic(to_pos)
        
        capture_symbol = 'x' if is_capture else ''
        
        # For pawns, include file if capturing
        if piece.upper() == 'P' and is_capture:
            from_file = self.files[from_pos[1]]
            return f"{from_file}{capture_symbol}{to_square}"
        elif piece.upper() == 'P':
            return to_square
        
        # For other pieces, add disambiguation if needed
        disambiguation = self._get_disambiguation(piece, from_pos, to_pos, board_state)
        
        return f"{piece_type}{disambiguation}{capture_symbol}{to_square}"
    
    def _get_disambiguation(self, piece: str, from_pos: Tuple[int, int], 
                           to_pos: Tuple[int, int], board_state: List[List[str]]) -> str:
        """Determine if file/rank disambiguation is needed"""
        
        # Find other pieces of same type that can move to same square
        piece_symbol = piece.upper()
        candidates = []
        
        for r in range(8):
            for c in range(8):
                if board_state[r][c].upper() == piece_symbol:
                    if (r, c) != from_pos:
                        if self._can_piece_move(piece_symbol, (r, c), to_pos, 
                                               board_state, False):
                            candidates.append((r, c))
        
        if not candidates:
            return ''
        
        # Check if file disambiguation is enough
        same_file = any(c == from_pos[1] for r, c in candidates)
        same_rank = any(r == from_pos[0] for r, c in candidates)
        
        if not same_file:
            return self.files[from_pos[1]]
        elif not same_rank:
            return str(from_pos[0] + 1)
        else:
            # Need both file and rank
            return self.coords_to_algebraic(from_pos)


# Example usage and testing
if __name__ == "__main__":
    parser = SANParser()
    
    # Test board setup (starting position)
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
    
    # Test moves
    test_moves = [
        ("e4", True),     # Pawn to e4
        ("Nf3", True),    # Knight to f3
        ("e5", False),    # Black pawn to e5
        ("Bc4", True),    # Bishop to c4
        ("O-O", True),    # Kingside castle
    ]
    
    print("SAN Parser Test:")
    for move, is_white in test_moves:
        result = parser.parse_move(move, test_board, is_white)
        if result:
            from_pos, to_pos, flags = result
            print(f"{move}: {from_pos} -> {to_pos} {flags}")
        else:
            print(f"{move}: Parse failed")
