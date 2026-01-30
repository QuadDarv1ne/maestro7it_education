#include "../../include/bitboard.hpp"
#include <cstring>
#include <cassert>
#include <sstream>
#include <cctype>
#include <cstdlib>

// Инициализация констант
const int BitboardUtils::KNIGHT_DELTAS[8] = {-17, -15, -10, -6, 6, 10, 15, 17};
const int BitboardUtils::KING_DELTAS[8] = {-9, -8, -7, -1, 1, 7, 8, 9};
const int BitboardUtils::BISHOP_DELTAS[4] = {-9, -7, 7, 9};
const int BitboardUtils::ROOK_DELTAS[4] = {-8, -1, 1, 8};

// Заглушки для magic numbers
Bitboard::BitboardType BitboardUtils::BISHOP_MAGICS[64];
Bitboard::BitboardType BitboardUtils::ROOK_MAGICS[64];

Bitboard::Bitboard() {
    clear();
    side_to_move_ = WHITE;
    en_passant_square_ = -1;
    half_move_clock_ = 0;
    full_move_number_ = 1;
    
    // Инициализация рокировок
    castling_rights_[WHITE][0] = castling_rights_[WHITE][1] = true;
    castling_rights_[BLACK][0] = castling_rights_[BLACK][1] = true;
}

void Bitboard::clear() {
    memset(pieces_, 0, sizeof(pieces_));
    memset(occupancy_, 0, sizeof(occupancy_));
    all_pieces_ = 0;
}

void Bitboard::setupStartPosition() {
    clear();
    
    // Белые пешки
    pieces_[WHITE][PAWN] = 0xFF00ULL; // Ранг 2
    // Черные пешки  
    pieces_[BLACK][PAWN] = 0xFF000000000000ULL; // Ранг 7
    
    // Белые фигуры (ранг 1)
    pieces_[WHITE][ROOK] = 0x81ULL;
    pieces_[WHITE][KNIGHT] = 0x42ULL;
    pieces_[WHITE][BISHOP] = 0x24ULL;
    pieces_[WHITE][QUEEN] = 0x8ULL;
    pieces_[WHITE][KING] = 0x10ULL;
    
    // Черные фигуры (ранг 8)
    pieces_[BLACK][ROOK] = 0x8100000000000000ULL;
    pieces_[BLACK][KNIGHT] = 0x4200000000000000ULL;
    pieces_[BLACK][BISHOP] = 0x2400000000000000ULL;
    pieces_[BLACK][QUEEN] = 0x800000000000000ULL;
    pieces_[BLACK][KING] = 0x1000000000000000ULL;
    
    // Обновляем occupancy bitboards
    for (int color = 0; color < COLOR_COUNT; color++) {
        occupancy_[color] = 0;
        for (int piece = 0; piece < PIECE_TYPE_COUNT; piece++) {
            occupancy_[color] |= pieces_[color][piece];
        }
    }
    
    all_pieces_ = occupancy_[WHITE] | occupancy_[BLACK];
    side_to_move_ = WHITE;
}

bool Bitboard::isEmpty(int square) const {
    return !BitboardUtils::getBit(all_pieces_, square);
}

bool Bitboard::isOccupied(int square) const {
    return BitboardUtils::getBit(all_pieces_, square);
}

Bitboard::PieceType Bitboard::getPieceType(int square) const {
    for (int piece = 0; piece < PIECE_TYPE_COUNT; piece++) {
        if (BitboardUtils::getBit(pieces_[WHITE][piece], square)) return static_cast<PieceType>(piece);
        if (BitboardUtils::getBit(pieces_[BLACK][piece], square)) return static_cast<PieceType>(piece);
    }
    return static_cast<PieceType>(PIECE_TYPE_COUNT); // Неверно
}

Bitboard::Color Bitboard::getPieceColor(int square) const {
    if (BitboardUtils::getBit(occupancy_[WHITE], square)) return WHITE;
    if (BitboardUtils::getBit(occupancy_[BLACK], square)) return BLACK;
    return static_cast<Color>(COLOR_COUNT); // Неверно
}

void Bitboard::setPiece(int square, PieceType piece, Color color) {
    // Удаляем любую существующую фигуру на этой клетке
    removePiece(square);
    
    // Устанавливаем новую фигуру
    pieces_[color][piece] = BitboardUtils::setBit(pieces_[color][piece], square);
    occupancy_[color] = BitboardUtils::setBit(occupancy_[color], square);
    all_pieces_ = BitboardUtils::setBit(all_pieces_, square);
}

