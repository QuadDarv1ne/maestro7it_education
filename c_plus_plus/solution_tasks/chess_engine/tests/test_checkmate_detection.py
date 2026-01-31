#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Комплексные тесты определения мата
Проверяет различные классические матовые позиции для проверки способности движка определять мат.
"""

import sys
sys.path.append('core')

from chess_engine_wrapper import ChessEngineWrapper

def notation_to_pos(notation):
    """Преобразование алгебраической нотации (например, 'e2') в позицию на доске (row, col)"""
    col = ord(notation[0]) - ord('a')
    row = 8 - int(notation[1])
    return (row, col)

def make_move(engine, from_notation, to_notation):
    """Выполнение хода с использованием алгебраической нотации"""
    from_pos = notation_to_pos(from_notation)
    to_pos = notation_to_pos(to_notation)
    return engine.make_move(from_pos, to_pos)

def print_board(board_state):
    """Вывод доски в читаемом формате"""
    print("\n   a b c d e f g h")
    print("  +----------------+")
    for i, row in enumerate(board_state):
        print(f"{8-i} |", end="")
        for piece in row:
            print(f"{piece} ", end="")
        print(f"| {8-i}")
    print("  +----------------+")
    print("   a b c d e f g h\n")

def test_fool_mate():
    """Тест 1: Дурацкий мат - самый быстрый мат в шахматах"""
    print("="*50)
    print("Test 1: Fool's Mate")
    print("="*50)
    
    engine = ChessEngineWrapper()
    
    # 1. f3
    make_move(engine, 'f2', 'f3')
    # 1...e5
    make_move(engine, 'e7', 'e5')
    # 2. g4
    make_move(engine, 'g2', 'g4')
    # 2...Фh4# - Мат!
    make_move(engine, 'd8', 'h4')
    
    print_board(engine.board_state)
    
    is_check = engine.is_king_in_check(True)  # White king
    is_mate = engine.is_checkmate(True)
    
    print(f"White king in check: {is_check}")
    print(f"Checkmate: {is_mate}")
    
    if is_check and is_mate:
        print("[PASS] PASSED: Fool's Mate correctly detected!")
        return True
    else:
        print("[FAIL] FAILED: Fool's Mate not detected!")
        return False

def test_scholar_mate():
    """Тест 2: Детский мат - классическая ловушка для начинающих"""
    print("\n" + "="*50)
    print("Test 2: Scholar's Mate")
    print("="*50)
    
    engine = ChessEngineWrapper()
    
    # 1. e4 e5
    make_move(engine, 'e2', 'e4')
    make_move(engine, 'e7', 'e5')
    # 2. Сc4 Кc6
    make_move(engine, 'f1', 'c4')
    make_move(engine, 'b8', 'c6')
    # 3. Фh5 Кf6
    make_move(engine, 'd1', 'h5')
    make_move(engine, 'g8', 'f6')
    # 4. Фxf7# - Мат!
    make_move(engine, 'h5', 'f7')
    
    print_board(engine.board_state)
    
    is_check = engine.is_king_in_check(False)  # Black king
    is_mate = engine.is_checkmate(False)
    
    print(f"Black king in check: {is_check}")
    print(f"Checkmate: {is_mate}")
    
    if is_check and is_mate:
        print("[PASS] PASSED: Scholar's Mate correctly detected!")
        return True
    else:
        print("[FAIL] FAILED: Scholar's Mate not detected!")
        return False

def test_back_rank_mate():
    """Тест 3: Линейный мат - ладья ставит мат на 8-й горизонтали"""
    print("\n" + "="*50)
    print("Test 3: Back Rank Mate")
    print("="*50)
    
    engine = ChessEngineWrapper()
    
    # Позиция: Чёрный король заперт своими пешками
    # Белые: Король на g1, Ладья на e1  
    # Чёрные: Король на g8, пешки на f7, g7, h7, ладья на d8
    # После хода ладьёй на e8 - мат!
    position = [
        ['.', '.', '.', 'r', '.', '.', 'k', '.'],  # 8-я горизонталь - король на g8, ладья на d8
        ['.', '.', '.', '.', '.', 'p', 'p', 'p'],  # 7-я горизонталь - пешки блокируют короля
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', 'P', 'P', 'P'],  # 2-я горизонталь
        ['.', '.', '.', '.', 'R', '.', 'K', '.']   # 1-я горизонталь - Ладья e1, Король g1
    ]
    
    engine.set_position(position, current_turn=True)  # Ход белых
    
    # Белые играют Лe8# - мат!
    success = make_move(engine, 'e1', 'e8')
    
    if not success:
        print("[FAIL] FAILED: Could not execute Rd8")
        return False
    
    print_board(engine.board_state)
    
    is_check = engine.is_king_in_check(False)  # Black king
    is_mate = engine.is_checkmate(False)
    
    print(f"Black king in check: {is_check}")
    print(f"Checkmate: {is_mate}")
    
    if is_check and is_mate:
        print("[PASS] PASSED: Back Rank Mate correctly detected!")
        return True
    else:
        print("[FAIL] FAILED: Back Rank Mate not detected!")
        return False

def test_smothered_mate():
    """Тест 4: Спёртый мат - конь ставит мат королю, окружённому своими фигурами"""
    print("\n" + "="*50)
    print("Test 4: Smothered Mate")
    print("="*50)
    
    engine = ChessEngineWrapper()
    
    # Классическая позиция спёртого мата
    # Чёрный король на h8, полностью окружён
    # Белый конь на f7 ставит мат
    position = [
        ['.', '.', '.', '.', '.', 'r', '.', 'k'],  # 8-я горизонталь - король на h8, ладья на f8
        ['.', '.', '.', '.', '.', '.', 'p', 'p'],  # 7-я горизонталь - пешки на g7, h7
        ['.', '.', '.', '.', '.', '.', '.', 'r'],  # 6-я горизонталь - ладья на h6
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', 'N', '.', '.'],  # 3-я горизонталь - конь на f3
        ['.', '.', '.', '.', '.', 'P', 'P', 'P'],
        ['.', '.', '.', '.', 'K', '.', '.', 'R']
    ]
    
    engine.set_position(position, current_turn=True)  # Ход белых
    
    # Переводим коня на f7 для мата
    # Сначала на e5
    success1 = make_move(engine, 'f3', 'e5')
    if not success1:
        print("[FAIL] FAILED: Could not move knight to e5")
        return False
    
    # Чёрные двигают ладью
    make_move(engine, 'h6', 'h5')
    
    # Затем конь на f7# - мат!  
    success2 = make_move(engine, 'e5', 'f7')
    if not success2:
        print("[FAIL] FAILED: Could not move knight to f7")
        return False
    
    print_board(engine.board_state)
    
    is_check = engine.is_king_in_check(False)  # Black king
    is_mate = engine.is_checkmate(False)
    
    print(f"Black king in check: {is_check}")
    print(f"Checkmate: {is_mate}")
    
    if is_check and is_mate:
        print("[PASS] PASSED: Smothered Mate correctly detected!")
        return True
    else:
        print("[FAIL] FAILED: Smothered Mate not detected!")
        return False

def test_stalemate():
    """Тест 5: Определение пата - король не под шахом, но нет легальных ходов"""
    print("\n" + "="*50)
    print("Test 5: Stalemate Detection")
    print("="*50)
    
    engine = ChessEngineWrapper()
    
    # Классическая позиция пата
    # Белые: Король на h6, Ферзь на g6
    # Чёрные: Король на h8 (не под шахом, но нет легальных ходов)
    position = [
        ['.', '.', '.', '.', '.', '.', '.', 'k'],  # 8-я горизонталь - чёрный король на h8
        ['.', '.', '.', '.', '.', '.', '.', '.'],  # 7-я горизонталь - пусто  
        ['.', '.', '.', '.', '.', '.', 'Q', 'K'],  # 6-я горизонталь - ферзь на g6, король на h6
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    engine.set_position(position, current_turn=False)  # Ход чёрных
    
    print_board(engine.board_state)
    
    is_check = engine.is_king_in_check(False)  # Black king
    is_stalemate = engine.is_stalemate(False)
    
    print(f"Black king in check: {is_check}")
    print(f"Stalemate: {is_stalemate}")
    
    if not is_check and is_stalemate:
        print("[PASS] PASSED: Stalemate correctly detected!")
        return True
    else:
        print("[FAIL] FAILED: Stalemate not detected correctly!")
        return False

def test_queen_and_king_mate():
    """Тест 6: Мат ферзём и королём против короля - базовый мат"""
    print("\n" + "="*50)
    print("Test 6: Queen and King Checkmate")
    print("="*50)
    
    engine = ChessEngineWrapper()
    
    # Позиция: Базовый эндшпиль ферзь+король против короля
    # Белые: Король на f6, Ферзь на g7
    # Чёрные: Король на h8 (матовая позиция)
    position = [
        ['.', '.', '.', '.', '.', '.', '.', 'k'],  # 8-я горизонталь
        ['.', '.', '.', '.', '.', '.', 'Q', '.'],  # 7-я горизонталь
        ['.', '.', '.', '.', '.', 'K', '.', '.'],  # 6-я горизонталь
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    engine.set_position(position, current_turn=False)  # Ход чёрных
    
    print_board(engine.board_state)
    
    is_check = engine.is_king_in_check(False)  # Black king
    is_mate = engine.is_checkmate(False)
    
    print(f"Black king in check: {is_check}")
    print(f"Checkmate: {is_mate}")
    
    if is_check and is_mate:
        print("[PASS] PASSED: Queen and King mate correctly detected!")
        return True
    else:
        print("[FAIL] FAILED: Queen and King mate not detected!")
        return False

def run_all_tests():
    """Запуск всех тестов определения мата"""
    print("\n" + "="*70)
    print(" CHECKMATE DETECTION TEST SUITE")
    print("="*70)
    
    results = []
    
    results.append(("Дурацкий мат", test_fool_mate()))
    results.append(("Детский мат", test_scholar_mate()))
    results.append(("Линейный мат", test_back_rank_mate()))
    results.append(("Спёртый мат", test_smothered_mate()))
    results.append(("Пат", test_stalemate()))
    results.append(("Мат ферзём и королём", test_queen_and_king_mate()))
    
    # Вывод итогов
    print("\n" + "="*70)
    print(" ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS] ПРОЙДЕН" if result else "[FAIL] ПРОВАЛЕН"
        print(f"{status}: {name}")
    
    print("-"*70)
    print(f"Всего: {passed}/{total} тестов пройдено ({100*passed//total}%)")
    print("="*70)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
