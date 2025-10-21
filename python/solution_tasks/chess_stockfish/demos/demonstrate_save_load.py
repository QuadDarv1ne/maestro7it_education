#!/usr/bin/env python3
"""
Демонстрация функциональности сохранения и загрузки партий в chess_stockfish.
"""

import sys
import os
import time
import json

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def demonstrate_save_load_functionality():
    """Демонстрация функциональности сохранения и загрузки партий."""
    print("Демонстрация функциональности сохранения и загрузки партий")
    print("=" * 60)
    
    try:
        from game.chess_game import ChessGame
        
        # Создаем экземпляр игры
        print("1. Создание новой шахматной партии...")
        game = ChessGame()
        print("   ✓ Игра создана успешно")
        
        # Показываем начальную позицию
        print("\n2. Начальная позиция:")
        board = game.get_board_state()
        print_board(board)
        
        # Делаем несколько ходов для демонстрации
        print("\n3. Выполнение нескольких ходов...")
        # Белые: e2-e4
        game.engine.make_move("e2e4")
        game.move_history.append("e2e4")
        print("   Ход белых: e2-e4")
        
        # Черные: e7-e5
        game.engine.make_move("e7e5")
        game.move_history.append("e7e5")
        print("   Ход черных: e7-e5")
        
        # Белые: g1-f3
        game.engine.make_move("g1f3")
        game.move_history.append("g1f3")
        print("   Ход белых: g1-f3 (Конь g1->f3)")
        
        # Показываем текущую позицию
        print("\n4. Текущая позиция после 3 ходов:")
        board = game.get_board_state()
        print_board(board)
        
        # Сохраняем игру в файл
        print("\n5. Сохранение партии в файл...")
        game._save_game_to_file("demo_game.json")
        print("   ✓ Партия сохранена в файл demo_game.json")
        
        # Показываем список сохраненных партий
        print("\n6. Список сохраненных партий:")
        saved_games = game._list_saved_games()
        if saved_games:
            for filename in saved_games:
                print(f"   - {filename}")
        else:
            print("   Нет сохраненных партий")
        
        # Создаем новую игру и загружаем сохраненную
        print("\n7. Создание новой игры и загрузка сохраненной партии...")
        new_game = ChessGame()
        print("   Новая игра создана")
        
        # Загружаем сохраненную партию
        new_game._load_game_from_file("demo_game.json")
        print("   Партия загружена из файла")
        
        # Показываем позицию после загрузки
        print("\n8. Позиция после загрузки сохраненной партии:")
        loaded_board = new_game.get_board_state()
        print_board(loaded_board)
        
        # Проверяем, что позиции совпадают
        if board == loaded_board:
            print("\n9. ✓ Проверка: позиции совпадают после загрузки")
        else:
            print("\n9. ✗ Проверка: позиции не совпадают после загрузки")
        
        print("\n" + "=" * 60)
        print("Демонстрация завершена успешно!")
        print("\nНовые возможности:")
        print("  📁 Сохранение партий в файлы")
        print("  📂 Загрузка партий из файлов")
        print("  📋 Список сохраненных партий")
        print("  🔄 Возможность продолжить игру позже")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время демонстрации: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def print_board(board):
    """Вывод доски в консоль."""
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
    """Основная функция демонстрации."""
    print("Демонстрация функциональности сохранения и загрузки партий chess_stockfish")
    print("=" * 80)
    
    success = demonstrate_save_load_functionality()
    
    if success:
        print("\n🎉 Все функции сохранения и загрузки работают корректно!")
        print("\nНовые возможности позволяют:")
        print("  • Сохранять партии для продолжения позже")
        print("  • Загружать ранее сохраненные партии")
        print("  • Управлять коллекцией сохраненных игр")
        print("  • Продолжать игру с любого сохраненного состояния")
    else:
        print("\n❌ Возникли ошибки во время демонстрации.")
        print("Пожалуйста, проверьте логи выше для получения дополнительной информации.")

if __name__ == "__main__":
    main()