void Bitboard::removePiece(int square) {
    // Находим и удаляем фигуру
    for (int color = 0; color < COLOR_COUNT; color++) {
        for (int piece = 0; piece < PIECE_TYPE_COUNT; piece++) {
            if (BitboardUtils::getBit(pieces_[color][piece], square)) {
                pieces_[color][piece] = BitboardUtils::clearBit(pieces_[color][piece], square);
                break;
            }
        }
        occupancy_[color] = BitboardUtils::clearBit(occupancy_[color], square);
    }
    all_pieces_ = BitboardUtils::clearBit(all_pieces_, square);
}

Bitboard::PieceType Bitboard::movePiece(int from_square, int to_square) {
    PieceType piece = getPieceType(from_square);
    Color color = getPieceColor(from_square);
    
    if (piece == PIECE_TYPE_COUNT || color == COLOR_COUNT) return PIECE_TYPE_COUNT;

    PieceType captured = getPieceType(to_square);
    
    // Сохраняем состояние для отмены
    MoveState state;
    state.from_square = from_square;
    state.to_square = to_square;
    state.moved_piece = piece;
    state.captured_piece = captured;
    state.moved_color = color;
    state.en_passant_square = en_passant_square_;
    state.half_move_clock = half_move_clock_;
    for (int c = 0; c < COLOR_COUNT; c++) {
        state.castling_rights[c][0] = castling_rights_[c][0];
        state.castling_rights[c][1] = castling_rights_[c][1];
    }
    move_history_.push_back(state);

    // 1. Обработка взятия на проходе
    if (piece == PAWN && to_square == en_passant_square_) {
        captured = PAWN;
        int capture_square = (color == WHITE) ? (to_square - 8) : (to_square + 8);
        removePiece(capture_square);
    }

    // 2. Обработка рокировки (движение ладьи)
    if (piece == KING) {
        int file_diff = (to_square % 8) - (from_square % 8);
        if (file_diff > 1 || file_diff < -1) {
            int rank = from_square / 8;
            if (to_square % 8 == 6) { // Короткая рокировка
                movePiece(rank * 8 + 7, rank * 8 + 5);
            } else if (to_square % 8 == 2) { // Длинная рокировка
                movePiece(rank * 8 + 0, rank * 8 + 3);
            }
        }
        // Сброс прав на рокировку при ходе короля
        castling_rights_[color][0] = castling_rights_[color][1] = false;
    }

    // Сброс прав на рокировку при ходе ладьи
    if (piece == ROOK) {
        int file = from_square % 8;
        if (file == 0) castling_rights_[color][1] = false;
        if (file == 7) castling_rights_[color][0] = false;
    }

    // 3. Обновление en passant square
    int rank_diff = (to_square / 8) - (from_square / 8);
    if (piece == PAWN && (rank_diff == 2 || rank_diff == -2)) {
        en_passant_square_ = (from_square + to_square) / 2;
    } else {
        en_passant_square_ = -1;
    }

    // Выполняем основное перемещение
    removePiece(from_square);
    
    // Обработка превращения (по умолчанию в ферзя)
    if (piece == PAWN && (to_square / 8 == 0 || to_square / 8 == 7)) {
        setPiece(to_square, QUEEN, color);
    } else {
        setPiece(to_square, piece, color);
    }

    // Смена хода
    side_to_move_ = (side_to_move_ == WHITE) ? BLACK : WHITE;
    if (side_to_move_ == WHITE) full_move_number_++;

    return captured;
}

Bitboard::BitboardType Bitboard::getPawnAttacks(int square, Color color) const {
    BitboardType attacks = 0;
    BitboardType pawn = 1ULL << square;
    
    if (color == WHITE) {
        // Белые пешки атакуют вверх-влево и вверх-вправо
        attacks |= (pawn << 7) & 0x7F7F7F7F7F7F7F7FULL; // Влево
        attacks |= (pawn << 9) & 0xFEFEFEFEFEFEFEFEULL; // Вправо
    } else {
        // Черные пешки атакуют вниз-влево и вниз-вправо
        attacks |= (pawn >> 7) & 0xFEFEFEFEFEFEFEFEULL; // Вправо
        attacks |= (pawn >> 9) & 0x7F7F7F7F7F7F7F7FULL; // Влево
    }
    
    return attacks;
}

