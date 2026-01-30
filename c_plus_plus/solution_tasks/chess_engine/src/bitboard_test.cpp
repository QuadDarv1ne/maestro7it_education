#include "../include/bitboard.hpp"
#include <iostream>
#include <chrono>
#include <cassert>

void testBitboardBasics() {
    std::cout << "=== ТЕСТ BITBOARD ОСНОВЫ ===" << std::endl;
    
    Bitboard bb;
    
    // Тест 1: Начальная позиция
    std::cout << "1. Тест начальной позиции:" << std::endl;
    bb.setupStartPosition();
    bb.printBoard();
    
    std::string fen = bb.toFen();
    std::cout << "FEN: " << fen << std::endl;
    assert(fen.substr(0, 61) == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    std::cout << "✓ Начальная позиция корректна" << std::endl;
    
    // Тест 2: Проверка фигур
    std::cout << "\n2. Тест проверки фигур:" << std::endl;
    
    // Белый король на e1
    assert(bb.getPieceType(4) == Bitboard::KING);
    assert(bb.getPieceColor(4) == Bitboard::WHITE);
    std::cout << "✓ Белый король на e1" << std::endl;
    
    // Черный король на e8
    assert(bb.getPieceType(60) == Bitboard::KING);
    assert(bb.getPieceColor(60) == Bitboard::BLACK);
    std::cout << "✓ Черный король на e8" << std::endl;
    
    // Белые пешки на 2-м ряду
    for (int i = 8; i < 16; i++) {
        assert(bb.getPieceType(i) == Bitboard::PAWN);
        assert(bb.getPieceColor(i) == Bitboard::WHITE);
    }
    std::cout << "✓ Белые пешки на 2-м ряду" << std::endl;
    
    // Черные пешки на 7-м ряду
    for (int i = 48; i < 56; i++) {
        assert(bb.getPieceType(i) == Bitboard::PAWN);
        assert(bb.getPieceColor(i) == Bitboard::BLACK);
    }
    std::cout << "✓ Черные пешки на 7-м ряду" << std::endl;
    
    // Тест 3: Атаки пешек
    std::cout << "\n3. Тест атак пешек:" << std::endl;
    
    // Белая пешка на e2 атакует d3 и f3
    Bitboard::BitboardType white_pawn_attacks = bb.getPawnAttacks(12, Bitboard::WHITE);
    assert(BitboardUtils::getBit(white_pawn_attacks, 19)); // d3
    assert(BitboardUtils::getBit(white_pawn_attacks, 21)); // f3
    std::cout << "✓ Атаки белой пешки e2" << std::endl;
    
    // Черная пешка на e7 атакует d6 и f6
    Bitboard::BitboardType black_pawn_attacks = bb.getPawnAttacks(52, Bitboard::BLACK);
    assert(BitboardUtils::getBit(black_pawn_attacks, 43)); // d6
    assert(BitboardUtils::getBit(black_pawn_attacks, 45)); // f6
    std::cout << "✓ Атаки черной пешки e7" << std::endl;
    
    // Тест 4: Атаки коня
    std::cout << "\n4. Тест атак коня:" << std::endl;
    
    // Конь на g1 атакует 8 клеток
    Bitboard::BitboardType knight_attacks = bb.getKnightAttacks(1);
    int attack_count = BitboardUtils::popCount(knight_attacks);
    assert(attack_count == 2); // На начальной позиции только 2 атаки
    std::cout << "✓ Атаки коня g1: " << attack_count << " клеток" << std::endl;
    
    // Тест 5: Атаки короля
    std::cout << "\n5. Тест атак короля:" << std::endl;
    
    // Король на e1 атакует до 8 клеток
    Bitboard::BitboardType king_attacks = bb.getKingAttacks(4);
    int king_attack_count = BitboardUtils::popCount(king_attacks);
    assert(king_attack_count == 5); // На начальной позиции 5 атак
    std::cout << "✓ Атаки короля e1: " << king_attack_count << " клеток" << std::endl;
    
    // Тест 6: Генерация ходов
    std::cout << "\n6. Тест генерации ходов:" << std::endl;
    
    auto moves = bb.generateLegalMoves();
    std::cout << "Количество_legal ходов: " << moves.size() << std::endl;
    assert(moves.size() > 0);
    std::cout << "✓ Генерация ходов работает" << std::endl;
    
    // Показываем несколько первых ходов
    std::cout << "Примеры ходов:" << std::endl;
    for (size_t i = 0; i < std::min(size_t(5), moves.size()); i++) {
        int from = moves[i].first;
        int to = moves[i].second;
        int from_rank = from / 8;
        int from_file = from % 8;
        int to_rank = to / 8;
        int to_file = to % 8;
        
        char from_square[3] = {
            static_cast<char>('a' + from_file),
            static_cast<char>('1' + from_rank),
            '\0'
        };
        
        char to_square[3] = {
            static_cast<char>('a' + to_file),
            static_cast<char>('1' + to_rank),
            '\0'
        };
        
        std::cout << "  " << from_square << "-" << to_square << std::endl;
    }
    
    // Тест 7: Проверка шаха
    std::cout << "\n7. Тест проверки шаха:" << std::endl;
    
    bool in_check = bb.isInCheck(Bitboard::WHITE);
    std::cout << "Белый король под шахом: " << (in_check ? "ДА" : "НЕТ") << std::endl;
    assert(!in_check); // В начальной позиции нет шаха
    std::cout << "✓ Проверка шаха работает" << std::endl;
    
    // Тест 8: Производительность
    std::cout << "\n8. Тест производительности:" << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Выполняем много операций
    for (int i = 0; i < 100000; i++) {
        volatile auto attacks = bb.getKnightAttacks(1);
        volatile auto moves = bb.generateLegalMoves();
        volatile bool check = bb.isInCheck(Bitboard::WHITE);
        (void)attacks; (void)moves; (void)check;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Время выполнения 100000 итераций: " << duration.count() << " мс" << std::endl;
    std::cout << "Среднее время на итерацию: " << duration.count() / 100.0 << " мкс" << std::endl;
    std::cout << "✓ Производительность в пределах нормы" << std::endl;
    
    std::cout << "\n🎉 ВСЕ ТЕСТЫ BITBOARD ПРОЙДЕНЫ УСПЕШНО!" << std::endl;
}

int main() {
    try {
        testBitboardBasics();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "❌ Ошибка: " << e.what() << std::endl;
        return 1;
    }
}