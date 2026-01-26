#include "../include/move_generator.hpp"
#include <algorithm>

MoveGenerator::MoveGenerator(const Board& board) : board_(board) {}

std::vector<Move> MoveGenerator::generateLegalMoves() const {
    std::vector<Move> pseudoLegalMoves = generatePseudoLegalMoves();
    std::vector<Move> legalMoves;
    
    // Фильтруем только легальные ходы (не оставляющие короля под шахом)
    for (const Move& move : pseudoLegalMoves) {
        if (isLegalMove(move)) {
            legalMoves.push_back(move);
        }
    }
    
    return legalMoves;
}

std::vector<Move> MoveGenerator::generatePseudoLegalMoves() const {
    std::vector<Move> moves;
    Color currentPlayer = board_.getCurrentPlayer();
    
    // Генерируем ходы для каждой фигуры текущего игрока
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getColor() == currentPlayer && !piece.isEmpty()) {
            std::vector<Move> pieceMoves;
            
            switch (piece.getType()) {
                case PieceType::PAWN:
                    pieceMoves = generatePawnMoves(square);
                    break;
                case PieceType::KNIGHT:
                    pieceMoves = generateKnightMoves(square);
                    break;
                case PieceType::BISHOP:
                    pieceMoves = generateBishopMoves(square);
                    break;
                case PieceType::ROOK:
                    pieceMoves = generateRookMoves(square);
                    break;
                case PieceType::QUEEN:
                    pieceMoves = generateQueenMoves(square);
                    break;
                case PieceType::KING:
                    pieceMoves = generateKingMoves(square);
                    break;
                default:
                    break;
            }
            
            moves.insert(moves.end(), pieceMoves.begin(), pieceMoves.end());
        }
    }
    
    // Добавляем специальные ходы
    std::vector<Move> specialMoves = generateCastlingMoves();
    moves.insert(moves.end(), specialMoves.begin(), specialMoves.end());
    
    specialMoves = generateEnPassantMoves();
    moves.insert(moves.end(), specialMoves.begin(), specialMoves.end());
    
    return moves;
}

bool MoveGenerator::isLegalMove(const Move& move) const {
    // Проверяем, не оставляет ли ход короля под шахом
    return !wouldBeInCheck(move.from, move.to);
}

