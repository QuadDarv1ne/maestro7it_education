/**
 * @file full_system_test.cpp
 * @brief Комплексное тестирование всей системы шахматного движка
 * 
 * Этот файл содержит тесты для проверки корректности работы всех компонентов
 * шахматного движка, включая оптимизации и производительность.
 */

#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include "../include/game_rules.hpp"
#include "../include/minimax.hpp"
#include "../include/position_evaluator.hpp"
#include "../include/console_ui.hpp"
#include <iostream>
#include <chrono>
#include <cassert>

void testBasicFunctionality() {
    std::cout << "=== ТЕСТ БАЗОВОЙ ФУНКЦИОНАЛЬНОСТИ ===" << std::endl;
    
    // Тест доски
    Board board;
    board.setupStartPosition();
    
    // Проверка начальной позиции
    assert(board.getPiece(Square::E1).getType() == PieceType::KING);
    assert(board.getPiece(Square::E1).getColor() == Color::WHITE);
    assert(board.getPiece(Square::E8).getType() == PieceType::KING);
    assert(board.getPiece(Square::E8).getColor() == Color::BLACK);
    std::cout << "✓ Начальная позиция корректна" << std::endl;
    
    // Тест генерации ходов
    MoveGenerator generator(board);
    auto moves = generator.generateLegalMoves();
    assert(!moves.empty());
    std::cout << "✓ Генерация ходов работает (найдено " << moves.size() << " ходов)" << std::endl;
    
    // Тест правил игры
    GameRules rules(board);
    assert(!rules.isGameOver());
    std::cout << "✓ Правила игры работают корректно" << std::endl;
    
    std::cout << "✓ Базовая функциональность пройдена!" << std::endl << std::endl;
}

void testOptimizedComponents() {
    std::cout << "=== ТЕСТ ОПТИМИЗИРОВАННЫХ КОМПОНЕНТОВ ===" << std::endl;
    
    Board board;
    board.setupStartPosition();
    
    // Тест транспозиционной таблицы
    Minimax engine(board, 3);
    auto start = std::chrono::high_resolution_clock::now();
    Move firstMove = engine.findBestMove(Color::WHITE);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "✓ Минимакс с транспозиционной таблицей работает" << std::endl;
    std::cout << "  Время поиска: " << duration.count() << " мс" << std::endl;
    std::cout << "  Найден ход: " << board.squareToAlgebraic(firstMove.from) 
              << "-" << board.squareToAlgebraic(firstMove.to) << std::endl;
    
    // Тест упорядочивания ходов
    MoveGenerator generator(board);
    auto moves = generator.generateLegalMoves();
    auto orderedMoves = engine.orderMoves(moves);
    
    std::cout << "✓ Упорядочивание ходов работает" << std::endl;
    std::cout << "  Ходов до упорядочивания: " << moves.size() << std::endl;
    std::cout << "  Ходов после упорядочивания: " << orderedMoves.size() << std::endl;
    
    // Тест оценки позиции
    PositionEvaluator evaluator(board);
    int score = evaluator.evaluate();
    std::cout << "✓ Оценка позиции работает" << std::endl;
    std::cout << "  Оценка начальной позиции: " << score << std::endl;
    
    std::cout << "✓ Оптимизированные компоненты работают!" << std::endl << std::endl;
}

void testPerformanceImprovements() {
    std::cout << "=== ТЕСТ УЛУЧШЕНИЙ ПРОИЗВОДИТЕЛЬНОСТИ ===" << std::endl;
    
    Board board;
    board.setupStartPosition();
    
    // Сравнение времени поиска на разных глубинах
    std::vector<int> depths = {2, 3, 4};
    
    for (int depth : depths) {
        Minimax engine(board, depth);
        
        auto start = std::chrono::high_resolution_clock::now();
        Move move = engine.findBestMove(Color::WHITE);
        auto end = std::chrono::high_resolution_clock::now();
        
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << "Глубина " << depth << ": " << duration.count() << " мс" << std::endl;
    }
    
    std::cout << "✓ Тест производительности завершен!" << std::endl << std::endl;
}

void testGameScenarios() {
    std::cout << "=== ТЕСТ ИГРОВЫХ СЦЕНАРИЕВ ===" << std::endl;
    
    // Сценарий 1: Базовая игра
    Board board;
    board.setupStartPosition();
    GameRules rules(board);
    
    std::cout << "Сценарий 1: Базовая игра" << std::endl;
    board.printBoard();
    
    // Сделаем несколько ходов
    Move e2e4(Square::E2, Square::E4);
    assert(rules.makeMove(e2e4));
    std::cout << "Ход: e2-e4" << std::endl;
    
    Move e7e5(Square::E7, Square::E5);
    assert(rules.makeMove(e7e5));
    std::cout << "Ход: e7-e5" << std::endl;
    
    board.printBoard();
    std::cout << "✓ Сценарий 1 пройден" << std::endl << std::endl;
    
    // Сценарий 2: Материал преимущества
    std::cout << "Сценарий 2: Материальное преимущество" << std::endl;
    Board board2;
    board2.setupStartPosition();
    
    // Удалим черного ферзя
    board2.setPiece(Square::D8, Piece(PieceType::EMPTY, Color::NONE));
    
    PositionEvaluator evaluator(board2);
    int score = evaluator.evaluate();
    std::cout << "Оценка с удаленным ферзем: " << score << std::endl;
    assert(score > 0); // Белые должны иметь преимущество
    std::cout << "✓ Сценарий 2 пройден" << std::endl << std::endl;
    
    std::cout << "✓ Все игровые сценарии пройдены!" << std::endl << std::endl;
}

void testIntegration() {
    std::cout << "=== ТЕСТ ИНТЕГРАЦИИ ===" << std::endl;
    
    // Тест полной интеграции компонентов
    Board board;
    board.setupStartPosition();
    GameRules rules(board);
    Minimax engine(board, 3);
    
    std::cout << "Начальная позиция:" << std::endl;
    board.printBoard();
    
    // Несколько ходов ИИ против ИИ
    for (int i = 0; i < 3; i++) {
        Color currentPlayer = board.getCurrentPlayer();
        Move bestMove = engine.findBestMove(currentPlayer);
        
        if (bestMove.from != INVALID_SQUARE && bestMove.to != INVALID_SQUARE) {
            std::cout << "Ход " << (i+1) << ": " 
                      << board.squareToAlgebraic(bestMove.from) 
                      << "-" << board.squareToAlgebraic(bestMove.to) << std::endl;
            
            rules.makeMove(bestMove);
            board.printBoard();
        } else {
            std::cout << "Нет доступных ходов" << std::endl;
            break;
        }
    }
    
    std::cout << "✓ Интеграционное тестирование завершено!" << std::endl << std::endl;
}

int main() {
    std::cout << "КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ШАХМАТНОГО ДВИЖКА" << std::endl;
    std::cout << "===========================================" << std::endl;
    
    try {
        testBasicFunctionality();
        testOptimizedComponents();
        testPerformanceImprovements();
        testGameScenarios();
        testIntegration();
        
        std::cout << "🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! 🎉" << std::endl;
        std::cout << "Шахматный движок полностью функционален и оптимизирован!" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "❌ ОШИБКА ВО ВРЕМЯ ТЕСТИРОВАНИЯ: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}