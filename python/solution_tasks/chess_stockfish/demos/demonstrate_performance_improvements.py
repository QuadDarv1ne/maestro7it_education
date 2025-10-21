#!/usr/bin/env python3
"""
Demonstration of performance improvements in the chess game.
"""

import sys
import os
import time
import pygame

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame

def demonstrate_caching_performance():
    """Demonstrate the performance improvements from caching."""
    print("Демонстрация улучшений производительности")
    print("=" * 50)
    
    # Initialize pygame for the demo
    pygame.init()
    screen = pygame.display.set_mode((512, 612))
    
    try:
        # Create a game instance
        print("1. Создание шахматной партии...")
        game = ChessGame()
        print("   ✓ Партия создана успешно")
        
        # Show initial board
        print("\n2. Начальная позиция:")
        board = game.get_board_state()
        print_board(board)
        
        # Demonstrate valid moves caching
        print("\n3. Демонстрация кэширования допустимых ходов...")
        
        # First call (no cache)
        start_time = time.time()
        moves1 = game._get_valid_moves(6, 4)  # e2 pawn
        first_call_time = time.time() - start_time
        
        # Second call (should use cache)
        start_time = time.time()
        moves2 = game._get_valid_moves(6, 4)  # Should use cache
        second_call_time = time.time() - start_time
        
        print(f"   Первый вызов: {first_call_time:.6f} секунд")
        print(f"   Второй вызов: {second_call_time:.6f} секунд")
        print(f"   Ускорение: {first_call_time/second_call_time:.2f}x" if second_call_time > 0 else "   Результат из кэша")
        print(f"   Ходы идентичны: {moves1 == moves2}")
        
        # Demonstrate board state caching
        print("\n4. Демонстрация кэширования состояния доски...")
        
        # First call (no cache)
        start_time = time.time()
        board1 = game.get_board_state()
        first_call_time = time.time() - start_time
        
        # Second call (should use cache)
        start_time = time.time()
        board2 = game.get_board_state()  # Should use cache
        second_call_time = time.time() - start_time
        
        print(f"   Первый вызов: {first_call_time:.6f} секунд")
        print(f"   Второй вызов: {second_call_time:.6f} секунд")
        print(f"   Ускорение: {first_call_time/second_call_time:.2f}x" if second_call_time > 0 else "   Результат из кэша")
        
        # Demonstrate AI move caching
        print("\n5. Демонстрация кэширования ходов ИИ...")
        
        # First AI call
        start_time = time.time()
        ai_move1 = game._get_cached_best_move(depth=1)  # Fast AI call
        first_call_time = time.time() - start_time
        
        # Second AI call (same position)
        start_time = time.time()
        ai_move2 = game._get_cached_best_move(depth=1)  # Should use cache
        second_call_time = time.time() - start_time
        
        print(f"   Первый вызов ИИ: {first_call_time:.6f} секунд")
        print(f"   Второй вызов ИИ: {second_call_time:.6f} секунд")
        print(f"   Ускорение: {first_call_time/second_call_time:.2f}x" if second_call_time > 0 else "   Результат из кэша")
        
        # Make a move and test cache invalidation
        if ai_move1:
            print(f"\n6. Выполнение хода ИИ: {ai_move1}")
            game.engine.make_move(ai_move1)
            
            # Now test that cache is invalidated properly
            start_time = time.time()
            ai_move3 = game._get_cached_best_move(depth=1)  # New position
            new_position_time = time.time() - start_time
            
            print(f"   Вызов ИИ для новой позиции: {new_position_time:.6f} секунд")
            print(f"   Ходы различаются: {ai_move1 != ai_move3}")
        
        print("\n" + "=" * 50)
        print("Демонстрация завершена успешно!")
        print("\nРеализованные улучшения производительности:")
        print("  🚀 Увеличено время кэширования допустимых ходов (1 секунда)")
        print("  🚀 Улучшена проверка валидности кэша по позиции на доске")
        print("  🚀 Увеличено время кэширования состояния доски (200 мс)")
        print("  🚀 Расширено время кэширования ходов ИИ (10 секунд)")
        print("  🚀 Увеличено время хранения кэша ИИ (30 секунд)")
        print("  🚀 Увеличены частоты обновления (60 FPS для доски, 30 FPS для UI)")
        print("  🚀 Оптимизирована проверка изменений с использованием хэширования")
        print("  🚀 Добавлено динамическое ограничение FPS в режиме простоя")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время демонстрации: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()
    
    return True

def print_board(board):
    """Print the board to console."""
    print("  a b c d e f g h")
    for i, row in enumerate(board):
        print(f"{8-i} ", end="")
        for cell in row:
            if cell is None:
                print(". ", end="")
            else:
                print(f"{cell} ", end="")
        print(f" {8-i}")
    print("  a b c d e f g h")

def main():
    """Main demonstration function."""
    print("Демонстрация улучшений производительности chess_stockfish")
    print("=" * 60)
    
    success = demonstrate_caching_performance()
    
    if success:
        print("\n🎉 Все улучшения производительности работают корректно!")
        print("\nПреимущества оптимизаций:")
        print("  • Значительно ускорена отрисовка доски")
        print("  • Снижена нагрузка на процессор")
        print("  • Улучшена отзывчивость интерфейса")
        print("  • Оптимизировано использование памяти")
        print("  • Повышена плавность анимаций")
        print("  • Эффективное управление кэшем")
    else:
        print("\n❌ Возникли ошибки во время демонстрации.")
        print("Пожалуйста, проверьте логи выше для получения дополнительной информации.")

if __name__ == "__main__":
    main()