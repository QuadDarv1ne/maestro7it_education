#include "../../include/optimized_move_generator.hpp"
#include <iostream>
#include <cassert>

// Статические переменные для таблиц
std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::bishop_magics_;
std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::rook_magics_;
std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::bishop_masks_;
std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::rook_masks_;
std::array<std::array<Bitboard::BitboardType, 512>, 64> OptimizedMoveGenerator::bishop_attacks_;
std::array<std::array<Bitboard::BitboardType, 4096>, 64> OptimizedMoveGenerator::rook_attacks_;

std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::pawn_attacks_white_;
std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::pawn_attacks_black_;
std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::pawn_pushes_white_;
std::array<Bitboard::BitboardType, 64> OptimizedMoveGenerator::pawn_pushes_black_;

// Глобальное состояние инициализации
namespace MoveGenInit {
    static bool initialized = false;
    
    void initialize() {
        if (!initialized) {
            OptimizedMoveGenerator::init();
            initialized = true;
        }
    }
    
    bool isInitialized() {
        return initialized;
    }
}

OptimizedMoveGenerator::OptimizedMoveGenerator(const Bitboard& board) 
    : board_(board) {
    MoveGenInit::initialize();
}

void OptimizedMoveGenerator::init() {
    initializeTables();
    initializePawnTables();
    initializeMagicBitboards();
}

void OptimizedMoveGenerator::initializeTables() {
    // Инициализация масок для bishop и rook
    for (int square = 0; square < 64; square++) {
        int rank = square / 8;
        int file = square % 8;
        
        // Bishop masks (диагонали)
        Bitboard::BitboardType bishop_mask = 0;
        for (int dr = -1; dr <= 1; dr += 2) {
            for (int df = -1; df <= 1; df += 2) {
                int r = rank + dr;
                int f = file + df;
                while (r >= 0 && r < 8 && f >= 0 && f < 8) {
                    if (r != rank + dr || f != file + df) { // Исключаем соседние клетки
                        bishop_mask |= (1ULL << (r * 8 + f));
                    }
                    r += dr;
                    f += df;
                }
            }
        }
        bishop_masks_[square] = bishop_mask;
        
        // Rook masks (горизонтали и вертикали)
        Bitboard::BitboardType rook_mask = 0;
        // Горизонталь
        for (int f = 0; f < 8; f++) {
            if (f != file) rook_mask |= (1ULL << (rank * 8 + f));
        }
        // Вертикаль
        for (int r = 0; r < 8; r++) {
            if (r != rank) rook_mask |= (1ULL << (r * 8 + file));
        }
        rook_masks_[square] = rook_mask;
    }
}

void OptimizedMoveGenerator::initializePawnTables() {
    for (int square = 0; square < 64; square++) {
        int rank = square / 8;
        int file = square % 8;
        
        // Белые пешки
        pawn_attacks_white_[square] = 0;
        pawn_pushes_white_[square] = 0;
        
        if (rank < 7) { // Не последний ряд
            // Атаки
            if (file > 0) pawn_attacks_white_[square] |= (1ULL << ((rank + 1) * 8 + (file - 1)));
            if (file < 7) pawn_attacks_white_[square] |= (1ULL << ((rank + 1) * 8 + (file + 1)));
            
            // Продвижение
            pawn_pushes_white_[square] = (1ULL << ((rank + 1) * 8 + file));
            
            // Двойной ход с 2-го ряда
            if (rank == 1) {
                pawn_pushes_white_[square] |= (1ULL << (3 * 8 + file));
            }
        }
        
        // Черные пешки (зеркально)
        pawn_attacks_black_[square] = 0;
        pawn_pushes_black_[square] = 0;
        
        if (rank > 0) { // Не первый ряд
            if (file > 0) pawn_attacks_black_[square] |= (1ULL << ((rank - 1) * 8 + (file - 1)));
            if (file < 7) pawn_attacks_black_[square] |= (1ULL << ((rank - 1) * 8 + (file + 1)));
            
            pawn_pushes_black_[square] = (1ULL << ((rank - 1) * 8 + file));
            
            if (rank == 6) {
                pawn_pushes_black_[square] |= (1ULL << (4 * 8 + file));
            }
        }
    }
}

