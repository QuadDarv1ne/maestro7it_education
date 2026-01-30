#include "../include/board.hpp"
#include <iostream>
#include <sstream>
#include <algorithm>
#include <cctype>

Board::Board() {
    initializeEmptyBoard();
    setupStartPosition();
}

void Board::initializeEmptyBoard() {
    squares_.assign(64, Piece());
    currentPlayer_ = Color::WHITE;
    moveCount_ = 1;
    whiteKingSideCastle_ = true;
    whiteQueenSideCastle_ = true;
    blackKingSideCastle_ = true;
    blackQueenSideCastle_ = true;
    enPassantSquare_ = INVALID_SQUARE;
    halfMoveClock_ = 0;
}

void Board::setupStartPosition() {
    // Clear the board first
    initializeEmptyBoard();
    
    // Set up pawns
    for (int file = 0; file < 8; file++) {
        setPiece(square(file, 1), Piece(PieceType::PAWN, Color::WHITE));
        setPiece(square(file, 6), Piece(PieceType::PAWN, Color::BLACK));
    }
    
    // Set up other pieces
    Piece pieces[] = {
        Piece(PieceType::ROOK, Color::WHITE),
        Piece(PieceType::KNIGHT, Color::WHITE),
        Piece(PieceType::BISHOP, Color::WHITE),
        Piece(PieceType::QUEEN, Color::WHITE),
        Piece(PieceType::KING, Color::WHITE),
        Piece(PieceType::BISHOP, Color::WHITE),
        Piece(PieceType::KNIGHT, Color::WHITE),
        Piece(PieceType::ROOK, Color::WHITE)
    };
    
    for (int file = 0; file < 8; file++) {
        setPiece(square(file, 0), pieces[file]);
        setPiece(square(file, 7), Piece(pieces[file].getType(), Color::BLACK));
    }
}

const Piece& Board::getPiece(Square square) const {
    if (!isInBounds(square)) {
        static Piece emptyPiece;
        return emptyPiece;
    }
    return squares_[square];
}

Color Board::getCurrentPlayer() const {
    return currentPlayer_;
}

int Board::getMoveCount() const {
    return moveCount_;
}

bool Board::canCastleKingSide(Color color) const {
    return (color == Color::WHITE) ? whiteKingSideCastle_ : blackKingSideCastle_;
}

bool Board::canCastleQueenSide(Color color) const {
    return (color == Color::WHITE) ? whiteQueenSideCastle_ : blackQueenSideCastle_;
}

Square Board::getEnPassantSquare() const {
    return enPassantSquare_;
}

int Board::getHalfMoveClock() const {
    return halfMoveClock_;
}

void Board::setPiece(Square square, const Piece& piece) {
    if (isInBounds(square)) {
        squares_[square] = piece;
    }
}

void Board::setCurrentPlayer(Color color) {
    currentPlayer_ = color;
}

void Board::setCastlingRights(bool whiteKingSide, bool whiteQueenSide, 
                             bool blackKingSide, bool blackQueenSide) {
    whiteKingSideCastle_ = whiteKingSide;
    whiteQueenSideCastle_ = whiteQueenSide;
    blackKingSideCastle_ = blackKingSide;
    blackQueenSideCastle_ = blackQueenSide;
}

void Board::setEnPassantSquare(Square square) {
    enPassantSquare_ = square;
}

void Board::setHalfMoveClock(int clock) {
    halfMoveClock_ = clock;
}

bool Board::isInBounds(Square square) const {
    return square >= 0 && square < 64;
}

int Board::rank(Square square) const {
    return square / 8;
}

int Board::file(Square square) const {
    return square % 8;
}

Square Board::square(int file, int rank) const {
    return rank * 8 + file;
}

Square Board::algebraicToSquare(const std::string& algebraic) const {
    if (algebraic.length() < 2) return INVALID_SQUARE;
    
    char fileChar = std::tolower(algebraic[0]);
    char rankChar = algebraic[1];
    
    if (fileChar < 'a' || fileChar > 'h') return INVALID_SQUARE;
    if (rankChar < '1' || rankChar > '8') return INVALID_SQUARE;
    
    int file = fileChar - 'a';
    int rank = rankChar - '1';
    
    return square(file, rank);
}

std::string Board::squareToAlgebraic(Square square) const {
    if (!isInBounds(square)) return "";
    
    char fileChar = 'a' + file(square);
    char rankChar = '1' + rank(square);
    
    return std::string(1, fileChar) + rankChar;
}

