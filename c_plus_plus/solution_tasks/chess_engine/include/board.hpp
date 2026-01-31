#ifndef BOARD_HPP
#define BOARD_HPP

#include "piece.hpp"
#include <vector>
#include <string>
#include <cstdint>

// Предварительное объявление Move
struct Move;

// Позиция на доске (0-63, где 0 - a1, 63 - h8)
typedef int Square;

/**
 * @brief Класс, представляющий шахматную доску
 * 
 * Управляет состоянием шахматной доски, фигурами, текущим игроком,
 * правилами рокировки, взятием на проходе и историей ходов
 */
class Board {
    friend class GameRules;  // Разрешаем GameRules доступ к приватным членам
    
    // Структура для хранения информации об отмене хода
    struct UndoInfo {
        Square from;
        Square to;
        Piece capturedPiece;
        bool whiteKS, whiteQS, blackKS, blackQS;
        Square enPassantSquare;
        int halfMoveClock;
        bool isCastling;
        bool isEnPassant;
        PieceType promotion;
        uint64_t hash;
    };
    
public:
    // Конструктор
    Board();
    
    // Методы настройки
    void setupStartPosition();              ///< Устанавливает начальную позицию
    void setupFromFEN(const std::string& fen);  ///< Загружает позицию из FEN-нотации
    
    // Геттеры
    const Piece& getPiece(Square square) const;  ///< Возвращает фигуру на указанной клетке
    Color getCurrentPlayer() const;              ///< Возвращает текущего игрока
    int getMoveCount() const;                    ///< Возвращает счетчик ходов
    bool canCastleKingSide(Color color) const;   ///< Проверяет право на короткую рокировку
    bool canCastleQueenSide(Color color) const;  ///< Проверяет право на длинную рокировку
    Square getEnPassantSquare() const;           ///< Возвращает клетку для взятия на проходе
    int getHalfMoveClock() const;                ///< Возвращает счетчик полуходов
    const std::vector<UndoInfo>& getHistory() const;  ///< Возвращает историю ходов
    
    // Сеттеры
    void setPiece(Square square, const Piece& piece);  ///< Устанавливает фигуру на клетку
    void setCurrentPlayer(Color color);                ///< Устанавливает текущего игрока
    void setCastlingRights(bool whiteKingSide, bool whiteQueenSide, 
                          bool blackKingSide, bool blackQueenSide);  ///< Устанавливает права на рокировку
    void setEnPassantSquare(Square square);            ///< Устанавливает клетку для взятия на проходе
    void setHalfMoveClock(int clock);                  ///< Устанавливает счетчик полуходов
    
    // Операции с доской
    void makeMove(const Move& move);                   ///< Выполняет полноценный ход со всеми правилами
    void makeMove(Square from, Square to);             ///< Выполняет ход с одной клетки на другую
    void makeMove(const std::string& algebraicNotation);  ///< Выполняет ход в алгебраической нотации
    void undoMove();                                   ///< Отменяет последний ход
    bool isValidMove(Square from, Square to) const;    ///< Проверяет корректность хода
    
    // Обновление состояния после хода
    void updateGameStateAfterMove(const Move& move);   ///< Обновляет права рокировки и ep после хода
    
    // Сохранение/загрузка истории (для makeMove в GameRules)
    void pushHistory(Square from, Square to, const Piece& captured, bool isCastling = false, bool isEnPassant = false, PieceType promotion = PieceType::EMPTY, uint64_t hash = 0);
    
    // Вспомогательные методы
    Square algebraicToSquare(const std::string& algebraic) const;  ///< Преобразует алгебраическую нотацию в клетку
    std::string squareToAlgebraic(Square square) const;           ///< Преобразует клетку в алгебраическую нотацию
    void printBoard() const;                                      ///< Выводит доску в консоль
    std::string getFEN() const;                                   ///< Возвращает FEN-нотацию текущей позиции
    uint64_t getZobristHash() const;                              ///< Возвращает Zobrist-хеш текущей позиции
    
    // Состояние игры
    bool isCheck(Color color) const;      ///< Проверяет, находится ли король под шахом
    bool isCheckmate(Color color) const;  ///< Проверяет, является ли позиция матом
    bool isStalemate(Color color) const;  ///< Проверяет, является ли позиция патом
    bool isRepetition() const;            ///< Проверяет на троекратное повторение
    bool isGameOver() const;              ///< Проверяет, завершена ли игра
    
    // Вспомогательные методы (публичные для доступа из других классов)
    void initializeEmptyBoard();          ///< Инициализирует пустую доску
    bool isInBounds(Square square) const; ///< Проверяет, находится ли клетка в пределах доски
    int rank(Square square) const;        ///< Возвращает горизонталь (0-7, где 0 - первая горизонталь)
    int file(Square square) const;        ///< Возвращает вертикаль (0-7, где 0 - вертикаль 'a')
    Square square(int file, int rank) const;  ///< Создает клетку из вертикали и горизонтали
    
private:
    std::vector<Piece> squares_;  ///< 64 клетки доски (8x8)
    Color currentPlayer_;         ///< Текущий игрок, чей ход
    int moveCount_;               ///< Счетчик ходов
    
    // Права на рокировку
    bool whiteKingSideCastle_;   ///< Право белых на короткую рокировку
    bool whiteQueenSideCastle_;  ///< Право белых на длинную рокировку
    bool blackKingSideCastle_;   ///< Право черных на короткую рокировку
    bool blackQueenSideCastle_;  ///< Право черных на длинную рокировку
    
    // Клетка для взятия на проходе
    Square enPassantSquare_;     ///< Клетка, где возможно взятие на проходе
    
    // Счетчик полуходов для правила 50 ходов
    int halfMoveClock_;          ///< Счетчик полуходов без взятия и движения пешек

    std::vector<UndoInfo> history_;
    

    
private:
    void initZobrist();
    uint64_t zobristTable[64][12];
    uint64_t zobristBlackToMove;
    uint64_t zobristCastling[16];
    uint64_t zobristEnPassant[8];
};

// Константы
const int BOARD_SIZE = 8;      ///< Размер доски (8x8)
const Square INVALID_SQUARE = -1;  ///< Неверная клетка

#endif // BOARD_HPP