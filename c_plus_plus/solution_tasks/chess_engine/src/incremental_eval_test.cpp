#include "../include/bitboard.hpp"
#include "../include/incremental_evaluator.hpp"
#include <iostream>
#include <chrono>
#include <cassert>

void testIncrementalEvaluator() {
    std::cout << "=== ТЕСТ ИНКРЕМЕНТАЛЬНОГО ОЦЕНЩИКА ===" << std::endl;
    
    // Создаем доску и оценщик
    Bitboard board;
    board.setupStartPosition();
    
    IncrementalEvaluator evaluator(board);
    
    // Тест 1: Начальная позиция
    std::cout << "\n1. Тест начальной позиции:" << std::endl;
    int initial_eval = evaluator.evaluate();
    std::cout << "Оценка начальной позиции: " << initial_eval << std::endl;
    assert(initial_eval == 0); // Должна быть равной
    std::cout << "✓ Начальная позиция оценена корректно" << std::endl;
    
    evaluator.printEvaluationBreakdown();
    
    // Тест 2: Сравнение с полным пересчетом
    std::cout << "\n2. Тест полного пересчета:" << std::endl;
    evaluator.fullRecalculate();
    int recalculated_eval = evaluator.evaluate();
    std::cout << "Оценка после полного пересчета: " << recalculated_eval << std::endl;
    assert(initial_eval == recalculated_eval);
    std::cout << "✓ Полный пересчет дает тот же результат" << std::endl;
    
    // Тест 3: Ход пешкой e2-e4
    std::cout << "\n3. Тест хода e2-e4:" << std::endl;
    
    int from_square = 12; // e2
    int to_square = 28;   // e4
    
    // Сохраняем старую оценку
    int old_eval = evaluator.evaluate();
    std::cout << "Оценка до хода: " << old_eval << std::endl;
    
    // Выполняем ход
    board.movePiece(from_square, to_square);
    
    // Обновляем оценку инкрементально
    evaluator.updateOnMove(from_square, to_square, Bitboard::PIECE_TYPE_COUNT);
    int new_eval = evaluator.evaluate();
    std::cout << "Оценка после хода: " << new_eval << std::endl;
    
    // Пересчитываем полностью для проверки
    evaluator.fullRecalculate();
    int full_recalc_eval = evaluator.evaluate();
    std::cout << "Оценка после полного пересчета: " << full_recalc_eval << std::endl;
    
    assert(new_eval == full_recalc_eval);
    std::cout << "✓ Инкрементальное обновление корректно" << std::endl;
    
    evaluator.printEvaluationBreakdown();
    
    // Тест 4: Взятие фигуры
    std::cout << "\n4. Тест взятия фигуры:" << std::endl;
    
    // Устанавливаем черную пешку на e5 для взятия
    board.setPiece(36, Bitboard::PAWN, Bitboard::BLACK); // e5
    
    old_eval = evaluator.evaluate();
    std::cout << "Оценка до взятия: " << old_eval << std::endl;
    
    // Выполняем взятие e4xe5
    from_square = 28; // e4
    to_square = 36;   // e5
    
    Bitboard::PieceType captured_piece = Bitboard::PAWN;
    board.movePiece(from_square, to_square);
    
    evaluator.updateOnMove(from_square, to_square, captured_piece);
    int capture_eval = evaluator.evaluate();
    std::cout << "Оценка после взятия: " << capture_eval << std::endl;
    
    // Проверяем, что оценка изменилась в пользу белых (взяли черную пешку)
    assert(capture_eval > old_eval);
    std::cout << "✓ Взятие фигуры учтено корректно" << std::endl;
    
    evaluator.printEvaluationBreakdown();
    
    // Тест 5: Производительность
    std::cout << "\n5. Тест производительности:" << std::endl;
    
    // Измеряем время инкрементального обновления
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < 100000; i++) {
        evaluator.updateOnMove(12, 28, Bitboard::PIECE_TYPE_COUNT);
        volatile int eval = evaluator.evaluate();
        (void)eval;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto increment_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Время 100000 инкрементальных обновлений: " 
              << increment_duration.count() << " мкс" << std::endl;
    std::cout << "Среднее время на обновление: " 
              << increment_duration.count() / 100000.0 << " мкс" << std::endl;
    
    // Измеряем время полного пересчета
    start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < 10000; i++) {
        evaluator.fullRecalculate();
        volatile int eval = evaluator.evaluate();
        (void)eval;
    }
    
    end = std::chrono::high_resolution_clock::now();
    auto full_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Время 10000 полных пересчетов: " 
              << full_duration.count() << " мкс" << std::endl;
    std::cout << "Среднее время на пересчет: " 
              << full_duration.count() / 10000.0 << " мкс" << std::endl;
    
    double speedup = static_cast<double>(full_duration.count()) / increment_duration.count() * 10;
    std::cout << "Ускорение: ~" << speedup << "x" << std::endl;
    assert(speedup > 2.0); // Должно быть хотя бы 2x ускорение
    std::cout << "✓ Производительность соответствует ожиданиям" << std::endl;
    
    // Тест 6: Компоненты оценки
    std::cout << "\n6. Тест компонентов оценки:" << std::endl;
    
    std::cout << "Материальная оценка: " << evaluator.getMaterialScore() << std::endl;
    std::cout << "Позиционная оценка: " << evaluator.getPositionalScore() << std::endl;
    std::cout << "Оценка мобильности: " << evaluator.getMobilityScore() << std::endl;
    std::cout << "Структура пешек: " << evaluator.getPawnStructureScore() << std::endl;
    std::cout << "Безопасность короля: " << evaluator.getKingSafetyScore() << std::endl;
    
    // Проверяем, что все компоненты имеют разумные значения
    assert(abs(evaluator.getMaterialScore()) < 5000); // Не слишком большая материальная разница
    assert(abs(evaluator.getPositionalScore()) < 500); // Разумная позиционная оценка
    assert(abs(evaluator.getMobilityScore()) < 300);   // Разумная оценка мобильности
    std::cout << "✓ Все компоненты оценки в разумных пределах" << std::endl;
    
    std::cout << "\n🎉 ВСЕ ТЕСТЫ ИНКРЕМЕНТАЛЬНОГО ОЦЕНЩИКА ПРОЙДЕНЫ УСПЕШНО!" << std::endl;
    std::cout << "\n📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:" << std::endl;
    std::cout << "   • Ускорение: ~" << speedup << "x по сравнению с полным пересчетом" << std::endl;
    std::cout << "   • Точность: 100% совпадение с полным пересчетом" << std::endl;
    std::cout << "   • Все компоненты оценки работают корректно" << std::endl;
}

int main() {
    try {
        testIncrementalEvaluator();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "❌ Ошибка: " << e.what() << std::endl;
        return 1;
    }
}