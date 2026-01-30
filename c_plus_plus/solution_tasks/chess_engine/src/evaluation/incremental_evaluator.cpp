#include "../../include/incremental_evaluator.hpp"
#include <iostream>
#include <sstream>
#include <cmath>

// Инициализация констант
const int IncrementalEvaluator::MATERIAL_WEIGHTS[Bitboard::PIECE_TYPE_COUNT] = {
    EvaluationConstants::PAWN_VALUE,
    EvaluationConstants::KNIGHT_VALUE,
    EvaluationConstants::BISHOP_VALUE,
    EvaluationConstants::ROOK_VALUE,
    EvaluationConstants::QUEEN_VALUE,
    EvaluationConstants::KING_VALUE
};

const int IncrementalEvaluator::POSITIONAL_BONUSES[64] = {
    // Ранг 1 (черные фигуры)
    0,  0,  0,  0,  0,  0,  0,  0,
    // Ранг 2
    5,  5,  5,  5,  5,  5,  5,  5,
    // Ранг 3
    10, 10, 15, 20, 20, 15, 10, 10,
    // Ранг 4
    15, 15, 25, 30, 30, 25, 15, 15,
    // Ранг 5
    15, 15, 25, 30, 30, 25, 15, 15,
    // Ранг 6
    10, 10, 15, 20, 20, 15, 10, 10,
    // Ранг 7
    5,  5,  5,  5,  5,  5,  5,  5,
    // Ранг 8 (белые фигуры)
    0,  0,  0,  0,  0,  0,  0,  0
};

const int IncrementalEvaluator::MOBILITY_BONUSES[Bitboard::PIECE_TYPE_COUNT] = {
    0,  // PAWN - ограниченная мобильность
    3,  // KNIGHT
    3,  // BISHOP
    4,  // ROOK
    5,  // QUEEN
    0   // KING - фиксированная позиция
};

IncrementalEvaluator::IncrementalEvaluator(const Bitboard& board) 
    : board_(board), material_score_(0), positional_score_(0), 
      mobility_score_(0), pawn_structure_score_(0), king_safety_score_(0) {
    initializeSquareValues();
    initializePawnShieldBonuses();
    fullRecalculate();
}

void IncrementalEvaluator::initializeSquareValues() {
    // Инициализируем таблицу позиционных значений
    for (int square = 0; square < 64; square++) {
        int rank = square / 8;
        int file = square % 8;
        
        // Центральные клетки получают бонус
        bool is_center = (file >= 2 && file <= 5) && (rank >= 2 && rank <= 5);
        square_values_[square] = is_center ? EvaluationConstants::CENTER_BONUS : 0;
        
        // Добавляем бонусы за развитие (для начальных позиций)
        if (rank == 1 || rank == 6) {
            square_values_[square] += EvaluationConstants::DEVELOPMENT_BONUS;
        }
    }
}

void IncrementalEvaluator::initializePawnShieldBonuses() {
    // Инициализируем бонусы для защиты короля пешками
    for (int square = 0; square < 64; square++) {
        int rank = square / 8;
        int file = square % 8;
        
        // Бонусы для клеток рядом с королем
        if ((file >= 3 && file <= 5) && (rank <= 1 || rank >= 6)) {
            pawn_shield_bonus_[square] = EvaluationConstants::KING_SHIELD_BONUS;
        } else {
            pawn_shield_bonus_[square] = 0;
        }
    }
}

int IncrementalEvaluator::calculateMaterialScore() const {
    int score = 0;
    
    // Подсчитываем материальные значения для белых
    for (int piece = 0; piece < Bitboard::PIECE_TYPE_COUNT; piece++) {
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::WHITE, 
                                                        static_cast<Bitboard::PieceType>(piece));
        int count = BitboardUtils::popCount(pieces);
        score += count * MATERIAL_WEIGHTS[piece];
    }
    
    // Вычитаем материальные значения для черных
    for (int piece = 0; piece < Bitboard::PIECE_TYPE_COUNT; piece++) {
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::BLACK, 
                                                        static_cast<Bitboard::PieceType>(piece));
        int count = BitboardUtils::popCount(pieces);
        score -= count * MATERIAL_WEIGHTS[piece];
    }
    
    return score;
}

int IncrementalEvaluator::calculatePositionalScore() const {
    int score = 0;
    
    // Позиционная оценка для белых фигур
    for (int piece = 0; piece < Bitboard::PIECE_TYPE_COUNT; piece++) {
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::WHITE, 
                                                        static_cast<Bitboard::PieceType>(piece));
        
        while (pieces) {
            int square = BitboardUtils::lsb(pieces);
            score += POSITIONAL_BONUSES[square];
            pieces &= pieces - 1; // Удаляем младший бит
        }
    }
    
    // Позиционная оценка для черных фигур (с отрицательным знаком)
    for (int piece = 0; piece < Bitboard::PIECE_TYPE_COUNT; piece++) {
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::BLACK, 
                                                        static_cast<Bitboard::PieceType>(piece));
        
        while (pieces) {
            int square = BitboardUtils::lsb(pieces);
            score -= POSITIONAL_BONUSES[square];
            pieces &= pieces - 1;
        }
    }
    
    return score;
}

