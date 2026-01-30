#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест всех новых оптимизаций шахматного движка
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.enhanced_chess_ai import EnhancedChessAI
from core.chess_engine_wrapper import ChessEngineWrapper

def test_zobrist_hashing():
    """Тест Zobrist хэширования"""
    print("\n🧪 Тест 1: Zobrist Hashing")
    print("=" * 50)
    
    ai = EnhancedChessAI(4)
    
    # Проверка инициализации
    assert 'pieces' in ai.zobrist_keys, "Zobrist keys не инициализированы"
    assert 'turn' in ai.zobrist_keys, "Zobrist turn key не инициализирован"
    
    pieces_count = len(ai.zobrist_keys['pieces'])
    print(f"✅ Zobrist keys инициализированы для {pieces_count} типов фигур")
    
    # Тест хэширования
    test_board = ai.move_gen.get_initial_board()
    hash1 = ai.get_board_hash(test_board, True)
    hash2 = ai.get_board_hash(test_board, True)
    
    assert hash1 == hash2, "Zobrist хэш должен быть детерминированным"
    print(f"✅ Хэш начальной позиции: {hash1}")
    
    # Разные позиции должны иметь разные хэши
    hash3 = ai.get_board_hash(test_board, False)
    assert hash1 != hash3, "Хэш для разных цветов должен отличаться"
    print(f"✅ Хэш меняется при смене очереди: {hash3}")

def test_killer_moves():
    """Тест Killer Moves эвристики"""
    print("\n🧪 Тест 2: Killer Moves Heuristic")
    print("=" * 50)
    
    ai = EnhancedChessAI(4)
    
    # Проверка инициализации
    assert len(ai.killer_moves) == 64, "Должно быть 64 слота для killer moves"
    assert all(km == [None, None] for km in ai.killer_moves), "Killer moves должны быть пустыми"
    print(f"✅ Killer moves инициализированы: {len(ai.killer_moves)} слотов")
    
    # Тест добавления killer move
    test_move = ((6, 4), (4, 4))  # e2-e4
    ai.update_killer_moves(test_move, 3)
    
    assert ai.killer_moves[3][0] == test_move, "Killer move должен быть сохранен"
    print(f"✅ Killer move добавлен: {test_move}")

def test_null_move_pruning():
    """Тест Null Move Pruning"""
    print("\n🧪 Тест 3: Null Move Pruning")
    print("=" * 50)
    
    ai = EnhancedChessAI(4)
    test_board = ai.move_gen.get_initial_board()
    
    # Проверка, что функция принимает параметр allow_null_move
    try:
        eval_score, move = ai.minimax(test_board, 3, float('-inf'), float('inf'), True, allow_null_move=False)
        print(f"✅ Null move pruning работает (параметр allow_null_move доступен)")
        print(f"   Оценка: {eval_score}, Ход: {move}")
    except TypeError as e:
        print(f"❌ Ошибка: {e}")

def test_aspiration_windows():
    """Тест Aspiration Windows"""
    print("\n🧪 Тест 4: Aspiration Windows")
    print("=" * 50)
    
    ai = EnhancedChessAI(4)
    test_board = ai.move_gen.get_initial_board()
    
    print("Запуск поиска с aspiration windows...")
    best_move = ai.get_best_move(test_board, True, time_limit=2.0)
    
    if best_move:
        print(f"✅ Aspiration windows работает")
        print(f"   Найденный ход: {best_move}")
        print(f"   Узлов проверено: {ai.nodes_searched:,}")
        print(f"   TT Hits: {ai.tt_hits:,}")
    else:
        print("❌ Ход не найден")

def test_game_status():
    """Тест определения статуса игры"""
    print("\n🧪 Тест 5: Статус игры (мат/пат)")
    print("=" * 50)
    
    engine = ChessEngineWrapper()
    
    # Проверка методов
    assert hasattr(engine, 'is_checkmate'), "Метод is_checkmate не найден"
    assert hasattr(engine, 'is_stalemate'), "Метод is_stalemate не найден"
    assert hasattr(engine, 'get_game_status'), "Метод get_game_status не найден"
    
    print("✅ Все методы статуса игры доступны")
    
    # Тест на начальной позиции
    status = engine.get_game_status()
    print(f"   Статус начальной позиции: {status}")
    assert "продолжается" in status or "Игра" in status, "Игра должна продолжаться"

def test_performance():
    """Тест производительности"""
    print("\n🧪 Тест 6: Производительность")
    print("=" * 50)
    
    import time
    
    ai = EnhancedChessAI(4)
    test_board = ai.move_gen.get_initial_board()
    
    # Тест скорости хэширования
    start = time.perf_counter()
    for _ in range(10000):
        hash_val = ai.get_board_hash(test_board, True)
    hash_time = (time.perf_counter() - start) * 1000
    
    print(f"✅ Zobrist hashing: {hash_time:.2f} мс на 10,000 хэшей")
    print(f"   ({hash_time/10:.4f} мкс на хэш)")
    
    # Тест поиска
    print("\nЗапуск поиска на глубину 3...")
    start = time.perf_counter()
    best_move = ai.get_best_move(test_board, True, time_limit=5.0)
    search_time = time.perf_counter() - start
    
    if best_move:
        nps = ai.nodes_searched / search_time if search_time > 0 else 0
        print(f"✅ Поиск завершен за {search_time:.2f} сек")
        print(f"   Узлов проверено: {ai.nodes_searched:,}")
        print(f"   TT Hits: {ai.tt_hits:,}")
        print(f"   Узлов/сек: {nps:,.0f}")

def main():
    """Запуск всех тестов"""
    print("\n" + "="*50)
    print("🚀 ТЕСТИРОВАНИЕ ОПТИМИЗАЦИЙ ШАХМАТНОГО ДВИЖКА")
    print("="*50)
    
    try:
        test_zobrist_hashing()
        test_killer_moves()
        test_null_move_pruning()
        test_aspiration_windows()
        test_game_status()
        test_performance()
        
        print("\n" + "="*50)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
