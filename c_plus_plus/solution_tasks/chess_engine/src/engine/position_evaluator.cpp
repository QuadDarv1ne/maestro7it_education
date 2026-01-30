#include "../include/position_evaluator.hpp"

// Таблицы позиционной оценки (упрощенные версии)
const int PositionEvaluator::pawnTable[64] = {
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
};

const int PositionEvaluator::knightTable[64] = {
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
};

const int PositionEvaluator::bishopTable[64] = {
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
};

const int PositionEvaluator::rookTable[64] = {
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
};

const int PositionEvaluator::queenTable[64] = {
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
};

const int PositionEvaluator::kingMiddleGameTable[64] = {
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
};

const int PositionEvaluator::kingEndGameTable[64] = {
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-20,-20,-30,-30,-50
};

PositionEvaluator::PositionEvaluator(const Board& board) : board_(board) {}

int PositionEvaluator::evaluate() const {
    int score = 0;
    
    // Материальная оценка
    score += materialEvaluation();
    
    // Позиционная оценка
    score += positionalEvaluation();
    
    // Оценка мобильности
    score += mobilityEvaluation();
    
    // Оценка безопасности короля
    score += kingSafetyEvaluation();
    
    // Оценка структуры пешек
    score += pawnStructureEvaluation();
    
    // Если текущий игрок - черные, меняем знак (так как белые положительны)
    return (board_.getCurrentPlayer() == Color::WHITE) ? score : -score;
}

int PositionEvaluator::materialEvaluation() const {
    int score = 0;
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (!piece.isEmpty()) {
            int value = piece.getValue(); // Уже масштабировано в Piece::getValue()
            
            // Учитываем цвет
            if (piece.getColor() == Color::WHITE) {
                score += value;
            } else {
                score -= value;
            }
        }
    }
    
    return score;
}

int PositionEvaluator::positionalEvaluation() const {
    int score = 0;
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (!piece.isEmpty()) {
            int posValue = evaluatePiece(piece.getType(), square, piece.getColor());
            
            if (piece.getColor() == Color::WHITE) {
                score += posValue;
            } else {
                score -= posValue;
            }
        }
    }
    
    return score;
}

int PositionEvaluator::mobilityEvaluation() const {
    // Оцениваем количество доступных ходов для каждой стороны
    int whiteMobility = 0;
    int blackMobility = 0;
    
    // Создаем временные доски для оценки мобильности
    Board tempBoard = board_;
    
    // Оцениваем мобильность белых
    tempBoard.setCurrentPlayer(Color::WHITE);
    MoveGenerator whiteGen(tempBoard);
    auto whiteMoves = whiteGen.generateLegalMoves();
    whiteMobility = static_cast<int>(whiteMoves.size());
    
    // Оцениваем мобильность черных
    tempBoard.setCurrentPlayer(Color::BLACK);
    MoveGenerator blackGen(tempBoard);
    auto blackMoves = blackGen.generateLegalMoves();
    blackMobility = static_cast<int>(blackMoves.size());
    
    // Мобильность стоит 10 пунктов за каждый возможный ход
    return (whiteMobility - blackMobility) * 10;
}

int PositionEvaluator::kingSafetyEvaluation() const {
    int score = 0;
    
    // Найдем позиции королей
    Square whiteKingPos = -1;
    Square blackKingPos = -1;
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() == PieceType::KING) {
            if (piece.getColor() == Color::WHITE) {
                whiteKingPos = square;
            } else {
                blackKingPos = square;
            }
        }
    }
    
    // Оцениваем безопасность белого короля
    if (whiteKingPos != -1) {
        int whiteSafety = evaluateKingSafety(whiteKingPos, Color::WHITE);
        score += whiteSafety;
    }
    
    // Оцениваем безопасность черного короля
    if (blackKingPos != -1) {
        int blackSafety = evaluateKingSafety(blackKingPos, Color::BLACK);
        score -= blackSafety; // Для черных со знаком минус
    }
    
    return score;
}

int PositionEvaluator::pawnStructureEvaluation() const {
    int score = 0;
    
    // Оцениваем пешечную структуру для белых
    score += evaluatePawnStructure(Color::WHITE);
    
    // Оцениваем пешечную структуру для черных (со знаком минус)
    score -= evaluatePawnStructure(Color::BLACK);
    
    return score;
}

