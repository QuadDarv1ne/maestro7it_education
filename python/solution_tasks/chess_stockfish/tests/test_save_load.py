#!/usr/bin/env python3
"""
Тестирование функциональности сохранения и загрузки партий в chess_stockfish.
"""

import sys
import os
import tempfile
import json

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_save_load_functionality():
    """Тестирование функциональности сохранения и загрузки партий."""
    print("Тестирование функциональности сохранения и загрузки партий...")
    
    try:
        from game.chess_game import ChessGame
        
        # Создаем экземпляр игры
        print("1. Создание новой шахматной партии...")
        game = ChessGame()
        print("   ✓ Игра создана успешно")
        
        # Проверяем начальное состояние
        print("2. Проверка начального состояния...")
        initial_board = game.get_board_state()
        assert initial_board is not None, "Начальная позиция не должна быть None"
        assert len(initial_board) == 8, "Доска должна иметь 8 рядов"
        assert len(initial_board[0]) == 8, "Доска должна иметь 8 колонок"
        print("   ✓ Начальное состояние корректно")
        
        # Делаем несколько ходов
        print("3. Выполнение ходов...")
        # Белые: e2-e4
        game.engine.make_move("e2e4")
        game.move_history.append("e2e4")
        
        # Черные: e7-e5
        game.engine.make_move("e7e5")
        game.move_history.append("e7e5")
        
        # Белые: g1-f3
        game.engine.make_move("g1f3")
        game.move_history.append("g1f3")
        
        board_after_moves = game.get_board_state()
        print("   ✓ Ходы выполнены успешно")
        
        # Создаем временный файл для тестирования
        print("4. Тестирование сохранения в файл...")
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
            temp_filename = os.path.basename(tmp_file.name)
            
        # Сохраняем игру
        game._save_game_to_file(temp_filename)
        print(f"   ✓ Игра сохранена в временный файл {temp_filename}")
        
        # Проверяем, что файл существует
        saves_dir = os.path.join(os.path.dirname(__file__), '..', 'saves')
        full_path = os.path.join(saves_dir, temp_filename)
        assert os.path.exists(full_path), f"Файл сохранения {full_path} не существует"
        print("   ✓ Файл сохранения существует")
        
        # Проверяем содержимое файла
        with open(full_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert 'player_color' in saved_data, "В сохранении должна быть информация о цвете игрока"
        assert 'skill_level' in saved_data, "В сохранении должна быть информация об уровне сложности"
        assert 'move_history' in saved_data, "В сохранении должна быть история ходов"
        assert 'fen' in saved_data, "В сохранении должна быть позиция в формате FEN"
        assert 'version' in saved_data, "В сохранении должна быть версия"
        print("   ✓ Содержимое файла сохранения корректно")
        
        # Создаем новую игру для тестирования загрузки
        print("5. Тестирование загрузки из файла...")
        new_game = ChessGame()
        
        # Загружаем игру из файла
        new_game._load_game_from_file(temp_filename)
        
        # Проверяем, что состояние совпадает (сравниваем через FEN)
        original_fen = game.engine.get_fen()
        loaded_fen = new_game.engine.get_fen()
        assert original_fen == loaded_fen, f"FEN позиции должны совпадать: {original_fen} vs {loaded_fen}"
        
        # Проверяем другие параметры
        assert new_game.player_color == game.player_color, "Цвет игрока должен совпадать"
        assert new_game.skill_level == game.skill_level, "Уровень сложности должен совпадать"
        assert new_game.move_history == game.move_history, "История ходов должна совпадать"
        print("   ✓ Загрузка из файла выполнена успешно")
        
        # Тестирование списка сохраненных игр
        print("6. Тестирование получения списка сохраненных игр...")
        saved_games = game._list_saved_games()
        assert isinstance(saved_games, list), "Список сохраненных игр должен быть списком"
        assert temp_filename in saved_games, "В списке должна быть наша тестовая игра"
        print("   ✓ Получение списка сохраненных игр работает корректно")
        
        # Очищаем временный файл
        if os.path.exists(full_path):
            os.unlink(full_path)
        print("   ✓ Временный файл удален")
        
        print("\n✅ Все тесты сохранения и загрузки пройдены успешно!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Тестирование граничных случаев."""
    print("\nТестирование граничных случаев...")
    
    try:
        from game.chess_game import ChessGame
        
        # Тестирование загрузки несуществующего файла
        print("1. Тестирование загрузки несуществующего файла...")
        game = ChessGame()
        game._load_game_from_file("nonexistent_file.json")
        # Должно появиться сообщение об ошибке в move_feedback
        feedback = game.move_feedback if game.move_feedback else ""
        assert "не найден" in feedback or "не найден" in feedback.lower()
        print("   ✓ Корректная обработка несуществующего файла")
        
        # Тестирование сохранения с автоматическим именем
        print("2. Тестирование сохранения с автоматическим именем...")
        game._save_game_to_file()  # Без параметров
        saved_games = game._list_saved_games()
        # Проверяем, что появился хотя бы один файл
        assert len(saved_games) > 0, "Должен появиться хотя бы один файл сохранения"
        print("   ✓ Сохранение с автоматическим именем работает")
        
        # Очищаем тестовые файлы
        for filename in saved_games:
            saves_dir = os.path.join(os.path.dirname(__file__), '..', 'saves')
            full_path = os.path.join(saves_dir, filename)
            if os.path.exists(full_path):
                os.unlink(full_path)
        print("   ✓ Тестовые файлы удалены")
        
        print("\n✅ Все тесты граничных случаев пройдены успешно!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка во время тестирования граничных случаев: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция тестирования."""
    print("Тестирование функциональности сохранения и загрузки партий chess_stockfish")
    print("=" * 70)
    
    # Запускаем основные тесты
    success1 = test_save_load_functionality()
    
    # Запускаем тесты граничных случаев
    success2 = test_edge_cases()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 Все тесты пройдены успешно!")
        print("\nРеализованные функции:")
        print("  ✅ Сохранение партий в файлы")
        print("  ✅ Загрузка партий из файлов")
        print("  ✅ Получение списка сохраненных партий")
        print("  ✅ Обработка ошибок (несуществующие файлы и т.д.)")
        print("  ✅ Совместимость форматов сохранения")
        return 0
    else:
        print("❌ Некоторые тесты не пройдены.")
        print("Пожалуйста, проверьте логи выше для получения дополнительной информации.")
        return 1

if __name__ == "__main__":
    sys.exit(main())