int IncrementalEvaluator::calculateMobilityScore() const {
    int score = 0;
    
    // Мобильность белых фигур
    for (int piece = 1; piece < Bitboard::PIECE_TYPE_COUNT - 1; piece++) { // Исключаем пешки и короля
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::WHITE, 
                                                        static_cast<Bitboard::PieceType>(piece));
        
        while (pieces) {
            int square = BitboardUtils::lsb(pieces);
            Bitboard::BitboardType attacks = 0;
            
            switch (piece) {
                case Bitboard::KNIGHT:
                    attacks = board_.getKnightAttacks(square);
                    break;
                case Bitboard::BISHOP:
                    attacks = board_.getBishopAttacks(square, board_.getAllPieces());
                    break;
                case Bitboard::ROOK:
                    attacks = board_.getRookAttacks(square, board_.getAllPieces());
                    break;
                case Bitboard::QUEEN:
                    attacks = board_.getQueenAttacks(square, board_.getAllPieces());
                    break;
            }
            
            int mobility = BitboardUtils::popCount(attacks & ~board_.getOccupancy(Bitboard::WHITE));
            score += mobility * MOBILITY_BONUSES[piece];
            pieces &= pieces - 1;
        }
    }
    
    // Мобильность черных фигур
    for (int piece = 1; piece < Bitboard::PIECE_TYPE_COUNT - 1; piece++) {
        Bitboard::BitboardType pieces = board_.getPieces(Bitboard::BLACK, 
                                                        static_cast<Bitboard::PieceType>(piece));
        
        while (pieces) {
            int square = BitboardUtils::lsb(pieces);
            Bitboard::BitboardType attacks = 0;
            
            switch (piece) {
                case Bitboard::KNIGHT:
                    attacks = board_.getKnightAttacks(square);
                    break;
                case Bitboard::BISHOP:
                    attacks = board_.getBishopAttacks(square, board_.getAllPieces());
                    break;
                case Bitboard::ROOK:
                    attacks = board_.getRookAttacks(square, board_.getAllPieces());
                    break;
                case Bitboard::QUEEN:
                    attacks = board_.getQueenAttacks(square, board_.getAllPieces());
                    break;
            }
            
            int mobility = BitboardUtils::popCount(attacks & ~board_.getOccupancy(Bitboard::BLACK));
            score -= mobility * MOBILITY_BONUSES[piece];
            pieces &= pieces - 1;
        }
    }
    
    return score;
}

int IncrementalEvaluator::calculatePawnStructureScore() const {
    int score = 0;
    
    // Анализ структуры пешек белых
    Bitboard::BitboardType white_pawns = board_.getPieces(Bitboard::WHITE, Bitboard::PAWN);
    Bitboard::BitboardType black_pawns = board_.getPieces(Bitboard::BLACK, Bitboard::PAWN);
    
    while (white_pawns) {
        int square = BitboardUtils::lsb(white_pawns);
        int file = square % 8;
        int rank = square / 8;
        
        // Проверка на удвоенные пешки
        Bitboard::BitboardType file_pawns = white_pawns & (0x0101010101010101ULL << file);
        if (BitboardUtils::popCount(file_pawns) > 1) {
            score += EvaluationConstants::DOUBLED_PAWN_PENALTY;
        }
        
        // Проверка на изолированные пешки
        Bitboard::BitboardType neighbor_files = 0;
        if (file > 0) neighbor_files |= (0x0101010101010101ULL << (file - 1));
        if (file < 7) neighbor_files |= (0x0101010101010101ULL << (file + 1));
        
        if (!(neighbor_files & white_pawns)) {
            score += EvaluationConstants::ISOLATED_PAWN_PENALTY;
        }
        
        // Проверка на проходные пешки
        Bitboard::BitboardType ahead_squares = 0;
        for (int r = rank + 1; r < 8; r++) {
            ahead_squares |= (1ULL << (r * 8 + file));
        }
        
        if (!(ahead_squares & black_pawns)) {
            score += EvaluationConstants::PASSED_PAWN_BONUS + (rank - 1) * 5;
        }
        
        white_pawns &= white_pawns - 1;
    }
    
    // Анализ структуры пешек черных (с отрицательным знаком)
    while (black_pawns) {
        int square = BitboardUtils::lsb(black_pawns);
        int file = square % 8;
        int rank = square / 8;
        
        // Проверка на удвоенные пешки
        Bitboard::BitboardType file_pawns = black_pawns & (0x0101010101010101ULL << file);
        if (BitboardUtils::popCount(file_pawns) > 1) {
            score -= EvaluationConstants::DOUBLED_PAWN_PENALTY;
        }
        
        // Проверка на изолированные пешки
        Bitboard::BitboardType neighbor_files = 0;
        if (file > 0) neighbor_files |= (0x0101010101010101ULL << (file - 1));
        if (file < 7) neighbor_files |= (0x0101010101010101ULL << (file + 1));
        
        if (!(neighbor_files & black_pawns)) {
            score -= EvaluationConstants::ISOLATED_PAWN_PENALTY;
        }
        
        // Проверка на проходные пешки
        Bitboard::BitboardType ahead_squares = 0;
        for (int r = rank - 1; r >= 0; r--) {
            ahead_squares |= (1ULL << (r * 8 + file));
        }
        
        if (!(ahead_squares & white_pawns)) {
            score -= EvaluationConstants::PASSED_PAWN_BONUS + (6 - rank) * 5;
        }
        
        black_pawns &= black_pawns - 1;
    }
    
    return score;
}

