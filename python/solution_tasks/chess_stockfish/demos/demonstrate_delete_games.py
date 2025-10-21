#!/usr/bin/env python3
"""
Демонстрация функциональности удаления сохраненных партий в chess_stockfish.
"""

import sys
import os
import time

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def demonstrate_delete_functionality():
    """Демонстрация функциональности удаления сохраненных партий."""
    print("Демонстрация функциональности удаления сохраненных партий")
    print("=" * 60)
    
    try:
        from game.chess_game import ChessGame
        
        # Создаем экземпляр игры
        print("1. Создание новой шахматной партии...")
        game = ChessGame()
        print("   ✓ Игра создана успешно")
        
        # Показываем начальный список сохраненных партий
        print("\n2. Начальный список сохраненных партий:")
        saved_games = game._list_saved_games()
        if saved_games:
            for filename in saved_games:
                print(f"   - {filename}")
        else:
            print("   Нет сохраненных партий")
        
        # Создаем несколько тестовых партий для демонстрации
        print("\n3. Создание тестовых партий для демонстрации...")
        test_files = []
        
        for i in range(3):
            filename = f"demo_game_{i+1}.json"
            test_files.append(filename)
            
            # Делаем несколько ходов
            if i == 0:
                # Белые: e2-e4
                game.engine.make_move("e2e4")
                game.move_history.append("e2e4")
            elif i == 1:
                # Белые: d2-d4
                game.engine.make_move("d2d4")
                game.move_history.append("d2d4")
            elif i == 2:
                # Белые: g1-f3
                game.engine.make_move("g1f3")
                game.move_history.append("g1f3")
            
            # Сохраняем игру
            game._save_game_to_file(filename)
            print(f"   ✓ Партия сохранена в файл {filename}")
            
            # Сбрасываем игру для следующей партии
            game.reset_game()
        
        # Показываем список сохраненных партий после создания тестовых
        print("\n4. Список сохраненных партий после создания тестовых:")
        saved_games = game._list_saved_games()
        if saved_games:
            for filename in saved_games:
                print(f"   - {filename}")
        else:
            print("   Нет сохраненных партий")
        
        # Демонстрируем удаление одной партии
        print("\n5. Демонстрация удаления одной партии...")
        if test_files:
            file_to_delete = test_files[0]
            print(f"   Удаление файла: {file_to_delete}")
            result = game._delete_saved_game(file_to_delete)
            if result:
                print(f"   ✓ Файл {file_to_delete} успешно удален")
            else:
                print(f"   ✗ Ошибка при удалении файла {file_to_delete}")
        
        # Показываем список сохраненных партий после удаления
        print("\n6. Список сохраненных партий после удаления:")
        saved_games = game._list_saved_games()
        if saved_games:
            for filename in saved_games:
                print(f"   - {filename}")
        else:
            print("   Нет сохраненных партий")
        
        # Очищаем оставшиеся тестовые файлы
        print("\n7. Очистка оставшихся тестовых файлов...")
        for filename in test_files[1:]:  # Пропускаем уже удаленный файл
            if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'saves', filename)):
                game._delete_saved_game(filename)
                print(f"   ✓ Файл {filename} удален")
        
        print("\n" + "=" * 60)
        print("Демонстрация завершена успешно!")
        print("\nНовые возможности:")
        print("  🗑 Удаление сохраненных партий")
        print("  📋 Управление коллекцией сохраненных игр")
        print("  ⚠ Обработка ошибок при удалении несуществующих файлов")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время демонстрации: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Основная функция демонстрации."""
    print("Демонстрация функциональности удаления сохраненных партий chess_stockfish")
    print("=" * 80)
    
    success = demonstrate_delete_functionality()
    
    if success:
        print("\n🎉 Все функции удаления сохраненных партий работают корректно!")
        print("\nНовые возможности позволяют:")
        print("  • Удалять ненужные сохраненные партии")
        print("  • Управлять коллекцией сохраненных игр")
        print("  • Освобождать место на диске")
    else:
        print("\n❌ Возникли ошибки во время демонстрации.")
        print("Пожалуйста, проверьте логи выше для получения дополнительной информации.")

if __name__ == "__main__":
    main()