#include "../include/piece.hpp"
#include <map>

Piece::Piece() : type_(PieceType::EMPTY), color_(Color::WHITE) {}

Piece::Piece(PieceType type, Color color) : type_(type), color_(color) {}

PieceType Piece::getType() const {
    return type_;
}

Color Piece::getColor() const {
    return color_;
}

bool Piece::isEmpty() const {
    return type_ == PieceType::EMPTY;
}

void Piece::setType(PieceType type) {
    type_ = type;
}

void Piece::setColor(Color color) {
    color_ = color;
}

char Piece::getSymbol() const {
    if (type_ == PieceType::EMPTY) return '.';
    
    char symbols[] = {'.', 'P', 'N', 'B', 'R', 'Q', 'K'};
    char symbol = symbols[static_cast<int>(type_)];
    
    return (color_ == Color::WHITE) ? symbol : static_cast<char>(symbol + 32);
}

std::string Piece::getName() const {
    switch (type_) {
        case PieceType::EMPTY: return "Empty";
        case PieceType::PAWN: return (color_ == Color::WHITE) ? "White Pawn" : "Black Pawn";
        case PieceType::KNIGHT: return (color_ == Color::WHITE) ? "White Knight" : "Black Knight";
        case PieceType::BISHOP: return (color_ == Color::WHITE) ? "White Bishop" : "Black Bishop";
        case PieceType::ROOK: return (color_ == Color::WHITE) ? "White Rook" : "Black Rook";
        case PieceType::QUEEN: return (color_ == Color::WHITE) ? "White Queen" : "Black Queen";
        case PieceType::KING: return (color_ == Color::WHITE) ? "White King" : "Black King";
        default: return "Unknown";
    }
}

int Piece::getValue() const {
    switch (type_) {
        case PieceType::EMPTY: return 0;
        case PieceType::PAWN: return 100;      // 1.0 пешки
        case PieceType::KNIGHT: return 320;    // 3.2 пешки
        case PieceType::BISHOP: return 330;    // 3.3 пешки
        case PieceType::ROOK: return 500;      // 5.0 пешок
        case PieceType::QUEEN: return 900;     // 9.0 пешок
        case PieceType::KING: return 20000;    // Король имеет бесконечную ценность (конец игры)
        default: return 0;
    }
}

bool Piece::operator==(const Piece& other) const {
    return type_ == other.type_ && color_ == other.color_;
}

bool Piece::operator!=(const Piece& other) const {
    return !(*this == other);
}

Piece Piece::createPiece(char symbol) {
    std::map<char, std::pair<PieceType, Color>> pieceMap = {
        {'P', {PieceType::PAWN, Color::WHITE}},
        {'N', {PieceType::KNIGHT, Color::WHITE}},
        {'B', {PieceType::BISHOP, Color::WHITE}},
        {'R', {PieceType::ROOK, Color::WHITE}},
        {'Q', {PieceType::QUEEN, Color::WHITE}},
        {'K', {PieceType::KING, Color::WHITE}},
        {'p', {PieceType::PAWN, Color::BLACK}},
        {'n', {PieceType::KNIGHT, Color::BLACK}},
        {'b', {PieceType::BISHOP, Color::BLACK}},
        {'r', {PieceType::ROOK, Color::BLACK}},
        {'q', {PieceType::QUEEN, Color::BLACK}},
        {'k', {PieceType::KING, Color::BLACK}},
        {'.', {PieceType::EMPTY, Color::WHITE}}
    };
    
    auto it = pieceMap.find(symbol);
    if (it != pieceMap.end()) {
        return Piece(it->second.first, it->second.second);
    }
    return Piece(); // Возвращаем пустую фигуру, если не найдена
}

Color Piece::oppositeColor(Color color) {
    return (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
}

std::ostream& operator<<(std::ostream& os, const Piece& piece) {
    os << piece.getSymbol();
    return os;
}