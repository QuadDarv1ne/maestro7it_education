#include "../include/incremental_evaluator.hpp"
#include <iostream>
#include <algorithm>

// Определение констант оценки
namespace EvaluationConstants {
    // Значения фигур в сантипешках
    const int PAWN_VALUE = 100;
    const int KNIGHT_VALUE = 320;
    const int BISHOP_VALUE = 330;
    const int ROOK_VALUE = 500;
    const int QUEEN_VALUE = 900;
    const int KING_VALUE = 20000;
    
    // Бонусы и штрафы
    const int CENTER_BONUS = 25;
    const int MOBILITY_BONUS = 10;
    const int KING_SAFETY_BONUS = 15;
    const int DOUBLED_PAWN_PENALTY = -15;
    const int ISOLATED_PAWN_PENALTY = -20;
    const int PASSED_PAWN_BONUS = 30;
    
    // Таблицы Piece-Square для позиционной оценки
    const int PAWN_PSQT[64] = {
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    };
    
    const int KNIGHT_PSQT[64] = {
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    };
    
    // Упрощенные таблицы для других фигур
    const int BISHOP_PSQT[64] = {0}; // Будет реализовано позже
    const int ROOK_PSQT[64] = {0};
    const int QUEEN_PSQT[64] = {0};
    const int KING_PSQT[64] = {0};
}

// Инициализация статических членов
const int IncrementalEvaluator::PIECE_VALUES[6] = {
    EvaluationConstants::KING_VALUE,
    EvaluationConstants::QUEEN_VALUE,
    EvaluationConstants::BISHOP_VALUE,
    EvaluationConstants::ROOK_VALUE,
    EvaluationConstants::KNIGHT_VALUE,
    EvaluationConstants::PAWN_VALUE
};

const int IncrementalEvaluator::PSQT[6][64] = {
    {0}, // King - специальная обработка
    EvaluationConstants::QUEEN_PSQT,
    EvaluationConstants::BISHOP_PSQT,
    EvaluationConstants::ROOK_PSQT,
    EvaluationConstants::KNIGHT_PSQT,
    EvaluationConstants::PAWN_PSQT
};

IncrementalEvaluator::IncrementalEvaluator(const BitboardEngine& board) 
    : board_(board) {
    // Инициализация всех компонентов
    fullRecalculation();
}

void IncrementalEvaluator::fullRecalculation() {
    // Полный пересчет всех компонентов
    for (int color = 0; color < 2; color++) {
        material_[color] = 0;
        mobility_[color] = 0;
        pawnStructure_[color] = 0;
        kingSafety_[color] = 0;
        centerControl_[color] = 0;
    }
    
    // Расчет материала
    for (int piece = 0; piece < 6; piece++) {
        for (int color = 0; color < 2; color++) {
            Bitboard pieceBB = board_.getPieceBitboard(color, piece);
            int count = BitboardEngine::popcount(pieceBB);
            material_[color] += count * PIECE_VALUES[piece];
        }
    }
    
    // Расчет мобильности
    for (int color = 0; color < 2; color++) {
        mobility_[color] = calculateMobility(color);
    }
    
    // Расчет пешечной структуры
    for (int color = 0; color < 2; color++) {
        pawnStructure_[color] = calculatePawnStructure(color);
    }
    
    // Расчет безопасности короля
    for (int color = 0; color < 2; color++) {
        int kingSquare = findKing(color);
        if (kingSquare != -1) {
            kingSafety_[color] = calculateKingSafety(kingSquare, color);
        }
    }
    
    // Расчет контроля центра
    for (int color = 0; color < 2; color++) {
        centerControl_[color] = calculateCenterControl(color);
    }
    
    // Сброс флагов изменений
    materialChanged_ = false;
    mobilityChanged_ = false;
    pawnStructureChanged_ = false;
    kingSafetyChanged_ = false;
    centerControlChanged_ = false;
}

int IncrementalEvaluator::evaluate() {
    int totalScore = 0;
    
    // Материал (наиболее важный компонент)
    totalScore += getMaterialScore();
    
    // Мобильность
    if (mobilityChanged_) {
        mobility_[0] = calculateMobility(0);
        mobility_[1] = calculateMobility(1);
        mobilityChanged_ = false;
    }
    totalScore += getMobilityScore();
    
    // Пешечная структура
    if (pawnStructureChanged_) {
        pawnStructure_[0] = calculatePawnStructure(0);
        pawnStructure_[1] = calculatePawnStructure(1);
        pawnStructureChanged_ = false;
    }
    totalScore += getPawnStructureScore();
    
    // Безопасность короля
    if (kingSafetyChanged_) {
        for (int color = 0; color < 2; color++) {
            int kingSquare = findKing(color);
            if (kingSquare != -1) {
                kingSafety_[color] = calculateKingSafety(kingSquare, color);
            }
        }
        kingSafetyChanged_ = false;
    }
    totalScore += getKingSafetyScore();
    
    // Контроль центра
    if (centerControlChanged_) {
        centerControl_[0] = calculateCenterControl(0);
        centerControl_[1] = calculateCenterControl(1);
        centerControlChanged_ = false;
    }
    totalScore += getCenterControlScore();
    
    return totalScore;
}

