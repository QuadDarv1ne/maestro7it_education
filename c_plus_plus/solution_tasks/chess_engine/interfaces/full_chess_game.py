#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Full Chess Game Implementation
Features:
- Two game modes: AI vs Human, Human vs Human
- Color selection (play as white or black)
- Console-based interface with Unicode chess pieces
- Move validation and game state management
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import time
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from core.chess_engine_wrapper import ChessEngineWrapper

@dataclass
class GameState:
    """Complete game state"""
    board: List[List[str]]
    current_turn: bool  # True = white, False = black
    selected_square: Optional[Tuple[int, int]] = None
    valid_moves: List[Tuple[int, int]] = None
    game_active: bool = True
    move_history: List[str] = None
    captured_pieces: Dict[str, List[str]] = None
    game_mode: str = 'computer'  # 'computer' or 'human'
    player_color: str = 'white'  # 'white' or 'black'
    ai_color: str = 'black'      # 'white' or 'black'

class FullChessGame:
    def __init__(self):
        self.engine = ChessEngineWrapper()
        self.state = GameState(
            board=self.engine.get_initial_board(),
            current_turn=True,
            valid_moves=[],
            move_history=[],
            captured_pieces={'white': [], 'black': []},
            game_mode='computer',
            player_color='white',
            ai_color='black'
        )
        
        # Unicode chess pieces
        self.piece_symbols = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }
        
        # Algebraic notation files
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    def print_board(self):
        """Print the chess board with coordinates"""
        print("\n   " + "  ".join(self.files))
        print("  +" + "---+" * 8)
        
        for row in range(8):
            row_str = f"{8-row}|"
            for col in range(8):
                piece = self.state.board[row][col]
                if piece == '.':
                    cell = "   "
                else:
                    symbol = self.piece_symbols.get(piece, piece)
                    # Highlight selected square
                    if self.state.selected_square == (row, col):
                        cell = f"[{symbol}]"
                    else:
                        cell = f" {symbol} "
                
                # Highlight valid moves
                if (row, col) in self.state.valid_moves:
                    target_piece = self.state.board[row][col]
                    if target_piece != '.':
                        cell = f"({symbol})"
                    else:
                        cell = " · "
                
                row_str += cell + "|"
            
            print(row_str + f" {8-row}")
            print("  +" + "---+" * 8)
        
        print("   " + "  ".join(self.files))
        
        # Show whose turn it is
        turn_color = "Белые" if self.state.current_turn else "Черные"
        in_check = self.engine.is_king_in_check(self.state.current_turn)
        check_status = " ⚠ ШАХ!" if in_check else ""
        
        print(f"\nХод: {turn_color}{check_status}")
        
        # Show game mode info
        if self.state.game_mode == 'computer':
            player_color = "Белые" if self.state.player_color == 'white' else "Черные"
            ai_color = "Белые" if self.state.ai_color == 'white' else "Черные"
            print(f"Режим: vs AI | Вы: {player_color} | AI: {ai_color}")
        else:
            print("Режим: Два игрока")
    
    def print_game_info(self):
        """Print game information panel"""
        print("\n" + "="*50)
        print("ИНФОРМАЦИЯ ИГРЫ:")
        print("="*50)
        
        # Move history (last 10 moves)
        if self.state.move_history:
            print("\nПоследние ходы:")
            start_idx = max(0, len(self.state.move_history) - 10)
            for i in range(start_idx, len(self.state.move_history)):
                print(f"  {i+1:2d}. {self.state.move_history[i]}")
        else:
            print("\nХодов пока нет")
        
        # Captured pieces
        if self.state.captured_pieces['white'] or self.state.captured_pieces['black']:
            print("\nЗахваченные фигуры:")
            if self.state.captured_pieces['white']:
                white_symbols = ''.join(self.piece_symbols.get(p, p) for p in self.state.captured_pieces['white'])
                print(f"  Белые: {white_symbols}")
            if self.state.captured_pieces['black']:
                black_symbols = ''.join(self.piece_symbols.get(p.lower(), p) for p in self.state.captured_pieces['black'])
                print(f"  Черные: {black_symbols}")
        
        # Game controls
        print("\nУПРАВЛЕНИЕ:")
        print("  [координаты] - сделать ход (например: e2 e4)")
        print("  s - выбрать/отменить выбор фигуры")
        print("  m - сменить режим игры")
        print("  c - сменить цвет (в режиме vs AI)")
        print("  n - новая игра")
        print("  save [файл] - сохранить игру")
        print("  load [файл] - загрузить игру")
        print("  q - выход")
        print("="*50)
    
    def parse_move_input(self, input_str: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Parse move input like 'e2 e4'"""
        try:
            parts = input_str.strip().split()
            if len(parts) != 2:
                return None
            
            from_square, to_square = parts
            
            # Parse from square
            if len(from_square) != 2:
                return None
            from_file = from_square[0].lower()
            from_rank = from_square[1]
            
            if from_file not in self.files or not from_rank.isdigit():
                return None
            
            from_col = self.files.index(from_file)
            from_row = 8 - int(from_rank)
            
            if not (0 <= from_row < 8 and 0 <= from_col < 8):
                return None
            
            # Parse to square
            if len(to_square) != 2:
                return None
            to_file = to_square[0].lower()
            to_rank = to_square[1]
            
            if to_file not in self.files or not to_rank.isdigit():
                return None
            
            to_col = self.files.index(to_file)
            to_row = 8 - int(to_rank)
            
            if not (0 <= to_row < 8 and 0 <= to_col < 8):
                return None
            
            return ((from_row, from_col), (to_row, to_col))
        
        except Exception:
            return None
    
    def get_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid moves for a piece"""
        valid_moves = []
        from_row, from_col = pos
        piece = self.state.board[from_row][from_col]
        
        if piece == '.':
            return valid_moves
        
        king_color = piece.isupper()
        
        for row in range(8):
            for col in range(8):
                if self.engine.is_valid_move(pos, (row, col)):
                    if not self.engine.would_still_be_in_check(pos, (row, col), king_color):
                        valid_moves.append((row, col))
        
        return valid_moves
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Execute a move"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check turn
        piece = self.state.board[from_row][from_col]
        is_white_piece = piece.isupper()
        
        if (is_white_piece and not self.state.current_turn) or \
           (not is_white_piece and self.state.current_turn):
            print("Не ваш ход!")
            return False
        
        # Save captured piece
        captured = self.state.board[to_row][to_col]
        
        # Execute move in engine
        if not self.engine.make_move(from_pos, to_pos):
            print("Неверный ход!")
            return False
        
        # Update game state
        self.state.board = [row[:] for row in self.engine.board_state]
        self.state.current_turn = self.engine.current_turn
        
        # Update history
        piece_symbol = '' if piece.lower() == 'p' else piece.upper()
        from_square = self.files[from_col] + str(8 - from_row)
        to_square = self.files[to_col] + str(8 - to_row)
        capture_symbol = 'x' if captured != '.' else '-'
        move_notation = f"{piece_symbol}{from_square}{capture_symbol}{to_square}"
        self.state.move_history.append(move_notation)
        
        # Update captured pieces
        if captured != '.':
            captured_color = 'white' if captured.isupper() else 'black'
            self.state.captured_pieces[captured_color].append(captured.upper())
        
        # Clear selection
        self.state.selected_square = None
        self.state.valid_moves = []
        
        # Check game end
        if self.engine.is_checkmate():
            self.state.game_active = False
            winner = "Черные" if self.state.current_turn else "Белые"
            print(f"\n🎉 ШАХ И МАТ! Победа: {winner}")
        elif self.engine.is_stalemate():
            self.state.game_active = False
            print("\n🤝 ПАТ! Ничья!")
        
        return True
    
    def ai_make_move(self):
        """AI makes a move"""
        print("\n🤖 AI думает...")
        start_time = time.time()
        
        # Get best move from engine
        best_move = self.engine.get_best_move(3)  # Depth 3 for reasonable thinking time
        
        thinking_time = time.time() - start_time
        print(f"⏱️  AI подумал {thinking_time:.1f} секунд")
        
        if best_move:
            from_pos, to_pos = best_move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            piece = self.state.board[from_row][from_col]
            piece_symbol = self.piece_symbols.get(piece, piece)
            from_square = self.files[from_col] + str(8 - from_row)
            to_square = self.files[to_col] + str(8 - to_row)
            
            print(f"🤖 AI ходит: {piece_symbol} {from_square}-{to_square}")
            
            self.make_move(from_pos, to_pos)
        else:
            print("🤖 AI не может сделать ход!")
    
    def handle_selection(self, square: Tuple[int, int]):
        """Handle piece selection"""
        row, col = square
        piece = self.state.board[row][col]
        
        if piece != '.':
            is_white_piece = piece.isupper()
            if (is_white_piece and self.state.current_turn) or \
               (not is_white_piece and not self.state.current_turn):
                self.state.selected_square = square
                self.state.valid_moves = self.get_valid_moves(square)
                print(f"Выбрана фигура: {self.piece_symbols.get(piece, piece)}")
            else:
                print("Это не ваша фигура!")
        else:
            print("Пустая клетка!")
    
    def toggle_game_mode(self):
        """Toggle between game modes"""
        self.state.game_mode = 'human' if self.state.game_mode == 'computer' else 'computer'
        self.reset_game()
        mode_name = "Два игрока" if self.state.game_mode == 'human' else "vs AI"
        print(f"Режим изменен на: {mode_name}")
    
    def toggle_player_color(self):
        """Toggle player color (only in computer mode)"""
        if self.state.game_mode == 'computer':
            self.state.player_color = 'black' if self.state.player_color == 'white' else 'white'
            self.state.ai_color = 'white' if self.state.player_color == 'black' else 'black'
            self.reset_game()
            player_color = "Белые" if self.state.player_color == 'white' else "Черные"
            print(f"Вы будете играть за: {player_color}")
    
    def reset_game(self):
        """Reset the game"""
        self.engine.board_state = self.engine.get_initial_board()
        self.engine.current_turn = True
        self.state.board = [row[:] for row in self.engine.board_state]
        self.state.current_turn = True
        self.state.selected_square = None
        self.state.valid_moves = []
        self.state.game_active = True
        self.state.move_history = []
        self.state.captured_pieces = {'white': [], 'black': []}
        print("🎮 Новая игра начата!")
    
    def run(self):
        """Main game loop"""
        print("♔ ♕ ♖ ♗ ♘ ♙  ШАХМАТЫ  ♟ ♞ ♝ ♜ ♛ ♚")
        print("Добро пожаловать в полнофункциональную шахматную игру!")
        
        while True:
            # AI move if it's AI's turn in computer mode
            if (self.state.game_mode == 'computer' and 
                self.state.game_active and
                ((self.state.ai_color == 'white' and self.state.current_turn) or
                 (self.state.ai_color == 'black' and not self.state.current_turn))):
                self.print_board()
                self.ai_make_move()
                continue
            
            # Print game state
            self.print_board()
            self.print_game_info()
            
            if not self.state.game_active:
                print("\nИгра окончена!")
                choice = input("\nНачать новую игру? (y/n): ").strip().lower()
                if choice == 'y':
                    self.reset_game()
                    continue
                else:
                    break
            
            # Get user input
            user_input = input("\nВведите команду или ход: ").strip().lower()
            
            if user_input == 'q':
                print("👋 До свидания!")
                break
            elif user_input.startswith('save'):
                parts = user_input.split()
                filename = parts[1] if len(parts) > 1 else "chess_save.json"
                if self.engine.save_game(filename):
                    print(f"✅ Игра сохранена в {filename}")
                else:
                    print("❌ Ошибка сохранения")
                input("Нажмите Enter...")
                continue
            elif user_input.startswith('load'):
                parts = user_input.split()
                filename = parts[1] if len(parts) > 1 else "chess_save.json"
                if self.engine.load_game(filename):
                    self.state.board = [row[:] for row in self.engine.board_state]
                    self.state.current_turn = self.engine.current_turn
                    self.state.move_history = self.engine.move_history
                    self.state.captured_pieces = self.engine.captured_pieces
                    print(f"✅ Игра загружена из {filename}")
                else:
                    print("❌ Ошибка загрузки")
                input("Нажмите Enter...")
                continue
            elif user_input == 'n':
                self.reset_game()
                continue
            elif user_input == 'm':
                self.toggle_game_mode()
                continue
            elif user_input == 'c':
                self.toggle_player_color()
                continue
            elif user_input == 's':
                if self.state.selected_square:
                    self.state.selected_square = None
                    self.state.valid_moves = []
                    print("Выбор отменен")
                else:
                    print("Введите координаты фигуры для выбора (например: e2)")
                continue
            else:
                # Try to parse as move
                move = self.parse_move_input(user_input)
                if move:
                    from_pos, to_pos = move
                    if self.state.selected_square:
                        # If piece is already selected, try to move
                        if to_pos in self.state.valid_moves:
                            self.make_move(self.state.selected_square, to_pos)
                        else:
                            print("Недопустимый ход!")
                        self.state.selected_square = None
                        self.state.valid_moves = []
                    else:
                        # Select piece first
                        self.handle_selection(from_pos)
                else:
                    print("Неверный формат ввода! Используйте: 'e2 e4' или команды")

if __name__ == "__main__":
    game = FullChessGame()
    game.run()