Bitboard::BitboardType Bitboard::getKnightAttacks(int square) const {
    BitboardType attacks = 0;
    int rank = square / 8;
    int file = square % 8;
    
    for (int i = 0; i < 8; i++) {
        int new_rank = rank + (BitboardUtils::KNIGHT_DELTAS[i] / 8);
        int new_file = file + (BitboardUtils::KNIGHT_DELTAS[i] % 8);
        
        if (new_rank >= 0 && new_rank < 8 && new_file >= 0 && new_file < 8) {
            int new_square = new_rank * 8 + new_file;
            attacks |= 1ULL << new_square;
        }
    }
    
    return attacks;
}

Bitboard::BitboardType Bitboard::getKingAttacks(int square) const {
    BitboardType attacks = 0;
    int rank = square / 8;
    int file = square % 8;
    
    for (int i = 0; i < 8; i++) {
        int new_rank = rank + (BitboardUtils::KING_DELTAS[i] / 8);
        int new_file = file + (BitboardUtils::KING_DELTAS[i] % 8);
        
        if (new_rank >= 0 && new_rank < 8 && new_file >= 0 && new_file < 8) {
            int new_square = new_rank * 8 + new_file;
            attacks |= 1ULL << new_square;
        }
    }
    
    return attacks;
}

Bitboard::BitboardType Bitboard::getBishopAttacks(int square, BitboardType occupied) const {
    BitboardType attacks = 0;
    int rank = square / 8;
    int file = square % 8;
    
    // Четыре диагональных направления
    for (int dir = 0; dir < 4; dir++) {
        int dr = BitboardUtils::BISHOP_DELTAS[dir] / 8;
        int df = BitboardUtils::BISHOP_DELTAS[dir] % 8;
        
        int r = rank + dr;
        int f = file + df;
        
        while (r >= 0 && r < 8 && f >= 0 && f < 8) {
            int sq = r * 8 + f;
            attacks |= 1ULL << sq;
            
            // Если клетка занята, останавливаемся
            if (BitboardUtils::getBit(occupied, sq)) break;
            
            r += dr;
            f += df;
        }
    }
    
    return attacks;
}

Bitboard::BitboardType Bitboard::getRookAttacks(int square, BitboardType occupied) const {
    BitboardType attacks = 0;
    int rank = square / 8;
    int file = square % 8;
    
    // Четыре ортогональных направления
    for (int dir = 0; dir < 4; dir++) {
        int dr = BitboardUtils::ROOK_DELTAS[dir] / 8;
        int df = BitboardUtils::ROOK_DELTAS[dir] % 8;
        
        int r = rank + dr;
        int f = file + df;
        
        while (r >= 0 && r < 8 && f >= 0 && f < 8) {
            int sq = r * 8 + f;
            attacks |= 1ULL << sq;
            
            // Если клетка занята, останавливаемся
            if (BitboardUtils::getBit(occupied, sq)) break;
            
            r += dr;
            f += df;
        }
    }
    
    return attacks;
}

Bitboard::BitboardType Bitboard::getQueenAttacks(int square, BitboardType occupied) const {
    return getBishopAttacks(square, occupied) | getRookAttacks(square, occupied);
}