void Board::pushHistory(Square from, Square to, const Piece& captured, bool isCastling, bool isEnPassant, PieceType promotion) {
    UndoInfo info;
    info.from = from;
    info.to = to;
    info.capturedPiece = captured;
    info.whiteKS = whiteKingSideCastle_;
    info.whiteQS = whiteQueenSideCastle_;
    info.blackKS = blackKingSideCastle_;
    info.blackQS = blackQueenSideCastle_;
    info.enPassantSquare = enPassantSquare_;
    info.halfMoveClock = halfMoveClock_;
    info.isCastling = isCastling;
    info.isEnPassant = isEnPassant;
    info.promotion = promotion;
    
    history_.push_back(info);
}

void Board::undoMove() {
    if (history_.empty()) return;
    
    UndoInfo info = history_.back();
    history_.pop_back();
    
    Piece movingPiece = getPiece(info.to);
    
    // 1. Отмена превращения (вернуть пешку)
    if (info.promotion != PieceType::EMPTY) {
        movingPiece = Piece(PieceType::PAWN, movingPiece.getColor());
    }
    
    // 2. Вернуть фигуру на место
    setPiece(info.from, movingPiece);
    setPiece(info.to, info.capturedPiece);
    
    // 3. Отмена рокировки
    if (info.isCastling) {
        int rank = rank(info.from);
        int toFile = file(info.to);
        
        if (toFile == 6) { // Была короткая рокировка
            Square rookFrom = square(7, rank);
            Square rookTo = square(5, rank);
            setPiece(rookFrom, getPiece(rookTo));
            setPiece(rookTo, Piece());
        } else if (toFile == 2) { // Была длинная рокировка
            Square rookFrom = square(0, rank);
            Square rookTo = square(3, rank);
            setPiece(rookFrom, getPiece(rookTo));
            setPiece(rookTo, Piece());
        }
    }
    
    // 4. Отмена взятия на проходе
    if (info.isEnPassant) {
        int fromRank = rank(info.from);
        int toFile = file(info.to);
        Square capturedPawnSquare = square(toFile, fromRank);
        setPiece(capturedPawnSquare, Piece(PieceType::PAWN, Piece::oppositeColor(movingPiece.getColor())));
    }
    
    // 5. Восстановить состояние
    whiteKingSideCastle_ = info.whiteKS;
    whiteQueenSideCastle_ = info.whiteQS;
    blackKingSideCastle_ = info.blackKS;
    blackQueenSideCastle_ = info.blackQS;
    enPassantSquare_ = info.enPassantSquare;
    halfMoveClock_ = info.halfMoveClock;
    
    // Смена игрока
    currentPlayer_ = Piece::oppositeColor(currentPlayer_);
    
    // Уменьшить счетчик ходов если ходили черные (т.е. сейчас опять ход белых)
    if (currentPlayer_ == Color::WHITE) {
        moveCount_--;
    }
}

void Board::makeMove(Square from, Square to) {
    // Эта функция в Board обычно выполняет ход БЕЗ валидации GameRules
    // (для внутреннего использования или когда валидация уже прошла)
    Piece movingPiece = getPiece(from);
    if (movingPiece.isEmpty()) return;
    
    // Для полноценного хода с правилами используйте GameRules::makeMove
    // Здесь мы просто переместим фигуру для базовой функциональности
    pushHistory(from, to, getPiece(to));
    setPiece(to, movingPiece);
    setPiece(from, Piece());
    
    currentPlayer_ = Piece::oppositeColor(currentPlayer_);
    if (currentPlayer_ == Color::WHITE) moveCount_++;
}

void Board::makeMove(const std::string& algebraicNotation) {
    if (algebraicNotation.length() < 4) return;
    Square from = algebraicToSquare(algebraicNotation.substr(0, 2));
    Square to = algebraicToSquare(algebraicNotation.substr(2, 2));
    makeMove(from, to);
}

bool Board::isValidMove(Square from, Square to) const {
    // Базовая проверка границ
    if (!isInBounds(from) || !isInBounds(to)) return false;
    if (getPiece(from).isEmpty()) return false;
    return true;
}

