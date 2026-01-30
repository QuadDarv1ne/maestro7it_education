#include "../include/enhanced_evaluator.hpp"
#include <iostream>
#include <iomanip>
#include <sstream>
#include <algorithm>
#include <cmath>

EnhancedPositionEvaluator::EnhancedPositionEvaluator(const Bitboard& board)
    : board_(board), cache_valid_(false), cached_score_(0), cached_hash_(0),
      last_mode_(ACCURATE_MODE), neural_weight_(EnhancedEvalConstants::DEFAULT_NEURAL_WEIGHT),
      incremental_weight_(EnhancedEvalConstants::DEFAULT_INCREMENTAL_WEIGHT),
      tactical_weight_(EnhancedEvalConstants::DEFAULT_TACTICAL_WEIGHT),
      endgame_weight_(EnhancedEvalConstants::DEFAULT_ENDGAME_WEIGHT),
      game_phase_(0), is_tactical_position_(false) {
    
    // Инициализируем компонентные оценщики
    neural_evaluator_ = std::make_unique<NeuralEvaluator>(board);
    incremental_evaluator_ = std::make_unique<IncrementalEvaluator>(board);
    
    initializeWeights();
    detectGamePhase();
}

void EnhancedPositionEvaluator::initializeWeights() {
    // Начальные веса основаны на фазе игры
    if (game_phase_ < 10) {
        // Дебют - больше нейросетевой оценки
        neural_weight_ = 0.5f;
        incremental_weight_ = 0.3f;
        tactical_weight_ = 0.15f;
        endgame_weight_ = 0.05f;
    } else if (game_phase_ < 25) {
        // Миттельшпиль - баланс
        neural_weight_ = 0.4f;
        incremental_weight_ = 0.4f;
        tactical_weight_ = 0.15f;
        endgame_weight_ = 0.05f;
    } else {
        // Эндшпиль - больше традиционной оценки
        neural_weight_ = 0.3f;
        incremental_weight_ = 0.5f;
        tactical_weight_ = 0.1f;
        endgame_weight_ = 0.1f;
    }
}

void EnhancedPositionEvaluator::detectGamePhase() {
    int total_pieces = BitboardUtils::popCount(board_.getAllPieces());
    game_phase_ = 32 - total_pieces; // 0-32, где 32 это эндшпиль
    
    // Определяем тактическую активность
    analyzeTacticalPatterns();
    is_tactical_position_ = (tactical_features_.threats + tactical_features_.forks + 
                           tactical_features_.discovered_attacks) > EnhancedEvalConstants::TACTICAL_POSITION_THRESHOLD;
}

int EnhancedPositionEvaluator::evaluate(EvaluationMode mode) const {
    // Проверяем кэш
    uint64_t current_hash = calculatePositionHash();
    if (cache_valid_ && cached_hash_ == current_hash && last_mode_ == mode) {
        return cached_score_;
    }
    
    last_mode_ = mode;
    int score = 0;
    
    switch (mode) {
        case FAST_MODE:
            // Быстрая оценка - только основные компоненты
            score = incremental_evaluator_->evaluate() * 0.7f + 
                   neural_evaluator_->evaluate() * 0.3f;
            break;
            
        case ACCURATE_MODE:
            // Точная оценка - все компоненты
            score = combineEvaluations(mode);
            break;
            
        case TACTICAL_MODE:
            // Тактическая оценка - усиленный анализ
            score = evaluateTactical();
            break;
    }
    
    // Обновляем кэш
    cached_score_ = score;
    cached_hash_ = current_hash;
    cache_valid_ = true;
    
    return score;
}

int EnhancedPositionEvaluator::combineEvaluations(EvaluationMode mode) const {
    int neural_score = neural_evaluator_->evaluate();
    int incremental_score = incremental_evaluator_->evaluate();
    
    // Базовая комбинация
    int base_score = static_cast<int>(
        neural_weight_ * neural_score + 
        incremental_weight_ * incremental_score
    );
    
    // Добавляем тактические бонусы если нужно
    if (is_tactical_position_ || mode == TACTICAL_MODE) {
        int tactical_bonus = analyzePins() + analyzeForks() + analyzeSkewers() +
                           analyzeDiscoveredAttacks() + analyzeDoubleAttacks() + 
                           analyzeThreats();
        base_score += static_cast<int>(tactical_weight_ * tactical_bonus);
    }
    
    // Добавляем эндшпильные бонусы
    if (endgame_features_.is_endgame) {
        int endgame_bonus = evaluateEndgameKingActivity() + 
                          evaluatePawnAdvantage() + 
                          evaluatePassedPawnsInEndgame();
        base_score += static_cast<int>(endgame_weight_ * endgame_bonus);
    }
    
    return base_score;
}