std::vector<std::pair<int, int>> Bitboard::generateLegalMoves() const {
    std::vector<std::pair<int, int>> pseudo_moves;
    
    BitboardType us = occupancy_[side_to_move_];
    BitboardType them = occupancy_[side_to_move_ == WHITE ? BLACK : WHITE];
    BitboardType empty = ~all_pieces_;
    
    for (int square = 0; square < 64; square++) {
        if (!BitboardUtils::getBit(us, square)) continue;
        
        PieceType piece = getPieceType(square);
        BitboardType attacks = 0;
        
        if (piece == PAWN) {
            // Тихие ходы пешек
            int dir = (side_to_move_ == WHITE) ? 8 : -8;
            int next_sq = square + dir;
            if (next_sq >= 0 && next_sq < 64 && isEmpty(next_sq)) {
                pseudo_moves.emplace_back(square, next_sq);
                // Двойной ход
                int start_rank = (side_to_move_ == WHITE) ? 1 : 6;
                if (square / 8 == start_rank) {
                    int double_next = next_sq + dir;
                    if (isEmpty(double_next)) pseudo_moves.emplace_back(square, double_next);
                }
            }
            // Взятия пешками
            attacks = getPawnAttacks(square, side_to_move_);
            BitboardType captures = attacks & them;
            if (en_passant_square_ != -1 && (attacks & (1ULL << en_passant_square_))) {
                captures |= (1ULL << en_passant_square_);
            }
            attacks = captures;
        } else if (piece == KNIGHT) {
            attacks = getKnightAttacks(square) & ~us;
        } else if (piece == BISHOP) {
            attacks = getBishopAttacks(square, all_pieces_) & ~us;
        } else if (piece == ROOK) {
            attacks = getRookAttacks(square, all_pieces_) & ~us;
        } else if (piece == QUEEN) {
            attacks = getQueenAttacks(square, all_pieces_) & ~us;
        } else if (piece == KING) {
            attacks = getKingAttacks(square) & ~us;
            // Рокировка (упрощенно добавим псевдо-легально)
            int rank = (side_to_move_ == WHITE) ? 0 : 7;
            if (castling_rights_[side_to_move_][0] && // King side
                isEmpty(rank * 8 + 5) && isEmpty(rank * 8 + 6)) {
                pseudo_moves.emplace_back(square, rank * 8 + 6);
            }
            if (castling_rights_[side_to_move_][1] && // Queen side
                isEmpty(rank * 8 + 1) && isEmpty(rank * 8 + 2) && isEmpty(rank * 8 + 3)) {
                pseudo_moves.emplace_back(square, rank * 8 + 2);
            }
        }
        
        BitboardType targets = attacks;
        while (targets) {
            int to_square = BitboardUtils::lsb(targets);
            pseudo_moves.emplace_back(square, to_square);
            targets &= targets - 1;
        }
    }
    
    // Фильтруем ходы, оставляющие короля под шахом
    std::vector<std::pair<int, int>> legal_moves;
    for (const auto& move : pseudo_moves) {
        Bitboard temp = *this;
        // Мы не можем использовать movePiece напрямую здесь если она меняет side_to_move_
        // Но нам нужно проверить шах для ТЕКУЩЕГО цвета после хода
        
        // Временно реализуем проверку легальности через копирование
        PieceType p = temp.getPieceType(move.first);
        Color c = temp.getPieceColor(move.first);
        
        // Специальная логика для рокировки: нельзя прыгать через битое поле
        if (p == KING && std::abs(move.second % 8 - move.first % 8) > 1) {
            if (isInCheck(c)) continue; // Нельзя из под шаха
            int step = (move.second > move.first) ? 1 : -1;
            Bitboard temp2 = *this;
            temp2.movePiece(move.first, move.first + step);
            if (temp2.isInCheck(c)) continue; // Нельзя через битое поле
        }

        temp.movePiece(move.first, move.second);
        if (!temp.isInCheck(c)) {
            legal_moves.push_back(move);
        }
    }
    
    return legal_moves;
}

bool Bitboard::isInCheck(Color color) const {
    // Находим короля
    BitboardType king_bb = pieces_[color][KING];
    if (!king_bb) return false;
    
    int king_square = BitboardUtils::lsb(king_bb);
    
    // Проверяем атаки противника
    Color opponent = (color == WHITE) ? BLACK : WHITE;
    BitboardType opponent_pieces = occupancy_[opponent];
    
    // Проверяем атаки пешек
    if (getPawnAttacks(king_square, opponent) & pieces_[opponent][PAWN])
        return true;
    
    // Проверяем атаки коней
    if (getKnightAttacks(king_square) & pieces_[opponent][KNIGHT])
        return true;
    
    // Проверяем атаки слонов и ферзей
    if (getBishopAttacks(king_square, all_pieces_) & 
        (pieces_[opponent][BISHOP] | pieces_[opponent][QUEEN]))
        return true;
    
    // Проверяем атаки ладей и ферзей
    if (getRookAttacks(king_square, all_pieces_) & 
        (pieces_[opponent][ROOK] | pieces_[opponent][QUEEN]))
        return true;
    
    // Проверяем атаки королей
    if (getKingAttacks(king_square) & pieces_[opponent][KING])
        return true;
    
    return false;
}

