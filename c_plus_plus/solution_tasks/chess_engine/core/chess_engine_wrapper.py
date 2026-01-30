#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import os
import sys
import time
from typing import Tuple, List, Optional, Dict
from functools import lru_cache
import hashlib
from collections import OrderedDict

class ChessEngineWrapper:
    """Python wrapper для С++ шахматного движка"""
    
    def __init__(self):
        self.lib = None
        self.board_state = self.get_initial_board()
        self.current_turn = True  # True = белые, False = черные
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.game_stats = {
            'moves_count': 0,
            'captures_count': 0,
            'check_count': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'position_evaluations': 0
        }
        self.game_active = True
        self.selected_square = None
        self.valid_moves = []
        
        # Кэширование для оптимизации
        self._position_hash_cache = {}
        # НОВОЕ: Используем OrderedDict для правильного LRU
        self._move_validation_cache = OrderedDict()
        self._king_check_cache = OrderedDict()
        self._legal_moves_cache = OrderedDict()
        self._cache_timestamps = {}
        self._cache_ttl = 120.0  # 2 минуты жизни записи
        self._cache_max_size = 10000
        
        # Метрики производительности
        self._performance_metrics = {
            'move_validation_time': 0.0,
            'checkmate_detection_time': 0.0,
            'ai_thinking_time': 0.0,
            'cache_cleanup_time': 0.0
        }
        
        # Рокировка и специальные ходы
        self.castling_rights = {
            'white_kingside': True,
            'white_queenside': True,
            'black_kingside': True,
            'black_queenside': True
        }
        self.king_moved = {'white': False, 'black': False}
        self.rook_moved = {
            'white_kingside': False,
            'white_queenside': False,
            'black_kingside': False,
            'black_queenside': False
        }
        self.en_passant_target = None
        
        # Интеграция оптимизированных компонентов
        # ВРЕМЕННО ОТКЛЮЧЕНО: BitboardMoveGenerator вызывает проблемы с валидацией
        # try:
        #     from core.optimized_move_generator import BitboardMoveGenerator
        #     self.move_gen = BitboardMoveGenerator()
        # except ImportError:
        #     try:
        #         from .optimized_move_generator import BitboardMoveGenerator
        #         self.move_gen = BitboardMoveGenerator()
        #     except ImportError:
        #         self.move_gen = None
        self.move_gen = None  # Используем только Python валидацию
            
        # ВКЛЮЧЕНО: EnhancedChessAI теперь работает без циклической зависимости
        try:
            from core.enhanced_chess_ai import EnhancedChessAI
            self.ai = EnhancedChessAI(search_depth=4, engine_wrapper=self)
        except ImportError:
            try:
                from .enhanced_chess_ai import EnhancedChessAI
                self.ai = EnhancedChessAI(search_depth=4, engine_wrapper=self)
            except ImportError:
                print("Предупреждение: EnhancedChessAI не найден, используем базовый AI")
                self.ai = None
                
        # Zobrist hashing для быстрой проверки позиций (синхронизируем с AI)
        if self.ai:
            self.zobrist_keys = self.ai.zobrist_keys
        else:
            # Резервная инициализация Zobrist если AI не найден
            import random
            random.seed(42)
            self.zobrist_keys = {
                'pieces': {p: [random.getrandbits(64) for _ in range(64)] for p in ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']},
                'turn': random.getrandbits(64)
            }
        
    def initialize_engine(self) -> bool:
        """Инициализация С++ библиотеки движка"""
        try:
            # Попытка загрузить скомпилированную библиотеку
            if os.name == 'nt':  # Windows
                lib_name = 'chess_engine.dll'
            else:  # Linux/Mac
                lib_name = 'libchess_engine.so'
            
            lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'build_gui', lib_name)
            if os.path.exists(lib_path):
                self.lib = ctypes.CDLL(lib_path)
                print("С++ движок успешно загружен")
                return True
            else:
                print("Библиотека движка не найдена, используем Python реализацию")
                return False
        except Exception as e:
            print(f"Ошибка загрузки движка: {e}")
            return False
    
    def get_initial_board(self) -> List[List[str]]:
        """Начальная позиция шахматной доски"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def get_game_statistics(self) -> dict:
        """Получение статистики текущей игры"""
        stats = self.game_stats.copy()
        stats['performance_metrics'] = self._performance_metrics.copy()
        stats['cache_size'] = {
            'position_hash': len(self._position_hash_cache),
            'move_validation': len(self._move_validation_cache),
            'king_check': len(self._king_check_cache),
            'legal_moves': len(self._legal_moves_cache)
        }
        if self.ai:
            stats['ai_nodes'] = self.nodes_searched = getattr(self.ai, 'nodes_searched', 0)
            stats['ai_tt_hits'] = getattr(self.ai, 'tt_hits', 0)
        return stats
    
    def print_board(self, show_coords: bool = True):
        """Красивый вывод доски в консоль"""
        print("\n" + "="*33)
        
        for row in range(8):
            if show_coords:
                print(f"{8-row} | ", end="")
            else:
                print("| ", end="")
            
            for col in range(8):
                piece = self.board_state[row][col]
                symbol = piece if piece != '.' else '·'
                print(f"{symbol} ", end="")
            print("|")
        
        print("="*33)
        if show_coords:
            print("    a b c d e f g h")
        
        print(f"Ход: {'Белые' if self.current_turn else 'Черные'}")
        
        # Показываем оценку позиции
        if self.ai:
            eval_score = self.get_evaluation()
            eval_pawns = eval_score / 100
            print(f"Оценка: {eval_score:+d} ({eval_pawns:+.2f} пешек)")
        
        print()
    
    def undo_last_move(self) -> bool:
        """Отмена последнего хода"""
        if len(self.move_history) < 1:
            print("Нет ходов для отмены")
            return False
        
        # Для полной реализации нужно сохранять состояния
        # Это упрощённая версия - просто очищаем историю
        self.move_history.pop()
        print("⚠️ Внимание: полная отмена хода не реализована")
        print("Рекомендуется использовать save_game() / load_game()")
        return False
    
    def quick_test(self):
        """Быстрый тест движка"""
        print("\n🧪 БЫСТРЫЙ ТЕСТ ДВИЖКА")
        print("="*50)
        
        # Тест 1: Начальная позиция
        print("\n1. Начальная позиция:")
        self.print_board(show_coords=True)
        
        # Тест 2: Ход e2-e4
        print("\n2. Тестовый ход e2-e4:")
        success = self.make_move((6, 4), (4, 4), verbose=True)
        if success:
            self.print_board()
        
        # Тест 3: Оценка позиции
        print("\n3. Оценка позиции:")
        if self.ai:
            eval_score = self.get_evaluation()
            print(f"   Оценка: {eval_score:+d} ({eval_score/100:+.2f} пешек)")
        
        # Тест 4: Генерация лучшего хода
        print("\n4. Генерация лучшего хода AI:")
        best_move = self.get_best_move(depth=3)
        if best_move:
            from_pos, to_pos = best_move
            print(f"   Лучший ход: {from_pos} -> {to_pos}")
        
        # Тест 5: Статистика
        print("\n5. Статистика:")
        self.print_performance_report()
        
        print("✅ Тест завершён!\n")
    
    def print_performance_report(self):
        """Вывод отчёта о производительности"""
        print("\n" + "="*50)
        print("📊 ОТЧЁТ О ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*50)
        
        stats = self.get_game_statistics()
        
        print(f"\n🎮 Игровая статистика:")
        print(f"  Ходов сделано: {stats['moves_count']}")
        print(f"  Взятий: {stats['captures_count']}")
        print(f"  Шахов: {stats['check_count']}")
        
        print(f"\n💾 Кэширование:")
        print(f"  Попадания: {stats['cache_hits']}")
        print(f"  Промахи: {stats['cache_misses']}")
        hit_rate = stats['cache_hits'] / (stats['cache_hits'] + stats['cache_misses']) * 100 if (stats['cache_hits'] + stats['cache_misses']) > 0 else 0
        print(f"  Эффективность: {hit_rate:.1f}%")
        
        print(f"\n🧮 Размеры кэша:")
        for name, size in stats['cache_size'].items():
            print(f"  {name}: {size} записей")
        
        if 'ai_nodes' in stats:
            print(f"\n🤖 ИИ:")
            print(f"  Узлов проверено: {stats['ai_nodes']:,}")
            print(f"  Попаданий в TT: {stats['ai_tt_hits']:,}")
        
        print(f"\n⏱️  Время выполнения:")
        metrics = stats['performance_metrics']
        for name, value in metrics.items():
            print(f"  {name}: {value:.3f}с")
        
        print("="*50 + "\n")
    
    def _get_from_cache(self, cache: OrderedDict, key: str):
        """Получение с проверкой TTL и LRU"""
        if key in cache:
            # Проверяем TTL
            if key in self._cache_timestamps:
                age = time.time() - self._cache_timestamps[key]
                if age > self._cache_ttl:
                    del cache[key]
                    if key in self._cache_timestamps:
                        del self._cache_timestamps[key]
                    return None
            
            # Перемещаем в конец (LRU)
            cache.move_to_end(key)
            return cache[key]
        return None
    
    def _put_in_cache(self, cache: OrderedDict, key: str, value):
        """Сохранение с TTL и автоочисткой"""
        cache[key] = value
        self._cache_timestamps[key] = time.time()
        
        # Автоочистка при превышении лимита
        while len(cache) > self._cache_max_size:
            oldest_key = next(iter(cache))
            del cache[oldest_key]
            if oldest_key in self._cache_timestamps:
                del self._cache_timestamps[oldest_key]
    
    def _get_position_hash(self) -> int:
        """Генерация хэша текущей позиции с использованием Zobrist hashing"""
        hash_value = 0
        
        # XOR всех фигур на доске
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.':
                    square = row * 8 + col
                    hash_value ^= self.zobrist_keys['pieces'][piece][square]
        
        # XOR ключа очереди хода
        if self.current_turn:
            hash_value ^= self.zobrist_keys['turn']
        
        return hash_value
    
    def _clear_caches(self):
        """УЛУЧШЕНО: Интеллектуальная очистка кэша с TTL"""
        start_time = time.perf_counter()
        
        # OrderedDict автоматически управляет LRU через move_to_end
        # Автоочистка происходит в _put_in_cache, здесь просто проверяем TTL
        current_time = time.time()
        
        # Проверяем и удаляем просроченные записи
        for cache in [self._move_validation_cache, self._king_check_cache, self._legal_moves_cache]:
            expired_keys = []
            for key in list(cache.keys()):
                if key in self._cache_timestamps:
                    age = current_time - self._cache_timestamps[key]
                    if age > self._cache_ttl:
                        expired_keys.append(key)
            
            # Удаляем просроченные записи
            for key in expired_keys:
                if key in cache:
                    del cache[key]
                if key in self._cache_timestamps:
                    del self._cache_timestamps[key]
        
        self._performance_metrics['cache_cleanup_time'] += time.perf_counter() - start_time
    
    def invalidate_caches(self):
        """Принудительная инвалидация всех кэшей"""
        self._position_hash_cache.clear()
        self._move_validation_cache.clear()
        self._king_check_cache.clear()
        self._legal_moves_cache.clear()
        self._cache_timestamps.clear()
    
    def is_checkmate(self, is_white: bool) -> bool:
        """Эффективная проверка мата с кэшированием"""
        start_time = time.perf_counter()
        
        # Кэширование результата
        cache_key = f"{self._get_position_hash()}_checkmate_{is_white}"
        
        # НОВОЕ: Используем безопасный метод
        cached = self._get_from_cache(self._king_check_cache, cache_key)
        if cached is not None:
            self.game_stats['cache_hits'] += 1
            self._performance_metrics['checkmate_detection_time'] += time.perf_counter() - start_time
            return cached
        
        self.game_stats['cache_misses'] += 1
        
        # Если нет шаха, то и мата нет
        if not self.is_king_in_check(is_white):
            result = False
            self._put_in_cache(self._king_check_cache, cache_key, result)
            self._performance_metrics['checkmate_detection_time'] += time.perf_counter() - start_time
            return result
        
        # Проверяем, есть ли хоть один легальный ход
        if self.move_gen:
            try:
                legal_moves = self.move_gen.generate_legal_moves(self.board_state, is_white)
                result = len(legal_moves) == 0
                self._put_in_cache(self._king_check_cache, cache_key, result)
                self._performance_metrics['checkmate_detection_time'] += time.perf_counter() - start_time
                return result
            except Exception as e:
                print(f"Ошибка MoveGen в is_checkmate: {e}")
        
        # Резервная Python-реализация
        result = self._is_checkmate_python(is_white)
        self._put_in_cache(self._king_check_cache, cache_key, result)
        self._performance_metrics['checkmate_detection_time'] += time.perf_counter() - start_time
        
        # Очистка кэша при необходимости
        self._clear_caches()
        
        return result
    
    def _find_all_attackers(self, king_pos: Tuple[int, int], king_is_white: bool) -> List[Tuple[int, int]]:
        """НОВОЕ: Находит ВСЕ фигуры, атакующие короля"""
        attackers = []
        kr, kc = king_pos
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.isupper() != king_is_white:
                    if self.can_piece_attack((row, col), king_pos, piece):
                        attackers.append((row, col))
        
        return attackers
    
    def _is_checkmate_python(self, is_white: bool) -> bool:
        """УЛУЧШЕНО с проверкой двойного шаха"""
        if not self.is_king_in_check(is_white):
            return False
        
        cache_key = f"{self._get_position_hash()}_mate_{is_white}"
        cached = self._get_from_cache(self._king_check_cache, cache_key)
        if cached is not None:
            return cached
        
        king_pos = self.find_king(self.board_state, is_white)
        if not king_pos:
            return True
        
        # НОВОЕ: Проверка двойного шаха
        attackers = self._find_all_attackers(king_pos, is_white)
        is_double_check = len(attackers) > 1
        
        # 1. Проверяем ходы короля
        from_row, from_col = king_pos
        king_directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dr, dc in king_directions:
            to_row, to_col = from_row + dr, from_col + dc
            if 0 <= to_row < 8 and 0 <= to_col < 8:
                target = self.board_state[to_row][to_col]
                if target != '.' and (target.isupper() == is_white or target.lower() == 'k'):
                    continue
                
                # Симуляция хода
                original_piece = self.board_state[to_row][to_col]
                self.board_state[to_row][to_col] = 'K' if is_white else 'k'
                self.board_state[from_row][from_col] = '.'
                
                still_in_check = self.is_king_in_check(is_white)
                
                self.board_state[from_row][from_col] = 'K' if is_white else 'k'
                self.board_state[to_row][to_col] = original_piece
                
                if not still_in_check:
                    self._put_in_cache(self._king_check_cache, cache_key, False)
                    return False
        
        # НОВОЕ: При двойном шахе только король может спасти
        if is_double_check:
            self._put_in_cache(self._king_check_cache, cache_key, True)
            return True
        
        # 2. Одинарный шах - проверяем блокировку/взятие
        attacker_pos = attackers[0] if attackers else None
        if attacker_pos:
            attacker_piece = self.board_state[attacker_pos[0]][attacker_pos[1]]
            
            if self._can_capture_attacker(attacker_pos, is_white):
                self._put_in_cache(self._king_check_cache, cache_key, False)
                return False
            
            if attacker_piece.lower() in 'rbq':
                if self._can_block_attack(king_pos, attacker_pos, is_white):
                    self._put_in_cache(self._king_check_cache, cache_key, False)
                    return False
        
        self._put_in_cache(self._king_check_cache, cache_key, True)
        return True
    
    def is_stalemate(self, is_white: bool) -> bool:
        """Эффективная проверка пата"""
        # Если есть шах, то пата нет
        if self.is_king_in_check(is_white):
            return False
        
        # Проверяем, есть ли хоть один легальный ход
        if self.move_gen:
            try:
                legal_moves = self.move_gen.generate_legal_moves(self.board_state, is_white)
                return len(legal_moves) == 0
            except Exception as e:
                print(f"Ошибка MoveGen в is_stalemate: {e}")
        
        # Резервная Python-реализация
        return self._is_stalemate_python(is_white)
    
    def _is_stalemate_python(self, is_white: bool) -> bool:
        """Резервная Python-реализация проверки пата"""
        # Пат - когда король не под шахом, но нет легальных ходов
        original_turn = self.current_turn
        self.current_turn = is_white
        
        # Перебираем все фигуры текущего цвета
        for from_row in range(8):
            for from_col in range(8):
                piece = self.board_state[from_row][from_col]
                if piece == '.':
                    continue
                
                piece_is_white = piece.isupper()
                if piece_is_white != is_white:
                    continue
                
                # Проверяем все возможные ходы этой фигуры
                for to_row in range(8):
                    for to_col in range(8):
                        if (from_row, from_col) == (to_row, to_col):
                            continue
                        
                        # Проверяем, является ли ход допустимым
                        if self.is_valid_move_python((from_row, from_col), (to_row, to_col)):
                            # Проверяем, не подставит ли ход короля под шах
                            if not self.would_still_be_in_check((from_row, from_col), (to_row, to_col), is_white):
                                # Нашли легальный ход - не пат!
                                self.current_turn = original_turn
                                return False
        
        # Не нашли ни одного легального хода - это пат!
        self.current_turn = original_turn
        return True
    
    def get_game_status(self) -> str:
        """Получение статуса игры (продолжается, мат, пат, ничья)"""
        current_color = self.current_turn
        
        # Проверка мата
        if self.is_checkmate(current_color):
            winner = "Черные" if current_color else "Белые"
            return f"Мат! Победа: {winner}"
        
        # Проверка пата
        if self.is_stalemate(current_color):
            return "Пат! Ничья"
        
        # Проверка шаха
        if self.is_king_in_check(current_color):
            return "Шах!"
        
        return "Игра продолжается"
    
    def set_position(self, board_state: List[List[str]], current_turn: bool = True):
        """Установка позиции на доске"""
        self.board_state = [row[:] for row in board_state]  # Копируем
        self.current_turn = current_turn
        # Сбрасываем права рокировки (для тестовых позиций)
        self.castling_rights = {
            'white_kingside': False,
            'white_queenside': False,
            'black_kingside': False,
            'black_queenside': False
        }
    
    def board_to_fen(self) -> str:
        """Преобразование доски в FEN нотацию"""
        fen = ""
        for row in self.board_state:
            empty_count = 0
            for piece in row:
                if piece == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += piece
            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"
        fen = fen[:-1]  # Убираем последний слеш
        
        # Добавляем информацию о ходе
        fen += " w " if self.current_turn else " b "
        fen += "KQkq - 0 1"  # Права рокировки, en passant, счетчики
        return fen
    
    def get_evaluation(self) -> int:
        """Получение численной оценки текущей позиции"""
        if self.ai:
            return self.ai.evaluate_position(self.board_state)
        return 0

    def save_game(self, filename: str) -> bool:
        """Сохранение игры в JSON файл"""
        try:
            import json
            data = {
                'board_state': self.board_state,
                'current_turn': self.current_turn,
                'move_history': self.move_history,
                'captured_pieces': self.captured_pieces,
                'game_stats': self.game_stats
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False

    def load_game(self, filename: str) -> bool:
        """Загрузка игры из JSON файла"""
        try:
            import json
            if not os.path.exists(filename):
                return False
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.board_state = data['board_state']
            self.current_turn = data['current_turn']
            self.move_history = data.get('move_history', [])
            self.captured_pieces = data.get('captured_pieces', {'white': [], 'black': []})
            self.game_stats = data.get('game_stats', {'moves_count': 0, 'captures_count': 0, 'check_count': 0})
            
            # Сброс временных состояний
            self.selected_square = None
            self.valid_moves = []
            
            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False

    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка допустимости хода через оптимизированный движок, С++ или Python"""
        # Сначала пробуем BitboardMoveGenerator
        if self.move_gen:
            try:
                # Bitboard generator usually returns all legal moves, 
                # but we can use it to check a specific move
                legal_moves = self.move_gen.generate_legal_moves(self.board_state, self.current_turn)
                return (from_pos, to_pos) in legal_moves
            except Exception as e:
                print(f"Ошибка Bitboard MoveGen: {e}")
        
        # Резервные варианты
        try:
            return self.is_valid_move_cpp(from_pos, to_pos)
        except:
            return self.is_valid_move_python(from_pos, to_pos)
    
    def is_valid_move_cpp(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка хода через С++ движок"""
        if self.lib is None:
            raise Exception("С++ библиотека не загружена")
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        result = self.lib.is_valid_move(
            self.engine_ptr,
            from_row, from_col,
            to_row, to_col
        )
        return bool(result)
    
    def is_valid_move_python(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], debug: bool = False) -> bool:
        """Python реализация проверки хода с отладкой"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        target_piece = self.board_state[to_row][to_col]
        
        if debug:
            print(f"Проверка хода: {piece} с ({from_row},{from_col}) на ({to_row},{to_col})")
            print(f"Целевая клетка: '{target_piece}'")
        
        # Проверка цвета фигуры
        is_white_piece = piece.isupper()
        if debug:
            print(f"Белая фигура: {is_white_piece}, Очередь белых: {self.current_turn}")
        
        if (is_white_piece and not self.current_turn) or (not is_white_piece and self.current_turn):
            if debug:
                print("Неправильная очередь хода!")
            return False
            
        # Проверка выхода за границы
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            if debug:
                print("Выход за границы доски!")
            return False
            
        # Проверка на то же поле
        if from_pos == to_pos:
            if debug:
                print("Нельзя ходить на ту же клетку!")
            return False
            
        # Проверка, что нельзя съесть свою фигуру
        if target_piece != '.' and ((target_piece.isupper() and is_white_piece) or 
                                   (target_piece.islower() and not is_white_piece)):
            if debug:
                print("Нельзя съесть свою фигуру!")
            return False
            
        # Проверка, что нельзя съесть короля
        if target_piece.lower() == 'k':
            if debug:
                print("Нельзя съесть короля!")
            return False
            
        piece_type = piece.lower()
        if debug:
            print(f"Тип фигуры: {piece_type}")
        
        # Логика для пешки
        if piece_type == 'p':
            direction = -1 if is_white_piece else 1
            start_row = 6 if is_white_piece else 1
            if debug:
                print(f"Пешка: направление={direction}, начальная строка={start_row}")
            
            # Ход вперед на одну клетку
            if from_col == to_col and to_row == from_row + direction and target_piece == '.':
                if debug:
                    print("Допустимый ход пешки вперед")
                return True
                
            # Двойной ход с начальной позиции
            if (from_row == start_row and from_col == to_col and 
                to_row == from_row + 2 * direction and 
                target_piece == '.' and self.board_state[from_row + direction][from_col] == '.'):
                if debug:
                    print("Допустимый двойной ход пешки")
                return True
                
            # Взятие по диагонали
            if (abs(from_col - to_col) == 1 and to_row == from_row + direction and 
                target_piece != '.' and target_piece.isupper() != is_white_piece):
                if debug:
                    print("Допустимое взятие пешкой")
                return True
                
        # Логика для ладьи
        elif piece_type == 'r':
            result = self.is_straight_move(from_pos, to_pos)
            if debug:
                print(f"Ладья: прямой ход = {result}")
            return result
            
        # Логика для слона
        elif piece_type == 'b':
            result = self.is_diagonal_move(from_pos, to_pos)
            if debug:
                print(f"Слон: диагональный ход = {result}")
            return result
            
        # Логика для ферзя
        elif piece_type == 'q':
            straight = self.is_straight_move(from_pos, to_pos)
            diagonal = self.is_diagonal_move(from_pos, to_pos)
            result = straight or diagonal
            if debug:
                print(f"Ферзь: прямой={straight}, диагональный={diagonal}, результат={result}")
            return result
            
        # Логика для короля
        elif piece_type == 'k':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            if debug:
                print(f"Король: разница строк={row_diff}, столбцов={col_diff}")
            
            # Проверка рокировки
            if row_diff == 0 and col_diff == 2:
                return self.is_castling_valid(from_pos, to_pos, is_white_piece)
            
            # Король может ходить только на одну клетку
            if row_diff <= 1 and col_diff <= 1:
                # Проверяем, не попадает ли под атаку
                attacked = self.would_king_be_attacked(from_pos, to_pos, is_white_piece)
                if debug:
                    print(f"Король под атакой после хода: {attacked}")
                return not attacked
            
        # Логика для коня
        elif piece_type == 'n':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            result = (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
            if debug:
                print(f"Конь: разница строк={row_diff}, столбцов={col_diff}, результат={result}")
            return result
            
        if debug:
            print("Ход не соответствует правилам!")
        return False
    
    def is_straight_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка прямого хода (ладья, ферзь)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверка прямой линии
        if from_row != to_row and from_col != to_col:
            return False
        
        # Проверка пути
        if from_row == to_row:  # Горизонталь
            step = 1 if from_col < to_col else -1
            for col in range(from_col + step, to_col, step):
                if self.board_state[from_row][col] != '.':
                    return False
        else:  # Вертикаль
            step = 1 if from_row < to_row else -1
            for row in range(from_row + step, to_row, step):
                if self.board_state[row][from_col] != '.':
                    return False
        
        return True
    
    def is_diagonal_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка диагонального хода (слон, ферзь)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверка диагонали
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        
        # Проверка пути
        row_step = 1 if from_row < to_row else -1
        col_step = 1 if from_col < to_col else -1
        
        row, col = from_row + row_step, from_col + col_step
        while row != to_row and col != to_col:
            if self.board_state[row][col] != '.':
                return False
            row += row_step
            col += col_step
        
        return True
    
    def is_castling_valid(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool) -> bool:
        """Проверка возможности рокировки"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Определяем тип рокировки
        kingside = to_col > from_col
        color = 'white' if is_white else 'black'
        
        # Проверка прав на рокировку
        if kingside:
            if not self.castling_rights[f'{color}_kingside']:
                return False
            rook_col = 7
        else:
            if not self.castling_rights[f'{color}_queenside']:
                return False
            rook_col = 0
        
        # Проверка что король не под шахом
        if self.is_king_in_check(is_white):
            return False
        
        # Проверка пути (должен быть свободен)
        step = 1 if kingside else -1
        for col in range(from_col + step, to_col + step, step):
            if self.board_state[from_row][col] != '.':
                return False
            
            # Проверяем что король не проходит через атакованное поле
            if col != to_col + step:  # Не проверяем поле за королем
                if self.is_square_under_attack((from_row, col), not is_white):
                    return False
        
        # Проверка наличия ладьи
        rook_piece = 'R' if is_white else 'r'
        if self.board_state[from_row][rook_col] != rook_piece:
            return False
        
        return True
    
    def is_square_under_attack(self, square: Tuple[int, int], by_white: bool) -> bool:
        """Проверка атаки клетки"""
        target_row, target_col = square
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.isupper() == by_white:
                    # Проверяем может ли фигура атаковать клетку
                    if self.can_piece_attack((row, col), square, piece):
                        return True
        return False
    
    def can_piece_attack(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], piece: str) -> bool:
        """Проверяет может ли фигура атаковать клетку"""
        piece_type = piece.lower()
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if piece_type == 'p':
            direction = -1 if piece.isupper() else 1
            return abs(from_col - to_col) == 1 and to_row == from_row + direction
        elif piece_type == 'n':
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        elif piece_type == 'b':
            return self.is_diagonal_move(from_pos, to_pos)
        elif piece_type == 'r':
            return self.is_straight_move(from_pos, to_pos)
        elif piece_type == 'q':
            return self.is_straight_move(from_pos, to_pos) or self.is_diagonal_move(from_pos, to_pos)
        elif piece_type == 'k':
            return abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1
        return False
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], verbose: bool = False) -> bool:
        """Выполнение хода (verbose=True для отладки)"""
        if verbose:
            print(f"\n=== ПОПЫТКА ХОДА ===")
            print(f"Из: {from_pos}, В: {to_pos}")
            print(f"Очередь белых: {self.current_turn}")
        
        if not self.is_valid_move(from_pos, to_pos):
            if verbose:
                print("Ход НЕДОПУСТИМ!")
            return False
        
        if verbose:
            print("Ход ДОПУСТИМ!")
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board_state[from_row][from_col]
        captured = self.board_state[to_row][to_col]
        
        # Запись в историю
        move_notation = f"{piece}{chr(97+from_col)}{8-from_row}-{chr(97+to_col)}{8-to_row}"
        if captured != '.':
            move_notation += f"x{captured}"
            self.captured_pieces['white' if captured.isupper() else 'black'].append(captured)
            self.game_stats['captures_count'] += 1
        
        self.move_history.append(move_notation)
        self.game_stats['moves_count'] += 1
        
        if verbose:
            print(f"Фигура: {piece}, Захват: '{captured}'")
            print(f"Ход записан: {move_notation}")
            print("Выполняю ход...")
        
        # Выполнение хода
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        # Инвалидация кэша после хода
        self.invalidate_caches()
        
        if verbose:
            print("Ход выполнен успешно!")
        
        # Проверка шаха
        if self.is_king_in_check(not self.current_turn):
            self.game_stats['check_count'] += 1
            if verbose:
                print("ШАХ!")
        
        # Смена очереди
        self.current_turn = not self.current_turn
        
        if verbose:
            print(f"Очередь перешла: {'белым' if self.current_turn else 'черным'}")
        
        # Сброс выбора
        self.selected_square = None
        self.valid_moves = []
        
        # Проверка окончания игры
        if self.is_checkmate(self.current_turn):
            self.game_active = False
            if verbose:
                winner = "Черные" if self.current_turn else "Белые"
                print(f"МАТ! Победили {winner}")
        elif self.is_stalemate(self.current_turn):
            self.game_active = False
            if verbose:
                print("ПАТ! Ничья")
        
        if verbose:
            print("=== ХОД ЗАВЕРШЕН ===\n")
        
        return True
    
    def get_best_move(self, depth: int = 3) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Получение лучшего хода для AI с кэшированием и оптимизацией"""
        start_time = time.perf_counter()
        
        # Проверяем кэш для текущей позиции
        cache_key = f"{self._get_position_hash()}_bestmove_{depth}"
        if cache_key in self._legal_moves_cache:
            self.game_stats['cache_hits'] += 1
            cached_move = self._legal_moves_cache[cache_key]
            self._performance_metrics['ai_thinking_time'] += time.perf_counter() - start_time
            return cached_move
        
        self.game_stats['cache_misses'] += 1
        
        if self.ai:
            try:
                self.ai.search_depth = depth
                result = self.ai.get_best_move(self.board_state, self.current_turn)
                self._legal_moves_cache[cache_key] = result
                self._performance_metrics['ai_thinking_time'] += time.perf_counter() - start_time
                return result
            except Exception as e:
                print(f"Ошибка Enhanced AI: {e}")
        
        # Оптимизированный резервный вариант
        result = self._get_best_move_optimized(depth)
        self._legal_moves_cache[cache_key] = result
        self._performance_metrics['ai_thinking_time'] += time.perf_counter() - start_time
        self._clear_caches()
        
        return result
    
    def _get_best_move_optimized(self, depth: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """УЛУЧШЕНО: Приоритетная генерация ходов"""
        if self.ai:
            return self.ai.get_best_move(self.board_state, self.current_turn, time_limit=3.0)
        
        # Резервный вариант
        piece_values = {'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000}
        
        # НОВОЕ: Сначала генерируем все возможные ходы
        capture_moves = []
        tactical_moves = []  # Шахи, угрозы
        positional_moves = []
        
        ai_is_white = self.current_turn
        
        # Приоритетные клетки (центр + развитие)
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        extended_center = [(2, 2), (2, 3), (2, 4), (2, 5), 
                           (3, 2), (3, 5), (4, 2), (4, 5),
                           (5, 2), (5, 3), (5, 4), (5, 5)]
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece == '.' or piece.isupper() != ai_is_white:
                    continue
                
                piece_type = piece.lower()
                piece_value = piece_values.get(piece_type, 0)
                
                # Оптимизация: используем заранее известные направления
                if piece_type == 'n':  # Конь
                    knight_offsets = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
                    targets = [(row+dr, col+dc) for dr, dc in knight_offsets 
                              if 0 <= row+dr < 8 and 0 <= col+dc < 8]
                elif piece_type == 'k':  # Король
                    king_offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
                    targets = [(row+dr, col+dc) for dr, dc in king_offsets 
                              if 0 <= row+dr < 8 and 0 <= col+dc < 8]
                elif piece_type == 'p':  # Пешка
                    direction = -1 if ai_is_white else 1
                    targets = [(row+direction, col)]  # Вперёд
                    if (ai_is_white and row == 6) or (not ai_is_white and row == 1):
                        targets.append((row+2*direction, col))  # Двойной ход
                    # Взятия
                    for dc in [-1, 1]:
                        if 0 <= col+dc < 8:
                            targets.append((row+direction, col+dc))
                else:  # Скользящие фигуры - проверяем по направлениям
                    targets = []
                    directions = []
                    if piece_type in 'rq':
                        directions.extend([(0,1), (0,-1), (1,0), (-1,0)])
                    if piece_type in 'bq':
                        directions.extend([(1,1), (1,-1), (-1,1), (-1,-1)])
                    
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        while 0 <= r < 8 and 0 <= c < 8:
                            targets.append((r, c))
                            if self.board_state[r][c] != '.':
                                break  # Остановились на фигуре
                            r += dr
                            c += dc
                
                # Проверяем каждую целевую клетку
                for to_row, to_col in targets:
                    if not (0 <= to_row < 8 and 0 <= to_col < 8):
                        continue
                    
                    target = self.board_state[to_row][to_col]
                    if target != '.' and target.isupper() == ai_is_white:
                        continue  # Своя фигура
                    
                    # Быстрая валидация
                    if not self.is_valid_move_python((row, col), (to_row, to_col)):
                        continue
                    
                    if self.would_still_be_in_check((row, col), (to_row, to_col), ai_is_white):
                        continue
                    
                    move = ((row, col), (to_row, to_col))
                    
                    # Категоризация хода
                    if target != '.':  # Взятие
                        victim_value = piece_values.get(target.lower(), 0)
                        # MVV-LVA: Most Valuable Victim - Least Valuable Attacker
                        score = 10000 + victim_value * 10 - piece_value
                        capture_moves.append((score, move))
                    elif self._move_gives_check(move, ai_is_white):  # Шах
                        tactical_moves.append((100, move))
                    else:  # Позиционный ход
                        score = 0
                        if (to_row, to_col) in center_squares:
                            score += 50
                        elif (to_row, to_col) in extended_center:
                            score += 20
                        
                        # Развитие фигур в дебюте
                        if piece_type in 'nb' and ((ai_is_white and row == 7) or (not ai_is_white and row == 0)):
                            score += 30
                        
                        positional_moves.append((score, move))
        
        # Объединяем в порядке приоритета
        all_moves = sorted(capture_moves, reverse=True) + \
                    sorted(tactical_moves, reverse=True) + \
                    sorted(positional_moves, reverse=True)
        
        return all_moves[0][1] if all_moves else None
    
    def _move_gives_check(self, move: Tuple[Tuple[int, int], Tuple[int, int]], is_white: bool) -> bool:
        """Проверяет, даёт ли ход шах"""
        from_pos, to_pos = move
        
        # Симулируем ход
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        captured = self.board_state[to_row][to_col]
        
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        gives_check = self.is_king_in_check(not is_white)
        
        # Откатываем
        self.board_state[from_row][from_col] = piece
        self.board_state[to_row][to_col] = captured
        
        return gives_check
    
    def is_king_in_check(self, king_color: bool) -> bool:
        """Проверка, находится ли король под шахом"""
        # Находим положение короля
        king_piece = 'K' if king_color else 'k'
        king_pos = None
        
        for row in range(8):
            for col in range(8):
                if self.board_state[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
            
        # Проверяем, может ли какая-либо вражеская фигура атаковать короля
        opponent_color = not king_color
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and ((piece.isupper() and not king_color) or 
                                   (piece.islower() and king_color)):
                    # Временно меняем очередь хода для проверки
                    original_turn = self.current_turn
                    self.current_turn = opponent_color
                    if self.is_valid_attack((row, col), king_pos):
                        self.current_turn = original_turn
                        return True
                    self.current_turn = original_turn
        
        return False
    
    def would_still_be_in_check(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], king_color: bool) -> bool:
        """Проверка, будет ли король все еще под шахом после хода"""
        # Сохраняем текущее состояние
        original_board = [row[:] for row in self.board_state]
        original_turn = self.current_turn
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Делаем временный ход
        piece = self.board_state[from_row][from_col]
        captured = self.board_state[to_row][to_col]
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        # Проверяем шах
        in_check = self.is_king_in_check(king_color)
        
        # Восстанавливаем доску
        self.board_state[from_row][from_col] = piece
        self.board_state[to_row][to_col] = captured
        self.current_turn = original_turn
        
        return in_check
    
    def would_king_be_attacked(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], king_color: bool) -> bool:
        """Проверка, будет ли король атакован после хода"""
        # Сохраняем текущее состояние
        original_board = [row[:] for row in self.board_state]
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Делаем временный ход
        piece = self.board_state[from_row][from_col]
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = '.'
        
        # Находим положение короля
        king_piece = 'K' if king_color else 'k'
        king_pos = None
        for row in range(8):
            for col in range(8):
                if self.board_state[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            # Восстанавливаем доску
            self.board_state = original_board
            return False
        
        # Проверяем, может ли какая-либо вражеская фигура атаковать короля
        opponent_color = not king_color
        attacked = False
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and ((piece.isupper() and not king_color) or 
                                   (piece.islower() and king_color)):
                    # Временно меняем очередь хода для проверки
                    original_turn = self.current_turn
                    self.current_turn = opponent_color
                    if self.is_valid_attack((row, col), king_pos):
                        attacked = True
                        self.current_turn = original_turn
                        break
                    self.current_turn = original_turn
            if attacked:
                break
        
        # Восстанавливаем доску
        self.board_state = original_board
        return attacked
    
    def _find_attacker(self, king_pos: Tuple[int, int], king_is_white: bool) -> Optional[Tuple[int, int]]:
        """Находит фигуру, атакующую короля"""
        kr, kc = king_pos
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.isupper() != king_is_white:
                    if self.can_piece_attack((row, col), king_pos, piece):
                        return (row, col)
        return None
    
    def _can_capture_attacker(self, attacker_pos: Tuple[int, int], defender_is_white: bool) -> bool:
        """Может ли какая-то фигура взять атакующего?"""
        ar, ac = attacker_pos
        
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece != '.' and piece.isupper() == defender_is_white:
                    if piece.lower() == 'k':
                        continue  # Короля проверили выше
                    
                    if self.is_valid_move_python((row, col), attacker_pos):
                        # Проверяем, не оставляет ли это короля под шахом
                        original = self.board_state[ar][ac]
                        self.board_state[ar][ac] = piece
                        self.board_state[row][col] = '.'
                        
                        still_check = self.is_king_in_check(defender_is_white)
                        
                        self.board_state[row][col] = piece
                        self.board_state[ar][ac] = original
                        
                        if not still_check:
                            return True
        return False
    
    def _can_block_attack(self, king_pos: Tuple[int, int], attacker_pos: Tuple[int, int], 
                          defender_is_white: bool) -> bool:
        """Может ли какая-то фигура заблокировать атаку?"""
        kr, kc = king_pos
        ar, ac = attacker_pos
        
        # Находим все клетки между королём и атакующим
        dr = 0 if ar == kr else (1 if ar > kr else -1)
        dc = 0 if ac == kc else (1 if ac > kc else -1)
        
        r, c = kr + dr, kc + dc
        blocking_squares = []
        while (r, c) != (ar, ac):
            blocking_squares.append((r, c))
            r += dr
            c += dc
        
        # Проверяем, может ли какая-то фигура встать на блокирующую клетку
        for block_square in blocking_squares:
            for row in range(8):
                for col in range(8):
                    piece = self.board_state[row][col]
                    if piece != '.' and piece.isupper() == defender_is_white and piece.lower() != 'k':
                        if self.is_valid_move_python((row, col), block_square):
                            # Проверяем, работает ли блокировка
                            br, bc = block_square
                            original = self.board_state[br][bc]
                            self.board_state[br][bc] = piece
                            self.board_state[row][col] = '.'
                            
                            still_check = self.is_king_in_check(defender_is_white)
                            
                            self.board_state[row][col] = piece
                            self.board_state[br][bc] = original
                            
                            if not still_check:
                                return True
        return False
    
    def find_king(self, board: List[List[str]], is_white: bool) -> Optional[Tuple[int, int]]:
        """Быстрый поиск короля"""
        king_char = 'K' if is_white else 'k'
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_char:
                    return (row, col)
        return None
    
    def is_valid_attack(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка, может ли фигура атаковать позицию (без проверки цвета)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        piece_type = piece.lower()
        
        # Не может атаковать саму себя или пустую клетку
        if from_pos == to_pos:
            return False
            
        # Логика атаки для разных фигур
        if piece_type == 'p':  # Пешка
            direction = -1 if piece.isupper() else 1
            return (abs(from_col - to_col) == 1 and to_row == from_row + direction)
            
        elif piece_type == 'r':  # Ладья
            return self.is_straight_move(from_pos, to_pos)
            
        elif piece_type == 'b':  # Слон
            return self.is_diagonal_move(from_pos, to_pos)
            
        elif piece_type == 'q':  # Ферзь
            return self.is_straight_move(from_pos, to_pos) or self.is_diagonal_move(from_pos, to_pos)
            
        elif piece_type == 'k':  # Король
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return row_diff <= 1 and col_diff <= 1
            
        elif piece_type == 'n':  # Конь
            row_diff = abs(to_row - from_row)
            col_diff = abs(to_col - from_col)
            return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
            
        return False
    
    def generate_legal_moves_bitboard(self, is_white: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Оптимизированная генерация легальных ходов с использованием битбордов"""
        moves = []
        
        # Предвычисленные маски для быстрого поиска
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        # Оптимизация: сначала проверяем центральные клетки
        center_priority = [
            (3, 3), (3, 4), (4, 3), (4, 4),  # Центр
            (2, 2), (2, 5), (5, 2), (5, 5),  # Расширенный центр
            (1, 1), (1, 6), (6, 1), (6, 6)   # Второй уровень
        ]
        
        # Проверяем фигуры в порядке приоритета
        for row in range(8):
            for col in range(8):
                piece = self.board_state[row][col]
                if piece == '.' or piece.isupper() != is_white:
                    continue
                
                piece_type = piece.lower()
                from_pos = (row, col)
                
                # Генерируем ходы в зависимости от типа фигуры
                if piece_type == 'p':  # Пешка
                    moves.extend(self._generate_pawn_moves(from_pos, is_white))
                elif piece_type == 'n':  # Конь
                    for dr, dc in knight_moves:
                        to_row, to_col = row + dr, col + dc
                        if 0 <= to_row < 8 and 0 <= to_col < 8:
                            if self._is_valid_destination(from_pos, (to_row, to_col), is_white):
                                moves.append((from_pos, (to_row, to_col)))
                elif piece_type == 'k':  # Король
                    for dr, dc in king_moves:
                        to_row, to_col = row + dr, col + dc
                        if 0 <= to_row < 8 and 0 <= to_col < 8:
                            if self._is_valid_destination(from_pos, (to_row, to_col), is_white):
                                moves.append((from_pos, (to_row, to_col)))
                elif piece_type in ['r', 'b', 'q']:  # Скользящие фигуры
                    moves.extend(self._generate_sliding_moves(from_pos, piece_type, is_white))
        
        return moves
    
    def _generate_pawn_moves(self, from_pos: Tuple[int, int], is_white: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Генерация ходов пешки"""
        moves = []
        from_row, from_col = from_pos
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        
        # Одиночный ход вперед
        to_row = from_row + direction
        if 0 <= to_row < 8 and self.board_state[to_row][from_col] == '.':
            if self._is_valid_destination(from_pos, (to_row, from_col), is_white):
                moves.append((from_pos, (to_row, from_col)))
            
            # Двойной ход с начальной позиции
            if from_row == start_row:
                to_row_2 = from_row + 2 * direction
                if (0 <= to_row_2 < 8 and 
                    self.board_state[to_row_2][from_col] == '.' and 
                    self.board_state[to_row][from_col] == '.'):
                    if self._is_valid_destination(from_pos, (to_row_2, from_col), is_white):
                        moves.append((from_pos, (to_row_2, from_col)))
        
        # Взятия по диагонали
        for dc in [-1, 1]:
            to_col = from_col + dc
            to_row = from_row + direction
            if 0 <= to_row < 8 and 0 <= to_col < 8:
                target = self.board_state[to_row][to_col]
                if target != '.' and target.isupper() != is_white:
                    if self._is_valid_destination(from_pos, (to_row, to_col), is_white):
                        moves.append((from_pos, (to_row, to_col)))
        
        return moves
    
    def _generate_sliding_moves(self, from_pos: Tuple[int, int], piece_type: str, is_white: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Генерация ходов скользящих фигур (ладья, слон, ферзь)"""
        moves = []
        from_row, from_col = from_pos
        
        # Определяем направления движения
        directions = []
        if piece_type in ['r', 'q']:  # Ладья или ферзь
            directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
        if piece_type in ['b', 'q']:  # Слон или ферзь
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        
        # Проверяем каждое направление
        for dr, dc in directions:
            to_row, to_col = from_row + dr, from_col + dc
            while 0 <= to_row < 8 and 0 <= to_col < 8:
                target = self.board_state[to_row][to_col]
                # Пустая клетка - можно двигаться дальше
                if target == '.':
                    if self._is_valid_destination(from_pos, (to_row, to_col), is_white):
                        moves.append((from_pos, (to_row, to_col)))
                # Вражеская фигура - можно взять, но не двигаться дальше
                elif target.isupper() != is_white:
                    if self._is_valid_destination(from_pos, (to_row, to_col), is_white):
                        moves.append((from_pos, (to_row, to_col)))
                    break
                # Своя фигура - нельзя двигаться дальше
                else:
                    break
                to_row += dr
                to_col += dc
        
        return moves
    
    def _is_valid_destination(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white: bool) -> bool:
        """Проверка, является ли клетка назначения допустимой"""
        # Проверяем базовую валидность хода
        if not self.is_valid_move_python(from_pos, to_pos):
            return False
        
        # Проверяем, не подставляет ли ход короля под шах
        return not self.would_still_be_in_check(from_pos, to_pos, is_white)


# Глобальный экземпляр движка
chess_engine = ChessEngineWrapper()