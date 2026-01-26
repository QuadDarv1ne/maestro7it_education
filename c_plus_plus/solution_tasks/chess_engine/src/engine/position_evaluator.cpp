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
            int value = piece.getValue() * 100; // Масштабируем для согласования с другими оценками
            
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
    MoveGenerator whiteGen(board_);
    MoveGenerator blackGen(board_);
    
    // Устанавливаем временно цвет для генераторов
    // Это упрощенная реализация - в реальности потребуется более точный подход
    // TODO: реализовать точную оценку мобильности
    return 0;
}

int PositionEvaluator::kingSafetyEvaluation() const {
    // TODO: реализовать оценку безопасности короля
    return 0;
}

int PositionEvaluator::pawnStructureEvaluation() const {
    // TODO: реализовать оценку структуры пешек
    return 0;
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
    // TODO: реализовать проверку проходной пешки
    return false;
}

bool PositionEvaluator::isIsolatedPawn(Square square) const {
    // TODO: реализовать проверку изолированной пешки
    return false;
}