void Bitboard::initMagicBitboards() {
    // Заглушка - в реальной реализации здесь будут инициализированы magic numbers
    // для быстрого вычисления атак слонов и ладей
}

void Bitboard::printBoard() const {
    std::cout << "\n  a b c d e f g h\n";
    for (int rank = 7; rank >= 0; rank--) {
        std::cout << (rank + 1) << " ";
        for (int file = 0; file < 8; file++) {
            int square = rank * 8 + file;
            char piece_char = '.';
            
            if (isOccupied(square)) {
                PieceType piece = getPieceType(square);
                Color color = getPieceColor(square);
                
                switch (piece) {
                    case PAWN: piece_char = 'P'; break;
                    case KNIGHT: piece_char = 'N'; break;
                    case BISHOP: piece_char = 'B'; break;
                    case ROOK: piece_char = 'R'; break;
                    case QUEEN: piece_char = 'Q'; break;
                    case KING: piece_char = 'K'; break;
                    default: piece_char = '?'; break;
                }
                
                if (color == BLACK) {
                    piece_char = tolower(piece_char);
                }
            }
            
            std::cout << piece_char << " ";
        }
        std::cout << (rank + 1) << "\n";
    }
    std::cout << "  a b c d e f g h\n";
    std::cout << "Side to move: " << (side_to_move_ == WHITE ? "White" : "Black") << "\n\n";
}

std::string Bitboard::toFen() const {
    std::string fen;
    int empty_count = 0;
    
    for (int rank = 7; rank >= 0; rank--) {
        for (int file = 0; file < 8; file++) {
            int square = rank * 8 + file;
            
            if (isEmpty(square)) {
                empty_count++;
            } else {
                if (empty_count > 0) {
                    fen += std::to_string(empty_count);
                    empty_count = 0;
                }
                
                PieceType piece = getPieceType(square);
                Color color = getPieceColor(square);
                char piece_char;
                
                switch (piece) {
                    case PAWN: piece_char = 'p'; break;
                    case KNIGHT: piece_char = 'n'; break;
                    case BISHOP: piece_char = 'b'; break;
                    case ROOK: piece_char = 'r'; break;
                    case QUEEN: piece_char = 'q'; break;
                    case KING: piece_char = 'k'; break;
                    default: piece_char = '?'; break;
                }
                
                if (color == WHITE) {
                    piece_char = toupper(piece_char);
                }
                
                fen += piece_char;
            }
        }
        
        if (empty_count > 0) {
            fen += std::to_string(empty_count);
            empty_count = 0;
        }
        
        if (rank > 0) fen += '/';
    }
    
    // Добавляем информацию о стороне, рокировках и т.д.
    fen += " ";
    fen += (side_to_move_ == WHITE) ? "w" : "b";
    fen += " ";
    
    // Рокировки
    bool has_castling = false;
    if (castling_rights_[WHITE][0]) { fen += "K"; has_castling = true; }
    if (castling_rights_[WHITE][1]) { fen += "Q"; has_castling = true; }
    if (castling_rights_[BLACK][0]) { fen += "k"; has_castling = true; }
    if (castling_rights_[BLACK][1]) { fen += "q"; has_castling = true; }
    if (!has_castling) fen += "-";
    
    fen += " ";
    
    // Взятие на проходе
    if (en_passant_square_ >= 0) {
        int file = en_passant_square_ % 8;
        int rank = en_passant_square_ / 8;
        fen += static_cast<char>('a' + file);
        fen += static_cast<char>('1' + rank);
    } else {
        fen += "-";
    }
    
    fen += " ";
    fen += std::to_string(half_move_clock_);
    fen += " ";
    fen += std::to_string(full_move_number_);
    
    return fen;
}