int EnhancedPositionEvaluator::evaluateTactical() const {
    // Тактическая оценка с максимальным вниманием к угрозам
    int base_score = incremental_evaluator_->evaluate();
    
    // Усиливаем тактические элементы
    int tactical_score = analyzePins() * 2 + 
                        analyzeForks() * 3 + 
                        analyzeSkewers() * 2 + 
                        analyzeDiscoveredAttacks() * 2 + 
                        analyzeDoubleAttacks() + 
                        analyzeThreats();
    
    return base_score + tactical_score;
}

int EnhancedPositionEvaluator::evaluateEndgame() const {
    int score = incremental_evaluator_->evaluate();
    
    if (endgame_features_.is_endgame) {
        score += evaluateEndgameKingActivity();
        score += evaluatePawnAdvantage();
        score += evaluatePassedPawnsInEndgame();
    }
    
    return score;
}

int EnhancedPositionEvaluator::evaluateMaterialOnly() const {
    return incremental_evaluator_->calculateMaterialScore();
}

void EnhancedPositionEvaluator::updateOnMove(int from_square, int to_square, 
                                           Bitboard::PieceType captured_piece) {
    // Инвалидируем кэш
    cache_valid_ = false;
    
    // Обновляем компонентные оценщики
    neural_evaluator_->updateOnMove(from_square, to_square, captured_piece);
    incremental_evaluator_->updateOnMove(from_square, to_square, captured_piece);
    
    // Перевычисляем фазу игры и тактические паттерны
    detectGamePhase();
}

// Тактический анализ
int EnhancedPositionEvaluator::analyzePins() const {
    int pins = 0;
    
    // Анализ связанных фигур для белых
    Bitboard::BitboardType white_pieces = board_.getOccupancy(Bitboard::WHITE);
    Bitboard::BitboardType black_sliders = board_.getPieces(Bitboard::BLACK, Bitboard::BISHOP) |
                                         board_.getPieces(Bitboard::BLACK, Bitboard::ROOK) |
                                         board_.getPieces(Bitboard::BLACK, Bitboard::QUEEN);
    
    while (white_pieces) {
        int piece_square = BitboardUtils::lsb(white_pieces);
        Bitboard::PieceType piece_type = board_.getPieceType(piece_square);
        
        // Проверяем, может ли эта фигура быть связана
        if (piece_type == Bitboard::QUEEN || piece_type == Bitboard::ROOK || piece_type == Bitboard::BISHOP) {
            // Упрощенная проверка связки
            // В реальной реализации здесь будет полноценный анализ связок
            pins += 5; // Заглушка
        }
        
        white_pieces &= white_pieces - 1;
    }
    
    tactical_features_.pins = pins;
    return pins * EnhancedEvalConstants::PIN_BONUS;
}

int EnhancedPositionEvaluator::analyzeForks() const {
    int forks = 0;
    
    // Анализ вилок (одна фигура атакует две цели)
    // Упрощенная реализация
    auto legal_moves = board_.generateLegalMoves();
    forks = legal_moves.size() / 10; // Примерная оценка
    
    tactical_features_.forks = forks;
    return forks * EnhancedEvalConstants::FORK_BONUS;
}

int EnhancedPositionEvaluator::analyzeSkewers() const {
    int skewers = 0;
    
    // Анализ скосов (атака через ценную фигуру на менее ценную)
    // Упрощенная реализация
    skewers = BitboardUtils::popCount(board_.getAllPieces()) / 8;
    
    tactical_features_.skewers = skewers;
    return skewers * EnhancedEvalConstants::SKEWER_BONUS;
}

int EnhancedPositionEvaluator::analyzeDiscoveredAttacks() const {
    int discovered = 0;
    
    // Анализ открытых атак
    // Упрощенная реализация
    discovered = 3; // Заглушка
    
    tactical_features_.discovered_attacks = discovered;
    return discovered * EnhancedEvalConstants::DISCOVERED_ATTACK_BONUS;
}

int EnhancedPositionEvaluator::analyzeDoubleAttacks() const {
    int double_attacks = 0;
    
    // Анализ двойных атак
    // Упрощенная реализация
    double_attacks = 2; // Заглушка
    
    tactical_features_.double_attacks = double_attacks;
    return double_attacks * EnhancedEvalConstants::DOUBLE_ATTACK_BONUS;
}

