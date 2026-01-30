/**
 * @file enhanced_evaluator_test.cpp
 * @brief Тестирование расширенного оценщика позиции
 * 
 * Демонстрирует работу EnhancedPositionEvaluator с различными режимами
 * оценки и продвинутыми функциями анализа.
 */

#include "../include/board.hpp"
#include "../include/bitboard.hpp"
#include "../include/enhanced_evaluator.hpp"
#include "../include/neural_evaluator.hpp"
#include "../include/incremental_evaluator.hpp"
#include <iostream>
#include <chrono>
#include <iomanip>

class EnhancedEvaluatorTest {
private:
    Bitboard board_;

public:
    EnhancedEvaluatorTest() {
        board_.setupStartPosition();
    }
    
    void runAllTests() {
        std::cout << "=== ТЕСТИРОВАНИЕ РАСШИРЕННОГО ОЦЕНЩИКА ===" << std::endl;
        
        testBasicFunctionality();
        testDifferentModes();
        testPerformanceComparison();
        testTacticalAnalysis();
        testEndgameFeatures();
        testAdaptiveWeights();
        
        std::cout << "\n=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===" << std::endl;
    }
    
private:
    void testBasicFunctionality() {
        std::cout << "\n1. БАЗОВАЯ ФУНКЦИОНАЛЬНОСТЬ" << std::endl;
        std::cout << "============================" << std::endl;
        
        EnhancedPositionEvaluator evaluator(board_);
        
        std::cout << "Начальная позиция:" << std::endl;
        board_.print();
        
        std::cout << "\nОценки в разных режимах:" << std::endl;
        std::cout << "Быстрая оценка:     " << evaluator.evaluate(EnhancedPositionEvaluator::FAST_MODE) << std::endl;
        std::cout << "Точная оценка:      " << evaluator.evaluate(EnhancedPositionEvaluator::ACCURATE_MODE) << std::endl;
        std::cout << "Тактическая оценка: " << evaluator.evaluate(EnhancedPositionEvaluator::TACTICAL_MODE) << std::endl;
        
        evaluator.printDetailedAnalysis();
    }
    
    void testDifferentModes() {
        std::cout << "\n2. СРАВНЕНИЕ РЕЖИМОВ ОЦЕНКИ" << std::endl;
        std::cout << "===========================" << std::endl;
        
        // Создаем несколько позиций для тестирования
        std::vector<std::string> test_positions = {
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  // Начальная
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3", // Итальянская партия
            "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 4 5" // Сицилианская защита
        };
        
        for (size_t i = 0; i < test_positions.size(); i++) {
            std::cout << "\nПозиция " << (i + 1) << ":" << std::endl;
            board_.setupFromFen(test_positions[i]);
            board_.print();
            
            EnhancedPositionEvaluator evaluator(board_);
            
            int fast_eval = evaluator.evaluate(EnhancedPositionEvaluator::FAST_MODE);
            int accurate_eval = evaluator.evaluate(EnhancedPositionEvaluator::ACCURATE_MODE);
            int tactical_eval = evaluator.evaluate(EnhancedPositionEvaluator::TACTICAL_MODE);
            
            std::cout << "Быстрая: " << std::setw(6) << fast_eval 
                      << " | Точная: " << std::setw(6) << accurate_eval
                      << " | Тактическая: " << std::setw(6) << tactical_eval << std::endl;
        }
    }
    
