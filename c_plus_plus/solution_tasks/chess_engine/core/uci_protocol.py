#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UCI Protocol Handler for Python Chess Engine
Universal Chess Interface implementation for professional GUI integration
"""

import sys
import threading
import time
from typing import List, Dict, Optional, Tuple
import re

class UCIOption:
    """Represents a UCI option"""
    
    def __init__(self, name: str, opt_type: str, default_value: str, 
                 min_val: Optional[str] = None, max_val: Optional[str] = None,
                 var: Optional[List[str]] = None):
        self.name = name
        self.type = opt_type
        self.default_value = default_value
        self.min_value = min_val
        self.max_value = max_val
        self.var = var or []
        self.current_value = default_value

class UCIProtocolHandler:
    """Handles UCI protocol communication"""
    
    def __init__(self, engine_wrapper=None):
        self.engine = engine_wrapper
        self.running = False
        self.searching = False
        self.search_thread = None
        self.options = {}
        
        # Engine identification
        self.engine_name = "Maestro Chess Engine"
        self.author = "Chess Engine Team"
        
        # Search parameters
        self.search_depth = 6
        self.search_time_ms = 1000
        self.infinite_search = False
        self.move_time = 0
        
        # Game state
        self.position_setup = "startpos"
        self.moves_made = []
        
        # Initialize default options
        self._initialize_options()
        
        print(f"🎯 UCI Protocol Handler initialized for {self.engine_name}")
    
    def _initialize_options(self):
        """Initialize UCI options"""
        self.options = {
            "Hash": UCIOption("Hash", "spin", "64", "1", "1024"),
            "Threads": UCIOption("Threads", "spin", "1", "1", "128"),
            "MultiPV": UCIOption("MultiPV", "spin", "1", "1", "5"),
            "Contempt": UCIOption("Contempt", "spin", "0", "-100", "100"),
            "Skill Level": UCIOption("Skill Level", "spin", "20", "0", "20"),
            "Ponder": UCIOption("Ponder", "check", "false"),
            "OwnBook": UCIOption("OwnBook", "check", "true"),
            "UCI_Chess960": UCIOption("UCI_Chess960", "check", "false"),
            "UCI_AnalyseMode": UCIOption("UCI_AnalyseMode", "check", "false"),
            "Clear Hash": UCIOption("Clear Hash", "button", ""),
        }
    
    def run(self):
        """Main UCI protocol loop"""
        self.running = True
        print("UCI protocol handler started")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                    
                if not self.running:
                    break
                    
                self._process_command(line)
                
        except KeyboardInterrupt:
            print("UCI handler interrupted")
        except EOFError:
            print("UCI input stream ended")
        finally:
            self._cleanup()
    
    def _process_command(self, command: str):
        """Process UCI command"""
        tokens = command.split()
        if not tokens:
            return
            
        cmd = tokens[0].lower()
        
        try:
            if cmd == "uci":
                self._handle_uci()
            elif cmd == "isready":
                self._handle_isready()
            elif cmd == "ucinewgame":
                self._handle_ucinewgame()
            elif cmd == "position":
                self._handle_position(tokens)
            elif cmd == "go":
                self._handle_go(tokens)
            elif cmd == "stop":
                self._handle_stop()
            elif cmd == "quit":
                self._handle_quit()
            elif cmd == "setoption":
                self._handle_setoption(tokens)
            elif cmd == "ponderhit":
                self._handle_ponderhit()
            else:
                print(f"info string Unknown command: {cmd}")
        except Exception as e:
            print(f"info string Error processing command '{cmd}': {e}")
    
    def _handle_uci(self):
        """Handle UCI command - engine identification"""
        print(f"id name {self.engine_name}")
        print(f"id author {self.author}")
        
        # Send all options
        for option in self.options.values():
            option_str = f"option name {option.name} type {option.type}"
            if option.default_value:
                option_str += f" default {option.default_value}"
            if option.min_value is not None:
                option_str += f" min {option.min_value}"
            if option.max_value is not None:
                option_str += f" max {option.max_value}"
            if option.var:
                for v in option.var:
                    option_str += f" var {v}"
            print(option_str)
        
        print("uciok")
    
    def _handle_isready(self):
        """Handle isready command - ready check"""
        # Perform any initialization here
        print("readyok")
    
    def _handle_ucinewgame(self):
        """Handle ucinewgame command - new game setup"""
        self._stop_search()
        self.moves_made = []
        if self.engine:
            self.engine.board_state = self.engine.get_initial_board()
            self.engine.current_turn = True
            if hasattr(self.engine, 'incremental_eval') and self.engine.incremental_eval:
                self.engine.incremental_eval.set_board(self.engine.board_state)
        print("info string New game started")
    
    def _handle_position(self, tokens: List[str]):
        """Handle position command - set up board position"""
        if len(tokens) < 2:
            return
            
        self._stop_search()
        
        if tokens[1] == "startpos":
            # Set up starting position
            if self.engine:
                self.engine.board_state = self.engine.get_initial_board()
                self.engine.current_turn = True
                if hasattr(self.engine, 'incremental_eval') and self.engine.incremental_eval:
                    self.engine.incremental_eval.set_board(self.engine.board_state)
            self.position_setup = "startpos"
            move_start_idx = 2
            
        elif tokens[1] == "fen":
            # Parse FEN string
            fen_parts = []
            i = 2
            while i < len(tokens) and tokens[i] != "moves":
                fen_parts.append(tokens[i])
                i += 1
            
            if fen_parts:
                fen_string = " ".join(fen_parts)
                self._setup_from_fen(fen_string)
                self.position_setup = f"fen {fen_string}"
                move_start_idx = i
            else:
                return
        else:
            return
        
        # Process moves if present
        if move_start_idx < len(tokens) and tokens[move_start_idx] == "moves":
            self.moves_made = tokens[move_start_idx + 1:]
            self._apply_moves(self.moves_made)
    
    def _setup_from_fen(self, fen: str):
        """Setup board from FEN string"""
        if not self.engine:
            return
            
        try:
            # Parse FEN components
            parts = fen.split()
            if len(parts) < 4:
                return
                
            piece_placement = parts[0]
            active_color = parts[1]
            castling = parts[2]
            en_passant = parts[3]
            
            # Convert piece placement to board
            board = [['.' for _ in range(8)] for _ in range(8)]
            row = 0
            col = 0
            
            for char in piece_placement:
                if char == '/':
                    row += 1
                    col = 0
                elif char.isdigit():
                    col += int(char)
                elif char in 'rnbqkpRNBQKP':
                    board[row][col] = char
                    col += 1
            
            # Set board state
            self.engine.board_state = board
            self.engine.current_turn = (active_color == 'w')
            
            # Set castling rights
            if hasattr(self.engine, 'castling_rights'):
                self.engine.castling_rights = {
                    'white_kingside': 'K' in castling,
                    'white_queenside': 'Q' in castling,
                    'black_kingside': 'k' in castling,
                    'black_queenside': 'q' in castling
                }
            
            # Set en passant target
            if hasattr(self.engine, 'en_passant_target'):
                if en_passant != '-' and len(en_passant) == 2:
                    file = ord(en_passant[0]) - ord('a')
                    rank = 8 - int(en_passant[1])
                    self.engine.en_passant_target = (rank, file)
                else:
                    self.engine.en_passant_target = None
            
            # Update incremental evaluator if present
            if hasattr(self.engine, 'incremental_eval') and self.engine.incremental_eval:
                self.engine.incremental_eval.set_board(board)
                
        except Exception as e:
            print(f"info string Error parsing FEN: {e}")
    
    def _apply_moves(self, moves: List[str]):
        """Apply moves to current position"""
        if not self.engine:
            return
            
        for move_str in moves:
            try:
                from_pos, to_pos = self._parse_move(move_str)
                if from_pos and to_pos:
                    self.engine.make_move(from_pos, to_pos)
            except Exception as e:
                print(f"info string Error applying move {move_str}: {e}")
                break
    
    def _parse_move(self, move_str: str) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """Parse algebraic notation move to coordinates"""
        if len(move_str) < 4:
            return None, None
            
        # Handle promotion (e.g., "e7e8q")
        promotion = None
        if len(move_str) > 4:
            promotion = move_str[4].lower()
            
        from_square = move_str[:2]
        to_square = move_str[2:4]
        
        try:
            from_file = ord(from_square[0].lower()) - ord('a')
            from_rank = 8 - int(from_square[1])
            to_file = ord(to_square[0].lower()) - ord('a')
            to_rank = 8 - int(to_square[1])
            
            return (from_rank, from_file), (to_rank, to_file)
        except:
            return None, None
    
    def _handle_go(self, tokens: List[str]):
        """Handle go command - start search"""
        self._stop_search()
        
        # Parse search parameters
        self.search_depth = 6
        self.search_time_ms = 0
        self.infinite_search = False
        self.move_time = 0
        
        i = 1
        while i < len(tokens):
            if tokens[i] == "depth" and i + 1 < len(tokens):
                self.search_depth = int(tokens[i + 1])
                i += 2
            elif tokens[i] == "movetime" and i + 1 < len(tokens):
                self.move_time = int(tokens[i + 1])
                i += 2
            elif tokens[i] == "wtime" and i + 1 < len(tokens):
                if self.engine and self.engine.current_turn:  # White to move
                    time_left = int(tokens[i + 1])
                    self.search_time_ms = time_left // 30  # Use 1/30th of remaining time
                i += 2
            elif tokens[i] == "btime" and i + 1 < len(tokens):
                if self.engine and not self.engine.current_turn:  # Black to move
                    time_left = int(tokens[i + 1])
                    self.search_time_ms = time_left // 30
                i += 2
            elif tokens[i] == "infinite":
                self.infinite_search = True
                i += 1
            else:
                i += 1
        
        # Start search in separate thread
        self.searching = True
        self.search_thread = threading.Thread(target=self._search_worker)
        self.search_thread.start()
    
    def _search_worker(self):
        """Worker thread for search"""
        try:
            if not self.engine:
                self._send_bestmove("(none)")
                return
            
            # Get best move using engine's AI
            if hasattr(self.engine, 'get_best_move'):
                best_move = self.engine.get_best_move(depth=self.search_depth)
                if best_move:
                    from_pos, to_pos = best_move
                    move_str = self._format_move(from_pos, to_pos)
                    self._send_bestmove(move_str)
                else:
                    self._send_bestmove("(none)")
            else:
                # Fallback to random move if no AI available
                legal_moves = self._get_legal_moves()
                if legal_moves:
                    from_pos, to_pos = legal_moves[0]
                    move_str = self._format_move(from_pos, to_pos)
                    self._send_bestmove(move_str)
                else:
                    self._send_bestmove("(none)")
                    
        except Exception as e:
            print(f"info string Search error: {e}")
            self._send_bestmove("(none)")
        finally:
            self.searching = False
    
    def _get_legal_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves from current position"""
        if not self.engine:
            return []
            
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.engine.board_state[row][col]
                if piece != '.':
                    # Check if piece belongs to current player
                    is_white = piece.isupper()
                    if (is_white and self.engine.current_turn) or (not is_white and not self.engine.current_turn):
                        # Try all destination squares
                        for to_row in range(8):
                            for to_col in range(8):
                                if self.engine.is_valid_move((row, col), (to_row, to_col)):
                                    if not self.engine.would_still_be_in_check((row, col), (to_row, to_col), self.engine.current_turn):
                                        legal_moves.append(((row, col), (to_row, to_col)))
        return legal_moves
    
    def _format_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> str:
        """Format move as algebraic notation"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        files = 'abcdefgh'
        from_square = f"{files[from_col]}{8-from_row}"
        to_square = f"{files[to_col]}{8-to_row}"
        
        return f"{from_square}{to_square}"
    
    def _send_bestmove(self, move: str):
        """Send bestmove response"""
        print(f"bestmove {move}")
    
    def _handle_stop(self):
        """Handle stop command"""
        self._stop_search()
    
    def _handle_quit(self):
        """Handle quit command"""
        self._stop_search()
        self.running = False
    
    def _handle_setoption(self, tokens: List[str]):
        """Handle setoption command"""
        if len(tokens) < 5 or tokens[1] != "name" or tokens[3] != "value":
            return
            
        option_name = tokens[2]
        option_value = tokens[4]
        
        if option_name in self.options:
            self.options[option_name].current_value = option_value
            print(f"info string Option {option_name} set to {option_value}")
        else:
            print(f"info string Unknown option: {option_name}")
    
    def _handle_ponderhit(self):
        """Handle ponderhit command"""
        # In simple implementation, just continue normal search
        print("info string Ponderhit received")
    
    def _stop_search(self):
        """Stop ongoing search"""
        self.searching = False
        if self.search_thread and self.search_thread.is_alive():
            self.search_thread.join(timeout=1.0)
    
    def _cleanup(self):
        """Cleanup resources"""
        self._stop_search()
        self.running = False
        print("UCI protocol handler stopped")

# Test function
def test_uci_handler():
    """Test UCI protocol handler"""
    print("🎯 UCI PROTOCOL HANDLER TEST")
    print("=" * 40)
    
    try:
        # Import engine wrapper if available
        try:
            from core.chess_engine_wrapper import ChessEngineWrapper
            engine = ChessEngineWrapper()
            print("✅ Chess engine loaded")
        except ImportError:
            engine = None
            print("⚠️ Chess engine not available, using dummy handler")
        
        # Create UCI handler
        uci_handler = UCIProtocolHandler(engine)
        print("✅ UCI handler created")
        
        # Test UCI identification
        print("\nTesting UCI identification:")
        uci_handler._handle_uci()
        
        # Test ready check
        print("\nTesting ready check:")
        uci_handler._handle_isready()
        
        # Test new game
        print("\nTesting new game:")
        uci_handler._handle_ucinewgame()
        
        # Test position setup
        print("\nTesting position setup:")
        uci_handler._handle_position(["position", "startpos"])
        
        # Test setting options
        print("\nTesting option setting:")
        uci_handler._handle_setoption(["setoption", "name", "Hash", "value", "128"])
        uci_handler._handle_setoption(["setoption", "name", "Threads", "value", "4"])
        
        # Test move parsing
        print("\nTesting move parsing:")
        test_moves = ["e2e4", "e7e5", "g1f3", "b8c6"]
        for move in test_moves:
            from_pos, to_pos = uci_handler._parse_move(move)
            if from_pos and to_pos:
                formatted = uci_handler._format_move(from_pos, to_pos)
                print(f"  {move} → {formatted}")
        
        print("\n✅ UCI protocol handler test completed!")
        print("Note: Interactive testing requires actual UCI communication")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # If run directly, test the handler
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_uci_handler()
    else:
        # Run as UCI engine
        try:
            from core.chess_engine_wrapper import ChessEngineWrapper
            engine = ChessEngineWrapper()
        except ImportError:
            engine = None
            print("info string Running without chess engine")
        
        uci_handler = UCIProtocolHandler(engine)
        uci_handler.run()