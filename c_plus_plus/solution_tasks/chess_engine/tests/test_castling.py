#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование функциональности рокировки
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from chess_engine_wrapper import ChessEngineWrapper

def test_castling_rights():
    """Тест прав на рокировку"""
    print("♔ ТЕСТИРОВАНИЕ РОКИРОВКИ ♚")
    print("=" * 40)
    
    # Создаем движок
    engine = ChessEngineWrapper()
    
    # Тест 1: Начальная позиция - должны быть все права
    print("\n1. Начальная позиция:")
    engine.board_state = engine.get_initial_board()
    engine.current_turn = True
    print("Права белых (короткая):", engine.can_castle_kingside(True))
    print("Права белых (длинная):", engine.can_castle_queenside(True))
    print("Права черных (короткая):", engine.can_castle_kingside(False))
    print("Права черных (длинная):", engine.can_castle_queenside(False))
    
    # Тест 2: Ход королем - теряет права рокировки
    print("\n2. Ход королем белых (Ke2):")
    engine.make_move_algebraic("e1e2")  # Ke2
    engine.make_move_algebraic("e8e7")  # Ke7
    
    print("Права белых (короткая):", engine.can_castle_kingside(True))
    print("Права белых (длинная):", engine.can_castle_queenside(True))
    
    # Вернемся к начальной позиции
    engine.board_state = engine.get_initial_board()
    engine.current_turn = True
    
    # Тест 3: Ход ладьей - теряет право на эту сторону
    print("\n3. Ход ладьей белых (Ra2):")
    engine.make_move_algebraic("a1a2")  # Ra2
    engine.make_move_algebraic("a8a7")  # Ra7
    
    print("Права белых (короткая):", engine.can_castle_kingside(True))
    print("Права белых (длинная):", engine.can_castle_queenside(True))
    
    # Вернемся к начальной позиции
    engine.board_state = engine.get_initial_board()
    engine.current_turn = True
    
    # Тест 4: Попытка рокировки
    print("\n4. Попытка короткой рокировки белых (O-O):")
    # Сначала освободим путь для рокировки
    engine.make_move_algebraic("e2e4")  # e4
    engine.make_move_algebraic("e7e5")  # e5
    engine.make_move_algebraic("g1f3")  # Nf3
    engine.make_move_algebraic("g8f6")  # Nf6
    engine.make_move_algebraic("f1c4")  # Bc4
    engine.make_move_algebraic("f8c5")  # Bc5
    
    print("До рокировки:")
    print("Права белых (короткая):", engine.can_castle_kingside(True))
    
    # Попытка рокировки
    success = engine.make_move_algebraic("e1g1")  # O-O
    print("Рокировка успешна:", success)
    
    if success:
        print("После рокировки:")
        print("Права белых (короткая):", engine.can_castle_kingside(True))
        print("Права белых (длинная):", engine.can_castle_queenside(True))
        
        # Проверим позицию короля и ладьи
        king_pos = None
        rook_pos = None
        for row in range(8):
            for col in range(8):
                piece = engine.board_state[row][col]
                if piece == 'K':
                    king_pos = (row, col)
                elif piece == 'R':
                    if col == 5:  # Ладья должна быть на f1 после короткой рокировки
                        rook_pos = (row, col)
        
        print("Позиция короля:", king_pos)
        print("Позиция ладьи:", rook_pos)
        
        # Проверим что король на g1 (ранг 0, файл 6)
        if king_pos == (0, 6) and rook_pos == (0, 5):
            print("✅ Рокировка выполнена правильно!")
        else:
            print("❌ Ошибка в позиции после рокировки")

def test_en_passant():
    """Тест взятия на проходе"""
    print("\n\n♙ ТЕСТИРОВАНИЕ ВЗЯТИЯ НА ПРОХОДЕ ♟")
    print("=" * 40)
    
    engine = ChessEngineWrapper()
    
    # Установим позицию для теста en passant
    # Белая пешка на e5, черная пешка на f7
    engine.board_state = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', '.', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'P', 'p', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', '.', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    engine.current_player = True  # Белые
    
    print("Начальная позиция для en passant:")
    engine.print_board()
    
    # Белые делают двойной ход пешкой
    print("\nБелые: f2f4 (двойной ход пешкой)")
    engine.make_move_algebraic("f2f4")
    print("En passant square:", engine.get_en_passant_square())
    
    # Черные могут взять на проходе
    print("\nЧерные могут взять на проходе: exf3")
    legal_moves = engine.get_legal_moves()
    en_passant_moves = [move for move in legal_moves if 'xf3' in move]
    print("Доступные en passant ходы:", en_passant_moves)
    
    if en_passant_moves:
        print("✅ En passant доступен!")
        # Выполним взятие
        engine.make_move_san(en_passant_moves[0])
        print("После взятия на проходе:")
        engine.print_board()
    else:
        print("❌ En passant недоступен!")

def test_check_detection():
    """Тест обнаружения шаха"""
    print("\n\n♔ ТЕСТИРОВАНИЕ ОБНАРУЖЕНИЯ ШАХА ♚")
    print("=" * 40)
    
    engine = ChessEngineWrapper()
    
    # Позиция: король на e1, ферзь на h5 - шах
    engine.board_state = [
        ['r', 'n', 'b', '.', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', 'q'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    engine.current_player = True  # Белые ходят
    
    print("Позиция с шахом:")
    engine.print_board()
    
    print("Белые под шахом:", engine.is_check(True))
    print("Черные под шахом:", engine.is_check(False))
    
    # Проверим генерацию легальных ходов
    legal_moves = engine.get_legal_moves()
    print(f"Легальных ходов у белых: {len(legal_moves)}")
    
    # Попробуем сделать ход, который не спасает от шаха
    print("\nПопытка сделать ход, не спасающий от шаха:")
    illegal_move_success = engine.make_move_algebraic("b1c3")  # Nc3
    print("Ход Nc3 успешен:", illegal_move_success)
    
    if not illegal_move_success:
        print("✅ Неверный ход заблокирован!")
    else:
        print("❌ Неверный ход разрешен!")

if __name__ == "__main__":
    test_castling_rights()
    test_en_passant()
    test_check_detection()
    print("\n🎉 Все тесты завершены!")