    void testPerformanceComparison() {
        std::cout << "\n3. СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ" << std::endl;
        std::cout << "================================" << std::endl;
        
        const int iterations = 10000;
        
        // Тестируем EnhancedPositionEvaluator
        auto start = std::chrono::high_resolution_clock::now();
        
        for (int i = 0; i < iterations; i++) {
            EnhancedPositionEvaluator evaluator(board_);
            volatile int score = evaluator.evaluate(EnhancedPositionEvaluator::FAST_MODE);
            (void)score;
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto enhanced_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        // Тестируем NeuralEvaluator для сравнения
        start = std::chrono::high_resolution_clock::now();
        
        for (int i = 0; i < iterations; i++) {
            NeuralEvaluator neural_eval(board_);
            volatile int score = neural_eval.evaluate();
            (void)score;
        }
        
        end = std::chrono::high_resolution_clock::now();
        auto neural_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        // Тестируем IncrementalEvaluator для сравнения
        start = std::chrono::high_resolution_clock::now();
        
        for (int i = 0; i < iterations; i++) {
            IncrementalEvaluator inc_eval(board_);
            volatile int score = inc_eval.evaluate();
            (void)score;
        }
        
        end = std::chrono::high_resolution_clock::now();
        auto incremental_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        std::cout << "Результаты (" << iterations << " итераций):" << std::endl;
        std::cout << "Enhanced Evaluator (FAST):    " << enhanced_duration.count() << " мкс" << std::endl;
        std::cout << "Neural Evaluator:             " << neural_duration.count() << " мкс" << std::endl;
        std::cout << "Incremental Evaluator:        " << incremental_duration.count() << " мкс" << std::endl;
        
        double enhanced_avg = static_cast<double>(enhanced_duration.count()) / iterations;
        double neural_avg = static_cast<double>(neural_duration.count()) / iterations;
        double incremental_avg = static_cast<double>(incremental_duration.count()) / iterations;
        
        std::cout << "\nСреднее время на оценку:" << std::endl;
        std::cout << "Enhanced:    " << std::fixed << std::setprecision(3) << enhanced_avg << " мкс" << std::endl;
        std::cout << "Neural:      " << neural_avg << " мкс" << std::endl;
        std::cout << "Incremental: " << incremental_avg << " мкс" << std::endl;
        
        std::cout << "\nУскорение относительно Neural:" << std::endl;
        std::cout << "Enhanced: " << std::fixed << std::setprecision(2) 
                  << (neural_avg / enhanced_avg) << "x быстрее" << std::endl;
    }
    
    void testTacticalAnalysis() {
        std::cout << "\n4. ТАКТИЧЕСКИЙ АНАЛИЗ" << std::endl;
        std::cout << "=====================" << std::endl;
        
        // Позиция с тактическими возможностями
        std::string tactical_fen = "r1bq1rk1/pp2bppp/2n1pn2/2pp4/3P1B2/2PBPN2/PP3PPP/RN1Q1RK1 w - - 0 10";
        board_.setupFromFen(tactical_fen);
        
        std::cout << "Тактическая позиция:" << std::endl;
        board_.print();
        
        EnhancedPositionEvaluator evaluator(board_);
        evaluator.printDetailedAnalysis();
        
        auto tactical_features = evaluator.getTacticalFeatures();
        auto endgame_features = evaluator.getEndgameFeatures();
        
        std::cout << "\nАнализ особенностей:" << std::endl;
        std::cout << "Общая тактическая активность: " 
                  << (tactical_features.pins + tactical_features.forks + tactical_features.threats) << std::endl;
        std::cout << "Эндшпиль: " << (endgame_features.is_endgame ? "Да" : "Нет") << std::endl;
    }
    
    void testEndgameFeatures() {
        std::cout << "\n5. ЭНДШПИЛЬНЫЕ ОСОБЕННОСТИ" << std::endl;
        std::cout << "==========================" << std::endl;
        
        // Эндшпильная позиция
        std::string endgame_fen = "8/8/4k3/8/4K3/8/8/8 w - - 0 1";
        board_.setupFromFen(endgame_fen);
        
        std::cout << "Эндшпильная позиция:" << std::endl;
        board_.print();
        
        EnhancedPositionEvaluator evaluator(board_);
        evaluator.printDetailedAnalysis();
        
        std::cout << "\nСравнение оценок:" << std::endl;
        std::cout << "Обычная оценка:  " << evaluator.evaluate(EnhancedPositionEvaluator::ACCURATE_MODE) << std::endl;
        std::cout << "Эндшпильная:     " << evaluator.evaluateEndgame() << std::endl;
    }
    
    void testAdaptiveWeights() {
        std::cout << "\n6. АДАПТИВНЫЕ ВЕСА" << std::endl;
        std::cout << "===================" << std::endl;
        
        EnhancedPositionEvaluator evaluator(board_);
        
        std::cout << "Начальные веса:" << std::endl;
        std::cout << evaluator.getEvaluationBreakdown() << std::endl;
        
        // Имитируем изменение позиции
        evaluator.setModeWeights(0.5f, 0.3f, 0.1f, 0.1f);
        
        std::cout << "\nИзмененные веса:" << std::endl;
        std::cout << evaluator.getEvaluationBreakdown() << std::endl;
    }
};

int main() {
    try {
        EnhancedEvaluatorTest test;
        test.runAllTests();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Ошибка: " << e.what() << std::endl;
        return 1;
    }
}