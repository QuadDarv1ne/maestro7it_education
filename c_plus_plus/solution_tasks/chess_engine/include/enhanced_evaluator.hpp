#ifndef ENHANCED_EVALUATOR_HPP
#define ENHANCED_EVALUATOR_HPP

#include "bitboard.hpp"
#include "neural_evaluator.hpp"
#include "incremental_evaluator.hpp"
#include <array>
#include <memory>

/**
 * @brief Расширенный оценщик позиции с продвинутыми функциями
 * 
 * Комбинирует нейросетевую и инкрементальную оценку с дополнительными
 * продвинутыми функциями анализа позиции:
 * - Тактический анализ (вилки, связки, скосы)
 * - Эндшпильные улучшения
 * - Динамическая адаптация весов
 * - Кэширование сложных вычислений
 */
class EnhancedPositionEvaluator {
public:
    enum EvaluationMode {
        FAST_MODE,          // Быстрая оценка для дерева поиска
        ACCURATE_MODE,      // Точная оценка для листьев
        TACTICAL_MODE       // Тактическая оценка для критических позиций
    };
    
    struct TacticalFeatures {
        int pins;           // Количество связанных фигур
        int forks;          // Количество вилок
        int skewers;        // Количество скосов
        int discovered_attacks; // Открытые атаки
        int double_attacks; // Двойные атаки
        int threats;        // Общие угрозы
    };
    
    struct EndgameFeatures {
        bool is_endgame;
        int piece_count;
        int pawn_advantage;
        bool has_passed_pawns;
        bool king_activity_bonus;
    };

private:
    const Bitboard& board_;
    
    // Компонентные оценщики
    std::unique_ptr<NeuralEvaluator> neural_evaluator_;
    std::unique_ptr<IncrementalEvaluator> incremental_evaluator_;
    
    // Кэшированные значения
    mutable bool cache_valid_;
    mutable int cached_score_;
    mutable uint64_t cached_hash_;
    mutable EvaluationMode last_mode_;
    
    // Веса для комбинирования оценок (адаптивные)
    float neural_weight_;
    float incremental_weight_;
    float tactical_weight_;
    float endgame_weight_;
    
    // Адаптивные параметры
    int game_phase_;
    bool is_tactical_position_;
    
    // Вспомогательные данные
    mutable TacticalFeatures tactical_features_;
    mutable EndgameFeatures endgame_features_;
    
    // Инициализация
    void initializeWeights();
    void detectGamePhase();
    void analyzeTacticalPatterns() const;
    void analyzeEndgameFeatures() const;
    
    // Комбинирование оценок
    int combineEvaluations(EvaluationMode mode) const;
    
    // Продвинутый тактический анализ
    int analyzePins() const;
    int analyzeForks() const;
    int analyzeSkewers() const;
    int analyzeDiscoveredAttacks() const;
    int analyzeDoubleAttacks() const;
    int analyzeThreats() const;
    
    // Эндшпильные улучшения
    int evaluateEndgameKingActivity() const;
    int evaluatePawnAdvantage() const;
    int evaluatePassedPawnsInEndgame() const;
    
    // Вспомогательные методы
    uint64_t calculatePositionHash() const;
    bool isCriticalPosition() const;
    void updateAdaptiveWeights();

public:
    explicit EnhancedPositionEvaluator(const Bitboard& board);
    
    // Основной интерфейс оценки
    int evaluate(EvaluationMode mode = ACCURATE_MODE) const;
    
    // Специализированные оценки
    int evaluateTactical() const;
    int evaluateEndgame() const;
    int evaluateMaterialOnly() const;
    
    // Инкрементальное обновление
    void updateOnMove(int from_square, int to_square, 
                     Bitboard::PieceType captured_piece = Bitboard::PIECE_TYPE_COUNT);
    
    // Анализ и отладка
    void printDetailedAnalysis() const;
    TacticalFeatures getTacticalFeatures() const;
    EndgameFeatures getEndgameFeatures() const;
    std::string getEvaluationBreakdown() const;
    
    // Конфигурация
    void setModeWeights(float neural_w, float incremental_w, 
                       float tactical_w, float endgame_w);
    void enableAdaptiveWeights(bool enable);
    
    // Производительность
    void invalidateCache();
    int getCachedScore() const;
    bool isCacheValid() const;
};

// Константы для оценки
namespace EnhancedEvalConstants {
    // Тактические бонусы
    const int PIN_BONUS = 25;
    const int FORK_BONUS = 40;
    const int SKEWER_BONUS = 35;
    const int DISCOVERED_ATTACK_BONUS = 30;
    const int DOUBLE_ATTACK_BONUS = 20;
    const int THREAT_BONUS = 15;
    
    // Эндшпильные бонусы
    const int KING_ACTIVITY_BONUS = 10;
    const int PASSED_PAWN_ENDGAME_BONUS = 50;
    const int PAWN_ADVANTAGE_MULTIPLIER = 20;
    
    // Адаптивные веса
    const float DEFAULT_NEURAL_WEIGHT = 0.4f;
    const float DEFAULT_INCREMENTAL_WEIGHT = 0.4f;
    const float DEFAULT_TACTICAL_WEIGHT = 0.15f;
    const float DEFAULT_ENDGAME_WEIGHT = 0.05f;
    
    // Пороговые значения
    const int ENDGAME_PIECE_THRESHOLD = 12;
    const int TACTICAL_POSITION_THRESHOLD = 50; // Минимальная тактическая активность
}

#endif // ENHANCED_EVALUATOR_HPP