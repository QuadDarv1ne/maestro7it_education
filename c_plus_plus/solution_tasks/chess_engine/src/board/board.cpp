#include "../../include/board.hpp"
#include "../../include/move_generator.hpp"
#include <iostream>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <random>
#include <limits>

Board::Board() {
    initZobrist();
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
    // Сначала очищаем доску
    initializeEmptyBoard();
    
    // Расставляем пешки
    for (int file = 0; file < 8; file++) {
        setPiece(square(file, 1), Piece(PieceType::PAWN, Color::WHITE));
        setPiece(square(file, 6), Piece(PieceType::PAWN, Color::BLACK));
    }
    
    // Расставляем остальные фигуры
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

void Board::pushHistory(Square from, Square to, const Piece& captured, bool isCastling, bool isEnPassant, PieceType promotion, uint64_t hash) {
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
    info.hash = hash;
    
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
        int kingRank = rank(info.from);
        int toFile = file(info.to);
        
        if (toFile == 6) { // Была короткая рокировка
            Square rookFrom = square(7, kingRank);
            Square rookTo = square(5, kingRank);
            setPiece(rookFrom, getPiece(rookTo));
            setPiece(rookTo, Piece());
        } else if (toFile == 2) { // Была длинная рокировка
            Square rookFrom = square(0, kingRank);
            Square rookTo = square(3, kingRank);
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

void Board::makeMove(const Move& move) {
    Piece movingPiece = getPiece(move.from);
    if (movingPiece.isEmpty()) return;
    
    // Сохраняем историю для отмены (включая хеш текущей позиции ПЕРЕД ходом)
    pushHistory(move.from, move.to, getPiece(move.to), move.isCastling, move.isEnPassant, move.promotion, getZobristHash());
    
    // 1. Обработка рокировки
    if (move.isCastling) {
        int r = rank(move.from);
        int toFile = file(move.to);
        
        // Перемещаем ладью
        if (toFile == 6) { // Короткая рокировка
            Square rookFrom = square(7, r);
            Square rookTo = square(5, r);
            setPiece(rookTo, getPiece(rookFrom));
            setPiece(rookFrom, Piece());
        } else if (toFile == 2) { // Длинная рокировка
            Square rookFrom = square(0, r);
            Square rookTo = square(3, r);
            setPiece(rookTo, getPiece(rookFrom));
            setPiece(rookFrom, Piece());
        }
    }
    
    // 2. Обработка взятия на проходе
    if (move.isEnPassant) {
        int toFile = file(move.to);
        int fromRank = rank(move.from);
        Square capturedPawnSquare = square(toFile, fromRank);
        setPiece(capturedPawnSquare, Piece());
    }
    
    // 3. Обработка превращения пешки
    if (move.promotion != PieceType::EMPTY) {
        movingPiece = Piece(move.promotion, movingPiece.getColor());
    }
    
    // Стандартное перемещение фигуры
    setPiece(move.to, movingPiece);
    setPiece(move.from, Piece());
    
    // Обновляем состояние игры (права рокировки, en passant и т.д.)
    updateGameStateAfterMove(move);
    
    // Смена игрока
    currentPlayer_ = Piece::oppositeColor(currentPlayer_);
    
    // Увеличиваем счетчик ходов если ходили черные
    if (currentPlayer_ == Color::WHITE) {
        moveCount_++;
    }
}

void Board::updateGameStateAfterMove(const Move& move) {
    Piece movingPiece = getPiece(move.to);
    if (movingPiece.isEmpty()) return;

    Color color = movingPiece.getColor();
    int fromRank = rank(move.from);
    int fromFile = file(move.from);
    int toRank = rank(move.to);
    int toFile = file(move.to);

    // 1. Обновление прав на рокировку
    // Если пошел король
    if (movingPiece.getType() == PieceType::KING) {
        if (color == Color::WHITE) {
            whiteKingSideCastle_ = whiteQueenSideCastle_ = false;
        } else {
            blackKingSideCastle_ = blackQueenSideCastle_ = false;
        }
    }

    // Если пошла ладья или ее съели
    if (move.from == square(0, 0) || move.to == square(0, 0)) whiteQueenSideCastle_ = false;
    if (move.from == square(7, 0) || move.to == square(7, 0)) whiteKingSideCastle_ = false;
    if (move.from == square(0, 7) || move.to == square(0, 7)) blackQueenSideCastle_ = false;
    if (move.from == square(7, 7) || move.to == square(7, 7)) blackKingSideCastle_ = false;

    // 2. Обновление en passant square
    if (movingPiece.getType() == PieceType::PAWN && std::abs(toRank - fromRank) == 2) {
        enPassantSquare_ = square(fromFile, (fromRank + toRank) / 2);
    } else {
        enPassantSquare_ = INVALID_SQUARE;
    }

    // 3. Обновление счетчика полуходов
    if (movingPiece.getType() == PieceType::PAWN || move.isCapture) {
        halfMoveClock_ = 0;
    } else {
        halfMoveClock_++;
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

void Board::printBoard() const {
    std::cout << "\n  a b c d e f g h\n";
    for (int rank = 7; rank >= 0; rank--) {
        std::cout << rank + 1 << " ";
        for (int file = 0; file < 8; file++) {
            Square sq = square(file, rank);
            const Piece& piece = getPiece(sq);
            
            if (piece.isEmpty()) {
                std::cout << ". ";
            } else {
                char symbol = ' ';
                switch (piece.getType()) {
                    case PieceType::PAWN: symbol = 'P'; break;
                    case PieceType::KNIGHT: symbol = 'N'; break;
                    case PieceType::BISHOP: symbol = 'B'; break;
                    case PieceType::ROOK: symbol = 'R'; break;
                    case PieceType::QUEEN: symbol = 'Q'; break;
                    case PieceType::KING: symbol = 'K'; break;
                    default: symbol = '?'; break;
                }
                
                if (piece.getColor() == Color::BLACK) {
                    symbol = std::tolower(symbol);
                }
                
                std::cout << symbol << " ";
            }
        }
        std::cout << rank + 1 << "\n";
    }
    std::cout << "  a b c d e f g h\n\n";
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

bool Board::isCheck(Color color) const {
    // Находим короля указанного цвета
    Square kingSquare = INVALID_SQUARE;
    for (int square = 0; square < 64; square++) {
        const Piece& piece = getPiece(square);
        if (piece.getType() == PieceType::KING && piece.getColor() == color) {
            kingSquare = square;
            break;
        }
    }
    
    if (kingSquare == INVALID_SQUARE) return false;
    
    MoveGenerator moveGen(*this);
    Color opponentColor = (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
    return moveGen.isSquareAttacked(kingSquare, opponentColor);
}

bool Board::isCheckmate(Color color) const {
    if (!isCheck(color)) return false;
    
    MoveGenerator moveGen(*this);
    std::vector<Move> legalMoves = moveGen.generateLegalMoves();
    
    // Если нет легальных ходов (generateLegalMoves уже фильтрует те, что оставляют под шахом)
    for (const Move& move : legalMoves) {
        if (getPiece(move.from).getColor() == color) {
            return false;
        }
    }
    
    return true;
}

bool Board::isStalemate(Color color) const {
    if (isCheck(color)) return false;
    
    MoveGenerator moveGen(*this);
    std::vector<Move> legalMoves = moveGen.generateLegalMoves();
    
    for (const Move& move : legalMoves) {
        if (getPiece(move.from).getColor() == color) {
            return false;
        }
    }
    
    return true;
}

bool Board::isGameOver() const {
    return isCheckmate(currentPlayer_) || isStalemate(currentPlayer_) || halfMoveClock_ >= 100 || isRepetition();
}

void Board::initZobrist() {
    std::mt19937_64 rng(123456789);
    std::uniform_int_distribution<uint64_t> dist(0, std::numeric_limits<uint64_t>::max());
    
    for (int i = 0; i < 64; i++) {
        for (int j = 0; j < 12; j++) {
            zobristTable[i][j] = dist(rng);
        }
    }
    
    zobristBlackToMove = dist(rng);
    
    for (int i = 0; i < 16; i++) {
        zobristCastling[i] = dist(rng);
    }
    
    for (int i = 0; i < 8; i++) {
        zobristEnPassant[i] = dist(rng);
    }
}

uint64_t Board::getZobristHash() const {
    uint64_t hash = 0;
    
    for (int square = 0; square < 64; square++) {
        const Piece& piece = getPiece(square);
        if (!piece.isEmpty()) {
            int pieceIdx = static_cast<int>(piece.getType()) - 1;
            if (piece.getColor() == Color::BLACK) pieceIdx += 6;
            hash ^= zobristTable[square][pieceIdx];
        }
    }
    
    if (currentPlayer_ == Color::BLACK) {
        hash ^= zobristBlackToMove;
    }
    
    int castlingIdx = 0;
    if (whiteKingSideCastle_) castlingIdx |= 1;
    if (whiteQueenSideCastle_) castlingIdx |= 2;
    if (blackKingSideCastle_) castlingIdx |= 4;
    if (blackQueenSideCastle_) castlingIdx |= 8;
    hash ^= zobristCastling[castlingIdx];
    
    if (enPassantSquare_ != INVALID_SQUARE) {
        hash ^= zobristEnPassant[file(enPassantSquare_)];
    }
    
    return hash;
}

bool Board::isRepetition() const {
    if (history_.empty()) return false;
    
    uint64_t currentHash = getZobristHash();
    int count = 1;
    
    // Проверяем историю. Нам нужно найти 2 таких же хеша (для 3-кратного повторения)
    // Но учитываем, что в истории хранятся хеши ПЕРЕД ходом.
    for (int i = history_.size() - 1; i >= 0; i--) {
        if (history_[i].hash == currentHash) {
            count++;
            if (count >= 3) return true;
        }
        
        // Оптимизация: сброс при необратимых ходах (взятие или ход пешки)
        // Если в истории был ход пешки или взятие, повторение до этого момента невозможно
        const Piece& captured = history_[i].capturedPiece;
        // Мы не знаем точно была ли это пешка, если только не сохранили тип двигавшейся фигуры
        // Но мы можем посмотреть в history_[i].from на текущей доске? Нет, доска изменилась.
        // Упростим: если halfMoveClock сбросился, то повторение невозможно.
        if (history_[i].halfMoveClock == 0) break;
    }
    
    return false;
}