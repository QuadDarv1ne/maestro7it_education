/**
 * @file advanced_evaluation_test.cpp
 * @brief Тестирование улучшенной системы оценки позиции
 * 
 * Этот файл содержит тесты для демонстрации работы улучшенной
 * системы оценки позиции шахматного движка.
 */

#include "../include/board.hpp"
#include "../include/position_evaluator.hpp"
#include "../include/move_generator.hpp"
#include "../include/game_rules.hpp"
#include <iostream>
#include <vector>
#include <iomanip>

void printEvaluationDetails(const Board& board, const std::string& positionName) {
    std::cout << "\n=== " << positionName << " ===" << std::endl;
    board.print();
    
    PositionEvaluator evaluator(board);
    
    std::cout << "\nПодробная оценка:" << std::endl;
    std::cout << "Материальная оценка: " << evaluator.materialEvaluation() << std::endl;
    std::cout << "Позиционная оценка: " << evaluator.positionalEvaluation() << std::endl;
    std::cout << "Оценка мобильности: " << evaluator.mobilityEvaluation() << std::endl;
    std::cout << "Безопасность короля: " << evaluator.kingSafetyEvaluation() << std::endl;
    std::cout << "Структура пешек: " << evaluator.pawnStructureEvaluation() << std::endl;
    std::cout << "Общая оценка: " << evaluator.evaluate() << std::endl;
    std::cout << "Фаза игры: " << (evaluator.isEndGame() ? "Эндшпиль" : "Миттельшпиль") << std::endl;
    
    // Покажем возможные ходы
    MoveGenerator gen(board);
    auto moves = gen.generateLegalMoves();
    std::cout << "Возможных ходов: " << moves.size() << std::endl;
}

void testStartingPosition() {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "ТЕСТ 1: Начальная позиция" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    Board board;
    board.setupStartPosition();
    printEvaluationDetails(board, "Начальная позиция");
}

void testOpenPosition() {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "ТЕСТ 2: Открытая позиция" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    Board board;
    // Быстрое развитие в центре
    board.makeMove(Move(Square::E2, Square::E4));   // e4
    board.makeMove(Move(Square::E7, Square::E5));   // e5
    board.makeMove(Move(Square::G1, Square::F3));   // Nf3
    board.makeMove(Move(Square::B8, Square::C6));   // Nc6
    board.makeMove(Move(Square::F1, Square::C4));   // Bc4
    
    printEvaluationDetails(board, "Открытая позиция после 1.e4 e5 2.Nf3 Nc6 3.Bc4");
}

void testClosedPosition() {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "ТЕСТ 3: Закрытая позиция" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    Board board;
    // Закрытый дебют
    board.makeMove(Move(Square::D2, Square::D4));   // d4
    board.makeMove(Move(Square::D7, Square::D5));   // d5
    board.makeMove(Move(Square::C2, Square::C4));   // c4
    board.makeMove(Move(Square::E7, Square::E6));   // e6
    board.makeMove(Move(Square::B1, Square::C3));   // Nc3
    board.makeMove(Move(Square::G8, Square::F6));   // Nf6
    
    printEvaluationDetails(board, "Закрытая позиция после закрытого дебюта");
}

void testMaterialAdvantage() {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "ТЕСТ 4: Материальное преимущество" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    Board board;
    board.setupStartPosition();
    
    // Удаляем черного ферзя для создания материального преимущества
    board.setPiece(Square::D8, Piece(PieceType::EMPTY, Color::NONE));
    
    printEvaluationDetails(board, "Белые без ферзя (материальное преимущество)");
}

void testKingSafety() {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "ТЕСТ 5: Безопасность короля" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    Board board;
    // Позиция с угрозой королю
    board.setPiece(Square::E1, Piece(PieceType::KING, Color::WHITE));
    board.setPiece(Square::E8, Piece(PieceType::KING, Color::BLACK));
    board.setPiece(Square::D1, Piece(PieceType::QUEEN, Color::WHITE));
    board.setPiece(Square::H5, Piece(PieceType::QUEEN, Color::BLACK));
    
    printEvaluationDetails(board, "Угроза королю");
}