int IncrementalEvaluator::calculateKingSafetyScore() const {
    int score = 0;
    
    // Безопасность белого короля
    Bitboard::BitboardType white_king_bb = board_.getPieces(Bitboard::WHITE, Bitboard::KING);
    if (white_king_bb) {
        int king_square = BitboardUtils::lsb(white_king_bb);
        int king_rank = king_square / 8;
        int king_file = king_square % 8;
        
        // Бонус за защиту пешками
        int shield_bonus = 0;
        for (int dr = -1; dr <= 1; dr++) {
            for (int df = -1; df <= 1; df++) {
                int r = king_rank + dr;
                int f = king_file + df;
                if (r >= 0 && r < 8 && f >= 0 && f < 8) {
                    int sq = r * 8 + f;
                    if (BitboardUtils::getBit(board_.getPieces(Bitboard::WHITE, Bitboard::PAWN), sq)) {
                        shield_bonus += pawn_shield_bonus_[sq];
                    }
                }
            }
        }
        score += shield_bonus;
        
        // Штраф за открытые линии рядом с королем
        Bitboard::BitboardType rook_attacks = board_.getRookAttacks(king_square, board_.getAllPieces());
        Bitboard::BitboardType enemy_rooks = board_.getPieces(Bitboard::BLACK, Bitboard::ROOK);
        if (rook_attacks & enemy_rooks) {
            score += EvaluationConstants::KING_EXPOSURE_PENALTY;
        }
    }
    
    // Безопасность черного короля (с отрицательным знаком)
    Bitboard::BitboardType black_king_bb = board_.getPieces(Bitboard::BLACK, Bitboard::KING);
    if (black_king_bb) {
        int king_square = BitboardUtils::lsb(black_king_bb);
        int king_rank = king_square / 8;
        int king_file = king_square % 8;
        
        // Бонус за защиту пешками
        int shield_bonus = 0;
        for (int dr = -1; dr <= 1; dr++) {
            for (int df = -1; df <= 1; df++) {
                int r = king_rank + dr;
                int f = king_file + df;
                if (r >= 0 && r < 8 && f >= 0 && f < 8) {
                    int sq = r * 8 + f;
                    if (BitboardUtils::getBit(board_.getPieces(Bitboard::BLACK, Bitboard::PAWN), sq)) {
                        shield_bonus += pawn_shield_bonus_[sq];
                    }
                }
            }
        }
        score -= shield_bonus;
        
        // Штраф за открытые линии рядом с королем
        Bitboard::BitboardType rook_attacks = board_.getRookAttacks(king_square, board_.getAllPieces());
        Bitboard::BitboardType enemy_rooks = board_.getPieces(Bitboard::WHITE, Bitboard::ROOK);
        if (rook_attacks & enemy_rooks) {
            score -= EvaluationConstants::KING_EXPOSURE_PENALTY;
        }
    }
    
    return score;
}

int IncrementalEvaluator::evaluate() const {
    return material_score_ + positional_score_ + mobility_score_ + 
           pawn_structure_score_ + king_safety_score_;
}

void IncrementalEvaluator::updateOnMove(int from_square, int to_square, 
                                       Bitboard::PieceType captured_piece) {
    Bitboard::PieceType moved_piece = board_.getPieceType(from_square);
    Bitboard::Color moved_color = board_.getPieceColor(from_square);
    
    if (moved_piece == Bitboard::PIECE_TYPE_COUNT) return;
    
    // Обновляем материальную оценку
    updateMaterialOnMove(from_square, to_square, captured_piece);
    
    // Обновляем позиционную оценку
    updatePositionalOnMove(from_square, to_square);
    
    // Обновляем мобильность
    updateMobilityOnMove(to_square, moved_piece);
    
    // Обновляем структуру пешек (если двигалась пешка)
    if (moved_piece == Bitboard::PAWN) {
        updatePawnStructureOnMove(from_square, to_square);
    }
    
    // Обновляем безопасность короля (если двигался король)
    if (moved_piece == Bitboard::KING) {
        updateKingSafetyOnMove(to_square);
    }
}

