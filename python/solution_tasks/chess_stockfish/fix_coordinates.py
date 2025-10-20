#!/usr/bin/env python3
"""
Fix for chess coordinate conversion issues
"""

import pygame
from ui.board_renderer import BoardRenderer
from engine.stockfish_wrapper import StockfishWrapper

# Constants
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

def demonstrate_coordinate_issue():
    """Demonstrate the coordinate conversion issue"""
    print("=== Демонстрация проблемы с координатами ===")
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    
    # Test with white perspective (standard)
    renderer = BoardRenderer(screen, 'white')
    
    print("\n--- Белая перспектива (стандартная) ---")
    print("На доске координаты идут от a1 (слева снизу) до h8 (справа сверху)")
    print("В FEN нотации: a1 = (7,0), h1 = (7,7), a8 = (0,0), h8 = (0,7)")
    print("На экране: a1 = (7,0), h1 = (7,7), a8 = (0,0), h8 = (0,7)")
    
    # Key positions
    positions = [
        ("a1", 7, 0),
        ("h1", 7, 7),
        ("a8", 0, 0),
        ("h8", 0, 7),
        ("e2", 6, 4),
        ("e4", 4, 4),
        ("e7", 1, 4),
    ]
    
    for name, fen_row, fen_col in positions:
        uci = chr(ord('a') + fen_col) + str(8 - fen_row)
        disp_row, disp_col = renderer._fen_to_display(fen_row, fen_col)
        print(f"{name} (FEN {fen_row},{fen_col}) -> UCI {uci} -> Display ({disp_row},{disp_col})")
    
    # Test click coordinates
    print("\n--- Тестирование кликов ---")
    click_positions = [
        (SQUARE_SIZE//2, SQUARE_SIZE//2),  # Should be a8 (0,0)
        (BOARD_SIZE - SQUARE_SIZE//2, SQUARE_SIZE//2),  # Should be h8 (0,7)
        (SQUARE_SIZE//2, BOARD_SIZE - SQUARE_SIZE//2),  # Should be a1 (7,0)
        (BOARD_SIZE - SQUARE_SIZE//2, BOARD_SIZE - SQUARE_SIZE//2),  # Should be h1 (7,7)
    ]
    
    for x, y in click_positions:
        disp_row = y // SQUARE_SIZE
        disp_col = x // SQUARE_SIZE
        fen_row, fen_col = renderer._display_to_fen(disp_row, disp_col)
        uci = chr(ord('a') + fen_col) + str(8 - fen_row)
        print(f"Клик ({x},{y}) -> Display ({disp_row},{disp_col}) -> FEN ({fen_row},{fen_col}) -> UCI {uci}")
    
    pygame.quit()

def test_pawn_movement():
    """Test pawn movement specifically"""
    print("\n=== Тестирование движения пешки ===")
    
    try:
        # Initialize engine
        engine = StockfishWrapper(skill_level=1)
        
        # Get initial board state
        board = engine.get_board_state()
        print("Начальная позиция доски:")
        for i, row in enumerate(board):
            print(f"Ряд {8-i}: {row}")
        
        # Test e2e4 (pawn moves two squares forward)
        print("\nПроверка хода e2e4 (пешка e2 -> e4):")
        is_valid = engine.is_move_correct("e2e4")
        print(f"Ход e2e4 корректен: {is_valid}")
        
        if is_valid:
            # Make the move
            success = engine.make_move("e2e4")
            print(f"Ход выполнен: {success}")
            
            if success:
                # Check new board state
                new_board = engine.get_board_state()
                print("\nПозиция после хода e2e4:")
                for i, row in enumerate(new_board):
                    print(f"Ряд {8-i}: {row}")
        
        engine.quit()
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")

if __name__ == "__main__":
    demonstrate_coordinate_issue()
    test_pawn_movement()
    print("\n=== Анализ завершен ===")