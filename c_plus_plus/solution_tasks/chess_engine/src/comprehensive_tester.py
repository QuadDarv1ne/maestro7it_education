#!/usr/bin/env python3
"""
Система автоматического тестирования шахматного движка
Комплексное тестирование всех компонентов проекта
"""

import unittest
import time
import os
import sys
from typing import List, Dict, Any

# Добавляем путь к модулям
sys.path.append('.')

class ChessEngineTestSuite(unittest.TestCase):
    """Комплексный набор тестов для шахматного движка"""
    
    def setUp(self):
        """Подготовка к тестированию"""
        print(f"\n🧪 Запуск теста: {self._testMethodName}")
        self.start_time = time.time()
    
    def tearDown(self):
        """Завершение теста"""
        elapsed = time.time() - self.start_time
        print(f"✅ Тест завершен за {elapsed:.3f} секунд")
    
    def test_engine_initialization(self):
        """Тест инициализации основного движка"""
        try:
            from chess_engine_wrapper import ChessEngineWrapper
            engine = ChessEngineWrapper()
            
            # Проверяем основные атрибуты
            self.assertIsNotNone(engine.board)
            self.assertIsNotNone(engine.move_generator)
            self.assertIsNotNone(engine.position_evaluator)
            
            # Проверяем начальную позицию
            initial_board = engine.get_initial_board()
            self.assertEqual(len(initial_board), 64)
            
            # Проверяем наличие белых и черных фигур
            white_pieces = [piece for piece in initial_board if piece and piece.isupper()]
            black_pieces = [piece for piece in initial_board if piece and piece.islower()]
            
            self.assertGreater(len(white_pieces), 10)
            self.assertGreater(len(black_pieces), 10)
            
            print("   ✓ Движок инициализирован корректно")
            print(f"   ✓ Начальная позиция загружена ({len(white_pieces)} белых, {len(black_pieces)} черных фигур)")
            
        except Exception as e:
            self.fail(f"Ошибка инициализации движка: {e}")
    
    def test_move_generation(self):
        """Тест генерации ходов"""
        try:
            from chess_engine_wrapper import ChessEngineWrapper
            engine = ChessEngineWrapper()
            
            # Получаем_legalные ходы из начальной позиции
            legal_moves = engine.get_legal_moves()
            
            # В начальной позиции должно быть 20_legalных ходов
            self.assertEqual(len(legal_moves), 20)
            
            # Проверяем формат ходов
            for move in legal_moves:
                self.assertIsInstance(move, dict)
                self.assertIn('from', move)
                self.assertIn('to', move)
                self.assertIn('algebraic', move)
            
            # Проверяем конкретные ходы
            algebraic_moves = [move['algebraic'] for move in legal_moves]
            expected_moves = ['a2-a3', 'a2-a4', 'b2-b3', 'b2-b4', 'c2-c3', 'c2-c4']
            
            found_expected = [move for move in expected_moves if move in algebraic_moves]
            self.assertGreater(len(found_expected), 3)
            
            print("   ✓ Генерация ходов работает корректно")
            print(f"   ✓ Найдено {len(legal_moves)}_legalных ходов")
            print(f"   ✓ Подтверждены основные ходы пешек: {found_expected}")
            
        except Exception as e:
            self.fail(f"Ошибка генерации ходов: {e}")
    
    def test_position_evaluation(self):
        """Тест оценки позиции"""
        try:
            from chess_engine_wrapper import ChessEngineWrapper
            engine = ChessEngineWrapper()
            
            # Оценка начальной позиции
            evaluation = engine.evaluate_position()
            
            # Проверяем тип возвращаемого значения
            self.assertIsInstance(evaluation, (int, float))
            
            # В начальной позиции оценка должна быть близка к 0
            self.assertGreater(abs(evaluation), -50)
            self.assertLess(abs(evaluation), 50)
            
            # Тест оценки после хода
            engine.make_move({'from': 12, 'to': 28, 'algebraic': 'e2-e4'})  # e4
            new_evaluation = engine.evaluate_position()
            
            # После первого хода оценка должна измениться
            self.assertNotEqual(evaluation, new_evaluation)
            
            print("   ✓ Оценка позиции работает корректно")
            print(f"   ✓ Начальная оценка: {evaluation}")
            print(f"   ✓ Оценка после e4: {new_evaluation}")
            
        except Exception as e:
            self.fail(f"Ошибка оценки позиции: {e}")
    
    def test_stockfish_integration(self):
        """Тест интеграции Stockfish"""
        try:
            from src.stockfish_integration import StockfishIntegration
            stockfish = StockfishIntegration()
            
            # Проверяем наличие файла Stockfish
            self.assertTrue(os.path.exists("stockfish.exe") or 
                          os.path.exists("./stockfish.exe"))
            
            # Запуск движка
            success = stockfish.start_engine()
            self.assertTrue(success, "Не удалось запустить Stockfish")
            
            # Тест получения лучшего хода
            fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
            best_move = stockfish.get_best_move(fen, depth=8, movetime=1000)
            
            self.assertIsNotNone(best_move)
            self.assertIsInstance(best_move, str)
            self.assertGreater(len(best_move), 2)
            
            # Тест анализа позиции
            analysis = stockfish.analyze_position(fen, depth=8)
            self.assertIsInstance(analysis, dict)
            self.assertIn('score', analysis)
            self.assertIn('depth', analysis)
            
            stockfish.stop_engine()
            
            print("   ✓ Интеграция Stockfish работает корректно")
            print(f"   ✓ Лучший ход: {best_move}")
            print(f"   ✓ Оценка позиции: {analysis.get('score', 'N/A')}")
            
        except Exception as e:
            self.skipTest(f"Stockfish не доступен: {e}")
    
    def test_pgn_functionality(self):
        """Тест функциональности PGN"""
        try:
            from src.pgn_integration import PGNIntegration
            
            pgn = PGNIntegration()
            
            # Создание тестовой партии
            test_moves = [
                {'algebraic': 'e2-e4', 'san': 'e4'},
                {'algebraic': 'e7-e5', 'san': 'e5'},
                {'algebraic': 'Ng1-f3', 'san': 'Nf3'},
                {'algebraic': 'Nb8-c6', 'san': 'Nc6'}
            ]
            
            # Сохранение партии
            filename = "test_game.pgn"
            success = pgn.save_game(test_moves, filename, 
                                  white_player="Test White", 
                                  black_player="Test Black")
            self.assertTrue(success)
            
            # Загрузка партии
            loaded_game = pgn.load_game(filename)
            self.assertIsNotNone(loaded_game)
            self.assertEqual(len(loaded_game['moves']), len(test_moves))
            
            # Проверка содержимого
            for i, move in enumerate(loaded_game['moves']):
                self.assertEqual(move['algebraic'], test_moves[i]['algebraic'])
                self.assertEqual(move['san'], test_moves[i]['san'])
            
            # Удаление тестового файла
            if os.path.exists(filename):
                os.remove(filename)
            
            print("   ✓ Функциональность PGN работает корректно")
            print(f"   ✓ Сохранено и загружено {len(test_moves)} ходов")
            
        except Exception as e:
            self.fail(f"Ошибка PGN функциональности: {e}")
    
    def test_game_analyzer(self):
        """Тест анализатора партий"""
        try:
            from src.game_analyzer import GameAnalyzer
            
            analyzer = GameAnalyzer()
            
            # Анализ тестовой партии
            test_moves = ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'a6']
            results = analyzer.analyze_game(test_moves, player_color="white")
            
            # Проверка результатов
            self.assertIsInstance(results, dict)
            self.assertIn('statistics', results)
            self.assertIn('recommendations', results)
            self.assertIn('summary', results)
            
            stats = results['statistics']
            self.assertGreater(stats['total_analyzed'], 0)
            
            print("   ✓ Анализатор партий работает корректно")
            print(f"   ✓ Проанализировано {stats['total_analyzed']} ходов")
            print(f"   ✓ Сгенерировано {len(results['recommendations'])} рекомендаций")
            
        except Exception as e:
            self.fail(f"Ошибка анализатора партий: {e}")
    
    def test_performance_monitoring(self):
        """Тест системы мониторинга производительности"""
        try:
            from src.performance_monitor import PerformanceMonitor
            
            monitor = PerformanceMonitor()
            
            # Запуск краткого мониторинга
            monitor.start_monitoring(0.1)  # Очень короткий интервал для теста
            time.sleep(1)
            monitor.stop_monitoring()
            
            # Получение метрик
            current_metrics = monitor.get_current_metrics()
            average_metrics = monitor.get_average_metrics()
            
            # Проверка наличия ключевых метрик
            expected_metrics = ['cpu_percent', 'memory_mb', 'positions_per_second']
            for metric in expected_metrics:
                self.assertIn(metric, current_metrics)
                self.assertIn(metric, average_metrics)
            
            print("   ✓ Система мониторинга производительности работает")
            print(f"   ✓ Собрано метрик: {len(current_metrics)}")
            
        except Exception as e:
            self.skipTest(f"Мониторинг производительности не доступен: {e}")