std::vector<Move> MoveGenerator::generatePawnMoves(Square from) const {
    std::vector<Move> moves;
    Piece pawn = board_.getPiece(from);
    Color color = pawn.getColor();
    int direction = (color == Color::WHITE) ? 1 : -1;
    
    // Одиночный ход вперед
    int rank = board_.rank(from);
    int file = board_.file(from);
    Square singleForward = board_.square(file, rank + direction);
    
    if (isValidSquare(singleForward) && board_.getPiece(singleForward).isEmpty()) {
        Move move(from, singleForward);
        
        // Превращение пешки
        if ((color == Color::WHITE && rank + direction == 7) ||
            (color == Color::BLACK && rank + direction == 0)) {
            // Добавляем все возможные превращения
            for (PieceType promotion : {PieceType::QUEEN, PieceType::ROOK, 
                                      PieceType::BISHOP, PieceType::KNIGHT}) {
                Move promotionMove = move;
                promotionMove.promotion = promotion;
                moves.push_back(promotionMove);
            }
        } else {
            moves.push_back(move);
        }
        
        // Двойной ход с начальной позиции
        if ((color == Color::WHITE && rank == 1) || 
            (color == Color::BLACK && rank == 6)) {
            Square doubleForward = board_.square(file, rank + 2 * direction);
            if (board_.getPiece(doubleForward).isEmpty()) {
                Move doubleMove(from, doubleForward);
                moves.push_back(doubleMove);
            }
        }
    }
    
    // Взятия по диагонали
    for (int df : {-1, 1}) {
        int newFile = file + df;
        if (newFile >= 0 && newFile < 8) {
            Square captureSquare = board_.square(newFile, rank + direction);
            Piece target = board_.getPiece(captureSquare);
            
            if (isValidSquare(captureSquare) && 
                !target.isEmpty() && 
                target.getColor() != color) {
                Move captureMove(from, captureSquare);
                captureMove.isCapture = true;
                
                // Превращение при взятии
                if ((color == Color::WHITE && rank + direction == 7) ||
                    (color == Color::BLACK && rank + direction == 0)) {
                    for (PieceType promotion : {PieceType::QUEEN, PieceType::ROOK, 
                                              PieceType::BISHOP, PieceType::KNIGHT}) {
                        Move promotionCapture = captureMove;
                        promotionCapture.promotion = promotion;
                        moves.push_back(promotionCapture);
                    }
                } else {
                    moves.push_back(captureMove);
                }
            }
        }
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateKnightMoves(Square from) const {
    std::vector<Move> moves;
    Piece knight = board_.getPiece(from);
    Color color = knight.getColor();
    
    int knightMoves[8][2] = {
        {-2, -1}, {-2, 1}, {-1, -2}, {-1, 2},
        {1, -2}, {1, 2}, {2, -1}, {2, 1}
    };
    
    int fromRank = board_.rank(from);
    int fromFile = board_.file(from);
    
    for (int i = 0; i < 8; i++) {
        int newRank = fromRank + knightMoves[i][0];
        int newFile = fromFile + knightMoves[i][1];
        
        if (newRank >= 0 && newRank < 8 && newFile >= 0 && newFile < 8) {
            Square to = board_.square(newFile, newRank);
            Piece target = board_.getPiece(to);
            
            if (target.isEmpty() || target.getColor() != color) {
                Move move(from, to);
                if (!target.isEmpty()) {
                    move.isCapture = true;
                }
                moves.push_back(move);
            }
        }
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateBishopMoves(Square from) const {
    std::vector<Move> moves;
    
    // Диагональные направления
    int directions[4][2] = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    
    for (int i = 0; i < 4; i++) {
        std::vector<Move> directionMoves = addMovesInDirection(from, 
                                                              directions[i][0], 
                                                              directions[i][1]);
        moves.insert(moves.end(), directionMoves.begin(), directionMoves.end());
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateRookMoves(Square from) const {
    std::vector<Move> moves;
    
    // Ортогональные направления
    int directions[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    
    for (int i = 0; i < 4; i++) {
        std::vector<Move> directionMoves = addMovesInDirection(from, 
                                                              directions[i][0], 
                                                              directions[i][1]);
        moves.insert(moves.end(), directionMoves.begin(), directionMoves.end());
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateQueenMoves(Square from) const {
    std::vector<Move> moves;
    
    // Все 8 направлений (ортогональные + диагональные)
    int directions[8][2] = {
        {0, 1}, {0, -1}, {1, 0}, {-1, 0},  // Ортогональные
        {1, 1}, {1, -1}, {-1, 1}, {-1, -1} // Диагональные
    };
    
    for (int i = 0; i < 8; i++) {
        std::vector<Move> directionMoves = addMovesInDirection(from, 
                                                              directions[i][0], 
                                                              directions[i][1]);
        moves.insert(moves.end(), directionMoves.begin(), directionMoves.end());
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::generateKingMoves(Square from) const {
    std::vector<Move> moves;
    Piece king = board_.getPiece(from);
    Color color = king.getColor();
    
    // Все 8 направлений вокруг короля
    int directions[8][2] = {
        {0, 1}, {0, -1}, {1, 0}, {-1, 0},
        {1, 1}, {1, -1}, {-1, 1}, {-1, -1}
    };
    
    int fromRank = board_.rank(from);
    int fromFile = board_.file(from);
    
    for (int i = 0; i < 8; i++) {
        int newRank = fromRank + directions[i][0];
        int newFile = fromFile + directions[i][1];
        
        if (newRank >= 0 && newRank < 8 && newFile >= 0 && newFile < 8) {
            Square to = board_.square(newFile, newRank);
            Piece target = board_.getPiece(to);
            
            if (target.isEmpty() || target.getColor() != color) {
                Move move(from, to);
                if (!target.isEmpty()) {
                    move.isCapture = true;
                }
                moves.push_back(move);
            }
        }
    }
    
    return moves;
}

std::vector<Move> MoveGenerator::addMovesInDirection(Square from, int fileDelta, int rankDelta) const {
    std::vector<Move> moves;
    Piece piece = board_.getPiece(from);
    Color color = piece.getColor();
    
    int currentRank = board_.rank(from);
    int currentFile = board_.file(from);
    
    for (int i = 1; i < 8; i++) {
        int newRank = currentRank + i * rankDelta;
        int newFile = currentFile + i * fileDelta;
        
        if (newRank < 0 || newRank >= 8 || newFile < 0 || newFile >= 8) {
            break;
        }
        
        Square to = board_.square(newFile, newRank);
        Piece target = board_.getPiece(to);
        
        if (target.isEmpty()) {
            moves.push_back(Move(from, to));
        } else {
            if (target.getColor() != color) {
                Move captureMove(from, to);
                captureMove.isCapture = true;
                moves.push_back(captureMove);
            }
            break; // Останавливаемся при встрече фигуры
        }
    }
    
    return moves;
}

bool MoveGenerator::isValidSquare(Square square) const {
    return square >= 0 && square < 64;
}

bool MoveGenerator::isOpponentPiece(Square square) const {
    Piece piece = board_.getPiece(square);
    return !piece.isEmpty() && piece.getColor() != board_.getCurrentPlayer();
}

bool MoveGenerator::isEmptySquare(Square square) const {
    return board_.getPiece(square).isEmpty();
}

// Заглушки для специальных ходов (будут реализованы позже)
std::vector<Move> MoveGenerator::generateCastlingMoves() const {
    return std::vector<Move>(); // TODO: реализовать рокировку
}

std::vector<Move> MoveGenerator::generateEnPassantMoves() const {
    return std::vector<Move>(); // TODO: реализовать взятие на проходе
}

bool MoveGenerator::wouldBeInCheck(Square from, Square to) const {
    return false; // TODO: реализовать проверку шаха
}

bool MoveGenerator::isSquareAttacked(Square square, Color byColor) const {
    return false; // TODO: реализовать проверку атаки
}