// Загрузка позиции из FEN-нотации
void Board::setupFromFEN(const std::string& fen) {
    initializeEmptyBoard();
    
    std::istringstream fenStream(fen);
    std::string boardPart, turn, castling, enPassant, halfMove, fullMove;
    
    // Разбираем FEN на части
    fenStream >> boardPart >> turn >> castling >> enPassant >> halfMove >> fullMove;
    
    // 1. Разбор расположения фигур
    int rank = 7; // Начинаем с 8-й горизонтали
    int file = 0;
    
    for (char c : boardPart) {
        if (c == '/') {
            rank--;
            file = 0;
        } else if (std::isdigit(c)) {
            // Пропускаем пустые клетки
            file += (c - '0');
        } else {
            // Определяем цвет и тип фигуры
            Color color = std::isupper(c) ? Color::WHITE : Color::BLACK;
            char pieceChar = std::toupper(c);
            
            PieceType type = PieceType::EMPTY;
            switch (pieceChar) {
                case 'P': type = PieceType::PAWN; break;
                case 'N': type = PieceType::KNIGHT; break;
                case 'B': type = PieceType::BISHOP; break;
                case 'R': type = PieceType::ROOK; break;
                case 'Q': type = PieceType::QUEEN; break;
                case 'K': type = PieceType::KING; break;
            }
            
            if (type != PieceType::EMPTY && file < 8) {
                setPiece(square(file, rank), Piece(type, color));
                file++;
            }
        }
    }
    
    // 2. Разбор очередности хода
    if (turn == "w" || turn == "W") {
        currentPlayer_ = Color::WHITE;
    } else {
        currentPlayer_ = Color::BLACK;
    }
    
    // 3. Разбор прав на рокировку
    whiteKingSideCastle_ = false;
    whiteQueenSideCastle_ = false;
    blackKingSideCastle_ = false;
    blackQueenSideCastle_ = false;
    
    for (char c : castling) {
        if (c == 'K') whiteKingSideCastle_ = true;
        if (c == 'Q') whiteQueenSideCastle_ = true;
        if (c == 'k') blackKingSideCastle_ = true;
        if (c == 'q') blackQueenSideCastle_ = true;
    }
    
    // 4. Разбор клетки для взятия на проходе
    if (enPassant != "-") {
        enPassantSquare_ = algebraicToSquare(enPassant);
    } else {
        enPassantSquare_ = INVALID_SQUARE;
    }
    
    // 5. Разбор счетчиков
    try {
        if (!halfMove.empty()) {
            halfMoveClock_ = std::stoi(halfMove);
        }
        if (!fullMove.empty()) {
            moveCount_ = std::stoi(fullMove);
        }
    } catch (...) {
        // Если не удалось разобрать счетчики, оставляем значения по умолчанию
    }
}

// Генерация FEN-нотации из текущей позиции
std::string Board::getFEN() const {
    std::ostringstream fen;
    
    // 1. Расположение фигур
    for (int rank = 7; rank >= 0; rank--) {
        int emptyCount = 0;
        
        for (int file = 0; file < 8; file++) {
            Square sq = square(file, rank);
            const Piece& piece = getPiece(sq);
            
            if (piece.isEmpty()) {
                emptyCount++;
            } else {
                if (emptyCount > 0) {
                    fen << emptyCount;
                    emptyCount = 0;
                }
                
                char pieceChar = ' ';
                switch (piece.getType()) {
                    case PieceType::PAWN: pieceChar = 'P'; break;
                    case PieceType::KNIGHT: pieceChar = 'N'; break;
                    case PieceType::BISHOP: pieceChar = 'B'; break;
                    case PieceType::ROOK: pieceChar = 'R'; break;
                    case PieceType::QUEEN: pieceChar = 'Q'; break;
                    case PieceType::KING: pieceChar = 'K'; break;
                    default: break;
                }
                
                // Черные фигуры в нижнем регистре
                if (piece.getColor() == Color::BLACK) {
                    pieceChar = std::tolower(pieceChar);
                }
                
                fen << pieceChar;
            }
        }
        
        if (emptyCount > 0) {
            fen << emptyCount;
        }
        
        if (rank > 0) {
            fen << '/';
        }
    }
    
    // 2. Очередность хода
    fen << ' ' << (currentPlayer_ == Color::WHITE ? 'w' : 'b');
    
    // 3. Права на рокировку
    fen << ' ';
    std::string castling = "";
    if (whiteKingSideCastle_) castling += 'K';
    if (whiteQueenSideCastle_) castling += 'Q';
    if (blackKingSideCastle_) castling += 'k';
    if (blackQueenSideCastle_) castling += 'q';
    
    if (castling.empty()) {
        fen << '-';
    } else {
        fen << castling;
    }
    
    // 4. Клетка для взятия на проходе
    fen << ' ';
    if (enPassantSquare_ == INVALID_SQUARE) {
        fen << '-';
    } else {
        fen << squareToAlgebraic(enPassantSquare_);
    }
    
    // 5. Счетчики
    fen << ' ' << halfMoveClock_;
    fen << ' ' << moveCount_;
    
    return fen.str();
}