#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вывод статистики оптимизированного шахматного движка
"""

import time
from core.enhanced_chess_ai import EnhancedChessAI

def show_stats():
    """Показать статистику движка"""
    print('\n' + '='*70)
    print('📊 КРАТКАЯ СТАТИСТИКА ОПТИМИЗИРОВАННОГО ШАХМАТНОГО ДВИЖКА')
    print('='*70)
    
    # Инициализация
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    
    ai = EnhancedChessAI(4)
    
    print(f'\n🔧 КОНФИГУРАЦИЯ:')
    print(f'  • Глубина поиска: {ai.search_depth}')
    print(f'  • Макс. размер TT: {ai.max_tt_size:,} позиций')
    print(f'  • Killer moves слотов: {len(ai.killer_moves)}')
    print(f'  • Zobrist keys: {len(ai.zobrist_keys["pieces"])} типов фигур')
    
    print(f'\n⚙️ ВКЛЮЧЕННЫЕ ОПТИМИЗАЦИИ:')
    optimizations = [
        'Zobrist Hashing (XOR-based)',
        'Transposition Table с управлением памятью',
        'Iterative Deepening',
        'Aspiration Windows',
        'Null Move Pruning (R=2)',
        'Principal Variation Search (PVS)',
        'Late Move Reduction (LMR)',
        'Killer Moves Heuristic (2 на глубину)',
        'History Heuristic',
        'MVV-LVA Move Ordering',
        'Quiescence Search (до глубины 8)',
        'Alpha-Beta Pruning'
    ]
    for i, opt in enumerate(optimizations, 1):
        print(f'  {i:2d}. ✓ {opt}')
    
    print(f'\n⚡ ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ:')
    print('  Запуск поиска на начальной позиции...')
    
    start = time.perf_counter()
    move = ai.get_best_move(board, True, 5.0)
    elapsed = time.perf_counter() - start
    
    nps = ai.nodes_searched / elapsed if elapsed > 0 else 0
    tt_rate = (ai.tt_hits / ai.nodes_searched * 100) if ai.nodes_searched > 0 else 0
    
    print(f'\n📈 РЕЗУЛЬТАТЫ:')
    print(f'  • Время поиска: {elapsed:.3f} сек')
    print(f'  • Узлов проверено: {ai.nodes_searched:,}')
    print(f'  • TT Hits: {ai.tt_hits:,} ({tt_rate:.1f}%)')
    print(f'  • Скорость: {nps:,.0f} узлов/сек')
    print(f'  • Найденный ход: {move}')
    print(f'  • Размер TT: {len(ai.transposition_table):,} позиций')
    
    # Оценка производительности
    print(f'\n🎯 ОЦЕНКА ЭФФЕКТИВНОСТИ:')
    if tt_rate > 5:
        print(f'  ✅ Отличная эффективность TT: {tt_rate:.1f}%')
    elif tt_rate > 2:
        print(f'  ✓  Хорошая эффективность TT: {tt_rate:.1f}%')
    else:
        print(f'  •  Умеренная эффективность TT: {tt_rate:.1f}%')
    
    if nps > 3000:
        print(f'  ✅ Отличная скорость поиска: {nps:,.0f} узлов/сек')
    elif nps > 1000:
        print(f'  ✓  Хорошая скорость поиска: {nps:,.0f} узлов/сек')
    else:
        print(f'  •  Умеренная скорость: {nps:,.0f} узлов/сек')
    
    print('\n' + '='*70)
    print('✅ Движок готов к использованию!')
    print('='*70 + '\n')

if __name__ == "__main__":
    show_stats()
