#!/usr/bin/env python3
"""
Test script for enhanced chess game features.
"""

from game.chess_game import ChessGame

def main():
    """Test the enhanced chess game."""
    try:
        print("Запуск тестовой игры с улучшенными функциями...")
        # Создаем игру с настройками по умолчанию
        game = ChessGame()
        print("Игра создана успешно!")
        print("Проверка доступа к новым функциям...")
        
        # Проверяем новые методы
        summary = game._get_game_summary()
        print(f"Резюме игры: {summary}")
        
        print("Тест завершен успешно!")
        print("Для полноценной игры запустите main.py")
        
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")

if __name__ == "__main__":
    main()