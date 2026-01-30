#include "../include/optimized_move_generator.hpp"
#include <iostream>
#include <algorithm>
#include <chrono>

OptimizedMoveGenerator::OptimizedMoveGenerator(const Board& board) 
    : board_(board), attack_tables_initialized_(false), occupancy_cache_(0) {
    initializeAttackTables();
}

void OptimizedMoveGenerator::initializeAttackTables() const {
    if (attack_tables_initialized_) return;
    
    initializeKnightAttacks();
    initializeKingAttacks();
    initializePawnAttacks();
    
    attack_tables_initialized_ = true;
}

void OptimizedMoveGenerator::initializeKnightAttacks() const {
    const int knight_moves[8][2] = {
        {-2, -1}, {-2, 1}, {-1, -2}, {-1, 2},
        {1, -2}, {1, 2}, {2, -1}, {2, 1}
    };
    
    for (int square = 0; square < 64; square++) {
        uint64_t attacks = 0;
        int rank = square / 8;
        int file = square % 8;
        
        for (int i = 0; i < 8; i++) {
            int new_rank = rank + knight_moves[i][0];
            int new_file = file + knight_moves[i][1];
            
            if (new_rank >= 0 && new_rank < 8 && new_file >= 0 && new_file < 8) {
                int target_square = new_rank * 8 + new_file;
                attacks |= (1ULL << target_square);
            }
        }
        
        knight_attacks_[square] = attacks;
    }
}

void OptimizedMoveGenerator::initializeKingAttacks() const {
    const int king_moves[8][2] = {
        {-1, -1}, {-1, 0}, {-1, 1},
        {0, -1},           {0, 1},
        {1, -1},  {1, 0},  {1, 1}
    };
    
    for (int square = 0; square < 64; square++) {
        uint64_t attacks = 0;
        int rank = square / 8;
        int file = square % 8;
        
        for (int i = 0; i < 8; i++) {
            int new_rank = rank + king_moves[i][0];
            int new_file = file + king_moves[i][1];
            
            if (new_rank >= 0 && new_rank < 8 && new_file >= 0 && new_file < 8) {
                int target_square = new_rank * 8 + new_file;
                attacks |= (1ULL << target_square);
            }
        }
        
        king_attacks_[square] = attacks;
    }
}

void OptimizedMoveGenerator::initializePawnAttacks() const {
    for (int color = 0; color < 2; color++) {
        for (int square = 0; square < 64; square++) {
            uint64_t attacks = 0;
            int rank = square / 8;
            int file = square % 8;
            
            if (color == 0) { // WHITE
                if (rank < 7) {
                    if (file > 0) attacks |= (1ULL << ((rank + 1) * 8 + (file - 1)));
                    if (file < 7) attacks |= (1ULL << ((rank + 1) * 8 + (file + 1)));
                }
            } else { // BLACK
                if (rank > 0) {
                    if (file > 0) attacks |= (1ULL << ((rank - 1) * 8 + (file - 1)));
                    if (file < 7) attacks |= (1ULL << ((rank - 1) * 8 + (file + 1)));
                }
            }
            
            pawn_attacks_[color][square] = attacks;
        }
    }
}

uint64_t OptimizedMoveGenerator::getBishopAttacks(int square, uint64_t occupancy) const {
    uint64_t attacks = 0;
    const int directions[4] = {-9, -7, 7, 9};
    
    for (int dir : directions) {
        int sq = square;
        while (true) {
            // Проверяем границы доски
            if ((dir == -9 || dir == 7) && (sq % 8 == 0)) break;
            if ((dir == -7 || dir == 9) && (sq % 8 == 7)) break;
            
            sq += dir;
            if (sq < 0 || sq >= 64) break;
            
            attacks |= (1ULL << sq);
            if (occupancy & (1ULL << sq)) break;
        }
    }
    
    return attacks;
}

uint64_t OptimizedMoveGenerator::getRookAttacks(int square, uint64_t occupancy) const {
    uint64_t attacks = 0;
    const int directions[4] = {-8, -1, 1, 8};
    
    for (int dir : directions) {
        int sq = square;
        while (true) {
            // Проверяем границы доски
            if ((dir == -1 || dir == 1) && ((sq % 8 == 0 && dir == -1) || (sq % 8 == 7 && dir == 1))) break;
            
            sq += dir;
            if (sq < 0 || sq >= 64) break;
            
            attacks |= (1ULL << sq);
            if (occupancy & (1ULL << sq)) break;
        }
    }
    
    return attacks;
}

uint64_t OptimizedMoveGenerator::getQueenAttacks(int square, uint64_t occupancy) const {
    return getBishopAttacks(square, occupancy) | getRookAttacks(square, occupancy);
}

