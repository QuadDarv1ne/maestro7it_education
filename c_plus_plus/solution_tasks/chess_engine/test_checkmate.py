#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование определения мата и пата в различных позициях
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.chess_engine_wrapper import ChessEngineWrapper

def test_fool_mate():
    """Тест детского мата (2 хода)"""
    print("\n=== Тест 1: Детский мат ===")
    engine = ChessEngineWrapper()
    
    # 1. f3 e5
    engine.make_move((6, 5), (5, 5))  # f2-f3
    engine.make_move((1, 4), (3, 4))  # e7-e5
    
    # 2. g4 Qh4#
    engine.make_move((6, 6), (4, 6))  # g2-g4
    engine.make_move((0, 3), (4, 7))  # Qd8-h4#
    
    is_mate = engine.is_checkmate(True)  # Проверка мата белым
    print(f"Мат белым: {is_mate}")
    print(f"Король под шахом: {engine.is_king_in_check(True)}")
    
    if is_mate:
        print("✓ Детский мат определен правильно!")
    else:
        print("✗ Ошибка: мат не определен!")
    
    return is_mate

def test_scholar_mate():
    """Тест мата ученого (4 хода)"""
    print("\n=== Тест 2: Мат ученого ===")
    engine = ChessEngineWrapper()
    
    # 1. e4 e5
    engine.make_move((6, 4), (4, 4))
    engine.make_move((1, 4), (3, 4))
    
    # 2. Bc4 Nc6
    engine.make_move((7, 5), (4, 2))
    engine.make_move((0, 1), (2, 2))
    
    # 3. Qh5 Nf6
    engine.make_move((7, 3), (3, 7))
    engine.make_move((0, 6), (2, 5))
    
    # 4. Qxf7#
    engine.make_move((3, 7), (1, 5))
    
    is_mate = engine.is_checkmate(False)  # Проверка мата черным
    print(f"Мат черным: {is_mate}")
    print(f"Король под шахом: {engine.is_king_in_check(False)}")
    
    if is_mate:
        print("✓ Мат ученого определен правильно!")
    else:
        print("✗ Ошибка: мат не определен!")
    
    return is_mate

def test_back_rank_mate():
    """Тест мата на последней горизонтали"""
    print("\n=== Тест 3: Мат на последней горизонтали ===")
    engine = ChessEngineWrapper()
    
    # Устанавливаем позицию вручную
    # Черный король на e8, белые пешки на f7, g7, h7, белая ладья на e1
    position = [
        ['r', '.', '.', '.', 'k', '.', '.', 'r'],
        ['.', '.', '.', '.', '.', 'P', 'P', 'P'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'R', '.', '.', 'K']
    ]
    engine.set_position(position, True)  # Ход белых
    
    # Ладья на e8 - мат
    engine.make_move((7, 4), (0, 4))  # Re1-e8#
    
    is_mate = engine.is_checkmate(False)  # Проверка мата черным
    print(f"Мат черным: {is_mate}")
    print(f"Король под шахом: {engine.is_king_in_check(False)}")
    
    if is_mate:
        print("✓ Мат на последней горизонтали определен правильно!")
    else:
        print("✗ Ошибка: мат не определен!")
    
    return is_mate

def test_stalemate():
    """Тест пата"""
    print("\n=== Тест 4: Пат ===")
    engine = ChessEngineWrapper()
    
    # Позиция пата: черный король в углу, белые король и ферзь
    position = [
        ['k', '.', '.', '.', '.', '.', '.', '.'],
        ['.', 'Q', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'K', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    engine.set_position(position, False)  # Ход черных
    
    is_stalemate = engine.is_stalemate(False)
    is_check = engine.is_king_in_check(False)
    
    print(f"Пат: {is_stalemate}")
    print(f"Король под шахом: {is_check}")
    
    if is_stalemate and not is_check:
        print("✓ Пат определен правильно!")
    else:
        print("✗ Ошибка: пат не определен или король под шахом!")
    
    return is_stalemate

def test_check_not_mate():
    """Тест: шах, но не мат"""
    print("\n=== Тест 5: Шах, но не мат ===")
    engine = ChessEngineWrapper()
    
    # Позиция: шах, но король может уйти
    position = [
        ['k', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['R', '.', '.', '.', 'K', '.', '.', '.']
    ]
    engine.set_position(position, True)  # Ход белых
    
    # Ладья дает шах
    engine.make_move((7, 0), (0, 0))  # Ra1-a8+
    
    is_check = engine.is_king_in_check(False)
    is_mate = engine.is_checkmate(False)
    
    print(f"Король под шахом: {is_check}")
    print(f"Мат: {is_mate}")
    
    if is_check and not is_mate:
        print("✓ Шах определен правильно, это не мат!")
    else:
        print("✗ Ошибка в определении!")
    
    return is_check and not is_mate

def main():
    """Запуск всех тестов"""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ОПРЕДЕЛЕНИЯ МАТА И ПАТА")
    print("=" * 60)
    
    tests = [
        ("Детский мат", test_fool_mate),
        ("Мат ученого", test_scholar_mate),
        ("Мат на последней горизонтали", test_back_rank_mate),
        ("Пат", test_stalemate),
        ("Шах, но не мат", test_check_not_mate)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ Ошибка при выполнении теста '{name}': {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
    print("=" * 60)
    
    if passed == total:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print(f"⚠️  {total - passed} тестов провалено")

if __name__ == "__main__":
    main()