void OptimizedMoveGenerator::initializeMagicBitboards() {
    // Упрощенная инициализация magic numbers
    // В реальной реализации здесь будут настоящие magic numbers
    
    for (int square = 0; square < 64; square++) {
        // Заглушки для magic numbers
        bishop_magics_[square] = 0x123456789ABCDEF0ULL;
        rook_magics_[square] = 0xFEDCBA9876543210ULL;
        
        // Инициализация таблиц атак (заглушки)
        for (int i = 0; i < 512; i++) {
            bishop_attacks_[square][i] = 0;
        }
        for (int i = 0; i < 4096; i++) {
            rook_attacks_[square][i] = 0;
        }
    }
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateLegalMoves() const {
    auto pseudo_legal = generatePseudoLegalMoves();
    std::vector<MoveType> legal_moves;
    
    for (MoveType move : pseudo_legal) {
        if (isLegalMove(move)) {
            legal_moves.push_back(move);
        }
    }
    
    return legal_moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generatePseudoLegalMoves() const {
    std::vector<MoveType> moves;
    Bitboard::Color color = board_.getSideToMove();
    
    // Генерируем ходы для всех фигур
    auto pawn_moves = generatePawnMoves(color);
    moves.insert(moves.end(), pawn_moves.begin(), pawn_moves.end());
    
    auto knight_moves = generateKnightMoves(color);
    moves.insert(moves.end(), knight_moves.begin(), knight_moves.end());
    
    auto bishop_moves = generateBishopMoves(color);
    moves.insert(moves.end(), bishop_moves.begin(), bishop_moves.end());
    
    auto rook_moves = generateRookMoves(color);
    moves.insert(moves.end(), rook_moves.begin(), rook_moves.end());
    
    auto queen_moves = generateQueenMoves(color);
    moves.insert(moves.end(), queen_moves.begin(), queen_moves.end());
    
    auto king_moves = generateKingMoves(color);
    moves.insert(moves.end(), king_moves.begin(), king_moves.end());
    
    // Специальные ходы
    auto castling_moves = generateCastlingMoves(color);
    moves.insert(moves.end(), castling_moves.begin(), castling_moves.end());
    
    auto en_passant_moves = generateEnPassantMoves(color);
    moves.insert(moves.end(), en_passant_moves.begin(), en_passant_moves.end());
    
    auto promotion_moves = generatePromotionMoves(color);
    moves.insert(moves.end(), promotion_moves.begin(), promotion_moves.end());
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generatePawnMoves(Bitboard::Color color) const {
    std::vector<MoveType> moves;
    Bitboard::BitboardType pawns = board_.getPieces(color, Bitboard::PAWN);
    Bitboard::BitboardType own_pieces = board_.getOccupancy(color);
    Bitboard::BitboardType enemy_pieces = board_.getOccupancy(color == Bitboard::WHITE ? Bitboard::BLACK : Bitboard::WHITE);
    Bitboard::BitboardType empty_squares = ~board_.getAllPieces();
    
    const auto& attacks_table = (color == Bitboard::WHITE) ? pawn_attacks_white_ : pawn_attacks_black_;
    const auto& pushes_table = (color == Bitboard::WHITE) ? pawn_pushes_white_ : pawn_pushes_black_;
    
    while (pawns) {
        int from_square = BitboardUtils::lsb(pawns);
        Bitboard::BitboardType attacks = attacks_table[from_square];
        Bitboard::BitboardType pushes = pushes_table[from_square];
        
        // Взятия
        Bitboard::BitboardType capture_targets = attacks & enemy_pieces;
        while (capture_targets) {
            int to_square = BitboardUtils::lsb(capture_targets);
            MoveType move = packMove(from_square, to_square, CAPTURE_FLAG);
            moves.push_back(move);
            capture_targets &= capture_targets - 1;
        }
        
        // Продвижения
        Bitboard::BitboardType push_targets = pushes & empty_squares;
        while (push_targets) {
            int to_square = BitboardUtils::lsb(push_targets);
            MoveType flags = 0;
            
            // Проверка на превращение (последний ряд)
            int rank = to_square / 8;
            if ((color == Bitboard::WHITE && rank == 7) || (color == Bitboard::BLACK && rank == 0)) {
                flags |= PROMOTION_FLAG;
            }
            
            moves.push_back(packMove(from_square, to_square, flags));
            push_targets &= push_targets - 1;
        }
        
        pawns &= pawns - 1;
    }
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateKnightMoves(Bitboard::Color color) const {
    std::vector<MoveType> moves;
    Bitboard::BitboardType knights = board_.getPieces(color, Bitboard::KNIGHT);
    Bitboard::BitboardType own_pieces = board_.getOccupancy(color);
    Bitboard::BitboardType enemy_pieces = board_.getOccupancy(color == Bitboard::WHITE ? Bitboard::BLACK : Bitboard::WHITE);
    
    while (knights) {
        int from_square = BitboardUtils::lsb(knights);
        Bitboard::BitboardType attacks = getKnightAttacks(from_square);
        
        auto piece_moves = addNonSlidingMoves(from_square, attacks, own_pieces, enemy_pieces);
        moves.insert(moves.end(), piece_moves.begin(), piece_moves.end());
        
        knights &= knights - 1;
    }
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateBishopMoves(Bitboard::Color color) const {
    std::vector<MoveType> moves;
    Bitboard::BitboardType bishops = board_.getPieces(color, Bitboard::BISHOP);
    Bitboard::BitboardType own_pieces = board_.getOccupancy(color);
    Bitboard::BitboardType enemy_pieces = board_.getOccupancy(color == Bitboard::WHITE ? Bitboard::BLACK : Bitboard::WHITE);
    Bitboard::BitboardType occupied = board_.getAllPieces();
    
    while (bishops) {
        int from_square = BitboardUtils::lsb(bishops);
        Bitboard::BitboardType attacks = getBishopAttacks(from_square, occupied);
        
        auto piece_moves = addSlidingMoves(from_square, attacks, own_pieces, enemy_pieces);
        moves.insert(moves.end(), piece_moves.begin(), piece_moves.end());
        
        bishops &= bishops - 1;
    }
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateRookMoves(Bitboard::Color color) const {
    std::vector<MoveType> moves;
    Bitboard::BitboardType rooks = board_.getPieces(color, Bitboard::ROOK);
    Bitboard::BitboardType own_pieces = board_.getOccupancy(color);
    Bitboard::BitboardType enemy_pieces = board_.getOccupancy(color == Bitboard::WHITE ? Bitboard::BLACK : Bitboard::WHITE);
    Bitboard::BitboardType occupied = board_.getAllPieces();
    
    while (rooks) {
        int from_square = BitboardUtils::lsb(rooks);
        Bitboard::BitboardType attacks = getRookAttacks(from_square, occupied);
        
        auto piece_moves = addSlidingMoves(from_square, attacks, own_pieces, enemy_pieces);
        moves.insert(moves.end(), piece_moves.begin(), piece_moves.end());
        
        rooks &= rooks - 1;
    }
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateQueenMoves(Bitboard::Color color) const {
    std::vector<MoveType> moves;
    Bitboard::BitboardType queens = board_.getPieces(color, Bitboard::QUEEN);
    Bitboard::BitboardType own_pieces = board_.getOccupancy(color);
    Bitboard::BitboardType enemy_pieces = board_.getOccupancy(color == Bitboard::WHITE ? Bitboard::BLACK : Bitboard::WHITE);
    Bitboard::BitboardType occupied = board_.getAllPieces();
    
    while (queens) {
        int from_square = BitboardUtils::lsb(queens);
        Bitboard::BitboardType attacks = getQueenAttacks(from_square, occupied);
        
        auto piece_moves = addSlidingMoves(from_square, attacks, own_pieces, enemy_pieces);
        moves.insert(moves.end(), piece_moves.begin(), piece_moves.end());
        
        queens &= queens - 1;
    }
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateKingMoves(Bitboard::Color color) const {
    std::vector<MoveType> moves;
    Bitboard::BitboardType kings = board_.getPieces(color, Bitboard::KING);
    Bitboard::BitboardType own_pieces = board_.getOccupancy(color);
    Bitboard::BitboardType enemy_pieces = board_.getOccupancy(color == Bitboard::WHITE ? Bitboard::BLACK : Bitboard::WHITE);
    
    while (kings) {
        int from_square = BitboardUtils::lsb(kings);
        Bitboard::BitboardType attacks = getKingAttacks(from_square);
        
        auto piece_moves = addNonSlidingMoves(from_square, attacks, own_pieces, enemy_pieces);
        moves.insert(moves.end(), piece_moves.begin(), piece_moves.end());
        
        kings &= kings - 1;
    }
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::addSlidingMoves(
    int square, Bitboard::BitboardType attacks, 
    Bitboard::BitboardType own_pieces, 
    Bitboard::BitboardType enemy_pieces) const {
    
    std::vector<MoveType> moves;
    
    // Ходы на пустые клетки
    Bitboard::BitboardType quiet_moves = attacks & (~own_pieces) & (~enemy_pieces);
    while (quiet_moves) {
        int to_square = BitboardUtils::lsb(quiet_moves);
        moves.push_back(packMove(square, to_square));
        quiet_moves &= quiet_moves - 1;
    }
    
    // Взятия
    Bitboard::BitboardType captures = attacks & enemy_pieces;
    while (captures) {
        int to_square = BitboardUtils::lsb(captures);
        moves.push_back(packMove(square, to_square, CAPTURE_FLAG));
        captures &= captures - 1;
    }
    
    return moves;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::addNonSlidingMoves(
    int square, Bitboard::BitboardType attacks,
    Bitboard::BitboardType own_pieces,
    Bitboard::BitboardType enemy_pieces) const {
    
    std::vector<MoveType> moves;
    
    // Исключаем свои фигуры
    Bitboard::BitboardType valid_targets = attacks & (~own_pieces);
    
    // Тихие ходы
    Bitboard::BitboardType quiet_moves = valid_targets & (~enemy_pieces);
    while (quiet_moves) {
        int to_square = BitboardUtils::lsb(quiet_moves);
        moves.push_back(packMove(square, to_square));
        quiet_moves &= quiet_moves - 1;
    }
    
    // Взятия
    Bitboard::BitboardType captures = valid_targets & enemy_pieces;
    while (captures) {
        int to_square = BitboardUtils::lsb(captures);
        moves.push_back(packMove(square, to_square, CAPTURE_FLAG));
        captures &= captures - 1;
    }
    
    return moves;
}

// Реализации атак (заглушки)
Bitboard::BitboardType OptimizedMoveGenerator::getBishopAttacks(int square, Bitboard::BitboardType occupied) {
    // В реальной реализации использовать magic bitboards
    return 0; // Заглушка
}

Bitboard::BitboardType OptimizedMoveGenerator::getRookAttacks(int square, Bitboard::BitboardType occupied) {
    // В реальной реализации использовать magic bitboards
    return 0; // Заглушка
}

Bitboard::BitboardType OptimizedMoveGenerator::getQueenAttacks(int square, Bitboard::BitboardType occupied) {
    return getBishopAttacks(square, occupied) | getRookAttacks(square, occupied);
}

Bitboard::BitboardType OptimizedMoveGenerator::getKnightAttacks(int square) {
    // Предвычисленные атаки коня
    static const int knight_deltas[8] = {-17, -15, -10, -6, 6, 10, 15, 17};
    Bitboard::BitboardType attacks = 0;
    int rank = square / 8;
    int file = square % 8;
    
    for (int delta : knight_deltas) {
        int new_rank = rank + (delta / 8);
        int new_file = file + (delta % 8);
        if (new_rank >= 0 && new_rank < 8 && new_file >= 0 && new_file < 8) {
            attacks |= (1ULL << (new_rank * 8 + new_file));
        }
    }
    
    return attacks;
}

Bitboard::BitboardType OptimizedMoveGenerator::getKingAttacks(int square) {
    static const int king_deltas[8] = {-9, -8, -7, -1, 1, 7, 8, 9};
    Bitboard::BitboardType attacks = 0;
    int rank = square / 8;
    int file = square % 8;
    
    for (int delta : king_deltas) {
        int new_rank = rank + (delta / 8);
        int new_file = file + (delta % 8);
        if (new_rank >= 0 && new_rank < 8 && new_file >= 0 && new_file < 8) {
            attacks |= (1ULL << (new_rank * 8 + new_file));
        }
    }
    
    return attacks;
}

Bitboard::BitboardType OptimizedMoveGenerator::getPawnAttacks(int square, Bitboard::Color color) {
    if (color == Bitboard::WHITE) {
        return pawn_attacks_white_[square];
    } else {
        return pawn_attacks_black_[square];
    }
}

bool OptimizedMoveGenerator::isLegalMove(MoveType move) const {
    // Проверка легальности хода
    // В реальной реализации нужно проверить:
    // 1. Не оставляет ли короля под шахом
    // 2. Корректность специальных ходов
    
    return !wouldLeaveKingInCheck(move);
}

bool OptimizedMoveGenerator::wouldLeaveKingInCheck(MoveType move) const {
    // Упрощенная проверка - в реальной реализации нужно моделировать ход
    (void)move; // Заглушка
    return false;
}

bool OptimizedMoveGenerator::isSquareAttacked(int square, Bitboard::Color by_color) const {
    // Проверка, атакована ли клетка фигурами цвета by_color
    (void)square; (void)by_color; // Заглушка
    return false;
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateCastlingMoves(Bitboard::Color color) const {
    return {}; // Заглушка
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generateEnPassantMoves(Bitboard::Color color) const {
    return {}; // Заглушка
}

std::vector<OptimizedMoveGenerator::MoveType> OptimizedMoveGenerator::generatePromotionMoves(Bitboard::Color color) const {
    return {}; // Заглушка
}

std::string OptimizedMoveGenerator::moveToAlgebraic(MoveType move) {
    int from = unpackFrom(move);
    int to = unpackTo(move);
    MoveType flags = unpackFlags(move);
    
    char from_file = 'a' + (from % 8);
    char from_rank = '1' + (from / 8);
    char to_file = 'a' + (to % 8);
    char to_rank = '1' + (to / 8);
    
    std::string result;
    result += from_file;
    result += from_rank;
    result += to_file;
    result += to_rank;
    
    if (flags & PROMOTION_FLAG) {
        result += "q"; // Превращение в ферзя по умолчанию
    }
    
    return result;
}

OptimizedMoveGenerator::MoveType OptimizedMoveGenerator::algebraicToMove(const std::string& alg) {
    if (alg.length() < 4) return 0;
    
    int from_file = alg[0] - 'a';
    int from_rank = alg[1] - '1';
    int to_file = alg[2] - 'a';
    int to_rank = alg[3] - '1';
    
    int from = from_rank * 8 + from_file;
    int to = to_rank * 8 + to_file;
    
    MoveType flags = 0;
    if (alg.length() > 4 && alg[4] == 'q') {
        flags |= PROMOTION_FLAG;
    }
    
    return packMove(from, to, flags);
}

bool OptimizedMoveGenerator::isValidSquare(int square) const {
    return square >= 0 && square < 64;
}