std::vector<Move> OptimizedMoveGenerator::generateLegalMoves(Color color) const {
    std::vector<Move> moves;
    
    // Генерируем ходы для всех фигур
    generatePawnMoves(moves, color);
    generateKnightMoves(moves, color);
    generateBishopMoves(moves, color);
    generateRookMoves(moves, color);
    generateQueenMoves(moves, color);
    generateKingMoves(moves, color);
    
    // Генерируем специальные ходы
    generateCastlingMoves(moves, color);
    generateEnPassantMoves(moves, color);
    generatePromotionMoves(moves, color);
    
    // Фильтруем нелегальные ходы
    moves.erase(
        std::remove_if(moves.begin(), moves.end(),
                      [this, color](const Move& move) {
                          return wouldBeInCheck(move.from, move.to, color);
                      }),
        moves.end()
    );
    
    return moves;
}

void OptimizedMoveGenerator::generatePawnMoves(std::vector<Move>& moves, Color color) const {
    int direction = (color == Color::WHITE) ? 1 : -1;
    int start_rank = (color == Color::WHITE) ? 1 : 6;
    int promotion_rank = (color == Color::WHITE) ? 6 : 1;
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() != PieceType::PAWN || piece.getColor() != color) continue;
        
        int rank = square / 8;
        int file = square % 8;
        
        // Одиночный ход вперед
        int forward_square = square + 8 * direction;
        if (forward_square >= 0 && forward_square < 64 && 
            board_.getPiece(forward_square).isEmpty()) {
            
            if (rank + direction == promotion_rank) {
                // Превращение
                moves.emplace_back(square, forward_square, PieceType::QUEEN);
                moves.emplace_back(square, forward_square, PieceType::ROOK);
                moves.emplace_back(square, forward_square, PieceType::BISHOP);
                moves.emplace_back(square, forward_square, PieceType::KNIGHT);
            } else {
                moves.emplace_back(square, forward_square);
            }
            
            // Двойной ход с начальной позиции
            if (rank == start_rank) {
                int double_forward = square + 16 * direction;
                if (double_forward >= 0 && double_forward < 64 &&
                    board_.getPiece(double_forward).isEmpty()) {
                    moves.emplace_back(square, double_forward);
                }
            }
        }
        
        // Взятия
        uint64_t attacks = pawn_attacks_[static_cast<int>(color)][square];
        while (attacks) {
            int target_square = __builtin_ctzll(attacks);
            Piece target_piece = board_.getPiece(target_square);
            
            if (!target_piece.isEmpty() && target_piece.getColor() != color) {
                if (rank + direction == promotion_rank) {
                    moves.emplace_back(square, target_square, PieceType::QUEEN);
                    moves.emplace_back(square, target_square, PieceType::ROOK);
                    moves.emplace_back(square, target_square, PieceType::BISHOP);
                    moves.emplace_back(square, target_square, PieceType::KNIGHT);
                } else {
                    moves.emplace_back(square, target_square);
                }
            }
            
            attacks &= attacks - 1;
        }
    }
}

void OptimizedMoveGenerator::generateKnightMoves(std::vector<Move>& moves, Color color) const {
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() != PieceType::KNIGHT || piece.getColor() != color) continue;
        
        uint64_t attacks = knight_attacks_[square];
        while (attacks) {
            int target_square = __builtin_ctzll(attacks);
            Piece target_piece = board_.getPiece(target_square);
            
            if (target_piece.isEmpty() || target_piece.getColor() != color) {
                moves.emplace_back(square, target_square);
            }
            
            attacks &= attacks - 1;
        }
    }
}

void OptimizedMoveGenerator::generateBishopMoves(std::vector<Move>& moves, Color color) const {
    uint64_t occupancy = board_.getOccupancy();
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() != PieceType::BISHOP || piece.getColor() != color) continue;
        
        uint64_t attacks = getBishopAttacks(square, occupancy);
        while (attacks) {
            int target_square = __builtin_ctzll(attacks);
            Piece target_piece = board_.getPiece(target_square);
            
            if (target_piece.isEmpty() || target_piece.getColor() != color) {
                moves.emplace_back(square, target_square);
            }
            
            attacks &= attacks - 1;
        }
    }
}

void OptimizedMoveGenerator::generateRookMoves(std::vector<Move>& moves, Color color) const {
    uint64_t occupancy = board_.getOccupancy();
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() != PieceType::ROOK || piece.getColor() != color) continue;
        
        uint64_t attacks = getRookAttacks(square, occupancy);
        while (attacks) {
            int target_square = __builtin_ctzll(attacks);
            Piece target_piece = board_.getPiece(target_square);
            
            if (target_piece.isEmpty() || target_piece.getColor() != color) {
                moves.emplace_back(square, target_square);
            }
            
            attacks &= attacks - 1;
        }
    }
}

