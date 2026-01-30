#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Полная реализация шахматной игры
Возможности:
- Два режима игры: ИИ против Человека, Человек против Человека
- Выбор цвета (игра за белых или черных)
- Консольный интерфейс с Unicode фигурами и цветным выводом
- Проверка ходов и управление состоянием игры
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import time
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from core.chess_engine_wrapper import ChessEngineWrapper

# ANSI цветовые коды для консоли
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_DARK = '\033[100m'
    BG_LIGHT = '\033[47m'

@dataclass
class GameState:
    """Полное состояние игры"""
    board: List[List[str]]
    current_turn: bool  # True = белые, False = черные
    selected_square: Optional[Tuple[int, int]] = None
    valid_moves: List[Tuple[int, int]] = None
    game_active: bool = True
    move_history: List[str] = None
    captured_pieces: Dict[str, List[str]] = None
    game_mode: str = 'computer'  # 'computer' или 'human'
    player_color: str = 'white'  # 'white' или 'black'
    ai_color: str = 'black'      # 'white' или 'black'

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
        
        # Unicode шахматные фигуры
        self.piece_symbols = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }
        
        # Алгебраическая нотация вертикалей
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_board(self):
        """Отрисовка шахматной доски с координатами и цветным оформлением"""
        print(f"\n{Colors.CYAN}   " + "  ".join(self.files) + Colors.RESET)
        print("  +" + "---+" * 8)
        
        for row in range(8):
            row_str = f"{Colors.CYAN}{8-row}{Colors.RESET}|"
            for col in range(8):
                piece = self.state.board[row][col]
                
                # Цвет фона клетки
                is_light_square = (row + col) % 2 == 0
                bg_color = Colors.BG_LIGHT if is_light_square else Colors.BG_DARK
                
                if piece == '.':
                    cell = "   "
                else:
                    symbol = self.piece_symbols.get(piece, piece)
                    # Цвет фигур
                    piece_color = Colors.WHITE if piece.isupper() else Colors.RED
                    
                    # Подсветка выбранной клетки
                    if self.state.selected_square == (row, col):
                        cell = f"{Colors.YELLOW}{Colors.BOLD}[{symbol}]{Colors.RESET}"
                    else:
                        cell = f"{piece_color} {symbol} {Colors.RESET}"
                
                # Подсветка доступных ходов
                if (row, col) in self.state.valid_moves:
                    target_piece = self.state.board[row][col]
                    if target_piece != '.':
                        symbol = self.piece_symbols.get(target_piece, target_piece)
                        piece_color = Colors.WHITE if target_piece.isupper() else Colors.RED
                        cell = f"{Colors.GREEN}({piece_color}{symbol}{Colors.GREEN}){Colors.RESET}"
                    else:
                        cell = f"{Colors.GREEN} · {Colors.RESET}"
                
                row_str += cell + "|"
            
            print(row_str + f" {Colors.CYAN}{8-row}{Colors.RESET}")
            print("  +" + "---+" * 8)
        
        print(f"{Colors.CYAN}   " + "  ".join(self.files) + Colors.RESET)
        
        # Показываем, чей ход
        turn_color = f"{Colors.WHITE}Белые{Colors.RESET}" if self.state.current_turn else f"{Colors.RED}Черные{Colors.RESET}"
        in_check = self.engine.is_king_in_check(self.state.current_turn)
        check_status = f" {Colors.YELLOW}{Colors.BOLD}⚠ ШАХ!{Colors.RESET}" if in_check else ""
        
        print(f"\n{Colors.BOLD}Ход: {turn_color}{check_status}{Colors.RESET}")
        
        # Информация о режиме игры
        if self.state.game_mode == 'computer':
            player_color = "Белые" if self.state.player_color == 'white' else "Черные"
            ai_color = "Белые" if self.state.ai_color == 'white' else "Черные"
            print(f"{Colors.CYAN}Режим: vs AI | Вы: {player_color} | AI: {ai_color}{Colors.RESET}")
        else:
            print(f"{Colors.CYAN}Режим: Два игрока{Colors.RESET}")
    
    def print_game_info(self):
        """Вывод информационной панели игры"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}" + "="*50 + Colors.RESET)
        print(f"{Colors.BOLD}{Colors.BLUE}ИНФОРМАЦИЯ ИГРЫ:{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}" + "="*50 + Colors.RESET)
        
        # История ходов (последние 10 ходов)
        if self.state.move_history:
            print(f"\n{Colors.GREEN}Последние ходы:{Colors.RESET}")
            start_idx = max(0, len(self.state.move_history) - 10)
            for i in range(start_idx, len(self.state.move_history)):
                print(f"  {i+1:2d}. {self.state.move_history[i]}")
        else:
            print(f"\n{Colors.YELLOW}Ходов пока нет{Colors.RESET}")
        
        # Захваченные фигуры
        if self.state.captured_pieces['white'] or self.state.captured_pieces['black']:
            print(f"\n{Colors.MAGENTA}Захваченные фигуры:{Colors.RESET}")
            if self.state.captured_pieces['white']:
                white_symbols = ''.join(self.piece_symbols.get(p, p) for p in self.state.captured_pieces['white'])
                print(f"  Белые: {white_symbols}")
            if self.state.captured_pieces['black']:
                black_symbols = ''.join(self.piece_symbols.get(p.lower(), p) for p in self.state.captured_pieces['black'])
                print(f"  Черные: {black_symbols}")
        
        # Управление игрой
        print(f"\n{Colors.CYAN}{Colors.BOLD}УПРАВЛЕНИЕ:{Colors.RESET}")
        print(f"{Colors.WHITE}  [координаты] - сделать ход (например: e2 e4){Colors.RESET}")
        print(f"{Colors.WHITE}  s - выбрать/отменить выбор фигуры{Colors.RESET}")
        print(f"{Colors.WHITE}  m - сменить режим игры{Colors.RESET}")
        print(f"{Colors.WHITE}  c - сменить цвет (в режиме vs AI){Colors.RESET}")
        print(f"{Colors.WHITE}  n - новая игра{Colors.RESET}")
        print(f"{Colors.WHITE}  save [файл] - сохранить игру{Colors.RESET}")
        print(f"{Colors.WHITE}  load [файл] - загрузить игру{Colors.RESET}")
        print(f"{Colors.WHITE}  q - выход{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}" + "="*50 + Colors.RESET)
    
    def parse_move_input(self, input_str: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Разбор ввода хода типа 'e2 e4'"""
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
        
        # Очистка выбора
        self.state.selected_square = None
        self.state.valid_moves = []
        
        # Проверка окончания игры
        game_status = self.engine.get_game_status()
        if "Мат" in game_status:
            self.state.game_active = False
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 {game_status}{Colors.RESET}")
        elif "Пат" in game_status:
            self.state.game_active = False
            print(f"\n{Colors.YELLOW}{Colors.BOLD}🤝 {game_status}{Colors.RESET}")
        
        return True
    
    def ai_make_move(self):
        """ИИ делает ход"""
        print(f"\n{Colors.CYAN}🤖 AI думает...{Colors.RESET}")
        start_time = time.time()
        
        # Получение лучшего хода от движка
        best_move = self.engine.get_best_move(4)  # Глубина 4 для сильной игры
        
        thinking_time = time.time() - start_time
        print(f"{Colors.MAGENTA}⏱️  AI подумал {thinking_time:.1f} секунд{Colors.RESET}")
        
        if best_move:
            from_pos, to_pos = best_move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            piece = self.state.board[from_row][from_col]
            piece_symbol = self.piece_symbols.get(piece, piece)
            from_square = self.files[from_col] + str(8 - from_row)
            to_square = self.files[to_col] + str(8 - to_row)
            
            # Показ статистики AI
            stats = self.engine.get_game_statistics()
            nodes = stats.get('ai_nodes', 0)
            tt_hits = stats.get('ai_tt_hits', 0)
            
            print(f"{Colors.GREEN}🤖 AI ходит: {piece_symbol} {from_square}-{to_square}{Colors.RESET}")
            if nodes > 0:
                print(f"{Colors.CYAN}📈 Узлов проверено: {nodes:,}, TT hits: {tt_hits:,}{Colors.RESET}")
            
            self.make_move(from_pos, to_pos)
        else:
            print(f"{Colors.RED}🤖 AI не может сделать ход!{Colors.RESET}")
    
    def handle_selection(self, square: Tuple[int, int]):
        """Обработка выбора фигуры"""
        row, col = square
        piece = self.state.board[row][col]
        
        if piece != '.':
            is_white_piece = piece.isupper()
            if (is_white_piece and self.state.current_turn) or \
               (not is_white_piece and not self.state.current_turn):
                self.state.selected_square = square
                self.state.valid_moves = self.get_valid_moves(square)
                print(f"{Colors.GREEN}Выбрана фигура: {self.piece_symbols.get(piece, piece)}{Colors.RESET}")
            else:
                print(f"{Colors.RED}Это не ваша фигура!{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}Пустая клетка!{Colors.RESET}")
    
    def toggle_game_mode(self):
        """Переключение между режимами игры"""
        self.state.game_mode = 'human' if self.state.game_mode == 'computer' else 'computer'
        self.reset_game()
        mode_name = "Два игрока" if self.state.game_mode == 'human' else "vs AI"
        print(f"{Colors.CYAN}Режим изменен на: {mode_name}{Colors.RESET}")
    
    def toggle_player_color(self):
        """Переключение цвета игрока (только в режиме против ИИ)"""
        if self.state.game_mode == 'computer':
            self.state.player_color = 'black' if self.state.player_color == 'white' else 'white'
            self.state.ai_color = 'white' if self.state.player_color == 'black' else 'black'
            self.reset_game()
            player_color = "Белые" if self.state.player_color == 'white' else "Черные"
            print(f"{Colors.GREEN}Вы будете играть за: {player_color}{Colors.RESET}")
    
    def reset_game(self):
        """Сброс игры"""
        self.engine.board_state = self.engine.get_initial_board()
        self.engine.current_turn = True
        self.state.board = [row[:] for row in self.engine.board_state]
        self.state.current_turn = True
        self.state.selected_square = None
        self.state.valid_moves = []
        self.state.game_active = True
        self.state.move_history = []
        self.state.captured_pieces = {'white': [], 'black': []}
        print(f"{Colors.GREEN}🎮 Новая игра начата!{Colors.RESET}")
    
    def run(self):
        """Главный цикл игры"""
        self.clear_screen()
        print(f"{Colors.BOLD}{Colors.MAGENTA}♔ ♕ ♖ ♗ ♘ ♙  ШАХМАТЫ  ♟ ♞ ♝ ♜ ♛ ♚{Colors.RESET}")
        print(f"{Colors.CYAN}Добро пожаловать в полнофункциональную шахматную игру!{Colors.RESET}\n")
        
        while True:
            # AI move if it's AI's turn in computer mode
            if (self.state.game_mode == 'computer' and 
                self.state.game_active and
                ((self.state.ai_color == 'white' and self.state.current_turn) or
                 (self.state.ai_color == 'black' and not self.state.current_turn))):
                self.print_board()
                self.ai_make_move()
                continue
            
            # Отображение состояния игры
            self.clear_screen()
            self.print_board()
            self.print_game_info()
            
            if not self.state.game_active:
                game_status = self.engine.get_game_status()
                print(f"\n{Colors.BOLD}{Colors.RED}Игра окончена! {game_status}{Colors.RESET}")
                choice = input(f"\n{Colors.CYAN}Начать новую игру? (y/n): {Colors.RESET}").strip().lower()
                if choice == 'y':
                    self.reset_game()
                    continue
                else:
                    break
            
            # Получение ввода пользователя
            user_input = input(f"\n{Colors.BOLD}{Colors.YELLOW}Введите команду или ход: {Colors.RESET}").strip().lower()
            
            if user_input == 'q':
                print(f"{Colors.CYAN}👋 До свидания!{Colors.RESET}")
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