int EnhancedPositionEvaluator::analyzeThreats() const {
    int threats = 0;
    
    // Общий анализ угроз
    // Упрощенная реализация
    threats = BitboardUtils::popCount(board_.getAllPieces()) / 4;
    
    tactical_features_.threats = threats;
    return threats * EnhancedEvalConstants::THREAT_BONUS;
}

// Эндшпильные улучшения
int EnhancedPositionEvaluator::evaluateEndgameKingActivity() const {
    if (!endgame_features_.is_endgame) return 0;
    
    int activity_bonus = 0;
    
    // Активность короля в эндшпиле
    Bitboard::BitboardType kings = board_.getPieces(Bitboard::WHITE, Bitboard::KING) |
                                 board_.getPieces(Bitboard::BLACK, Bitboard::KING);
    
    while (kings) {
        int king_square = BitboardUtils::lsb(kings);
        int rank = king_square / 8;
        int file = king_square % 8;
        
        // Бонус за центральные позиции
        if (rank >= 2 && rank <= 5 && file >= 2 && file <= 5) {
            activity_bonus += EnhancedEvalConstants::KING_ACTIVITY_BONUS;
        }
        
        kings &= kings - 1;
    }
    
    return activity_bonus;
}

int EnhancedPositionEvaluator::evaluatePawnAdvantage() const {
    int pawn_diff = endgame_features_.pawn_advantage;
    return pawn_diff * EnhancedEvalConstants::PAWN_ADVANTAGE_MULTIPLIER;
}

int EnhancedPositionEvaluator::evaluatePassedPawnsInEndgame() const {
    if (!endgame_features_.is_endgame || !endgame_features_.has_passed_pawns) {
        return 0;
    }
    
    int passed_pawns = 0;
    
    // Подсчет проходных пешек
    Bitboard::BitboardType white_pawns = board_.getPieces(Bitboard::WHITE, Bitboard::PAWN);
    Bitboard::BitboardType black_pawns = board_.getPieces(Bitboard::BLACK, Bitboard::PAWN);
    
    // Упрощенная реализация
    passed_pawns = BitboardUtils::popCount(white_pawns) + BitboardUtils::popCount(black_pawns);
    
    return passed_pawns * EnhancedEvalConstants::PASSED_PAWN_ENDGAME_BONUS;
}

void EnhancedPositionEvaluator::analyzeTacticalPatterns() const {
    // Анализ тактических паттернов
    tactical_features_ = {};
    tactical_features_.pins = analyzePins() / EnhancedEvalConstants::PIN_BONUS;
    tactical_features_.forks = analyzeForks() / EnhancedEvalConstants::FORK_BONUS;
    tactical_features_.skewers = analyzeSkewers() / EnhancedEvalConstants::SKEWER_BONUS;
    tactical_features_.discovered_attacks = analyzeDiscoveredAttacks() / EnhancedEvalConstants::DISCOVERED_ATTACK_BONUS;
    tactical_features_.double_attacks = analyzeDoubleAttacks() / EnhancedEvalConstants::DOUBLE_ATTACK_BONUS;
    tactical_features_.threats = analyzeThreats() / EnhancedEvalConstants::THREAT_BONUS;
}

void EnhancedPositionEvaluator::analyzeEndgameFeatures() const {
    endgame_features_ = {};
    
    int total_pieces = BitboardUtils::popCount(board_.getAllPieces());
    endgame_features_.is_endgame = total_pieces <= EnhancedEvalConstants::ENDGAME_PIECE_THRESHOLD;
    endgame_features_.piece_count = total_pieces;
    
    // Анализ пешечного преимущества
    int white_pawns = BitboardUtils::popCount(board_.getPieces(Bitboard::WHITE, Bitboard::PAWN));
    int black_pawns = BitboardUtils::popCount(board_.getPieces(Bitboard::BLACK, Bitboard::PAWN));
    endgame_features_.pawn_advantage = white_pawns - black_pawns;
    
    // Проверка наличия проходных пешек
    endgame_features_.has_passed_pawns = (white_pawns > 0 || black_pawns > 0);
    
    // Король становится активным в эндшпиле
    endgame_features_.king_activity_bonus = endgame_features_.is_endgame;
}

uint64_t EnhancedPositionEvaluator::calculatePositionHash() const {
    return neural_evaluator_->calculateBoardHash(); // Переиспользуем существующий метод
}

bool EnhancedPositionEvaluator::isCriticalPosition() const {
    return is_tactical_position_ || endgame_features_.is_endgame;
}