void OptimizedMoveGenerator::generateQueenMoves(std::vector<Move>& moves, Color color) const {
    uint64_t occupancy = board_.getOccupancy();
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() != PieceType::QUEEN || piece.getColor() != color) continue;
        
        uint64_t attacks = getQueenAttacks(square, occupancy);
        while (attacks) {
            int target_square = __builtin_ctzll(attacks);
            Piece target_piece = board_.getPiece(target_square);
            
            if (target_piece.isEmpty() || target_piece.getColor() != color) {
                moves.emplace_back(square, target_square);
            }
            
            attacks &= attacks - 1;
        }
    }
}

void OptimizedMoveGenerator::generateKingMoves(std::vector<Move>& moves, Color color) const {
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() != PieceType::KING || piece.getColor() != color) continue;
        
        uint64_t attacks = king_attacks_[square];
        while (attacks) {
            int target_square = __builtin_ctzll(attacks);
            Piece target_piece = board_.getPiece(target_square);
            
            if (target_piece.isEmpty() || target_piece.getColor() != color) {
                moves.emplace_back(square, target_square);
            }
            
            attacks &= attacks - 1;
        }
    }
}

void OptimizedMoveGenerator::generateCastlingMoves(std::vector<Move>& moves, Color color) const {
    // Упрощенная реализация рокировки
    // В реальной реализации здесь будет полная проверка условий рокировки
    (void)moves;
    (void)color;
}

void OptimizedMoveGenerator::generateEnPassantMoves(std::vector<Move>& moves, Color color) const {
    // Упрощенная реализация взятия на проходе
    // В реальной реализации здесь будет проверка позиции en passant
    (void)moves;
    (void)color;
}

void OptimizedMoveGenerator::generatePromotionMoves(std::vector<Move>& moves, Color color) const {
    // Превращения уже обрабатываются в generatePawnMoves
    (void)moves;
    (void)color;
}

bool OptimizedMoveGenerator::wouldBeInCheck(int from, int to, Color color) const {
    // Упрощенная проверка шаха
    // В реальной реализации здесь будет полноценная проверка
    (void)from;
    (void)to;
    (void)color;
    return false;
}

bool OptimizedMoveGenerator::isInCheck(Color color) const {
    // Упрощенная проверка шаха
    (void)color;
    return false;
}

bool OptimizedMoveGenerator::isCheckmate(Color color) const {
    return isInCheck(color) && !hasLegalMoves(color);
}

bool OptimizedMoveGenerator::isStalemate(Color color) const {
    return !isInCheck(color) && !hasLegalMoves(color);
}

bool OptimizedMoveGenerator::hasLegalMoves(Color color) const {
    auto moves = generateLegalMoves(color);
    return !moves.empty();
}

size_t OptimizedMoveGenerator::countLegalMoves(Color color) const {
    return generateLegalMoves(color).size();
}

size_t OptimizedMoveGenerator::countCaptureMoves(Color color) const {
    auto moves = generateLegalMoves(color);
    return std::count_if(moves.begin(), moves.end(),
                        [this](const Move& move) {
                            return !board_.getPiece(move.to).isEmpty();
                        });
}

void OptimizedMoveGenerator::printMoveStatistics(Color color) const {
    auto start = std::chrono::high_resolution_clock::now();
    auto moves = generateLegalMoves(color);
    auto end = std::chrono::high_resolution_clock::now();
    
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "\n=== MOVE GENERATION STATISTICS ===" << std::endl;
    std::cout << "Color: " << (color == Color::WHITE ? "White" : "Black") << std::endl;
    std::cout << "Total legal moves: " << moves.size() << std::endl;
    std::cout << "Generation time: " << duration.count() << " microseconds" << std::endl;
    std::cout << "Moves per microsecond: " << (moves.size() * 1000000.0 / duration.count()) << std::endl;
    
    // Подсчет типов ходов
    size_t captures = 0, promotions = 0, castlings = 0;
    for (const auto& move : moves) {
        if (!board_.getPiece(move.to).isEmpty()) captures++;
        if (move.promotion != PieceType::NONE) promotions++;
    }
    
    std::cout << "Captures: " << captures << std::endl;
    std::cout << "Promotions: " << promotions << std::endl;
    std::cout << "Castlings: " << castlings << std::endl;
    std::cout << "==================================" << std::endl;
}

std::string OptimizedMoveGenerator::getMoveGenerationStats(Color color) const {
    auto moves = generateLegalMoves(color);
    size_t captures = std::count_if(moves.begin(), moves.end(),
                                   [this](const Move& move) {
                                       return !board_.getPiece(move.to).isEmpty();
                                   });
    
    return "Legal moves: " + std::to_string(moves.size()) + 
           ", Captures: " + std::to_string(captures);
}

void OptimizedMoveGenerator::enableAggressivePruning(bool enable) {
    // Настройка агрессивной обрезки ходов
    (void)enable;
}

void OptimizedMoveGenerator::setDepthLimit(int max_depth) {
    // Установка ограничения глубины поиска
    (void)max_depth;
}