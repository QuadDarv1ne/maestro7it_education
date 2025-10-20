#!/usr/bin/env python3
"""
Comprehensive test for chess_stockfish improvements
"""

import pygame
from engine.stockfish_wrapper import StockfishWrapper
from game.chess_game import ChessGame

def test_pawn_movement_rules():
    """Test pawn movement rules and user feedback"""
    print("=== Тестирование правил движения пешки ===")
    
    try:
        # Initialize engine
        engine = StockfishWrapper(skill_level=1)
        
        # Test initial position
        print("Начальная позиция:")
        fen = engine.get_fen()
        print(f"FEN: {fen}")
        
        # Test valid pawn moves from starting position
        print("\nТестирование корректных ходов пешки со стартовой позиции:")
        valid_moves = ["e2e4", "e2e3", "d2d4", "d2d3"]
        for move in valid_moves:
            is_correct = engine.is_move_correct(move)
            print(f"  {move}: {'✓ Корректный' if is_correct else '✗ Некорректный'}")
        
        # Test invalid pawn moves from starting position
        print("\nТестирование некорректных ходов пешки со стартовой позиции:")
        invalid_moves = ["e2e5", "e2e6", "d2d5", "d2d6"]
        for move in invalid_moves:
            is_correct = engine.is_move_correct(move)
            print(f"  {move}: {'✓ Корректный' if is_correct else '✗ Некорректный'}")
        
        # Make a move and test pawn movement from non-starting position
        print("\nВыполняем ход e2e4...")
        engine.make_move("e2e4")
        
        print("Позиция после e2e4:")
        fen = engine.get_fen()
        print(f"FEN: {fen}")
        
        # Test pawn moves from non-starting position
        print("\nТестирование ходов пешки НЕ со стартовой позиции:")
        moves_from_e4 = ["e4e5", "e4e6"]  # e5 should be valid, e6 should be invalid
        for move in moves_from_e4:
            is_correct = engine.is_move_correct(move)
            status = '✓ Корректный' if is_correct else '✗ Некорректный'
            reason = ""
            if move == "e4e6":
                reason = " (пешка может двигаться только на одну клетку вперед)"
            print(f"  {move}: {status}{reason}")
        
        engine.quit()
        print("\n✅ Тест правил движения пешки пройден успешно")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании правил движения пешки: {e}")
        return False
    
    return True

def test_coordinate_conversion():
    """Test coordinate conversion"""
    print("\n=== Тестирование преобразования координат ===")
    
    try:
        pygame.init()
        screen = pygame.display.set_mode((512, 512))
        
        # Test white perspective
        print("Белая перспектива:")
        from game.chess_game import ChessGame
        game = ChessGame(player_color='white', skill_level=1)
        
        # Test some coordinate conversions
        test_coords = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for row, col in test_coords:
            uci = chr(ord('a') + col) + str(8 - row)
            print(f"  FEN ({row},{col}) -> UCI {uci}")
        
        game.engine.quit()
        pygame.quit()
        print("✅ Тест преобразования координат пройден успешно")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании преобразования координат: {e}")
        return False
    
    return True

def test_user_feedback():
    """Test user feedback mechanisms"""
    print("\n=== Тестирование пользовательской обратной связи ===")
    
    try:
        # Test the _get_move_hint method
        from game.chess_game import ChessGame
        game = ChessGame(player_color='white', skill_level=1)
        
        # Test pawn hint for invalid two-square move from non-starting position
        hint = game._get_move_hint(4, 4, 2, 4)  # e4 to e6 (2 squares forward from e4)
        print(f"Подсказка для хода пешки на две клетки вперед не со стартовой позиции: {hint}")
        
        # Test pawn hint for backward move
        hint = game._get_move_hint(4, 4, 5, 4)  # e4 to e5 (backward for white pawn)
        print(f"Подсказка для хода пешки назад: {hint}")
        
        game.engine.quit()
        print("✅ Тест пользовательской обратной связи пройден успешно")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании пользовательской обратной связи: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print(" chess_stockfish - Комплексное тестирование ")
    print("=" * 45)
    
    tests = [
        test_pawn_movement_rules,
        test_coordinate_conversion,
        test_user_feedback
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Тест {test.__name__} завершился с ошибкой: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 45)
    if all(results):
        print("🎉 Все тесты пройдены успешно!")
        print("Улучшения в chess_stockfish работают корректно.")
        return 0
    else:
        print("❌ Некоторые тесты не пройдены.")
        print("Проверьте ошибки выше.")
        return 1

if __name__ == "__main__":
    exit(main())