void IncrementalEvaluator::updateAfterMove(int fromSquare, int toSquare, int pieceType, int color, int capturedPiece) {
    // Обновление материала
    if (capturedPiece != -1) {
        material_[1 - color] -= PIECE_VALUES[capturedPiece];
        materialChanged_ = true;
        
        // Если захвачена пешка, пешечная структура противника изменилась
        if (capturedPiece == 5) {
            pawnStructureChanged_ = true;
        }
    }
    
    // Обновление мобильности (всегда изменяется)
    mobilityChanged_ = true;
    
    // Обновление пешечной структуры (если двигалась пешка)
    if (pieceType == 5) {
        pawnStructureChanged_ = true;
    }
    
    // Обновление безопасности короля (если двигался король)
    if (pieceType == 0) {
        kingSafetyChanged_ = true;
    }
    
    // Обновление контроля центра (всегда потенциально изменяется)
    centerControlChanged_ = true;
}

// Вспомогательные функции
int IncrementalEvaluator::calculateMobility(int color) const {
    int totalMobility = 0;
    Bitboard myPieces = board_.getColorOccupancy(color);
    Bitboard opponentPieces = board_.getColorOccupancy(1 - color);
    
    // Для каждой фигуры рассчитываем мобильность
    for (int piece = 1; piece < 6; piece++) { // кроме короля
        Bitboard pieceBB = board_.getPieceBitboard(color, piece);
        while (pieceBB) {
            int square = BitboardEngine::lsb(pieceBB);
            Bitboard attacks = getPieceAttacks(square, piece, color);
            totalMobility += calculatePieceMobility(attacks, opponentPieces);
            pieceBB &= pieceBB - 1; // Удалить младший бит
        }
    }
    
    return totalMobility;
}

int IncrementalEvaluator::calculatePieceMobility(Bitboard attacks, Bitboard opponentPieces) const {
    // Мобильность = количество доступных ходов
    int mobility = BitboardEngine::popcount(attacks);
    
    // Бонус за контроль центра
    Bitboard center = 0x0000001818000000ULL; // d4, d5, e4, e5
    int centerControl = BitboardEngine::popcount(attacks & center);
    mobility += centerControl * EvaluationConstants::CENTER_BONUS;
    
    return mobility * EvaluationConstants::MOBILITY_BONUS;
}

int IncrementalEvaluator::calculatePawnStructure(int color) const {
    int structureScore = 0;
    Bitboard pawns = board_.getPieceBitboard(color, 5); // Пешки
    
    while (pawns) {
        int square = BitboardEngine::lsb(pawns);
        int file = square % 8;
        int rank = square / 8;
        
        // Проверка на изолированные пешки
        Bitboard fileMask = 0x0101010101010101ULL << file;
        if (!(pawns & (fileMask << 1)) && !(pawns & (fileMask >> 1))) {
            structureScore += EvaluationConstants::ISOLATED_PAWN_PENALTY;
        }
        
        // Проверка на удвоенные пешки
        if (BitboardEngine::popcount(pawns & fileMask) > 1) {
            structureScore += EvaluationConstants::DOUBLED_PAWN_PENALTY;
        }
        
        // Бонус за проходные пешки
        Bitboard promotionPath = (color == 0) ? 
            (0xFF00000000000000ULL >> (8 * (7 - rank))) : 
            (0x00000000000000FFULL << (8 * rank));
        if (!(board_.getPieceBitboard(1 - color, 5) & promotionPath)) {
            structureScore += EvaluationConstants::PASSED_PAWN_BONUS;
        }
        
        pawns &= pawns - 1;
    }
    
    return structureScore;
}

int IncrementalEvaluator::calculateKingSafety(int kingSquare, int color) const {
    int safety = 0;
    
    // Количество защитников короля
    Bitboard kingAttacks = board_.generateKingAttacks(kingSquare);
    Bitboard defenders = board_.getColorOccupancy(color) & kingAttacks;
    safety += BitboardEngine::popcount(defenders) * EvaluationConstants::KING_SAFETY_BONUS;
    
    // Расстояние от центра (король лучше в углу на эндшпиле)
    int centerDistance = std::max(abs(kingSquare % 8 - 3), abs(kingSquare / 8 - 3));
    safety += centerDistance * 5; // Небольшой бонус за отход от центра
    
    return safety;
}

int IncrementalEvaluator::calculateCenterControl(int color) const {
    int control = 0;
    Bitboard center = 0x0000001818000000ULL; // d4, d5, e4, e5
    Bitboard myPieces = board_.getColorOccupancy(color);
    
    // Контроль центра своими фигурами
    control += BitboardEngine::popcount(myPieces & center) * 20;
    
    // Атака центра
    Bitboard attacks = 0;
    for (int piece = 1; piece < 6; piece++) {
        Bitboard pieceBB = board_.getPieceBitboard(color, piece);
        while (pieceBB) {
            int square = BitboardEngine::lsb(pieceBB);
            attacks |= getPieceAttacks(square, piece, color);
            pieceBB &= pieceBB - 1;
        }
    }
    control += BitboardEngine::popcount(attacks & center) * 10;
    
    return control;
}

int IncrementalEvaluator::findKing(int color) const {
    Bitboard kingBB = board_.getPieceBitboard(color, 0);
    return kingBB ? BitboardEngine::lsb(kingBB) : -1;
}

Bitboard IncrementalEvaluator::getPieceAttacks(int square, int pieceType, int color) const {
    switch (pieceType) {
        case 0: return board_.generateKingAttacks(square);
        case 1: return board_.generateQueenAttacks(square, board_.getOccupancy());
        case 2: return board_.generateBishopAttacks(square, board_.getOccupancy());
        case 3: return board_.generateRookAttacks(square, board_.getOccupancy());
        case 4: return board_.generateKnightAttacks(square);
        case 5: return board_.generatePawnAttacks(square, color);
        default: return 0;
    }
}