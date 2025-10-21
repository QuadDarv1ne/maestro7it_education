#!/usr/bin/env python3
"""
Test script for UI enhancements in the chess game.
"""

import pygame
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.board_renderer import BoardRenderer, BoardTheme
from game.chess_game import ChessGame

def test_ui_components():
    """Test UI components and visual enhancements."""
    print("Testing UI enhancements...")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((512, 612))
    pygame.display.set_caption("UI Enhancements Test")
    
    try:
        # Create a board renderer
        renderer = BoardRenderer(screen, 'white')
        
        # Test board with some pieces
        test_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        # Test various UI components
        clock = pygame.time.Clock()
        running = True
        test_duration = 5  # seconds
        start_time = pygame.time.get_ticks()
        
        while running:
            current_time = pygame.time.get_ticks()
            if (current_time - start_time) / 1000 > test_duration:
                running = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Fill background
            screen.fill((40, 40, 40))
            
            # Draw the board
            renderer.draw(test_board, evaluation=0.5, thinking=True, 
                         mouse_pos=(256, 256), move_count=10,
                         capture_count=(3, 2), check_count=1)
            
            # Test additional UI components
            test_rect = pygame.Rect(100, 550, 300, 40)
            
            # Test progress bar
            progress_rect = pygame.Rect(100, 520, 200, 20)
            renderer._draw_progress_bar(progress_rect, 0.7, (100, 200, 100))
            
            # Test status indicator
            status_rect = pygame.Rect(320, 520, 150, 20)
            renderer._draw_status_indicator(status_rect, "Тест статуса", (255, 200, 100))
            
            # Test enhanced feedback
            feedback_rect = pygame.Rect(50, 570, 400, 30)
            renderer._draw_enhanced_feedback("Тест обратной связи", feedback_rect, "success")
            
            pygame.display.flip()
            clock.tick(30)
            
        print("UI enhancements test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during UI testing: {e}")
        return False
    finally:
        pygame.quit()

def test_game_with_enhanced_ui():
    """Test the full game with enhanced UI."""
    print("Testing game with enhanced UI...")
    
    try:
        # Create a game instance (but don't start the full game loop)
        game = ChessGame()
        print("Game instance created successfully with enhanced UI features")
        
        # Test that the enhanced methods exist
        assert hasattr(game.renderer, '_draw_progress_bar'), "Progress bar method missing"
        assert hasattr(game.renderer, '_draw_status_indicator'), "Status indicator method missing"
        assert hasattr(game.renderer, '_draw_enhanced_feedback'), "Enhanced feedback method missing"
        assert hasattr(game.renderer, '_draw_additional_indicators'), "Additional indicators method missing"
        
        print("All enhanced UI methods are available")
        return True
        
    except Exception as e:
        print(f"Error during game UI testing: {e}")
        return False

def main():
    """Run all UI enhancement tests."""
    print("Running UI enhancement tests...\n")
    
    try:
        # Test individual UI components
        success1 = test_ui_components()
        
        # Test game with enhanced UI
        success2 = test_game_with_enhanced_ui()
        
        if success1 and success2:
            print("\nAll UI enhancement tests completed successfully!")
            print("\nUI improvements implemented:")
            print("1. Enhanced progress bars with gradient effects")
            print("2. Visual status indicators with icons")
            print("3. Enhanced feedback system with colored messages")
            print("4. Additional game statistics indicators")
            print("5. Improved visual design with shadows and borders")
            print("6. Better categorization of feedback types")
        else:
            print("\nSome UI enhancement tests failed!")
            
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()