void EnhancedPositionEvaluator::updateAdaptiveWeights() {
    // Адаптивное обновление весов на основе текущей позиции
    if (is_tactical_position_) {
        tactical_weight_ = std::min(tactical_weight_ + 0.05f, 0.3f);
        neural_weight_ = std::max(neural_weight_ - 0.02f, 0.2f);
    }
    
    if (endgame_features_.is_endgame) {
        endgame_weight_ = std::min(endgame_weight_ + 0.03f, 0.2f);
        incremental_weight_ = std::max(incremental_weight_ + 0.02f, 0.6f);
    }
}

// Интерфейсные методы
void EnhancedPositionEvaluator::printDetailedAnalysis() const {
    std::cout << "\n=== ДЕТАЛЬНЫЙ АНАЛИЗ ПОЗИЦИИ ===" << std::endl;
    std::cout << "Фаза игры: " << game_phase_ << std::endl;
    std::cout << "Тактическая позиция: " << (is_tactical_position_ ? "Да" : "Нет") << std::endl;
    
    std::cout << "\nТактические особенности:" << std::endl;
    std::cout << "  Связки: " << tactical_features_.pins << std::endl;
    std::cout << "  Вилки: " << tactical_features_.forks << std::endl;
    std::cout << "  Скосы: " << tactical_features_.skewers << std::endl;
    std::cout << "  Открытые атаки: " << tactical_features_.discovered_attacks << std::endl;
    std::cout << "  Двойные атаки: " << tactical_features_.double_attacks << std::endl;
    std::cout << "  Угрозы: " << tactical_features_.threats << std::endl;
    
    std::cout << "\nЭндшпильные особенности:" << std::endl;
    std::cout << "  Эндшпиль: " << (endgame_features_.is_endgame ? "Да" : "Нет") << std::endl;
    std::cout << "  Количество фигур: " << endgame_features_.piece_count << std::endl;
    std::cout << "  Пешечное преимущество: " << endgame_features_.pawn_advantage << std::endl;
    std::cout << "  Проходные пешки: " << (endgame_features_.has_passed_pawns ? "Да" : "Нет") << std::endl;
    
    std::cout << "\nВеса оценки:" << std::endl;
    std::cout << "  Нейросеть: " << std::fixed << std::setprecision(2) << neural_weight_ << std::endl;
    std::cout << "  Инкрементальная: " << incremental_weight_ << std::endl;
    std::cout << "  Тактика: " << tactical_weight_ << std::endl;
    std::cout << "  Эндшпиль: " << endgame_weight_ << std::endl;
    
    std::cout << "\nОценки:" << std::endl;
    std::cout << "  Быстрая: " << evaluate(FAST_MODE) << std::endl;
    std::cout << "  Точная: " << evaluate(ACCURATE_MODE) << std::endl;
    std::cout << "  Тактическая: " << evaluate(TACTICAL_MODE) << std::endl;
    std::cout << "===============================" << std::endl;
}

EnhancedPositionEvaluator::TacticalFeatures EnhancedPositionEvaluator::getTacticalFeatures() const {
    return tactical_features_;
}

EnhancedPositionEvaluator::EndgameFeatures EnhancedPositionEvaluator::getEndgameFeatures() const {
    return endgame_features_;
}

std::string EnhancedPositionEvaluator::getEvaluationBreakdown() const {
    std::stringstream ss;
    ss << "Phase: " << game_phase_
       << ", Tactical: " << (is_tactical_position_ ? "Yes" : "No")
       << ", Fast: " << evaluate(FAST_MODE)
       << ", Accurate: " << evaluate(ACCURATE_MODE)
       << ", Tactical Eval: " << evaluate(TACTICAL_MODE);
    return ss.str();
}

void EnhancedPositionEvaluator::setModeWeights(float neural_w, float incremental_w, 
                                             float tactical_w, float endgame_w) {
    neural_weight_ = neural_w;
    incremental_weight_ = incremental_w;
    tactical_weight_ = tactical_w;
    endgame_weight_ = endgame_w;
    
    // Нормализуем веса
    float total = neural_weight_ + incremental_weight_ + tactical_weight_ + endgame_weight_;
    if (total > 0) {
        neural_weight_ /= total;
        incremental_weight_ /= total;
        tactical_weight_ /= total;
        endgame_weight_ /= total;
    }
}

void EnhancedPositionEvaluator::enableAdaptiveWeights(bool enable) {
    // В реальной реализации здесь будет логика адаптивных весов
    (void)enable;
}

void EnhancedPositionEvaluator::invalidateCache() {
    cache_valid_ = false;
}

int EnhancedPositionEvaluator::getCachedScore() const {
    return cache_valid_ ? cached_score_ : 0;
}

bool EnhancedPositionEvaluator::isCacheValid() const {
    return cache_valid_;
}