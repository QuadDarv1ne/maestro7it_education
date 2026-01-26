#ifndef BOARD_HPP
#define BOARD_HPP

#include "piece.hpp"
#include <vector>
#include <string>

// Position on the board (0-63, where 0 is a1, 63 is h8)
typedef int Square;

class Board {
private:
    std::vector<Piece> squares_;  // 64 squares (8x8 board)
    Color currentPlayer_;
    int moveCount_;
    
    // Castling rights
    bool whiteKingSideCastle_;
    bool whiteQueenSideCastle_;
    bool blackKingSideCastle_;
    bool blackQueenSideCastle_;
    
    // En passant square
    Square enPassantSquare_;
    
    // Halfmove clock for 50-move rule
    int halfMoveClock_;
    
public:
    // Constructor
    Board();
    
    // Setup methods
    void setupStartPosition();
    void setupFromFEN(const std::string& fen);
    
    // Getters
    const Piece& getPiece(Square square) const;
    Color getCurrentPlayer() const;
    int getMoveCount() const;
    bool canCastleKingSide(Color color) const;
    bool canCastleQueenSide(Color color) const;
    Square getEnPassantSquare() const;
    int getHalfMoveClock() const;
    
    // Setters
    void setPiece(Square square, const Piece& piece);
    void setCurrentPlayer(Color color);
    void setCastlingRights(bool whiteKingSide, bool whiteQueenSide, 
                          bool blackKingSide, bool blackQueenSide);
    void setEnPassantSquare(Square square);
    void setHalfMoveClock(int clock);
    
    // Board operations
    void makeMove(Square from, Square to);
    void makeMove(const std::string& algebraicNotation);
    bool isValidMove(Square from, Square to) const;
    
    // Utility methods
    Square algebraicToSquare(const std::string& algebraic) const;
    std::string squareToAlgebraic(Square square) const;
    void printBoard() const;
    std::string getFEN() const;
    
    // Game state
    bool isCheck(Color color) const;
    bool isCheckmate(Color color) const;
    bool isStalemate(Color color) const;
    bool isGameOver() const;
    
public:
    // Helper methods
    void initializeEmptyBoard();
    bool isInBounds(Square square) const;
    int rank(Square square) const;  // 0-7 (rank 1-8)
    int file(Square square) const;  // 0-7 (file a-h)
    Square square(int file, int rank) const;
};

// Constants
const int BOARD_SIZE = 8;
const Square INVALID_SQUARE = -1;

#endif // BOARD_HPP