void IncrementalEvaluator::updateMaterialOnMove(int from_square, int to_square, 
                                               Bitboard::PieceType captured_piece) {
    // Если была захвачена фигура, обновляем материальную оценку
    if (captured_piece != Bitboard::PIECE_TYPE_COUNT) {
        // Мы предполагаем, что captured_piece имеет цвет, противоположный ходящему
        // На tempBoard после movePiece ход уже сменился, но мы в updateOnMove вызываем это ПЕРЕД сменой хода? 
        // Нет, ParallelSearch вызывает movePiece, которая меняет side_to_move_.
        
        // ВАЖНО: Мы должны знать цвет захваченной фигуры. 
        // Так как ход уже сменился в movePiece, то captured_color - это цвет того, кто СЕЙЧАС должен ходить? 
        // Нет, captured_color - это цвет того, КТО СХОДИЛ (т.е. противоположный текущему side_to_move_).
        
        Bitboard::Color current_side = board_.getSideToMove();
        // Тот кто сходил - это opposite(current_side). Тот кого съели - это current_side.
        Bitboard::Color captured_color = current_side; 
        
        int value = MATERIAL_WEIGHTS[captured_piece];
        
        if (captured_color == Bitboard::WHITE) {
            material_score_ -= value; // Белая фигура захвачена - счет уменьшается
        } else {
            material_score_ += value; // Черная фигура захвачена - счет увеличивается
        }
    }
}

void IncrementalEvaluator::updatePositionalOnMove(int from_square, int to_square) {
    Bitboard::Color color = board_.getPieceColor(to_square); // Фигура уже перемещена
    
    if (color == Bitboard::WHITE) {
        positional_score_ -= POSITIONAL_BONUSES[from_square];
        positional_score_ += POSITIONAL_BONUSES[to_square];
    } else {
        positional_score_ += POSITIONAL_BONUSES[from_square];
        positional_score_ -= POSITIONAL_BONUSES[to_square];
    }
}

void IncrementalEvaluator::updateMobilityOnMove(int square, Bitboard::PieceType piece_type) {
    // В реальной реализации здесь будет обновление мобильности конкретной фигуры
    // Пока используем упрощенную версию
    (void)square;
    (void)piece_type;
}

void IncrementalEvaluator::updatePawnStructureOnMove(int from_square, int to_square) {
    // В реальной реализации здесь будет обновление структуры пешек
    // Пока используем упрощенную версию
    (void)from_square;
    (void)to_square;
}

void IncrementalEvaluator::updateKingSafetyOnMove(int square) {
    // В реальной реализации здесь будет обновление безопасности короля
    // Пока используем упрощенную версию
    (void)square;
}

void IncrementalEvaluator::reset() {
    material_score_ = 0;
    positional_score_ = 0;
    mobility_score_ = 0;
    pawn_structure_score_ = 0;
    king_safety_score_ = 0;
}

void IncrementalEvaluator::fullRecalculate() {
    reset();
    material_score_ = calculateMaterialScore();
    positional_score_ = calculatePositionalScore();
    mobility_score_ = calculateMobilityScore();
    pawn_structure_score_ = calculatePawnStructureScore();
    king_safety_score_ = calculateKingSafetyScore();
}

void IncrementalEvaluator::printEvaluationBreakdown() const {
    std::cout << "\n=== РАЗБИВКА ОЦЕНКИ ПОЗИЦИИ ===" << std::endl;
    std::cout << "Материальная оценка:     " << material_score_ << std::endl;
    std::cout << "Позиционная оценка:      " << positional_score_ << std::endl;
    std::cout << "Оценка мобильности:      " << mobility_score_ << std::endl;
    std::cout << "Структура пешек:         " << pawn_structure_score_ << std::endl;
    std::cout << "Безопасность короля:     " << king_safety_score_ << std::endl;
    std::cout << "-------------------------------" << std::endl;
    std::cout << "Итоговая оценка:         " << evaluate() << std::endl;
    std::cout << "===============================" << std::endl;
}

std::string IncrementalEvaluator::getEvaluationDetails() const {
    std::stringstream ss;
    ss << "Material: " << material_score_ 
       << ", Positional: " << positional_score_
       << ", Mobility: " << mobility_score_
       << ", Pawn Structure: " << pawn_structure_score_
       << ", King Safety: " << king_safety_score_
       << ", Total: " << evaluate();
    return ss.str();
}