#!/usr/bin/env python3
"""
Оптимизированная многопоточная интеграция Stockfish для Pygame
"""

import threading
import queue
import time
from typing import Optional, Dict, Any
from stockfish_integration import StockfishIntegration

class AsyncStockfish:
    """Асинхронная многопоточная интеграция Stockfish для Pygame"""
    
    def __init__(self, threads: int = 8, hash_size: int = 4096):
        self.stockfish = StockfishIntegration(threads=threads, hash_size=hash_size)
        self.is_ready = False
        self.result_queue = queue.Queue()
        self.analysis_thread = None
        self.current_fen = None
        
    def initialize(self) -> bool:
        """Асинхронная инициализация Stockfish"""
        def init_worker():
            try:
                success = self.stockfish.start_engine()
                self.result_queue.put(("init", success))
                if success:
                    self.is_ready = True
            except Exception as e:
                self.result_queue.put(("init_error", str(e)))
        
        self.analysis_thread = threading.Thread(target=init_worker, daemon=True)
        self.analysis_thread.start()
        return True
    
    def get_best_move_async(self, fen: str, depth: int = 16, movetime: int = 1000):
        """Асинхронное получение лучшего хода"""
        if not self.is_ready:
            return None
            
        def move_worker():
            try:
                move = self.stockfish.get_best_move(fen, depth, movetime)
                self.result_queue.put(("move", move, fen))
            except Exception as e:
                self.result_queue.put(("move_error", str(e), fen))
        
        thread = threading.Thread(target=move_worker, daemon=True)
        thread.start()
        self.current_fen = fen
        return True
    
    def analyze_position_async(self, fen: str, depth: int = 16, multipv: int = 3):
        """Асинхронный анализ позиции"""
        if not self.is_ready:
            return None
            
        def analysis_worker():
            try:
                analysis = self.stockfish.analyze_position(fen, depth, multipv)
                self.result_queue.put(("analysis", analysis, fen))
            except Exception as e:
                self.result_queue.put(("analysis_error", str(e), fen))
        
        thread = threading.Thread(target=analysis_worker, daemon=True)
        thread.start()
        return True
    
    def get_results(self) -> tuple:
        """Получение результатов из очереди"""
        try:
            if not self.result_queue.empty():
                return self.result_queue.get_nowait()
        except queue.Empty:
            pass
        return None
    
    def shutdown(self):
        """Корректное завершение работы"""
        self.is_ready = False
        if self.stockfish:
            self.stockfish.stop_engine()