bool PositionEvaluator::isEndGame() const {
    // Определяем, является ли позиция эндшпилем по количеству фигур
    int piecesCount = 0;
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (!piece.isEmpty() && piece.getType() != PieceType::PAWN && piece.getType() != PieceType::KING) {
            piecesCount++;
        }
    }
    
    // Если мало фигур кроме пешек и королей, это эндшпиль
    return piecesCount <= 6;
}

int PositionEvaluator::getGamePhase() const {
    // Определяем фазу игры (от 0 до 24, где 24 - начальная фаза)
    int phase = 0;
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (!piece.isEmpty()) {
            switch (piece.getType()) {
                case PieceType::PAWN:   phase += 0; break;
                case PieceType::KNIGHT: phase += 1; break;
                case PieceType::BISHOP: phase += 1; break;
                case PieceType::ROOK:   phase += 2; break;
                case PieceType::QUEEN:  phase += 4; break;
                default: break;
            }
        }
    }
    return phase;
}

int PositionEvaluator::evaluatePiece(PieceType type, Square square, Color color) const {
    int pstValue = getPSTValue(type, square, color);
    
    // Дополнительные бонусы/штрафы в зависимости от типа фигуры
    switch (type) {
        case PieceType::PAWN:
            // Пешки ценятся за продвижение
            return pstValue;
        case PieceType::KNIGHT:
            // Кони ценятся за центральные позиции
            return pstValue;
        case PieceType::BISHOP:
            // Слоны ценятся за открытые диагонали
            return pstValue;
        case PieceType::ROOK:
            // Ладьи ценятся за открытые линии
            return pstValue;
        case PieceType::QUEEN:
            // Ферзи ценятся за активные позиции
            return pstValue;
        case PieceType::KING:
            // Короли оцениваются по другой таблице в зависимости от фазы игры
            if (isEndGame()) {
                return pstValue + kingEndGameTable[square];
            } else {
                return pstValue + kingMiddleGameTable[square];
            }
        default:
            return 0;
    }
}

int PositionEvaluator::getPSTValue(PieceType type, Square square, Color color) const {
    // В зависимости от типа фигуры возвращаем соответствующую таблицу
    const int* table = nullptr;
    switch (type) {
        case PieceType::PAWN:   table = pawnTable; break;
        case PieceType::KNIGHT: table = knightTable; break;
        case PieceType::BISHOP: table = bishopTable; break;
        case PieceType::ROOK:   table = rookTable; break;
        case PieceType::QUEEN:  table = queenTable; break;
        case PieceType::KING:   table = (isEndGame()) ? kingEndGameTable : kingMiddleGameTable; break;
        default: return 0;
    }
    
    // Если цвет черный, отражаем позицию
    Square adjustedSquare = (color == Color::BLACK) ? flipSquare(square) : square;
    return table[adjustedSquare];
}

int PositionEvaluator::flipSquare(Square square) const {
    // Отражаем квадрат по вертикали (для черных)
    int rank = board_.rank(square);
    int file = board_.file(square);
    return board_.square(file, 7 - rank);
}

int PositionEvaluator::getPieceMobility(Square square) const {
    // TODO: реализовать оценку мобильности фигуры
    return 0;
}

int PositionEvaluator::getKingSafety(Color color) const {
    // TODO: реализовать оценку безопасности короля
    return 0;
}

int PositionEvaluator::getPawnStructure(Color color) const {
    // TODO: реализовать оценку пешечной структуры
    return 0;
}

bool PositionEvaluator::isPassedPawn(Square square) const {
    Piece piece = board_.getPiece(square);
    Color color = piece.getColor();
    int rank = board_.rank(square);
    int file = board_.file(square);
    int direction = (color == Color::WHITE) ? 1 : -1;
    
    // Проверяем все клетки впереди на той же и соседних вертикалях
    for (int r = rank + direction; r >= 0 && r < 8; r += direction) {
        for (int f = std::max(0, file - 1); f <= std::min(7, file + 1); f++) {
            Piece target = board_.getPiece(board_.square(f, r));
            if (target.getType() == PieceType::PAWN && target.getColor() != color) {
                return false;
            }
        }
    }
    return true;
}

