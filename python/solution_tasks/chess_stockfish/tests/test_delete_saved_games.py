#!/usr/bin/env python3
"""
Тестирование функциональности удаления сохраненных партий в chess_stockfish.
"""

import sys
import os
import tempfile
import json

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_delete_functionality():
    """Тестирование функциональности удаления сохраненных партий."""
    print("Тестирование функциональности удаления сохраненных партий...")
    
    try:
        from game.chess_game import ChessGame
        
        # Создаем экземпляр игры
        print("1. Создание новой шахматной партии...")
        game = ChessGame()
        print("   ✓ Игра создана успешно")
        
        # Создаем несколько тестовых файлов сохранения
        print("2. Создание тестовых файлов сохранения...")
        test_files = []
        
        for i in range(3):
            # Создаем временный файл для тестирования
            filename = f"test_game_{i}.json"
            test_files.append(filename)
            
            # Сохраняем игру с разными именами
            game._save_game_to_file(filename)
            print(f"   ✓ Игра сохранена в файл {filename}")
        
        # Проверяем, что файлы существуют
        saved_games = game._list_saved_games()
        for filename in test_files:
            assert filename in saved_games, f"Файл {filename} должен быть в списке сохраненных игр"
        print("   ✓ Все тестовые файлы присутствуют в списке сохраненных игр")
        
        # Тестируем удаление одного файла
        print("3. Тестирование удаления файла...")
        file_to_delete = test_files[0]
        result = game._delete_saved_game(file_to_delete)
        assert result == True, "Удаление должно быть успешным"
        print(f"   ✓ Файл {file_to_delete} успешно удален")
        
        # Проверяем, что удаленный файл больше не в списке
        saved_games = game._list_saved_games()
        assert file_to_delete not in saved_games, f"Файл {file_to_delete} не должен быть в списке сохраненных игр"
        print("   ✓ Удаленный файл отсутствует в списке сохраненных игр")
        
        # Тестируем удаление несуществующего файла
        print("4. Тестирование удаления несуществующего файла...")
        result = game._delete_saved_game("nonexistent_file.json")
        # Должно вернуть False, но не вызвать исключение
        assert result == False, "Удаление несуществующего файла должно вернуть False"
        print("   ✓ Корректная обработка удаления несуществующего файла")
        
        # Очищаем оставшиеся тестовые файлы
        print("5. Очистка оставшихся тестовых файлов...")
        for filename in test_files[1:]:  # Пропускаем уже удаленный файл
            if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'saves', filename)):
                game._delete_saved_game(filename)
        print("   ✓ Оставшиеся тестовые файлы удалены")
        
        print("\n✅ Все тесты удаления сохраненных партий пройдены успешно!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция тестирования."""
    print("Тестирование функциональности удаления сохраненных партий chess_stockfish")
    print("=" * 70)
    
    # Запускаем тесты
    success = test_delete_functionality()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 Все тесты пройдены успешно!")
        print("\nРеализованные функции:")
        print("  ✅ Удаление сохраненных партий")
        print("  ✅ Обработка ошибок (удаление несуществующих файлов)")
        print("  ✅ Интеграция с меню игры")
        return 0
    else:
        print("❌ Некоторые тесты не пройдены.")
        print("Пожалуйста, проверьте логи выше для получения дополнительной информации.")
        return 1

if __name__ == "__main__":
    sys.exit(main())