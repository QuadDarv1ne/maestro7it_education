#ifndef PIECE_HPP
#define PIECE_HPP

#include <iostream>
#include <string>

enum class PieceType {
    EMPTY = 0,
    PAWN = 1,
    KNIGHT = 2,
    BISHOP = 3,
    ROOK = 4,
    QUEEN = 5,
    KING = 6
};

enum class Color {
    WHITE = 0,
    BLACK = 1
};

class Piece {
private:
    PieceType type_;
    Color color_;

public:
    // Constructors
    Piece();
    Piece(PieceType type, Color color);
    
    // Getters
    PieceType getType() const;
    Color getColor() const;
    bool isEmpty() const;
    
    // Setters
    void setType(PieceType type);
    void setColor(Color color);
    
    // Utility methods
    char getSymbol() const;
    std::string getName() const;
    int getValue() const;
    
    // Operators
    bool operator==(const Piece& other) const;
    bool operator!=(const Piece& other) const;
    
    // Static utility methods
    static Piece createPiece(char symbol);
    static Color oppositeColor(Color color);
};

// Helper functions
std::ostream& operator<<(std::ostream& os, const Piece& piece);

#endif // PIECE_HPP