void Bitboard::loadFromFEN(const std::string& fen) {
    // Очистка всех bitboards
    for (int c = 0; c < COLOR_COUNT; c++) {
        for (int p = 0; p < PIECE_TYPE_COUNT; p++) {
            pieces_[c][p] = 0ULL;
        }
        occupancy_[c] = 0ULL;
    }
    all_pieces_ = 0ULL;
    
    std::istringstream ss(fen);
    std::string board_part, side_part, castling_part, ep_part;
    int half_move_clock, full_move_number;
    
    // Разбор FEN: позиция стороны рокировки en-passant полуходы полныеходы
    ss >> board_part >> side_part >> castling_part >> ep_part >> half_move_clock >> full_move_number;
    
    // 1. Расстановка фигур на доске
    int square = 56; // Начинаем с a8 (rank 7, file 0)
    for (char c : board_part) {
        if (c == '/') {
            square -= 16; // Переход на следующую горизонталь (rank)
        } else if (c >= '1' && c <= '8') {
            square += (c - '0'); // Пропуск пустых клеток
        } else {
            // Определяем цвет и тип фигуры
            Color color = isupper(c) ? WHITE : BLACK;
            char piece_char = tolower(c);
            PieceType piece_type;
            
            switch (piece_char) {
                case 'p': piece_type = PAWN; break;
                case 'n': piece_type = KNIGHT; break;
                case 'b': piece_type = BISHOP; break;
                case 'r': piece_type = ROOK; break;
                case 'q': piece_type = QUEEN; break;
                case 'k': piece_type = KING; break;
                default: square++; continue; // Некорректный символ
            }
            
            setPiece(square, piece_type, color);
            square++;
        }
    }
    
    // 2. Определение стороны
    side_to_move_ = (side_part == "w" || side_part == "W") ? WHITE : BLACK;
    
    // 3. Права на рокировку
    castling_rights_[WHITE][0] = castling_rights_[WHITE][1] = false;
    castling_rights_[BLACK][0] = castling_rights_[BLACK][1] = false;
    
    if (castling_part != "-") {
        for (char c : castling_part) {
            if (c == 'K') castling_rights_[WHITE][0] = true; // White kingside
            if (c == 'Q') castling_rights_[WHITE][1] = true; // White queenside
            if (c == 'k') castling_rights_[BLACK][0] = true; // Black kingside
            if (c == 'q') castling_rights_[BLACK][1] = true; // Black queenside
        }
    }
    
    // 4. Взятие на проходе
    if (ep_part != "-" && ep_part.length() >= 2) {
        int file = ep_part[0] - 'a';
        int rank = ep_part[1] - '1';
        en_passant_square_ = rank * 8 + file;
    } else {
        en_passant_square_ = -1;
    }
    
    // 5. Счетчики
    half_move_clock_ = half_move_clock;
    full_move_number_ = full_move_number;
}

void Bitboard::undoMove() {
    if (move_history_.empty()) return;
    
    const MoveState& state = move_history_.back();
    
    // Восстанавливаем фигуру на исходной позиции
    PieceType piece = getPieceType(state.to_square);
    removePiece(state.to_square);
    setPiece(state.from_square, state.moved_piece, state.moved_color);
    
    // Восстанавливаем съеденную фигуру
    if (state.captured_piece != PIECE_TYPE_COUNT) {
        Color opponent_color = (state.moved_color == WHITE) ? BLACK : WHITE;
        setPiece(state.to_square, state.captured_piece, opponent_color);
    }
    
    // Восстанавливаем состояние
    en_passant_square_ = state.en_passant_square;
    half_move_clock_ = state.half_move_clock;
    for (int c = 0; c < COLOR_COUNT; c++) {
        castling_rights_[c][0] = state.castling_rights[c][0];
        castling_rights_[c][1] = state.castling_rights[c][1];
    }
    
    // Возвращаем сторону
    side_to_move_ = state.moved_color;
    
    move_history_.pop_back();
}

bool Bitboard::operator==(const Bitboard& other) const {
    // Сравниваем все bitboards
    for (int color = 0; color < COLOR_COUNT; color++) {
        for (int piece = 0; piece < PIECE_TYPE_COUNT; piece++) {
            if (pieces_[color][piece] != other.pieces_[color][piece])
                return false;
        }
        if (occupancy_[color] != other.occupancy_[color])
            return false;
    }
    
    if (all_pieces_ != other.all_pieces_)
        return false;
    
    if (side_to_move_ != other.side_to_move_)
        return false;
    
    if (en_passant_square_ != other.en_passant_square_)
        return false;
    
    if (half_move_clock_ != other.half_move_clock_)
        return false;
    
    if (full_move_number_ != other.full_move_number_)
        return false;
    
    for (int color = 0; color < COLOR_COUNT; color++) {
        for (int side = 0; side < 2; side++) {
            if (castling_rights_[color][side] != other.castling_rights_[color][side])
                return false;
        }
    }
    
    return true;
}