class PygameStockfishOptimizer:
    """Оптимизатор Stockfish для Pygame интерфейса"""
    
    def __init__(self):
        # Настройки для максимальной производительности в Pygame
        self.async_stockfish = AsyncStockfish(threads=8, hash_size=4096)
        self.cache = {}  # Кэш для быстрого доступа к часто используемым позициям
        self.last_analysis = {}
        self.performance_stats = {
            "moves_calculated": 0,
            "analyses_performed": 0,
            "avg_response_time": 0,
            "cache_hits": 0
        }
        
    def start_optimized_engine(self) -> bool:
        """Запуск оптимизированного движка"""
        print("🚀 Запуск оптимизированного Stockfish для Pygame...")
        return self.async_stockfish.initialize()
    
    def get_move_with_timeout(self, fen: str, max_wait_time: float = 2.0) -> Optional[str]:
        """
        Получение хода с таймаутом для отзывчивости интерфейса
        
        Args:
            fen: FEN позиция
            max_wait_time: Максимальное время ожидания в секундах
            
        Returns:
            Ход или None если превышен таймаут
        """
        start_time = time.time()
        
        # Проверяем кэш
        if fen in self.cache:
            self.performance_stats["cache_hits"] += 1
            return self.cache[fen]["move"]
        
        # Запускаем асинхронный запрос
        self.async_stockfish.get_best_move_async(fen, depth=14, movetime=800)
        
        # Ждем результат с таймаутом
        while time.time() - start_time < max_wait_time:
            result = self.async_stockfish.get_results()
            if result and result[0] == "move" and result[2] == fen:
                move = result[1]
                if move:
                    # Сохраняем в кэш
                    self.cache[fen] = {
                        "move": move,
                        "timestamp": time.time(),
                        "analysis": None
                    }
                    self.performance_stats["moves_calculated"] += 1
                    return move
            time.sleep(0.01)  # Небольшая пауза для снижения нагрузки CPU
        
        return None  # Таймаут
    
    def get_detailed_analysis(self, fen: str, depth: int = 16) -> Dict[str, Any]:
        """Получение подробного анализа позиции"""
        # Проверяем кэш анализа
        cache_key = f"{fen}_{depth}"
        if cache_key in self.cache and self.cache[cache_key].get("analysis"):
            self.performance_stats["cache_hits"] += 1
            return self.cache[cache_key]["analysis"]
        
        # Запускаем асинхронный анализ
        self.async_stockfish.analyze_position_async(fen, depth, multipv=3)
        
        # Ждем немного для получения быстрого анализа
        time.sleep(0.5)
        
        result = self.async_stockfish.get_results()
        if result and result[0] == "analysis" and result[2] == fen:
            analysis = result[1]
            if analysis:
                # Сохраняем в кэш
                self.cache[cache_key] = {
                    "analysis": analysis,
                    "timestamp": time.time()
                }
                self.performance_stats["analyses_performed"] += 1
                return analysis
        
        return {}
    
    def cleanup_cache(self, max_age: int = 300):
        """Очистка старых записей в кэше"""
        current_time = time.time()
        keys_to_remove = []
        
        for key, value in self.cache.items():
            if current_time - value.get("timestamp", 0) > max_age:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.cache[key]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Получение статистики производительности"""
        return self.performance_stats.copy()
    
    def shutdown(self):
        """Корректное завершение работы"""
        self.async_stockfish.shutdown()
        print("✅ Stockfish оптимизатор остановлен")

# Демонстрация оптимизированной интеграции
def demonstrate_optimized_integration():
    """Демонстрация оптимизированной многопоточной интеграции"""
    print("=== ОПТИМИЗИРОВАННАЯ ИНТЕГРАЦИЯ STOCKFISH ДЛЯ PYGAME ===")
    print("Многопоточная обработка с асинхронными вызовами\n")
    
    optimizer = PygameStockfishOptimizer()
    
    # Запуск оптимизированного движка
    if not optimizer.start_optimized_engine():
        print("❌ Не удалось запустить оптимизированный Stockfish")
        return
    
    print("✅ Оптимизированный Stockfish запущен")
    print("📊 Параметры:")
    print("   Потоки CPU: 8")
    print("   Хэш-таблица: 4096 MB")
    print("   Асинхронная обработка: ВКЛ")
    print("   Кэширование: ВКЛ")
    
    # Тестовая позиция
    test_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    print(f"\nТестовая позиция: {test_fen}")
    
    # Получаем ход с таймаутом
    print("Получение хода с таймаутом 1.5 секунды...")
    move = optimizer.get_move_with_timeout(test_fen, max_wait_time=1.5)
    
    if move:
        print(f"✅ Лучший ход: {move}")
    else:
        print("⏳ Таймаут - ход еще рассчитывается")
    
    # Подробный анализ
    print("\nПодробный анализ позиции...")
    analysis = optimizer.get_detailed_analysis(test_fen, depth=14)
    
    if analysis:
        print("✅ Анализ получен:")
        print(f"   Оценка: {analysis.get('score', 'N/A')}")
        print(f"   Глубина: {analysis.get('depth', 0)}")
        print(f"   Узлы: {analysis.get('nodes', 0):,}")
        print(f"   NPS: {analysis.get('nps', 0):,}")
        if analysis.get('pv'):
            print(f"   Главная линия: {' '.join(analysis['pv'][:3])}")
    
    # Статистика производительности
    stats = optimizer.get_performance_stats()
    print(f"\n📈 Статистика производительности:")
    print(f"   Рассчитано ходов: {stats['moves_calculated']}")
    print(f"   Выполнено анализов: {stats['analyses_performed']}")
    print(f"   Попаданий в кэш: {stats['cache_hits']}")
    
    # Завершение
    optimizer.shutdown()
    print("\n🎉 Оптимизированная интеграция готова к использованию в Pygame!")

if __name__ == "__main__":
    try:
        demonstrate_optimized_integration()
        print("\n\nНажмите Enter для завершения...")
        input()
    except KeyboardInterrupt:
        print("\n\nДемонстрация прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")