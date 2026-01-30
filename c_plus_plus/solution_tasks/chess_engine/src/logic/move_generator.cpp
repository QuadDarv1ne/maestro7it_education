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

// Генерация ходов рокировки
std::vector<Move> MoveGenerator::generateCastlingMoves() const {
    std::vector<Move> moves;
    Color currentPlayer = board_.getCurrentPlayer();
    
    // Проверяем, что король не находится под шахом
    Square kingSquare = findKingSquare(currentPlayer);
    if (kingSquare == -1 || isSquareAttacked(kingSquare, oppositeColor(currentPlayer))) {
        return moves; // Рокировка невозможна если король под шахом
    }
    
    int homeRank = (currentPlayer == Color::WHITE) ? 0 : 7;
    
    // Короткая рокировка (kingside)
    if (canCastleKingside(currentPlayer)) {
        Square kingFrom = board_.square(4, homeRank);
        Square kingTo = board_.square(6, homeRank);
        Square rookFrom = board_.square(7, homeRank);
        
        // Проверяем что клетки между королем и ладьей пусты
        bool pathClear = board_.getPiece(board_.square(5, homeRank)).isEmpty() &&
                        board_.getPiece(board_.square(6, homeRank)).isEmpty();
        
        // Проверяем что проходимые королем клетки не атакованы
        bool pathSafe = !isSquareAttacked(board_.square(5, homeRank), oppositeColor(currentPlayer)) &&
                       !isSquareAttacked(board_.square(6, homeRank), oppositeColor(currentPlayer));
        
        if (pathClear && pathSafe) {
            Move castlingMove(kingFrom, kingTo);
            castlingMove.isCastling = true;
            moves.push_back(castlingMove);
        }
    }
    
    // Длинная рокировка (queenside)
    if (canCastleQueenside(currentPlayer)) {
        Square kingFrom = board_.square(4, homeRank);
        Square kingTo = board_.square(2, homeRank);
        Square rookFrom = board_.square(0, homeRank);
        
        // Проверяем что клетки между королем и ладьей пусты
        bool pathClear = board_.getPiece(board_.square(1, homeRank)).isEmpty() &&
                        board_.getPiece(board_.square(2, homeRank)).isEmpty() &&
                        board_.getPiece(board_.square(3, homeRank)).isEmpty();
        
        // Проверяем что проходимые королем клетки не атакованы
        bool pathSafe = !isSquareAttacked(board_.square(2, homeRank), oppositeColor(currentPlayer)) &&
                       !isSquareAttacked(board_.square(3, homeRank), oppositeColor(currentPlayer));
        
        if (pathClear && pathSafe) {
            Move castlingMove(kingFrom, kingTo);
            castlingMove.isCastling = true;
            moves.push_back(castlingMove);
        }
    }
    
    return moves;
}

// Вспомогательные функции для рокировки
bool MoveGenerator::canCastleKingside(Color color) const {
    // Проверка прав на рокировку через Board API
    // Предполагается что Board имеет методы для отслеживания прав на рокировку
    return board_.canCastleKingSide(color);
}

bool MoveGenerator::canCastleQueenside(Color color) const {
    return board_.canCastleQueenSide(color);
}

Square MoveGenerator::findKingSquare(Color color) const {
    // Поиск позиции короля на доске
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() == PieceType::KING && piece.getColor() == color) {
            return square;
        }
    }
    return -1; // Король не найден (некорректная позиция)
}