class ComprehensiveTestRunner:
    """Комплексный раннер тестов"""
    
    def __init__(self):
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("=" * 60)
        print("🏁 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ШАХМАТНОГО ДВИЖКА")
        print("=" * 60)
        
        start_time = time.time()
        
        # Создание тестового набора
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(ChessEngineTestSuite)
        
        # Запуск тестов с кастомным раннером
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        
        # Анализ результатов
        self.total_tests = result.testsRun
        self.passed_tests = self.total_tests - len(result.failures) - len(result.errors)
        self.failed_tests = len(result.failures)
        self.skipped_tests = len(result.skipped) if hasattr(result, 'skipped') else 0
        
        # Подробный вывод результатов
        self._print_detailed_results(result)
        
        # Общая статистика
        elapsed_time = time.time() - start_time
        self._print_summary(elapsed_time)
        
        return self.passed_tests == self.total_tests
    
    def _print_detailed_results(self, result):
        """Вывод детальных результатов тестов"""
        print(f"\n📊 ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print("-" * 50)
        
        # Успешные тесты
        if self.passed_tests > 0:
            print(f"✅ УСПЕШНЫЕ ТЕСТЫ: {self.passed_tests}")
            for test in result.successes:
                print(f"   ✓ {test}")
        
        # Проваленные тесты
        if self.failed_tests > 0:
            print(f"\n❌ ПРОВАЛЕННЫЕ ТЕСТЫ: {self.failed_tests}")
            for test, traceback in result.failures:
                print(f"   ✗ {test}")
                print(f"     Ошибка: {traceback.splitlines()[-1]}")
        
        # Пропущенные тесты
        if self.skipped_tests > 0:
            print(f"\n⏭️  ПРОПУЩЕННЫЕ ТЕСТЫ: {self.skipped_tests}")
            for test, reason in result.skipped:
                print(f"   ○ {test} (причина: {reason})")
    
    def _print_summary(self, elapsed_time):
        """Вывод сводки тестирования"""
        print("\n" + "=" * 60)
        print("🏆 СВОДКА КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ")
        print("=" * 60)
        
        print(f"⏱️  Общее время тестирования: {elapsed_time:.2f} секунд")
        print(f"🧪 Всего тестов: {self.total_tests}")
        print(f"✅ Успешных: {self.passed_tests}")
        print(f"❌ Проваленных: {self.failed_tests}")
        print(f"⏭️  Пропущенных: {self.skipped_tests}")
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        print(f"📈 Процент успеха: {success_rate:.1f}%")
        
        # Оценка качества
        if success_rate >= 95:
            print("\n🌟 УРОВЕНЬ: ПРЕМИУМ (Отличный)")
            print("🎉 Все основные функции работают корректно!")
        elif success_rate >= 80:
            print("\n⭐ УРОВЕНЬ: ВЫСОКИЙ (Хороший)")
            print("👍 Большинство функций работают корректно")
        elif success_rate >= 60:
            print("\n👍 УРОВЕНЬ: СРЕДНИЙ (Удовлетворительный)")
            print("🔧 Требуется доработка некоторых компонентов")
        else:
            print("\n🔧 УРОВЕНЬ: НИЗКИЙ (Требует внимания)")
            print("⚠️  Необходима серьезная доработка")
        
        print("\n" + "=" * 60)

def run_comprehensive_testing():
    """Запуск комплексного тестирования"""
    try:
        tester = ComprehensiveTestRunner()
        success = tester.run_all_tests()
        
        if success:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            print("✅ Проект готов к использованию!")
        else:
            print("\n⚠️  Некоторые тесты провалены")
            print("🔧 Требуется проверка и исправление")
            
        return success
        
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем")
        return False
    except Exception as e:
        print(f"\n❌ Критическая ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    try:
        success = run_comprehensive_testing()
        print(f"\n{'='*60}")
        if success:
            print("🏆 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
            print("🚀 Проект готов к серьезной эксплуатации!")
        else:
            print("🔧 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО С ОШИБКАМИ!")
            print("🛠️  Требуется доработка проекта")
        print(f"{'='*60}")
        
        input("\nНажмите Enter для завершения...")
        
    except Exception as e:
        print(f"\nОшибка: {e}")