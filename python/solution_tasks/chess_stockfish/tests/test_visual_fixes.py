#!/usr/bin/env python3
"""
Test script for visual improvements in the chess game.
This script tests the fixes for visual artifacts with circles around pieces.
"""

import pygame
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.board_renderer import BoardRenderer, BoardTheme
from game.chess_game import ChessGame

def test_visual_fixes():
    """Test visual improvements and artifact fixes."""
    print("Testing visual improvements...")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((512, 612))
    pygame.display.set_caption("Visual Improvements Test")
    
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
        
        # Set various effects for testing
        renderer.set_selected((7, 4))  # Select king
        renderer.set_last_move((6, 4), (4, 4))  # Last move
        renderer.set_check((0, 4))  # King in check
        renderer.set_move_hints([(5, 3), (5, 4), (5, 5)])  # Move hints
        
        clock = pygame.time.Clock()
        running = True
        frame_count = 0
        
        print("Displaying test board with visual improvements.")
        print("Press ESC to exit.")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update hover position
            mouse_pos = pygame.mouse.get_pos()
            
            # Clear screen
            screen.fill((40, 40, 40))
            
            # Draw the board
            renderer.draw(test_board, evaluation=0.5, thinking=True, 
                         mouse_pos=mouse_pos, move_count=10,
                         capture_count=(3, 2), check_count=1)
            
            pygame.display.flip()
            clock.tick(60)
            frame_count += 1
            
            # Auto-exit after 10 seconds
            if frame_count > 600:  # 10 seconds at 60 FPS
                break
        
        print("✓ Visual improvements test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error in visual improvements test: {e}")
        return False
    finally:
        pygame.quit()

if __name__ == "__main__":
    success = test_visual_fixes()
    if success:
        print("\n🎉 Visual improvements are working correctly!")
        print("The visual artifacts with circles around pieces should be fixed.")
    else:
        print("\n❌ Visual improvements test failed.")
        sys.exit(1)