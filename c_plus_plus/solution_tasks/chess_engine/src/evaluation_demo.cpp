/**
 * @file evaluation_demo.cpp
 * @brief Демонстрация улучшенной системы оценки позиции
 * 
 * Показывает ключевые улучшения в системе оценки:
 * - Комбинирование нейросетевой и традиционной оценки
 * - Тактический анализ позиции
 * - Адаптивные веса в зависимости от фазы игры
 * - Производительность различных подходов
 */

#include <iostream>
#include <chrono>
#include <vector>
#include <iomanip>

// Упрощенные классы для демонстрации
class SimpleBoard {
public:
    void setupStartPosition() { /* имитация */ }
    void print() const { 
        std::cout << "  a b c d e f g h" << std::endl;
        std::cout << "8 r n b q k b n r" << std::endl;
        std::cout << "7 p p p p p p p p" << std::endl;
        std::cout << "6 . . . . . . . ." << std::endl;
        std::cout << "5 . . . . . . . ." << std::endl;
        std::cout << "4 . . . . . . . ." << std::endl;
        std::cout << "3 . . . . . . . ." << std::endl;
        std::cout << "2 P P P P P P P P" << std::endl;
        std::cout << "1 R N B Q K B N R" << std::endl;
    }
};

class SimpleEvaluator {
public:
    int evaluate() const { 
        // Имитация оценки
        return 15; // Белые немного лучше
    }
};

class EnhancedEvaluatorDemo {
private:
    SimpleBoard board_;

public:
    void demonstrateEnhancedEvaluation() {
        std::cout << "=== ДЕМОНСТРАЦИЯ УЛУЧШЕННОЙ ОЦЕНКИ ===" << std::endl;
        
        std::cout << "\n1. НАЧАЛЬНАЯ ПОЗИЦИЯ:" << std::endl;
        board_.setupStartPosition();
        board_.print();
        
        // Сравнение разных подходов к оценке
        std::cout << "\n2. СРАВНЕНИЕ ПОДХОДОВ К ОЦЕНКЕ:" << std::endl;
        
        // Традиционная оценка
        SimpleEvaluator traditional_eval;
        int traditional_score = traditional_eval.evaluate();
        
        // Нейросетевая оценка (имитация)
        int neural_score = 12; // Более консервативная
        
        // Инкрементальная оценка (имитация)
        int incremental_score = 18; // Более точная
        
        // Комбинированная оценка
        float combined_score = 0.4f * neural_score + 0.4f * incremental_score + 0.2f * traditional_score;
        
        std::cout << "Традиционная оценка:    " << std::setw(3) << traditional_score << std::endl;
        std::cout << "Нейросетевая оценка:    " << std::setw(3) << neural_score << std::endl;
        std::cout << "Инкрементальная оценка: " << std::setw(3) << incremental_score << std::endl;
        std::cout << "Комбинированная оценка: " << std::setw(3) << static_cast<int>(combined_score) << std::endl;
        
        // Демонстрация тактического анализа
        std::cout << "\n3. ТАКТИЧЕСКИЙ АНАЛИЗ:" << std::endl;
        demonstrateTacticalAnalysis();
        
        // Демонстрация адаптивных весов
        std::cout << "\n4. АДАПТИВНЫЕ ВЕСА:" << std::endl;
        demonstrateAdaptiveWeights();
        
        // Тест производительности
        std::cout << "\n5. ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ:" << std::endl;
        performanceBenchmark();
        
        std::cout << "\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===" << std::endl;
    }

private:
    void demonstrateTacticalAnalysis() {
        std::cout << "Анализ тактических возможностей:" << std::endl;
        
        // Имитация анализа различных тактических элементов
        struct TacticalElement {
            std::string name;
            int count;
            int bonus;
        };
        
        std::vector<TacticalElement> elements = {
            {"Связки", 2, 25},
            {"Вилки", 1, 40},
            {"Скосы", 0, 35},
            {"Открытые атаки", 3, 30},
            {"Двойные атаки", 1, 20},
            {"Общие угрозы", 5, 15}
        };
        
        int total_tactical_bonus = 0;
        for (const auto& elem : elements) {
            int contribution = elem.count * elem.bonus;
            total_tactical_bonus += contribution;
            std::cout << "  " << elem.name << ": " << std::setw(2) << elem.count 
                      << " × " << std::setw(2) << elem.bonus 
                      << " = " << std::setw(3) << contribution << std::endl;
        }
        
        std::cout << "Общий тактический бонус: " << total_tactical_bonus << std::endl;
    }
    
    void demonstrateAdaptiveWeights() {
        std::cout << "Веса оценки в зависимости от фазы игры:" << std::endl;
        
        struct GamePhase {
            std::string name;
            float neural_weight;
            float incremental_weight;
            float tactical_weight;
            float endgame_weight;
        };
        
        std::vector<GamePhase> phases = {
            {"Дебют", 0.50f, 0.30f, 0.15f, 0.05f},
            {"Миттельшпиль", 0.40f, 0.40f, 0.15f, 0.05f},
            {"Эндшпиль", 0.30f, 0.50f, 0.10f, 0.10f}
        };
        
        std::cout << std::fixed << std::setprecision(2);
        std::cout << "Фаза      | Нейро | Инкр | Такт | Эндш" << std::endl;
        std::cout << "----------|-------|------|------|------" << std::endl;
        
        for (const auto& phase : phases) {
            std::cout << std::setw(9) << phase.name << " | "
                      << std::setw(5) << phase.neural_weight << " | "
                      << std::setw(4) << phase.incremental_weight << " | "
                      << std::setw(4) << phase.tactical_weight << " | "
                      << std::setw(4) << phase.endgame_weight << std::endl;
        }
    }
    
    void performanceBenchmark() {
        const int iterations = 100000;
        
        std::cout << "Сравнение скорости оценки (" << iterations << " итераций):" << std::endl;
        
        // Тест традиционной оценки
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < iterations; i++) {
            volatile int score = traditionalEvaluation();
            (void)score;
        }
        auto end = std::chrono::high_resolution_clock::now();
        auto traditional_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        // Тест улучшенной оценки
        start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < iterations; i++) {
            volatile int score = enhancedEvaluation();
            (void)score;
        }
        end = std::chrono::high_resolution_clock::now();
        auto enhanced_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        double traditional_avg = static_cast<double>(traditional_time.count()) / iterations;
        double enhanced_avg = static_cast<double>(enhanced_time.count()) / iterations;
        
        std::cout << "Традиционная оценка: " << std::fixed << std::setprecision(3) 
                  << traditional_avg << " мкс/оценка" << std::endl;
        std::cout << "Улучшенная оценка:   " << enhanced_avg << " мкс/оценка" << std::endl;
        std::cout << "Ускорение: " << std::fixed << std::setprecision(2) 
                  << (traditional_avg / enhanced_avg) << "x" << std::endl;
    }
    
    // Имитационные функции оценки
    int traditionalEvaluation() const {
        // Имитация простой оценки
        return 15;
    }
    
    int enhancedEvaluation() const {
        // Имитация улучшенной оценки с дополнительными вычислениями
        int base = 15;
        int tactical_bonus = 8;  // Тактический анализ
        int phase_adjustment = 2; // Адаптация к фазе
        return base + tactical_bonus + phase_adjustment;
    }
};

int main() {
    try {
        EnhancedEvaluatorDemo demo;
        demo.demonstrateEnhancedEvaluation();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Ошибка: " << e.what() << std::endl;
        return 1;
    }
}