Color MoveGenerator::oppositeColor(Color color) const {
    return (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
}

// Генерация ходов взятия на проходе
std::vector<Move> MoveGenerator::generateEnPassantMoves() const {
    std::vector<Move> moves;
    Color currentPlayer = board_.getCurrentPlayer();
    Square enPassantSquare = board_.getEnPassantSquare();
    
    // Если нет возможности взятия на проходе
    if (enPassantSquare == -1) {
        return moves;
    }
    
    int targetRank = board_.rank(enPassantSquare);
    int targetFile = board_.file(enPassantSquare);
    int direction = (currentPlayer == Color::WHITE) ? 1 : -1;
    int pawnRank = (currentPlayer == Color::WHITE) ? 4 : 3; // Пешки на 5-й/4-й горизонтали
    
    // Проверяем пешки слева и справа от целевой клетки
    for (int df : {-1, 1}) {
        int attackerFile = targetFile + df;
        
        if (attackerFile >= 0 && attackerFile < 8) {
            Square attackerSquare = board_.square(attackerFile, pawnRank);
            Piece attacker = board_.getPiece(attackerSquare);
            
            // Проверяем что это пешка текущего игрока
            if (attacker.getType() == PieceType::PAWN && 
                attacker.getColor() == currentPlayer) {
                
                Move enPassantMove(attackerSquare, enPassantSquare);
                enPassantMove.isCapture = true;
                enPassantMove.isEnPassant = true;
                moves.push_back(enPassantMove);
            }
        }
    }
    
    return moves;
}

// Проверка, оставляет ли ход короля под шахом
bool MoveGenerator::wouldBeInCheck(Square from, Square to) const {
    // Создаем временную копию доски и выполняем ход
    Board tempBoard = board_;
    Piece movingPiece = tempBoard.getPiece(from);
    Color playerColor = movingPiece.getColor();
    
    // Выполняем ход на временной доске
    tempBoard.setPiece(to, movingPiece);
    tempBoard.setPiece(from, Piece()); // Пустая клетка
    
    // Находим позицию короля после хода
    Square kingSquare = -1;
    if (movingPiece.getType() == PieceType::KING) {
        kingSquare = to; // Король переместился
    } else {
        // Ищем короля на доске
        for (int sq = 0; sq < 64; sq++) {
            Piece piece = tempBoard.getPiece(sq);
            if (piece.getType() == PieceType::KING && piece.getColor() == playerColor) {
                kingSquare = sq;
                break;
            }
        }
    }
    
    if (kingSquare == -1) {
        return true; // Король не найден - критическая ошибка, считаем что под шахом
    }
    
    // Проверяем, атакована ли клетка короля противником
    return isSquareAttackedOnBoard(tempBoard, kingSquare, oppositeColor(playerColor));
}

// Проверка атаки клетки определенным цветом
bool MoveGenerator::isSquareAttacked(Square square, Color byColor) const {
    return isSquareAttackedOnBoard(board_, square, byColor);
}

// Проверка атаки клетки на заданной доске
bool MoveGenerator::isSquareAttackedOnBoard(const Board& board, Square square, Color byColor) const {
    int targetRank = board.rank(square);
    int targetFile = board.file(square);
    
    // Проверяем атаки пешек
    int pawnDirection = (byColor == Color::WHITE) ? 1 : -1;
    for (int df : {-1, 1}) {
        int attackRank = targetRank - pawnDirection;
        int attackFile = targetFile + df;
        
        if (attackRank >= 0 && attackRank < 8 && attackFile >= 0 && attackFile < 8) {
            Square attackSquare = board.square(attackFile, attackRank);
            Piece piece = board.getPiece(attackSquare);
            
            if (piece.getType() == PieceType::PAWN && piece.getColor() == byColor) {
                return true;
            }
        }
    }
    
    // Проверяем атаки коня
    int knightMoves[8][2] = {
        {-2, -1}, {-2, 1}, {-1, -2}, {-1, 2},
        {1, -2}, {1, 2}, {2, -1}, {2, 1}
    };
    
    for (int i = 0; i < 8; i++) {
        int attackRank = targetRank + knightMoves[i][0];
        int attackFile = targetFile + knightMoves[i][1];
        
        if (attackRank >= 0 && attackRank < 8 && attackFile >= 0 && attackFile < 8) {
            Square attackSquare = board.square(attackFile, attackRank);
            Piece piece = board.getPiece(attackSquare);
            
            if (piece.getType() == PieceType::KNIGHT && piece.getColor() == byColor) {
                return true;
            }
        }
    }
    
    // Проверяем атаки по диагоналям (слон, ферзь)
    int diagonalDirections[4][2] = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    for (int i = 0; i < 4; i++) {
        if (isAttackedInDirection(board, square, diagonalDirections[i][0], 
                                 diagonalDirections[i][1], byColor, true)) {
            return true;
        }
    }
    
    // Проверяем атаки по вертикали/горизонтали (ладья, ферзь)
    int orthogonalDirections[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    for (int i = 0; i < 4; i++) {
        if (isAttackedInDirection(board, square, orthogonalDirections[i][0], 
                                 orthogonalDirections[i][1], byColor, false)) {
            return true;
        }
    }
    
    // Проверяем атаки короля (на расстоянии 1 клетки)
    int kingDirections[8][2] = {
        {0, 1}, {0, -1}, {1, 0}, {-1, 0},
        {1, 1}, {1, -1}, {-1, 1}, {-1, -1}
    };
    
    for (int i = 0; i < 8; i++) {
        int attackRank = targetRank + kingDirections[i][0];
        int attackFile = targetFile + kingDirections[i][1];
        
        if (attackRank >= 0 && attackRank < 8 && attackFile >= 0 && attackFile < 8) {
            Square attackSquare = board.square(attackFile, attackRank);
            Piece piece = board.getPiece(attackSquare);
            
            if (piece.getType() == PieceType::KING && piece.getColor() == byColor) {
                return true;
            }
        }
    }
    
    return false;
}

// Проверка атаки в определенном направлении
bool MoveGenerator::isAttackedInDirection(const Board& board, Square square, 
                                          int rankDelta, int fileDelta, 
                                          Color byColor, bool diagonal) const {
    int currentRank = board.rank(square);
    int currentFile = board.file(square);
    
    for (int i = 1; i < 8; i++) {
        int attackRank = currentRank + i * rankDelta;
        int attackFile = currentFile + i * fileDelta;
        
        if (attackRank < 0 || attackRank >= 8 || attackFile < 0 || attackFile >= 8) {
            break;
        }
        
        Square attackSquare = board.square(attackFile, attackRank);
        Piece piece = board.getPiece(attackSquare);
        
        if (!piece.isEmpty()) {
            if (piece.getColor() == byColor) {
                // Проверяем тип фигуры
                if (diagonal) {
                    // Диагональная атака: слон или ферзь
                    if (piece.getType() == PieceType::BISHOP || 
                        piece.getType() == PieceType::QUEEN) {
                        return true;
                    }
                } else {
                    // Ортогональная атака: ладья или ферзь
                    if (piece.getType() == PieceType::ROOK || 
                        piece.getType() == PieceType::QUEEN) {
                        return true;
                    }
                }
            }
            break; // Фигура блокирует дальнейшую проверку
        }
    }
    
    return false;
}