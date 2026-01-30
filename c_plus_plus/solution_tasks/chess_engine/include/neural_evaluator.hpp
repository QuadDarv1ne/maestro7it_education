#ifndef NEURAL_EVALUATOR_HPP
#define NEURAL_EVALUATOR_HPP

#include "bitboard.hpp"
#include <vector>
#include <array>
#include <memory>

/**
 * @brief Нейросетевой оценщик позиции
 * 
 * Использует упрощенную нейронную сеть для оценки шахматных позиций.
 * Комбинирует традиционные эвристики с машинным обучением.
 */
class NeuralEvaluator {
public:
    // Размеры сети
    static const int INPUT_SIZE = 772;    // 64 squares * 12 piece types + game phase features
    static const int HIDDEN_SIZE = 256;   // Скрытый слой
    static const int OUTPUT_SIZE = 1;     // Одно значение оценки
    
private:
    const Bitboard& board_;
    
    // Веса нейронной сети (упрощенная реализация)
    std::array<float, INPUT_SIZE * HIDDEN_SIZE> weights_input_hidden_;
    std::array<float, HIDDEN_SIZE> biases_hidden_;
    std::array<float, HIDDEN_SIZE * OUTPUT_SIZE> weights_hidden_output_;
    std::array<float, OUTPUT_SIZE> biases_output_;
    
    // Кэширование для производительности
    mutable bool cache_valid_;
    mutable float cached_evaluation_;
    mutable uint64_t cached_hash_;
    
    // Игровая фаза (для адаптивной оценки)
    enum GamePhase {
        OPENING = 0,
        MIDDLEGAME = 1,
        ENDGAME = 2
    };
    
    // Традиционные компоненты оценки
    int material_score_;
    int positional_score_;
    int mobility_score_;
    int king_safety_score_;
    int pawn_structure_score_;
    
    // Веса для комбинирования
    static const float NN_WEIGHT;
    static const float TRADITIONAL_WEIGHT;
    
    // Инициализация весов
    void initializeWeights();
    void loadPretrainedWeights();
    
    // Преобразование доски в входной вектор
    std::vector<float> boardToInputVector() const;
    
    // Прямое распространение через сеть
    float forwardPass(const std::vector<float>& input) const;
    
    // Активационные функции
    static float relu(float x);
    static float tanh_approx(float x);
    
    // Традиционная оценка
    int traditionalEvaluation() const;
    int calculateMaterial() const;
    int calculatePositional() const;
    int calculateMobility() const;
    int calculateKingSafety() const;
    int calculatePawnStructure() const;
    
    // Вспомогательные функции
    GamePhase getCurrentGamePhase() const;
    uint64_t calculateBoardHash() const;
    float normalizeScore(int score) const;
    int denormalizeScore(float normalized) const;
    
public:
    NeuralEvaluator(const Bitboard& board);
    
    // Основной метод оценки
    int evaluate() const;
    
    // Инкрементальное обновление
    void updateOnMove(int from_square, int to_square, 
                     Bitboard::PieceType captured_piece = Bitboard::PIECE_TYPE_COUNT);
    
    // Обучение (заглушка)
    void train(const std::vector<std::pair<Bitboard, int>>& training_data);
    
    // Утилиты
    void resetCache();
    float getNetworkConfidence() const;
    std::vector<float> getHiddenActivations() const;
    
    // Отладка
    void printFeatureImportance() const;
    void analyzePosition() const;
};

// Константы
namespace NeuralConstants {
    // Диапазон оценок
    const int MIN_SCORE = -20000;  // Мат
    const int MAX_SCORE = 20000;   // Мат
    
    // Нормализация
    const float SCORE_SCALE = 10000.0f;
    
    // Веса компонентов
    const float MATERIAL_WEIGHT = 0.8f;
    const float POSITIONAL_WEIGHT = 0.1f;
    const float MOBILITY_WEIGHT = 0.05f;
    const float KING_SAFETY_WEIGHT = 0.03f;
    const float PAWN_STRUCTURE_WEIGHT = 0.02f;
}

#endif // NEURAL_EVALUATOR_HPP