void testPawnStructure() {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "ТЕСТ 6: Пешечная структура" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    Board board;
    board.setPiece(Square::E1, Piece(PieceType::KING, Color::WHITE));
    board.setPiece(Square::E8, Piece(PieceType::KING, Color::BLACK));
    
    // Создаем различные пешечные структуры
    board.setPiece(Square::A2, Piece(PieceType::PAWN, Color::WHITE));
    board.setPiece(Square::B2, Piece(PieceType::PAWN, Color::WHITE));
    board.setPiece(Square::C2, Piece(PieceType::PAWN, Color::WHITE)); // Связанные пешки
    board.setPiece(Square::D4, Piece(PieceType::PAWN, Color::WHITE)); // Изолированная пешка
    board.setPiece(Square::H2, Piece(PieceType::PAWN, Color::WHITE)); // Проходная пешка
    
    board.setPiece(Square::A7, Piece(PieceType::PAWN, Color::BLACK));
    board.setPiece(Square::B7, Piece(PieceType::PAWN, Color::BLACK));
    board.setPiece(Square::C7, Piece(PieceType::PAWN, Color::BLACK));
    board.setPiece(Square::D5, Piece(PieceType::PAWN, Color::BLACK));
    board.setPiece(Square::H7, Piece(PieceType::PAWN, Color::BLACK));
    
    printEvaluationDetails(board, "Различные пешечные структуры");
}

void demonstratePieceValues() {
    std::cout << "\n" << std::string(50, '=') << std::endl;
    std::cout << "ДЕМОНСТРАЦИЯ: Значения фигур" << std::endl;
    std::cout << std::string(50, '=') << std::endl;
    
    std::cout << "Значения фигур в сантипешках:" << std::endl;
    std::cout << "Пешка:     " << Piece(PieceType::PAWN, Color::WHITE).getValue() << std::endl;
    std::cout << "Конь:      " << Piece(PieceType::KNIGHT, Color::WHITE).getValue() << std::endl;
    std::cout << "Слон:      " << Piece(PieceType::BISHOP, Color::WHITE).getValue() << std::endl;
    std::cout << "Ладья:     " << Piece(PieceType::ROOK, Color::WHITE).getValue() << std::endl;
    std::cout << "Ферзь:     " << Piece(PieceType::QUEEN, Color::WHITE).getValue() << std::endl;
    std::cout << "Король:    " << Piece(PieceType::KING, Color::WHITE).getValue() << std::endl;
    
    // Покажем соотношения
    std::cout << "\nСоотношения:" << std::endl;
    std::cout << "Ферзь ≈ " << std::fixed << std::setprecision(1) 
              << (double)Piece(PieceType::QUEEN, Color::WHITE).getValue() / Piece(PieceType::PAWN, Color::WHITE).getValue() 
              << " пешкам" << std::endl;
    std::cout << "Ладья ≈ " << std::fixed << std::setprecision(1)
              << (double)Piece(PieceType::ROOK, Color::WHITE).getValue() / Piece(PieceType::PAWN, Color::WHITE).getValue() 
              << " пешкам" << std::endl;
    std::cout << "Слон ≈ " << std::fixed << std::setprecision(1)
              << (double)Piece(PieceType::BISHOP, Color::WHITE).getValue() / Piece(PieceType::PAWN, Color::WHITE).getValue() 
              << " пешкам" << std::endl;
    std::cout << "Конь ≈ " << std::fixed << std::setprecision(1)
              << (double)Piece(PieceType::KNIGHT, Color::WHITE).getValue() / Piece(PieceType::PAWN, Color::WHITE).getValue() 
              << " пешкам" << std::endl;
}

int main() {
    std::cout << "ШАХМАТНЫЙ ДВИЖОК - ТЕСТИРОВАНИЕ УЛУЧШЕННОЙ СИСТЕМЫ ОЦЕНКИ" << std::endl;
    std::cout << "=========================================================" << std::endl;
    
    try {
        demonstratePieceValues();
        testStartingPosition();
        testOpenPosition();
        testClosedPosition();
        testMaterialAdvantage();
        testKingSafety();
        testPawnStructure();
        
        std::cout << "\n" << std::string(60, '=') << std::endl;
        std::cout << "ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!" << std::endl;
        std::cout << std::string(60, '=') << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Ошибка во время тестирования: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
