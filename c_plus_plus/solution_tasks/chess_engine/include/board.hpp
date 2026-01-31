#ifndef BOARD_HPP
#define BOARD_HPP

#include "piece.hpp"
#include <vector>
#include <string>
#include <cstdint>
#include <utility>  // for std::move

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
    Board() noexcept;
    Board(Board&& other) noexcept = default;  // Move constructor
    Board& operator=(Board&& other) noexcept = default;  // Move assignment
    Board(const Board&) = default;  // Copy constructor
    Board& operator=(const Board&) = default;  // Copy assignment
    
    // Методы настройки
    void setupStartPosition() noexcept;              ///< Устанавливает начальную позицию
    void setupFromFEN(const std::string& fen);       ///< Загружает позицию из FEN-нотации
    
    // Геттеры
    [[nodiscard]] const Piece& getPiece(Square square) const noexcept;  ///< Возвращает фигуру на указанной клетке
    [[nodiscard]] Color getCurrentPlayer() const noexcept;              ///< Возвращает текущего игрока
    [[nodiscard]] int getMoveCount() const noexcept;                    ///< Возвращает счетчик ходов
    [[nodiscard]] bool canCastleKingSide(Color color) const noexcept;   ///< Проверяет право на короткую рокировку
    [[nodiscard]] bool canCastleQueenSide(Color color) const noexcept;  ///< Проверяет право на длинную рокировку
    [[nodiscard]] Square getEnPassantSquare() const noexcept;           ///< Возвращает клетку для взятия на проходе
    [[nodiscard]] int getHalfMoveClock() const noexcept;                ///< Возвращает счетчик полуходов
    [[nodiscard]] const std::vector<UndoInfo>& getHistory() const noexcept;  ///< Возвращает историю ходов
    
    // Сеттеры
    void setPiece(Square square, const Piece& piece) noexcept;  ///< Устанавливает фигуру на клетку
    void setCurrentPlayer(Color color) noexcept;                ///< Устанавливает текущего игрока
    void setCastlingRights(bool whiteKingSide, bool whiteQueenSide, 
                          bool blackKingSide, bool blackQueenSide) noexcept;  ///< Устанавливает права на рокировку
    void setEnPassantSquare(Square square) noexcept;            ///< Устанавливает клетку для взятия на проходе
    void setHalfMoveClock(int clock) noexcept;                  ///< Устанавливает счетчик полуходов
    
    // Операции с доской
    void makeMove(const Move& move);                           ///< Выполняет полноценный ход со всеми правилами
    void makeMove(Square from, Square to);                     ///< Выполняет ход с одной клетки на другую
    void makeMove(const std::string& algebraicNotation);       ///< Выполняет ход в алгебраической нотации
    void undoMove();                                           ///< Отменяет последний ход
    [[nodiscard]] bool isValidMove(Square from, Square to) const noexcept;    ///< Проверяет корректность хода
    
    // Обновление состояния после хода
    void updateGameStateAfterMove(const Move& move) noexcept;   ///< Обновляет права рокировки и ep после хода
    
    // Сохранение/загрузка истории (для makeMove в GameRules)
    void pushHistory(Square from, Square to, const Piece& captured, bool isCastling = false, bool isEnPassant = false, PieceType promotion = PieceType::EMPTY, uint64_t hash = 0);
    
    // Вспомогательные методы
    [[nodiscard]] Square algebraicToSquare(const std::string& algebraic) const;  ///< Преобразует алгебраическую нотацию в клетку
    [[nodiscard]] std::string squareToAlgebraic(Square square) const noexcept;   ///< Преобразует клетку в алгебраическую нотацию
    void printBoard() const;                                                    ///< Выводит доску в консоль
    [[nodiscard]] std::string getFEN() const;                                   ///< Возвращает FEN-нотацию текущей позиции
    [[nodiscard]] uint64_t getZobristHash() const noexcept;                     ///< Возвращает Zobrist-хеш текущей позиции
    
    // Состояние игры
    [[nodiscard]] bool isCheck(Color color) const noexcept;      ///< Проверяет, находится ли король под шахом
    [[nodiscard]] bool isCheckmate(Color color) const noexcept;  ///< Проверяет, является ли позиция матом
    [[nodiscard]] bool isStalemate(Color color) const noexcept;  ///< Проверяет, является ли позиция патом
    [[nodiscard]] bool isRepetition() const noexcept;            ///< Проверяет на троекратное повторение
    [[nodiscard]] bool isGameOver() const noexcept;              ///< Проверяет, завершена ли игра
    
    // Вспомогательные методы (публичные для доступа из других классов)
    void initializeEmptyBoard() noexcept;          ///< Инициализирует пустую доску
    [[nodiscard]] bool isInBounds(Square square) const noexcept; ///< Проверяет, находится ли клетка в пределах доски
    [[nodiscard]] int rank(Square square) const noexcept;        ///< Возвращает горизонталь (0-7, где 0 - первая горизонталь)
    [[nodiscard]] int file(Square square) const noexcept;        ///< Возвращает вертикаль (0-7, где 0 - вертикаль 'a')
    [[nodiscard]] Square square(int file, int rank) const noexcept;  ///< Создает клетку из вертикали и горизонтали
    
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