bool PositionEvaluator::isIsolatedPawn(Square square) const {
    Piece piece = board_.getPiece(square);
    Color color = piece.getColor();
    int file = board_.file(square);
    
    // Проверяем соседние вертикали на наличие своих пешек
    for (int f : {file - 1, file + 1}) {
        if (f < 0 || f > 7) continue;
        for (int r = 0; r < 8; r++) {
            Piece target = board_.getPiece(board_.square(f, r));
            if (target.getType() == PieceType::PAWN && target.getColor() == color) {
                return false;
            }
        }
    }
    return true;
}

// Вспомогательные функции для оценки безопасности короля
int PositionEvaluator::evaluateKingSafety(Square kingSquare, Color color) const {
    int safetyScore = 0;
    
    // Проверяем, сколько фигур защищает короля
    int defenders = countDefenders(kingSquare, color);
    safetyScore += defenders * 15; // 15 пунктов за каждого защитника
    
    // Проверяем, есть ли открытые линии к королю
    int attackers = countAttackers(kingSquare, color);
    safetyScore -= attackers * 25; // 25 пунктов за каждого атакующего
    
    // Бонус за центральные позиции в эндшпиле
    if (isEndGame()) {
        int centerDistance = getDistanceToCenter(kingSquare);
        safetyScore -= centerDistance * 5; // Чем ближе к центру, тем лучше
    }
    
    return safetyScore;
}

// Вспомогательные функции для оценки пешечной структуры
int PositionEvaluator::evaluatePawnStructure(Color color) const {
    int structureScore = 0;
    
    // Ищем пешки нужного цвета
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (piece.getType() == PieceType::PAWN && piece.getColor() == color) {
            // Бонус за связанные пешки
            if (isConnectedPawn(square)) {
                structureScore += 10;
            }
            
            // Штраф за изолированные пешки
            if (isIsolatedPawn(square)) {
                structureScore -= 15;
            }
            
            // Бонус за проходные пешки
            if (isPassedPawn(square)) {
                structureScore += 25;
            }
            
            // Бонус за защищенные пешки
            if (isProtectedPawn(square)) {
                structureScore += 5;
            }
        }
    }
    
    return structureScore;
}

// Вспомогательные функции
int PositionEvaluator::countDefenders(Square square, Color color) const {
    int defenders = 0;
    MoveGenerator moveGen(board_);
    
    // Проверяем атаку со стороны своего цвета (защита)
    if (moveGen.isSquareAttacked(square, color)) {
        defenders++;
    }
    
    return defenders;
}

int PositionEvaluator::countAttackers(Square square, Color color) const {
    MoveGenerator moveGen(board_);
    Color opponent = (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
    
    int count = 0;
    if (moveGen.isSquareAttacked(square, opponent)) {
        count = 1; 
    }
    
    return count;
}

int PositionEvaluator::getDistanceToCenter(Square square) const {
    int file = board_.file(square);
    int rank = board_.rank(square);
    
    // Расстояние до центра (e4, d4, e5, d5)
    int centerFiles[] = {3, 4};
    int centerRanks[] = {3, 4};
    
    int minDistance = 14; // Максимальное расстояние
    
    for (int cf : centerFiles) {
        for (int cr : centerRanks) {
            int distance = abs(file - cf) + abs(rank - cr);
            if (distance < minDistance) {
                minDistance = distance;
            }
        }
    }
    
    return minDistance;
}

bool PositionEvaluator::isConnectedPawn(Square square) const {
    Piece piece = board_.getPiece(square);
    Color color = piece.getColor();
    int rank = board_.rank(square);
    int file = board_.file(square);
    
    for (int f : {file - 1, file + 1}) {
        if (f < 0 || f > 7) continue;
        for (int r : {rank - 1, rank, rank + 1}) {
            if (r < 0 || r > 7) continue;
            Piece target = board_.getPiece(board_.square(f, r));
            if (target.getType() == PieceType::PAWN && target.getColor() == color) {
                return true;
            }
        }
    }
    return false;
}

bool PositionEvaluator::isProtectedPawn(Square square) const {
    Piece piece = board_.getPiece(square);
    Color color = piece.getColor();
    int rank = board_.rank(square);
    int file = board_.file(square);
    int direction = (color == Color::WHITE) ? -1 : 1; 
    
    for (int df : {-1, 1}) {
        int nr = rank + direction;
        int nf = file + df;
        if (nr >= 0 && nr < 8 && nf >= 0 && nf < 8) {
            Piece protector = board_.getPiece(board_.square(nf, nr));
            if (protector.getType() == PieceType::PAWN && protector.getColor() == color) {
                return true;
            }
        }
    }
    return false;
}