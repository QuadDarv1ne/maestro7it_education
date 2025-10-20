#!/usr/bin/env python3
"""
Debug script for chess coordinate conversion issues
"""

import pygame
from ui.board_renderer import BoardRenderer
from engine.stockfish_wrapper import StockfishWrapper

# Constants
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

def test_coordinate_conversion():
    """Test coordinate conversion functions"""
    print("=== Тестирование преобразования координат ===")
    
    # Test with white perspective
    print("\n--- Белая перспектива ---")
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    renderer = BoardRenderer(screen, 'white')
    
    # Test a few coordinates
    test_cases = [
        (0, 0),   # a8
        (0, 7),   # h8
        (7, 0),   # a1
        (7, 7),   # h1
        (1, 1),   # b7
        (6, 6),   # g2
    ]
    
    for fen_row, fen_col in test_cases:
        uci = chr(ord('a') + fen_col) + str(8 - fen_row)
        disp_row, disp_col = renderer._fen_to_display(fen_row, fen_col)
        back_row, back_col = renderer._display_to_fen(disp_row, disp_col)
        print(f"FEN ({fen_row},{fen_col}) -> UCI {uci} -> Display ({disp_row},{disp_col}) -> Back ({back_row},{back_col})")
    
    # Test with black perspective
    print("\n--- Черная перспектива ---")
    renderer_black = BoardRenderer(screen, 'black')
    
    for fen_row, fen_col in test_cases:
        uci = chr(ord('a') + fen_col) + str(8 - fen_row)
        disp_row, disp_col = renderer_black._fen_to_display(fen_row, fen_col)
        back_row, back_col = renderer_black._display_to_fen(disp_row, disp_col)
        print(f"FEN ({fen_row},{fen_col}) -> UCI {uci} -> Display ({disp_row},{disp_col}) -> Back ({back_row},{back_col})")
    
    pygame.quit()

def test_click_coordinates():
    """Test click coordinate conversion"""
    print("\n=== Тестирование преобразования координат клика ===")
    
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    renderer = BoardRenderer(screen, 'white')
    
    # Test click positions
    click_tests = [
        (0, 0),           # Top-left corner
        (SQUARE_SIZE//2, SQUARE_SIZE//2),  # Center of a1
        (BOARD_SIZE-1, BOARD_SIZE-1),      # Bottom-right corner
        (SQUARE_SIZE + 10, SQUARE_SIZE + 10),  # Center of b2
        (3 * SQUARE_SIZE + 5, 4 * SQUARE_SIZE + 5),  # Somewhere in middle
    ]
    
    for x, y in click_tests:
        if y > BOARD_SIZE:
            print(f"Клик ({x},{y}) вне доски")
            continue
            
        disp_row = y // SQUARE_SIZE
        disp_col = x // SQUARE_SIZE
        
        if disp_row >= 8 or disp_col >= 8:
            print(f"Клик ({x},{y}) вне доски (координаты: {disp_row},{disp_col})")
            continue
            
        fen_row, fen_col = renderer._display_to_fen(disp_row, disp_col)
        uci = chr(ord('a') + fen_col) + str(8 - fen_row)
        print(f"Клик ({x},{y}) -> Display ({disp_row},{disp_col}) -> FEN ({fen_row},{fen_col}) -> UCI {uci}")
    
    pygame.quit()

def test_move_validation():
    """Test move validation with Stockfish"""
    print("\n=== Тестирование валидации ходов ===")
    
    try:
        engine = StockfishWrapper(skill_level=1)
        
        # Test some basic moves
        test_moves = [
            "e2e4",  # Valid pawn move
            "e2e5",  # Invalid pawn move (2 squares forward from starting position)
            "e2e3",  # Valid pawn move (1 square forward)
            "b1c3",  # Valid knight move
            "b1b3",  # Invalid knight move
        ]
        
        for move in test_moves:
            is_correct = engine.is_move_correct(move)
            print(f"Ход {move}: {'Корректный' if is_correct else 'Некорректный'}")
            
        engine.quit()
    except Exception as e:
        print(f"Ошибка при тестировании движка: {e}")

if __name__ == "__main__":
    test_coordinate_conversion()
    test_click_coordinates()
    test_move_validation()
    print("\n=== Тестирование завершено ===")