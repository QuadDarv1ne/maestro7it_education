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

void Board::printBoard() const {
    std::cout << "\n  a b c d e f g h\n";
    std::cout << " +-----------------+\n";
    
    for (int rank = 7; rank >= 0; rank--) {
        std::cout << (rank + 1) << "| ";
        for (int file = 0; file < 8; file++) {
            Square sq = square(file, rank);
            std::cout << getPiece(sq) << " ";
        }
        std::cout << "|" << (rank + 1) << "\n";
    }
    
    std::cout << " +-----------------+\n";
    std::cout << "  a b c d e f g h\n";
    std::cout << "\nCurrent player: " << (currentPlayer_ == Color::WHITE ? "White" : "Black") << "\n";
}